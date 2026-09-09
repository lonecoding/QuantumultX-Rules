# Contributing

This project provides Quantumult X configurations and policy groups backed by upstream resources.
Describe the expected policy and affected service when suggesting a change.

## Configuration changes

- Edit policy candidates and resource bindings in scripts/config-builder.js.
- Use published Quantumult X upstream rule URLs and explicit force-policy bindings.
- Keep recommended and extended resource coverage aligned; selected groups control routing choices.
- Keep full.conf and daily.conf identical to recommended.conf.
- Preserve fixed Direct behavior and independent AdBlock/Hijacking controls.
- Update user-facing policy documentation and include regression checks for changed behavior.
- Do not submit nodes, subscription URLs, credentials or personal request logs.

## Validation

Use Node.js 22+ and Python 3.10+ from the repository root:

```bash
node scripts/generate_profiles.js --write
node scripts/generate_profiles.js --check
node --test tests/config-builder.test.js
python scripts/generate_compat.py --check
python scripts/generate_daily.py --check
python scripts/generate_readme.py --check
python scripts/validate_rules.py
python scripts/check_routing.py
python -m unittest discover -s tests -v
```

To check the external URLs in published configurations:

```bash
python scripts/validate_rules.py --check-external-urls
```

## Existing standalone subscriptions

Standalone rule files remain available through the [compatibility index](docs/legacy-rule-files.md).
Their offline regression fixture is tests/fixtures/standalone.conf; complete profiles do not load them.
For a confirmed correction, edit the canonical service file, regenerate compatibility output and
statistics, and add a regression case. Preserve public subscription paths.

## Evidence and device checks

Provide the rule source or sanitized request log, expected policy and verification date.
Record Quantumult X/iOS versions and actual device behavior, or explicitly state that no device
verification was performed. Tests of configuration references do not prove actual upstream matching.
See [maintenance and verification](docs/maintenance.md).
