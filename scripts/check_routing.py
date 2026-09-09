#!/usr/bin/env python3
"""Check the repository's ordered routing contract, not the Quantumult X engine.

Local exceptions precede enabled remote lists in configuration order; FINAL is
the fallback. Only the rule types used by this repository are modeled. Client
matching optimizations, DNS, excluded routes, GeoIP and node selection are not
emulated. See docs/maintenance.md for the scope and on-device verification.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass, replace
import ipaddress
import json
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parents[1]
REPOSITORY = ("lonecoding", "QuantumultX-Rules")
SUPPORTED_TYPES = {"HOST", "HOST-SUFFIX", "IP-CIDR", "IP6-CIDR", "FINAL"}


def content_lines(path: Path) -> list[tuple[int, str]]:
    return [
        (number, line.strip())
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1)
        if line.strip() and not line.lstrip().startswith(("#", ";", "//"))
    ]


def sections(path: Path) -> dict[str, list[tuple[int, str]]]:
    result: dict[str, list[tuple[int, str]]] = {}
    section = ""
    for number, line in content_lines(path):
        if line.startswith("[") and line.endswith("]"):
            section = line[1:-1].strip().lower()
            result.setdefault(section, [])
        else:
            result.setdefault(section, []).append((number, line))
    return result


@dataclass(frozen=True)
class Rule:
    kind: str
    value: str
    policy: str
    source: str

    def matches(self, target: str) -> bool:
        target = target.lower().rstrip(".")
        try:
            address = ipaddress.ip_address(target)
        except ValueError:
            address = None
        if self.kind == "FINAL":
            return True
        if self.kind in {"IP-CIDR", "IP6-CIDR"}:
            return address is not None and address in ipaddress.ip_network(self.value)
        if address is not None:
            return False
        if self.kind == "HOST":
            return target == self.value
        return target == self.value or target.endswith("." + self.value)


def parse_rule(line: str, source: str) -> Rule:
    parts = [part.strip() for part in line.split(",")]
    kind = parts[0].upper()
    if kind not in SUPPORTED_TYPES:
        raise ValueError(f"{source}: routing contract does not support {kind}; extend it explicitly")
    lengths = {2} if kind == "FINAL" else {3, 4} if kind in {"IP-CIDR", "IP6-CIDR"} else {3}
    if len(parts) not in lengths or any(not part for part in parts):
        raise ValueError(f"{source}: invalid rule fields")
    if len(parts) == 4 and parts[3].lower() != "no-resolve":
        raise ValueError(f"{source}: unsupported routing option {parts[3]}")
    if kind in {"IP-CIDR", "IP6-CIDR"}:
        network = ipaddress.ip_network(parts[1], strict=True)
        if network.version != (6 if kind == "IP6-CIDR" else 4):
            raise ValueError(f"{source}: IP version does not match {kind}")
    return Rule(kind, "" if kind == "FINAL" else parts[1].lower(), parts[-1] if kind == "FINAL" else parts[2], source)


def remote_resource(line: str, root: Path) -> tuple[Path, dict[str, str]]:
    parts = [part.strip() for part in line.split(",")]
    parsed = urlparse(parts[0])
    components = tuple(unquote(part) for part in parsed.path.split("/") if part)
    if parsed.scheme != "https" or parsed.netloc != "raw.githubusercontent.com" or len(components) < 4 or components[:2] != REPOSITORY:
        raise ValueError(f"unsupported remote resource in routing contract: {parts[0]}")
    # Resolve the referenced file in this checkout, never download main during a PR.
    path = root.joinpath(*components[3:]).resolve()
    if not path.is_relative_to(root.resolve()) or not path.is_file():
        raise ValueError(f"missing or unsafe remote resource: {parts[0]}")
    options: dict[str, str] = {}
    for option in parts[1:]:
        key, separator, value = option.partition("=")
        if not separator or not value.strip() or key.strip() in options:
            raise ValueError(f"invalid remote option: {option}")
        options[key.strip()] = value.strip()
    if options.get("enabled", "true").lower() not in {"true", "false"}:
        raise ValueError("enabled must be true or false")
    unsupported = set(options) - {"tag", "update-interval", "enabled", "force-policy"}
    if unsupported:
        raise ValueError(f"unsupported remote options in routing contract: {sorted(unsupported)}")
    return path, options


def load_rules(root: Path = ROOT) -> list[Rule]:
    root = root.resolve()
    config = sections(root / "tests/fixtures/standalone.conf")
    local = [parse_rule(line, f"tests/fixtures/standalone.conf:{number}") for number, line in config.get("filter_local", [])]
    finals = [rule for rule in local if rule.kind == "FINAL"]
    if len(finals) != 1 or not local or local[-1].kind != "FINAL":
        raise ValueError("filter_local must end with exactly one FINAL rule")
    rules = [rule for rule in local if rule.kind != "FINAL"]
    for _, line in config.get("filter_remote", []):
        path, options = remote_resource(line, root)
        if options.get("enabled", "true").lower() == "false":
            continue
        for number, text in content_lines(path):
            rule = parse_rule(text, f"{path.relative_to(root)}:{number}")
            if rule.kind == "FINAL":
                raise ValueError(f"{rule.source}: FINAL is only allowed in filter_local")
            rules.append(replace(rule, policy=options.get("force-policy", rule.policy)))
    return rules + finals


def resolve(target: str, rules: list[Rule]) -> Rule:
    for rule in rules:
        if rule.matches(target):
            return rule
    raise ValueError(f"no rule matches {target}; FINAL is missing")


def check_cases(root: Path = ROOT) -> tuple[list[str], int]:
    rules = load_rules(root)
    cases = json.loads((root / "tests/routing_cases.json").read_text(encoding="utf-8"))
    if not isinstance(cases, list) or not cases:
        raise ValueError("routing cases must be a non-empty list")
    expected_sources = {str(path.relative_to(root)) for path in (root / "rules").glob("*/*.list")}
    covered_sources = {case["source"] for case in cases}
    errors = [f"{source}: no routing regression case" for source in sorted(expected_sources - covered_sources)]
    for case in cases:
        result = resolve(case["target"], rules)
        # Check both policy and owning module: fallback to another list is a regression.
        if result.policy != case["policy"] or result.source.split(":", 1)[0] != case["source"]:
            errors.append(
                f'{case["target"]}: expected {case["policy"]} via {case["source"]}; '
                f"got {result.policy} via {result.source}"
            )
    return errors, len(cases)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", help="Explain one domain or literal IP in the ordered contract")
    args = parser.parse_args()
    try:
        if args.target:
            result = resolve(args.target, load_rules())
            print(f"Ordered contract: {args.target} -> {result.policy} ({result.source})")
            return 0
        errors, count = check_cases()
    except (ValueError, OSError, KeyError, TypeError) as error:
        print(f"Routing contract failed: {error}")
        return 1
    if errors:
        print("Routing contract failed:\n- " + "\n- ".join(errors))
        return 1
    print(f"Routing contract passed: {count} cases (offline model; on-device verification is separate).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
