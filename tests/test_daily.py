"""Check compatibility profile aliases and discovery of upstream resources."""

from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from check_routing import sections
from generate_daily import render_daily
import validate_rules


class DailyTemplateTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        shutil.copytree(ROOT / "config", self.root / "config")
        self.daily = self.root / "config/daily.conf"

    def test_aliases_match_recommended_profile(self):
        for name in ("full", "daily"):
            self.assertEqual((self.root / f"config/{name}.conf").read_text(), render_daily(self.root))
        config = sections(self.daily)
        self.assertEqual([line for _, line in config['filter_local']], ['final, ✈️Final'])
        self.assertEqual(config['server_remote'], [])
        for _, line in config['filter_remote']:
            self.assertTrue(line.startswith(('FILTER_LAN,', 'FILTER_REGION,', 'https://raw.githubusercontent.com/blackmatrix7/')))

    def test_wrong_upstream_policy_is_detected(self):
        self.daily.write_text(self.daily.read_text().replace("force-policy=direct", "force-policy=Proxies"))
        with patch.object(validate_rules, "ROOT", self.root):
            self.assertTrue(validate_rules.validate_daily_template())

    def test_disabled_resource_is_detected(self):
        self.daily.write_text(self.daily.read_text().replace("tag=Upstream-China, force-policy=direct, update-interval=86400, enabled=true", "tag=Upstream-China, force-policy=direct, update-interval=86400, enabled=false"))
        with patch.object(validate_rules, "ROOT", self.root):
            self.assertTrue(validate_rules.validate_daily_template())

    def test_stale_recommended_settings_are_detected(self):
        path = self.root / "config/recommended.conf"
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
        with patch.object(validate_rules, "ROOT", self.root):
            self.assertIn(url, validate_rules.external_config_urls())

    def test_external_url_checks_include_current_resources(self):
        with patch.object(validate_rules, "ROOT", self.root):
            urls = validate_rules.external_config_urls()
        for name in ("AdvertisingLite", "OpenAI", "Copilot", "Hijacking", "Global", "China"):
            self.assertIn(f"https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/QuantumultX/{name}/{name}.list", urls)
        self.assertIn("https://raw.githubusercontent.com/KOP-XIAO/QuantumultX/master/Scripts/resource-parser.js", urls)
        self.assertEqual(len(urls), len(set(urls)))
        self.assertFalse(any("example.com" in url for url in urls))


if __name__ == "__main__":
    unittest.main()
