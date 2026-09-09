# Contributing

Submit rules for services you can identify and test. Avoid large lists with
unclear sources.

## Report a false positive

Use the **False positive** issue form and include the affected app or site,
blocked domain, matching rule file, and whether disabling that rule resolves
the problem. Until a fix is available, add an exact-host exception using the
original working policy, following the [setup guide](docs/setup.md). Some
services still need a proxy after their advertising rejection is removed.

## Add or update rules

```text
HOST-SUFFIX,example.com,PolicyName
```

- Use lowercase domains without a protocol or path.
- Prefer `HOST-SUFFIX`; use `HOST` when an exact match is necessary.
- Add `no-resolve` to IP rules.
- Use an existing policy, or update the configuration and documentation together.
- Include the source and test results in your pull request.
- Record the verification date, affected functionality, and working policy.
- Add a regression case for new routing behavior and every confirmed false positive.
- Edit only `rules/Advertising/Advertising.list` for advertising changes; generate the legacy file.
- Do not submit servers, subscriptions, keys, or personal information.

## Validate changes

Use Python 3.10+ and Node.js 22+, from the repository root:

```bash
node scripts/generate_profiles.js --write
node scripts/generate_profiles.js --check
node --test tests/config-builder.test.js
python scripts/generate_compat.py
python scripts/generate_daily.py
python scripts/generate_readme.py
python scripts/validate_rules.py
python scripts/generate_compat.py --check
python scripts/generate_daily.py --check
python scripts/generate_readme.py --check
python scripts/check_routing.py
python -m unittest discover -s tests -v
```

Regenerate the service READMEs and root rules table after editing rules. The
validator checks layout, blank lines, syntax, duplicates, IP/CIDR values, policy
names, counts, raw URLs, legacy usernames, and advertising-list consistency.
It also checks enabled module imports, policy candidates, local documentation
links, the generated compatibility file, and the optional daily template.
Edit daily-template bindings in scripts/generate_daily.py, then regenerate;
do not copy upstream rule bodies into the service directories.
Edit complete-profile service bindings in scripts/config-builder.js and regenerate
the three presets. See [complete profiles](docs/profiles.md) for defaults and custom groups.
GitHub Actions runs these checks,
the routing contract, and maintenance tests on pushes and pull requests.

The ordered routing contract is a deliberately limited offline model, not the
Quantumult X engine. Follow [maintenance and device verification](docs/maintenance.md)
for its assumptions, supported rule types, and release checks. Do not report
offline test success as successful device testing.

To check external configuration URLs as well:

```bash
python scripts/validate_rules.py --check-external-urls
```
