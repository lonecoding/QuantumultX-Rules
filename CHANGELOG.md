# Changelog

## Unreleased

- Offer recommended and extended presets, with custom policy-group generation.

## [0.4.0] - 2026-09-09

- Add complete mainland-China profiles: recommended (10 groups) and
  extended (16), with the existing upstream parser, DNS defaults, configurable
  advertising blocking, service upstream coverage, and built-in China IP routing.
- Add an original dependency-free JavaScript configuration composer with preset,
  custom-group and interactive modes. All profiles retain the same resource coverage.
- Make the complete recommended profile the README entry point; document migration,
  subscriptions, group defaults, upstream ownership and device verification limits.
- Test all 4096 group combinations for valid references and cycles; check generated
  presets in CI and include every profile in external URL checks.


- Reference the upstream KOP-XIAO resource parser in daily.conf; add an opt-parser
  node-subscription example, source attribution, and Chinese setup/recovery guidance.

- Add optional config/daily.conf, generated from full.conf with direct upstream
  blackmatrix7 Hijacking, Global, and China subscriptions.
- Preserve the full template and self-maintained service rules; document external
  ownership, daily-template behavior, and Chinese setup instructions.
- Check generated upstream bindings offline and include upstream URLs in network
  checks. On-device validation of the optional daily template remains pending.

## [0.3.0] - 2026-09-09

### Added

- Offline ordered routing regression cases covering every service module, domain boundaries, IP networks, and FINAL fallback.
- Mutation tests for changed import order, removed rules, resource overrides, direct/proxy exceptions, and maintenance validation failures.
- Copyable exact-host exception examples and explicit default-routing, policy-binding, and rollback instructions.
- Maintenance guidance covering rule evidence, device checks, and protected-branch releases.

### Changed

- Generate the legacy adblock.list from rules/Advertising/Advertising.list as the single source of truth.
- Validate enabled module imports, policy candidates, local documentation links, and missing or stale compatibility output.
- Permit intentional local overrides of remote rules while still rejecting duplicates within each scope.
- Run regression and maintenance tests in CI; report scheduled/manual external-URL checks in a separate job.
- Use English throughout documentation, configuration comments, and contribution templates.
- Simplify the README and move detailed setup instructions into `docs/setup.md`.
- Clarify the distinction between this rules collection and the experimental LoneRules build tool.

### Compatibility and verification

- Preserve all existing subscription paths, policy names, and effective production rules.
- The ordered routing checker is a limited offline model, not the Quantumult X engine; no on-device testing was performed for this tooling/documentation release.

## [0.2.0] - 2026-09-03

### Changed

- Organize rules under `rules/Service/Service.list`.
- Split AI rules into ChatGPT, Claude, Gemini, and general AI groups.
- Move LAN rules from the configuration into a separate list.
- Generate service READMEs and the root rules table automatically.
- Extend validation to cover layout, blank lines, syntax, duplicates, IP/CIDR values, and README counts.
- Update rule paths in configuration, documentation, issue forms, and GitHub Actions.

## [0.1.0] - 2026-09-02

### Added

- Importable `config/full.conf` configuration.
- Separate AI, YouTube, Telegram, Google, TikTok, and Apple rules.
- Modular advertising rules and false-positive exceptions loaded before them.
- Rule validation and GitHub Actions.
- Contributor guide, issue forms, and pull request template.
- Updated YouTube, Telegram, and Apple icon URLs.
- Project documentation, usage instructions, policy descriptions, and troubleshooting notes.

### Compatibility

- Retain the root `adblock.list` for existing raw URLs.
- Retain policy names, default order, and icon URLs.
