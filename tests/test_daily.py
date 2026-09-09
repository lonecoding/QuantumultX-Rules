"""Verify upstream bindings and compatibility without downloading upstream rules."""

from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from check_routing import sections
from generate_daily import RESOURCE_PARSER_URL, render_daily, upstream_line
import validate_rules


class DailyTemplateTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        shutil.copytree(ROOT / "config", self.root / "config")
        self.daily = self.root / "config/daily.conf"
        self.daily.write_text(render_daily(self.root), encoding="utf-8")

    def test_exact_upstreams_order_and_policies(self):
        config = sections(self.daily)
        lines = [line for _, line in config["filter_remote"]]
        upstream = [line for line in lines if "/blackmatrix7/" in line]
        self.assertEqual(upstream, [upstream_line(name) for name in ("Hijacking", "Global", "China")])
        self.assertIn("/LAN/LAN.list,", lines[0])
        self.assertEqual(lines[1], upstream_line("Hijacking"))
        self.assertEqual(lines[-2:], [upstream_line("Global"), upstream_line("China")])
        base = sections(self.root / "config/full.conf")
        self.assertEqual([line for line in lines if line not in upstream], [line for _, line in base["filter_remote"]])
        general = [line for _, line in config["general"]]
        parser = "resource_parser_url=" + RESOURCE_PARSER_URL
        self.assertEqual(general.count(parser), 1)
        self.assertEqual([line for line in general if line != parser], [line for _, line in base["general"]])
        self.assertIn("opt-parser=true", self.daily.read_text())
        self.assertFalse(any("opt-parser=" in line for line in lines))
        for section in ("policy", "server_remote", "filter_local"):
            self.assertEqual([line for _, line in config[section]], [line for _, line in base[section]])
        self.assertEqual(config["server_remote"], [])

    def test_wrong_upstream_policy_is_detected(self):
        self.daily.write_text(self.daily.read_text().replace("force-policy=direct", "force-policy=Proxies"))
        with patch.object(validate_rules, "ROOT", self.root):
            self.assertTrue(validate_rules.validate_daily_template())

    def test_removed_or_disabled_resource_is_detected(self):
        for replacement in ("", upstream_line("China").replace("enabled=true", "enabled=false")):
            with self.subTest(replacement=replacement):
                self.daily.write_text(render_daily(self.root).replace(upstream_line("China"), replacement))
                with patch.object(validate_rules, "ROOT", self.root):
                    self.assertTrue(validate_rules.validate_daily_template())

    def test_stale_base_settings_are_detected(self):
        path = self.root / "config/full.conf"
        path.write_text(path.read_text().replace("server_check_timeout=5000", "server_check_timeout=4000"))
        with patch.object(validate_rules, "ROOT", self.root):
            self.assertTrue(validate_rules.validate_daily_template())

    def test_missing_daily_is_detected(self):
        self.daily.unlink()
        with patch.object(validate_rules, "ROOT", self.root):
            self.assertTrue(validate_rules.validate_daily_template())

    def test_external_url_checks_discover_additional_profiles(self):
        profile = self.root / "config/custom-test.conf"
        url = "https://rules.example.net/service.list"
        profile.write_text("[filter_remote]\n" + url + ", enabled=true\n")
        with patch.multiple(validate_rules, ROOT=self.root, CONFIG=self.root / "config/full.conf"):
            self.assertIn(url, validate_rules.external_config_urls())

    def test_external_url_checks_include_all_three_upstreams(self):
        with patch.multiple(validate_rules, ROOT=self.root, CONFIG=self.root / "config/full.conf"):
            urls = validate_rules.external_config_urls()
        for name in ("Hijacking", "Global", "China"):
            self.assertIn(upstream_line(name).split(",", 1)[0], urls)
        self.assertIn(RESOURCE_PARSER_URL, urls)
        self.assertEqual(len(urls), len(set(urls)))
        self.assertFalse(any("example.com" in url for url in urls))


if __name__ == "__main__":
    unittest.main()
