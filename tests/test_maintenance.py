"""Regression and mutation tests for the maintenance checks; no network needed."""

from __future__ import annotations

import shutil
import json
import subprocess
import sys
import tempfile
from pathlib import Path
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import check_routing as routing
import generate_compat
import generate_readme
import validate_rules


class MaintenanceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        for directory in ("config", "rules", "tests", "docs"):
            shutil.copytree(ROOT / directory, self.root / directory, ignore=shutil.ignore_patterns("__pycache__"))
        self.config = self.root / "tests/fixtures/standalone.conf"

    def edit_config(self, old, new):
        content = self.config.read_text(encoding="utf-8")
        self.assertIn(old, content)
        self.config.write_text(content.replace(old, new), encoding="utf-8")

    def configuration_errors(self):
        with patch.multiple(validate_rules, ROOT=self.root, CONFIG=self.config):
            return validate_rules.validate_config_references(list((self.root / "rules").glob("*/*.list")))

    def test_repository_routing_cases(self):
        errors, count = routing.check_cases(self.root)
        self.assertGreaterEqual(count, 30)
        self.assertEqual(errors, [])

    def test_reversing_remote_order_is_detected(self):
        lines = self.config.read_text(encoding="utf-8").splitlines()
        indices = [i for i, line in enumerate(lines) if line.startswith("https://raw.githubusercontent.com/")]
        replacements = list(reversed([lines[i] for i in indices]))
        for index, line in zip(indices, replacements):
            lines[index] = line
        self.config.write_text("\n".join(lines) + "\n", encoding="utf-8")
        errors, _ = routing.check_cases(self.root)
        self.assertTrue(any("gemini.google.com" in error for error in errors))
        self.assertTrue(any("youtubei.googleapis.com" in error for error in errors))

    def test_missing_service_rule_is_detected(self):
        path = self.root / "rules/Gemini/Gemini.list"
        path.write_text(path.read_text().replace("HOST,gemini.google.com,AI\n", ""))
        errors, _ = routing.check_cases(self.root)
        self.assertTrue(any("gemini.google.com" in error for error in errors))

    def test_module_without_regression_cases_is_detected(self):
        path = self.root / "tests/routing_cases.json"
        cases = json.loads(path.read_text())
        path.write_text(json.dumps([case for case in cases if "Claude" not in case["source"]]))
        errors, _ = routing.check_cases(self.root)
        self.assertTrue(any("Claude" in error and "no routing regression case" in error for error in errors))

    def test_comment_formats_are_consistent(self):
        path = self.root / "rules/AI/AI.list"
        path.write_text("# comment\n; comment\n// comment\nHOST,example.com,AI\n")
        self.assertEqual(len(routing.content_lines(path)), 1)
        self.assertEqual(len(validate_rules.meaningful_lines(path)), 1)
        self.assertEqual(generate_readme.statistics(path)[1], 1)

    def test_disabled_list_is_not_loaded_and_is_reported(self):
        self.edit_config("tag=ChatGPT, update-interval=86400, enabled=true", "tag=ChatGPT, update-interval=86400, enabled=false")
        result = routing.resolve("chatgpt.com", routing.load_rules(self.root))
        self.assertEqual(result.policy, "✈️Final")
        self.assertTrue(any("ChatGPT" in error for error in self.configuration_errors()))

    def test_force_policy_overrides_list(self):
        self.edit_config("tag=ChatGPT,", "tag=ChatGPT, force-policy=Google,")
        result = routing.resolve("chatgpt.com", routing.load_rules(self.root))
        self.assertEqual(result.policy, "Google")
        self.assertTrue(routing.check_cases(self.root)[0])

    def test_undefined_policy_candidate_is_detected(self):
        self.edit_config("static=AI, Proxies,", "static=AI, MissingPolicy,")
        self.assertTrue(any("undefined policy candidate MissingPolicy" in error for error in self.configuration_errors()))

    def test_undefined_force_policy_is_detected(self):
        self.edit_config("tag=ChatGPT,", "tag=ChatGPT, force-policy=MissingPolicy,")
        self.assertTrue(any("undefined force-policy MissingPolicy" in error for error in self.configuration_errors()))

    def test_documented_exceptions_restore_direct_and_proxy(self):
        # Reserved domains are synthetic examples, not allegations of real false positives.
        examples = routing.sections(self.root / "config/exceptions.example.conf")["filter_local"]
        self.edit_config("FINAL,✈️Final", "\n".join(line for _, line in examples) + "\nFINAL,✈️Final")
        advertising = self.root / "rules/Advertising/Advertising.list"
        advertising.write_text(advertising.read_text() + "HOST-SUFFIX,example.com,REJECT\nHOST-SUFFIX,example.net,REJECT\n")
        rules = routing.load_rules(self.root)
        self.assertEqual(routing.resolve("ads.example.com", rules).policy, "direct")
        self.assertEqual(routing.resolve("assets.example.net", rules).policy, "AI")
        self.assertEqual(routing.resolve("other.example.com", rules).policy, "REJECT")
        self.assertEqual(routing.resolve("child.ads.example.com", rules).policy, "REJECT")
        # Moving exceptions after FINAL is a configuration error, not a silent success.
        self.edit_config("HOST,ads.example.com,direct", "")
        self.config.write_text(self.config.read_text() + "HOST,ads.example.com,direct\n")
        with self.assertRaisesRegex(ValueError, "end with exactly one FINAL"):
            routing.load_rules(self.root)

    def test_local_override_of_identical_remote_rule_is_allowed(self):
        self.edit_config("FINAL,✈️Final", "HOST-SUFFIX,doubleclick.net,direct\nFINAL,✈️Final")
        with patch.multiple(validate_rules, ROOT=self.root, CONFIG=self.config):
            errors, _ = validate_rules.validate_rules(list((self.root / "rules").glob("*/*.list")))
        self.assertEqual(errors, [])
        self.assertEqual(routing.resolve("doubleclick.net", routing.load_rules(self.root)).policy, "direct")

    def test_duplicate_local_rule_is_still_rejected(self):
        self.edit_config("FINAL,✈️Final", "HOST,example.com,direct\nHOST,example.com,AI\nFINAL,✈️Final")
        with patch.multiple(validate_rules, ROOT=self.root, CONFIG=self.config):
            errors, _ = validate_rules.validate_rules([])
        self.assertTrue(any("duplicates" in error for error in errors))

    def test_suffix_boundaries_and_host_exactness(self):
        suffix = routing.parse_rule("HOST-SUFFIX,example.com,AI", "test")
        exact = routing.parse_rule("HOST,example.com,AI", "test")
        for target in ("example.com", "a.example.com", "EXAMPLE.COM."):
            self.assertTrue(suffix.matches(target))
        for target in ("notexample.com", "example.com.evil", "1.2.3.4"):
            self.assertFalse(suffix.matches(target))
        self.assertFalse(exact.matches("a.example.com"))

    def test_ip_version_and_network_boundaries(self):
        ipv4 = routing.parse_rule("IP-CIDR,192.168.0.0/16,direct,no-resolve", "test")
        ipv6 = routing.parse_rule("IP6-CIDR,2001:b28:f23d::/48,Telegram,no-resolve", "test")
        self.assertTrue(ipv4.matches("192.168.255.255"))
        self.assertFalse(ipv4.matches("192.169.0.0"))
        self.assertFalse(ipv4.matches("2001:b28:f23d::1"))
        self.assertTrue(ipv6.matches("2001:b28:f23d::1"))
        self.assertFalse(ipv6.matches("2001:b28:f23e::1"))
        self.assertFalse(ipv4.matches("example.com"))

    def test_unsupported_rule_fails_instead_of_silently_skipping(self):
        self.edit_config("FINAL,✈️Final", "GEOIP,CN,direct\nFINAL,✈️Final")
        with self.assertRaisesRegex(ValueError, "does not support GEOIP"):
            routing.load_rules(self.root)

    def test_remote_final_is_rejected(self):
        path = self.root / "rules/AI/AI.list"
        path.write_text(path.read_text() + "FINAL,AI\n")
        with self.assertRaisesRegex(ValueError, "FINAL is only allowed"):
            routing.load_rules(self.root)

    def test_missing_final_is_rejected(self):
        self.edit_config("FINAL,✈️Final", "")
        with self.assertRaisesRegex(ValueError, "exactly one FINAL"):
            routing.load_rules(self.root)

    def test_external_and_unsafe_resources_are_rejected(self):
        raw_base = "https://raw.githubusercontent.com/" + "/".join(routing.REPOSITORY)
        for url in ("https://example.com/rules.list", raw_base + "/main/../../outside.list"):
            with self.assertRaises(ValueError):
                routing.remote_resource(url, self.root)

    def test_compat_generation_and_check(self):
        shutil.copytree(ROOT / "scripts", self.root / "scripts", ignore=shutil.ignore_patterns("__pycache__"))
        command = [sys.executable, str(self.root / "scripts/generate_compat.py")]
        self.assertEqual(subprocess.run(command, capture_output=True).returncode, 0)
        destination = self.root / "adblock.list"
        initial = destination.read_bytes()
        self.assertEqual(subprocess.run(command + ["--check"], capture_output=True).returncode, 0)
        self.assertEqual(subprocess.run(command, capture_output=True).returncode, 0)
        self.assertEqual(destination.read_bytes(), initial)
        source = self.root / "rules/Advertising/Advertising.list"
        source.write_text(source.read_text() + "HOST,ads.example.com,REJECT\n")
        self.assertEqual(subprocess.run(command + ["--check"], capture_output=True).returncode, 1)
        self.assertEqual(destination.read_bytes(), initial)  # --check must not write.
        self.assertEqual(subprocess.run(command, capture_output=True).returncode, 0)
        self.assertEqual(destination.read_text(), generate_compat.render_compat(source))

    def test_missing_compat_file_is_an_error(self):
        with patch.multiple(validate_rules, CANONICAL_ADBLOCK=self.root / "rules/Advertising/Advertising.list", COMPAT_ADBLOCK=self.root / "adblock.list"):
            self.assertTrue(validate_rules.validate_adblock_sync())

    def test_broken_local_document_link_is_detected(self):
        (self.root / "README.md").write_text("[Broken](docs/missing.md)\n[External](https://example.com)\n[Anchor](#here)\n")
        with patch.object(validate_rules, "ROOT", self.root):
            errors = validate_rules.validate_document_links()
        self.assertTrue(any("docs/missing.md" in error for error in errors))
        self.assertFalse(any("https://example.com" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
