# Maintenance and releases

## Sources of truth

- Edit service rules in `rules/Service/Service.list`.
- Edit advertising rules only in `rules/Advertising/Advertising.list`; run
  `python scripts/generate_compat.py` to update the legacy `adblock.list`.
- Run `python scripts/generate_readme.py` after changing rule counts.
- Keep every service module enabled in the full template. The validator checks
  this contract; personal configurations may import any subset.
- Preserve public subscription paths and policy names unless a release explicitly
  documents a migration. LoneRules remains experimental and is not required to
  build or validate this repository.

## Routing regression cases

`tests/routing_cases.json` records a target domain or literal IP, its expected
policy, and the owning rule file. Checking the source prevents a removed service
rule from being silently replaced by a broad list or FINAL with the same policy.

```bash
python scripts/check_routing.py
python scripts/check_routing.py --target gemini.google.com
python -m unittest discover -s tests -v
```

The checker resolves repository Raw URLs against the current checkout, so a pull
request tests its own files. It performs no DNS lookup or network request.
Its **ordered contract** is: local non-FINAL exceptions first, enabled remote
lists in configuration order, then the single local FINAL. A remote
`force-policy` overrides the policy in that resource. Domain suffix matching
respects label boundaries; IP matching uses literal IPv4/IPv6 addresses.

Supported types are `HOST`, `HOST-SUFFIX`, `IP-CIDR`, `IP6-CIDR`, and `FINAL`.
Unsupported rules/options fail explicitly and require extending the model and
its tests. This is a conservative ordering regression check, **not an emulator
of Quantumult X**. Matching optimization may give rule types different priority.
DNS resolution, GeoIP, excluded routes, client settings, network availability,
and the final node selected by a policy are outside this model. For example,
an IP covered by `excluded_routes` may bypass Quantumult X before rule matching.

The unit tests deliberately reverse imports, remove a Gemini rule, disable a
resource, change `force-policy`, break policy references and document links,
and let the generated advertising file become stale. Synthetic advertising
rules under reserved example domains test both direct and AI-policy exceptions,
including that sibling domains remain blocked. Synthetic fixtures are not
production rules or evidence of a real-world false positive.

## Rule evidence and device checks

For each rule change, record in the PR: source URL or sanitized request-log
evidence, reason for the rule, verification date, Quantumult X/iOS version,
network environment, affected feature, and before/after behavior. Existing
rules without recorded evidence remain unaudited; do not invent a verification
date or remove a domain only because a single DNS/HTTP probe fails.

On a device, refresh the changed resources and test the affected service:
sign-in, a normal request, and relevant uploads, streaming or other features.
For a false positive, reproduce the failure with blocking enabled, verify the
working policy with the block disabled, then re-enable blocking and verify the
narrow exception. Inspect the actual matched rule and full policy route. Record
matching-optimization settings where precedence matters. Retest an unaffected
sibling hostname where practical.

Offline tests do not establish real-world service coverage or absence of false
positives. If device testing is unavailable for a tooling/documentation release,
state that explicitly in its release notes. Behavior-changing rule releases
should include device evidence before publication.

## Maintenance cadence

- Every change: regenerate derived files, run all checks, and test affected behavior.
- Weekly: review false-positive reports and the separate external-URL job.
- Monthly: audit one service module's sources, scope, and coverage.
- Release: summarize user-visible changes and known verification limits.

External-URL checks cover configuration dependencies such as icons and the node
check URL. An unavailable icon is not evidence of a broken routing rule. Network
checks run separately on the weekly schedule and manual workflow dispatch.

## Release procedure

1. Update the changelog with an unused version and the publication date.
2. Regenerate compatibility output and READMEs; run the commands in
   [Contributing](../CONTRIBUTING.md).
3. Open a pull request, wait for the required `validate` check, and merge through
   the protected branch. Do not bypass protection for a release.
4. Verify the merged commit's checks. Tag that exact commit and publish release
   notes with the validation performed and any device-testing limitations.
5. Verify the release tag and public subscription contents. Preserve the root
   `adblock.list` URL for existing users.

For rollback, restore a known-good rule change through a checked PR or pin the
affected subscription URLs to a previous published tag. The
[setup guide](setup.md) explains how to pin all references in a configuration.
