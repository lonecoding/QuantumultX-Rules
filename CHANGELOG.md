# Changelog

## Unreleased

- Use English throughout documentation, configuration comments, and contribution templates.
- Simplify the README and move detailed setup instructions into `docs/setup.md`.
- Clarify the distinction between this rules collection and the experimental LoneRules build tool.

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
