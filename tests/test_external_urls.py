"""Exercise transient failures and real broken links without network requests."""

from contextlib import ExitStack
import io
from pathlib import Path
import sys
import unittest
from unittest.mock import MagicMock, call, patch
from urllib.error import HTTPError, URLError

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import validate_rules


class ExternalURLTests(unittest.TestCase):
    URL = "https://rules.example.net/service.list"

    def setUp(self):
        context = ExitStack()
        self.addCleanup(context.close)
        self.urls = context.enter_context(
            patch.object(validate_rules, "external_config_urls", return_value=[self.URL])
        )
        self.urlopen = context.enter_context(patch.object(validate_rules.urllib.request, "urlopen"))
        self.sleep = context.enter_context(patch.object(validate_rules.time, "sleep"))
        self.stderr = context.enter_context(patch.object(sys, "stderr", new_callable=io.StringIO))

    def response(self, status=206):
        response = MagicMock()
        response.__enter__.return_value.status = status
        return response

    def http_error(self, status):
        return HTTPError(self.URL, status, "test failure", {}, io.BytesIO())

    def test_success_needs_one_request(self):
        response = self.response()
        self.urlopen.return_value = response
        self.assertEqual(validate_rules.validate_external_urls(), [])
        self.urlopen.assert_called_once()
        self.sleep.assert_not_called()
        response.__exit__.assert_called_once()

    def test_transient_http_error_recovers_and_closes_error_response(self):
        error = self.http_error(503)
        self.urlopen.side_effect = [error, self.response()]
        self.assertEqual(validate_rules.validate_external_urls(), [])
        self.assertTrue(error.closed)
        self.assertEqual(self.urlopen.call_count, 2)
        self.sleep.assert_called_once_with(1)
        self.assertIn("attempt 2/3", self.stderr.getvalue())

    def test_transient_http_statuses_recover(self):
        for status in (408, 500, 502, 504):
            with self.subTest(status=status):
                self.urlopen.side_effect = [self.http_error(status), self.response()]
                self.assertEqual(validate_rules.validate_external_urls(), [])

    def test_network_failures_recover(self):
        for error in (URLError("connection reset"), TimeoutError("timed out"), ConnectionResetError()):
            with self.subTest(error=type(error).__name__):
                self.urlopen.side_effect = [error, self.response()]
                self.assertEqual(validate_rules.validate_external_urls(), [])

    def test_repeated_failure_still_fails_after_three_requests(self):
        self.urlopen.side_effect = [self.http_error(503) for _ in range(3)]
        errors = validate_rules.validate_external_urls()
        self.assertEqual(len(errors), 1)
        self.assertIn("HTTP Error 503", errors[0])
        self.assertIn("after 3 attempts", errors[0])
        self.assertEqual(self.urlopen.call_count, 3)
        self.assertEqual(self.sleep.call_args_list, [call(1), call(2)])

    def test_permanent_http_failure_is_not_retried(self):
        for status in (401, 403, 404, 410):
            with self.subTest(status=status):
                self.urlopen.reset_mock()
                self.urlopen.side_effect = self.http_error(status)
                errors = validate_rules.validate_external_urls()
                self.assertEqual(len(errors), 1)
                self.assertIn(f"HTTP Error {status}", errors[0])
                self.urlopen.assert_called_once()
                self.sleep.assert_not_called()

    def test_permanent_failure_after_transient_error_stops_retrying(self):
        self.urlopen.side_effect = [self.http_error(503), self.http_error(404)]
        errors = validate_rules.validate_external_urls()
        self.assertEqual(len(errors), 1)
        self.assertIn("HTTP Error 404", errors[0])
        self.assertEqual(self.urlopen.call_count, 2)
        self.sleep.assert_called_once_with(1)

    def test_returned_error_status_is_retried(self):
        response = self.response(503)
        self.urlopen.side_effect = [response, self.response()]
        self.assertEqual(validate_rules.validate_external_urls(), [])
        response.__exit__.assert_called_once()
        self.assertEqual(self.urlopen.call_count, 2)

    def test_failed_url_does_not_stop_checking_other_urls(self):
        self.urls.return_value = [self.URL, "https://rules.example.net/second.list"]
        self.urlopen.side_effect = [self.http_error(503) for _ in range(3)] + [self.response()]
        errors = validate_rules.validate_external_urls()
        self.assertEqual(len(errors), 1)
        self.assertEqual(self.urlopen.call_count, 4)


if __name__ == "__main__":
    unittest.main()
