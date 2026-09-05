# Contributing

Submit rules for services you can identify and test. Avoid large lists with
unclear sources.

## Report a false positive

Use the **False positive** issue form and include the affected app or site,
blocked domain, matching rule file, and whether disabling that rule resolves
the problem. Until a fix is available, place a direct exception before the
advertising rules in your own configuration.

## Add or update rules

```text
HOST-SUFFIX,example.com,PolicyName
```

- Use lowercase domains without a protocol or path.
- Prefer `HOST-SUFFIX`; use `HOST` when an exact match is necessary.
- Add `no-resolve` to IP rules.
- Use an existing policy, or update the configuration and documentation together.
- Include the source and test results in your pull request.
- Do not submit servers, subscriptions, keys, or personal information.

## Validate changes

Use Python 3.10 or newer, from the repository root:

```bash
python scripts/generate_readme.py
python scripts/validate_rules.py
python scripts/generate_readme.py --check
```

Regenerate the service READMEs and root rules table after editing rules. The
validator checks layout, blank lines, syntax, duplicates, IP/CIDR values, policy
names, counts, raw URLs, legacy usernames, and advertising-list consistency.
GitHub Actions runs the same checks on pushes and pull requests.

To check external configuration URLs as well:

```bash
python scripts/validate_rules.py --check-external-urls
```
