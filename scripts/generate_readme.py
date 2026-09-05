#!/usr/bin/env python3
"""Generate service READMEs and the root table from the rule files."""

from __future__ import annotations

import argparse
import sys
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RULES_ROOT = ROOT / "rules"
ROOT_README = ROOT / "README.md"
TABLE_START = "<!-- RULES_TABLE_START -->"
TABLE_END = "<!-- RULES_TABLE_END -->"

SERVICE_ORDER = [
    "AI",
    "ChatGPT",
    "Claude",
    "Gemini",
    "GitHub",
    "Google",
    "YouTube",
    "Telegram",
    "TikTok",
    "Microsoft",
    "Apple",
    "Netflix",
    "DisneyPlus",
    "Spotify",
    "Discord",
    "Reddit",
    "Facebook",
    "Instagram",
    "Advertising",
    "China",
    "LAN",
]

DESCRIPTIONS = {
    "AI": "General AI services",
    "ChatGPT": "OpenAI / ChatGPT",
    "Claude": "Anthropic / Claude",
    "Gemini": "Google Gemini",
    "GitHub": "GitHub",
    "Google": "Google services",
    "YouTube": "YouTube / YouTube Music",
    "Telegram": "Telegram",
    "TikTok": "TikTok",
    "Microsoft": "Microsoft services",
    "Apple": "Apple / iCloud",
    "Netflix": "Netflix",
    "DisneyPlus": "Disney+",
    "Spotify": "Spotify",
    "Discord": "Discord",
    "Reddit": "Reddit",
    "Facebook": "Facebook",
    "Instagram": "Instagram",
    "Advertising": "Advertising blocking",
    "China": "China direct connection",
    "LAN": "LAN / private networks",
}

STAT_TYPES = [
    "HOST",
    "HOST-SUFFIX",
    "HOST-KEYWORD",
    "IP-CIDR",
    "IP6-CIDR",
    "GEOIP",
    "USER-AGENT",
    "FINAL",
]


def service_sort_key(name: str) -> tuple[int, str]:
    try:
        return SERVICE_ORDER.index(name), name.lower()
    except ValueError:
        return len(SERVICE_ORDER), name.lower()


def discover_rule_files() -> list[Path]:
    if not RULES_ROOT.is_dir():
        return []
    files: list[Path] = []
    for directory in RULES_ROOT.iterdir():
        if not directory.is_dir():
            continue
        expected = directory / f"{directory.name}.list"
        if expected.is_file():
            files.append(expected)
    return sorted(files, key=lambda path: service_sort_key(path.parent.name))


def rule_lines(path: Path) -> list[str]:
    return [
        line.strip()
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith(("#", ";"))
    ]


def statistics(path: Path) -> tuple[Counter[str], int]:
    lines = rule_lines(path)
    counts = Counter(line.split(",", 1)[0].strip().upper() for line in lines)
    return counts, len(lines)


def subscription_url(service: str) -> str:
    return (
        "https://raw.githubusercontent.com/lonecoding/QuantumultX-Rules/"
        f"main/rules/{service}/{service}.list"
    )


def render_service_readme(path: Path) -> str:
    service = path.parent.name
    counts, total = statistics(path)
    description = DESCRIPTIONS.get(service, service)
    stats = "\n".join(f"- {rule_type}: {counts[rule_type]}" for rule_type in STAT_TYPES)
    return (
        f"# {service}\n\n"
        f"Quantumult X rules for {description}.\n\n"
        "## Rule Statistics\n\n"
        f"{stats}\n"
        f"- TOTAL: {total}\n\n"
        "## Subscription\n\n"
        f"{subscription_url(service)}\n\n"
        "## Maintenance\n\n"
        "Maintained by lonecoding.\n"
    )


def render_rules_table(paths: list[Path]) -> str:
    rows = [
        "| Rule | Description | Rules | Subscription |",
        "|------|-------------|------:|--------------|",
    ]
    for path in paths:
        service = path.parent.name
        _, total = statistics(path)
        description = DESCRIPTIONS.get(service, service)
        rows.append(
            f"| {service} | {description} | {total} | "
            f"[Link]({subscription_url(service)}) |"
        )
    return "\n".join(rows)


def render_root_readme(paths: list[Path]) -> str:
    content = ROOT_README.read_text(encoding="utf-8")
    table_block = f"{TABLE_START}\n{render_rules_table(paths)}\n{TABLE_END}"
    if TABLE_START in content and TABLE_END in content:
        before, remainder = content.split(TABLE_START, 1)
        _, after = remainder.split(TABLE_END, 1)
        return f"{before}{table_block}{after}"

    section = f"## Rules\n\n{table_block}\n\n"
    anchor = "## Policy groups"
    if anchor in content:
        return content.replace(anchor, f"{section}{anchor}", 1)
    return f"{content.rstrip()}\n\n{section}"


def update_file(path: Path, expected: str, check: bool) -> bool:
    current = path.read_text(encoding="utf-8") if path.exists() else ""
    if current == expected:
        return True
    if check:
        print(f"Regeneration required: {path.relative_to(ROOT)}")
        return False
    path.write_text(expected, encoding="utf-8", newline="\n")
    print(f"Updated: {path.relative_to(ROOT)}")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="Check README statistics without writing files",
    )
    args = parser.parse_args()

    paths = discover_rule_files()
    if not paths:
        print("No rule files found.")
        return 1

    valid = True
    for path in paths:
        valid &= update_file(path.parent / "README.md", render_service_readme(path), args.check)
    valid &= update_file(ROOT_README, render_root_readme(paths), args.check)

    if args.check and not valid:
        print("README statistics are outdated. Run python scripts/generate_readme.py.")
        return 1
    if args.check:
        print(f"README checks passed: {len(paths)} services.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
