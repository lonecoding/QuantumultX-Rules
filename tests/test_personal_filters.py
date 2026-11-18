"""Regression checks for the user's separately maintained subscriptions."""
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def rules(name):
    return [s.strip().split(',') for s in (ROOT / f'{name}.list').read_text().splitlines()
            if s.strip() and not s.startswith('#')]


def matches(domain, entries):
    for kind, value, *_ in entries:
        if kind == 'HOST' and value == domain:
            return True
        if kind == 'HOST-SUFFIX' and (domain == value or domain.endswith('.' + value)):
            return True
        if kind == 'HOST-KEYWORD' and value in domain:
            return True
        if kind == 'HOST-WILDCARD' and re.fullmatch(re.escape(value).replace(r'\*', '.*').replace(r'\?', '.'), domain):
            return True
    return False


class PersonalFiltersTests(unittest.TestCase):
    def test_subscription_bindings_and_final(self):
        text = (ROOT / 'personal-filters.conf').read_text()
        expected = {'Hijacking': 'reject', 'Diagnostics': 'Proxies', 'Telegram': 'Telegram',
                    'OpenAI': 'AI', 'Claude': 'AI', 'YouTube': 'YouTube', 'TikTok': 'TikTok',
                    'Apple': 'Apple', 'Google': 'Google', 'Global': 'Proxies', 'China': 'direct'}
        active = [s for s in text.splitlines() if s.startswith('https://')]
        self.assertEqual(len(active), len(expected))
        for name, policy in expected.items():
            prefix = 'https://' + f'raw.githubusercontent.com/lonecoding/QuantumultX-Rules/main/{name}.list,'
            line, = [s for s in active if s.startswith(prefix)]
            self.assertIn(f'force-policy={policy},', line)
            self.assertTrue((ROOT / f'{name}.list').is_file())
        self.assertIn('final, ✈️Final', text)
        self.assertFalse(any(s.startswith('FILTER_REGION') for s in text.splitlines()))

    def test_no_ip_lookup_rules_and_manifest_counts(self):
        manifest = json.loads((ROOT / 'docs/personal-rules-sources.json').read_text())
        for name, info in manifest['lists'].items():
            entries = rules(name)
            self.assertEqual(len(entries), info['output_rules'], name)
            self.assertFalse({'IP-CIDR', 'IP6-CIDR', 'IP-ASN', 'GEOIP'} & {s[0] for s in entries}, name)

    def test_common_domestic_services_and_cdn_stay_direct(self):
        entries = rules('China')
        for domain in ['qpic.cn', 'qlogo.cn', 'bilivideo.cn', 'biliimg.com', 'icbc.com.cn',
                       '95588.com.cn', 'jd.cn', '10086.cn', '12306.cn', 'alicdn.com',
                       'hdslb.com', 'bilivideo.com', 'taobao.com', 'alipay.com', 'xiaohongshu.com']:
            self.assertTrue(matches(domain, entries), domain)

    def test_diagnostics_are_explicit_proxy_exceptions(self):
        china, diagnostics = rules('China'), rules('Diagnostics')
        for domain in ['2026.ip138.com', 'my.ip.cn', 'api.myip.la', 'browserleaks.com',
                       'random.d.ip.net.coffee', 'ip.istatmenus.app', 'ipip.net']:
            self.assertFalse(matches(domain, china), domain)
            self.assertTrue(matches(domain, diagnostics), domain)
        self.assertNotIn(['HOST-SUFFIX', 'cn', 'China'], china)


if __name__ == '__main__':
    unittest.main()
