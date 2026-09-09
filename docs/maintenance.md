# Maintenance and releases

## Complete configurations

Edit `scripts/config-builder.js` for policy candidates, upstream resources and bindings.
Generate recommended.conf, extended.conf, full.conf and daily.conf with
`node scripts/generate_profiles.js --write`. The last two are exact aliases of recommended.conf.
The repository references upstream rules directly; do not copy upstream rule bodies into the profiles.

The JavaScript tests check all 32768 optional group selections, valid and acyclic policy references,
fixed Direct behavior, independent blocking controls, resource placement, parent-group inheritance,
upstream-only subscriptions and generated output consistency. They do not emulate Quantumult X.
See [profile setup and checks](profiles.md) for the complete command list.

## Standalone subscription compatibility

Existing `rules/Service/Service.list` and `adblock.list` URLs remain available to prior subscribers.
Their documentation is in [the compatibility index](legacy-rule-files.md), separate from the homepage's
client policy-group table. Complete configurations do not load these rule files.

- Edit an existing standalone rule at its canonical `rules/Service/Service.list` path.
- Generate adblock.list from Advertising.list with `python scripts/generate_compat.py`.
- Generate service READMEs and the compatibility index with `python scripts/generate_readme.py`.
- Keep the offline fixture `tests/fixtures/standalone.conf` aligned with those standalone modules.

The 34 cases in `tests/routing_cases.json` use only that fixture and standalone files. Run
`python scripts/check_routing.py` or `python scripts/check_routing.py --target gemini.google.com`.
The fixture is not an importable recommended configuration and is not used to claim upstream coverage.

Its deliberately limited ordered model evaluates local exceptions, enabled remote resources in file
order, then Final. Repository resource URLs resolve against the checkout. It supports HOST,
HOST-SUFFIX, IP-CIDR, IP6-CIDR and FINAL, and performs no DNS or network request.
Tests cover mutations to resource order, policies, rules, options and generated compatibility files.
They do not model actual client matching optimization, DNS, GeoIP, excluded routes or node selection.

## Device verification

Record the client/iOS version, network, affected service, expected policy and actual request-log result.
Check initial import, resource refresh, sign-in, ordinary requests, relevant streaming or uploads,
independent policy selection, and false-positive recovery. Avoid publishing subscription credentials.

Offline tests and URL reachability cannot establish service availability or rule precedence in the app.
If no device is available, state that in release notes and keep device verification pending.

## Checks and publishing

Run the checks in [CONTRIBUTING](../CONTRIBUTING.md). Network checks discover external URLs from the
published configuration directory and run separately on scheduled/manual workflows.
Standalone fixture URLs are not part of those production network checks.

Use a feature branch and pull request, wait for the required validate check, and merge through main's
protection rules. Publish a version from the verified merge commit with concrete user-visible behavior,
migration instructions, upstream ownership and actual verification limits. Verify public downloads.
For rollback, restore a device backup or select a known-good configuration version and reviewed resources.
