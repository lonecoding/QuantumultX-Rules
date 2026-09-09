#!/usr/bin/env python3
"""Synchronize compatibility configuration URLs with the recommended profile.

Generate the recommended profile first with node scripts/generate_profiles.js --write.
This compatibility command requires only Python and never downloads resources.
"""
from __future__ import annotations

import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def render_daily(root: Path = ROOT) -> str:
    return (root / "config/recommended.conf").read_text(encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Check without writing")
    args = parser.parse_args()
    expected = render_daily()
    valid = True
    for name in ("full", "daily"):
        path = ROOT / "config" / f"{name}.conf"
        if path.is_file() and path.read_text(encoding="utf-8") == expected:
            continue
        if args.check:
            print(f"Regeneration required: config/{name}.conf")
            valid = False
        else:
            path.write_text(expected, encoding="utf-8", newline="\n")
            print(f"Updated: config/{name}.conf")
    return 0 if valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
