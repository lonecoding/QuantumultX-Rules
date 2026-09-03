#!/usr/bin/env python3
"""检查 Quantumult X 规则、目录结构、README 统计和配置引用。"""

from __future__ import annotations

import argparse
import ipaddress
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path
from urllib.parse import urlparse

from generate_readme import (
    discover_rule_files,
    render_root_readme,
    render_service_readme,
)


ROOT = Path(__file__).resolve().parents[1]
RULES_ROOT = ROOT / "rules"
CONFIG = ROOT / "config" / "full.conf"
ROOT_README = ROOT / "README.md"
CANONICAL_ADBLOCK = RULES_ROOT / "Advertising" / "Advertising.list"
COMPAT_ADBLOCK = ROOT / "adblock.list"
REPOSITORY_PATH = ("lonecoding", "QuantumultX-Rules")
OLD_USERNAME = "Cooper" + "We1"

ALLOWED_RULE_TYPES = {
    "FINAL",
    "GEOIP",
    "HOST",
    "HOST-KEYWORD",
    "HOST-SUFFIX",
    "IP-CIDR",
    "IP6-CIDR",
    "USER-AGENT",
}
BUILTIN_POLICIES = {
    "direct",
    "reject",
    "reject-200",
    "reject-array",
    "reject-dict",
    "reject-img",
    "reject-tinygif",
}
DOMAIN_RULE_TYPES = {"HOST", "HOST-SUFFIX"}
IP_RULE_TYPES = {"IP-CIDR", "IP6-CIDR"}
TEXT_SUFFIXES = {".conf", ".list", ".md", ".py", ".yaml", ".yml"}
URL_RE = re.compile(r"https?://[^\s<>()`]+")
DOMAIN_RE = re.compile(
    r"^(?=.{1,253}$)(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)*"
    r"[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?$",
    re.IGNORECASE,
)


def meaningful_lines(path: Path) -> list[tuple[int, str]]:
    lines: list[tuple[int, str]] = []
    for number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.strip()
        if line and not line.startswith(("#", ";")):
            lines.append((number, line))
    return lines


def configured_policies() -> set[str]:
    policies: set[str] = set()
    section = ""
    for _, line in meaningful_lines(CONFIG):
        if line.startswith("[") and line.endswith("]"):
            section = line[1:-1].strip().lower()
            continue
        if section == "policy" and "=" in line:
            _, value = line.split("=", 1)
            policies.add(value.split(",", 1)[0].strip())
    return policies


def validate_layout(paths: list[Path]) -> list[str]:
    errors: list[str] = []
    if not RULES_ROOT.is_dir():
        return ["rules: 规则目录不存在"]
    discovered = set(paths)
    all_rule_files = set(RULES_ROOT.rglob("*.list"))
    for path in sorted(all_rule_files - discovered):
        errors.append(
            f"{path.relative_to(ROOT)}: 规则文件必须位于同名服务目录中，"
            "格式为 rules/Service/Service.list"
        )
    for path in paths:
        readme = path.parent / "README.md"
        if not readme.is_file():
            errors.append(f"{readme.relative_to(ROOT)}: 缺少服务 README")
    for directory in RULES_ROOT.iterdir():
        if not directory.is_dir():
            continue
        expected = directory / f"{directory.name}.list"
        if not expected.is_file():
            errors.append(f"{expected.relative_to(ROOT)}: 缺少与服务目录同名的规则文件")
    return errors


def validate_blank_lines(path: Path) -> list[str]:
    errors: list[str] = []
    for number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip():
            errors.append(f"{path.relative_to(ROOT)}:{number}: 不允许空行")
    return errors


def validate_rule_line(
    path: Path,
    number: int,
    line: str,
    policies: set[str],
    seen: dict[tuple[str, str], tuple[Path, int]],
) -> list[str]:
    errors: list[str] = []
    parts = [part.strip() for part in line.split(",")]
    rule_type = parts[0].upper()

    if rule_type not in ALLOWED_RULE_TYPES:
        return [f"{path.relative_to(ROOT)}:{number}: 不支持的规则类型 {parts[0]}"]

    if rule_type == "FINAL":
        expected_lengths = {2}
    elif rule_type in IP_RULE_TYPES or rule_type == "GEOIP":
        expected_lengths = {3, 4}
    else:
        expected_lengths = {3}

    if len(parts) not in expected_lengths or any(not item for item in parts):
        return [f"{path.relative_to(ROOT)}:{number}: 字段数量或内容不合法"]

    if len(parts) == 4 and parts[3].lower() != "no-resolve":
        errors.append(f"{path.relative_to(ROOT)}:{number}: 不支持的规则选项 {parts[3]}")

    if rule_type in DOMAIN_RULE_TYPES and not DOMAIN_RE.fullmatch(parts[1]):
        errors.append(f"{path.relative_to(ROOT)}:{number}: 非法域名 {parts[1]}")

    if rule_type in IP_RULE_TYPES:
        try:
            network = ipaddress.ip_network(parts[1], strict=True)
            expected_version = 6 if rule_type == "IP6-CIDR" else 4
            if network.version != expected_version:
                errors.append(
                    f"{path.relative_to(ROOT)}:{number}: {rule_type} 与地址版本不一致"
                )
        except ValueError:
            errors.append(f"{path.relative_to(ROOT)}:{number}: 非法 IP/CIDR {parts[1]}")

    policy_index = 1 if rule_type == "FINAL" else 2
    policy = parts[policy_index]
    if policy not in policies and policy.lower() not in BUILTIN_POLICIES:
        errors.append(f"{path.relative_to(ROOT)}:{number}: 未定义策略 {policy}")

    if rule_type != "FINAL":
        key = (rule_type, parts[1].lower())
        if key in seen:
            old_path, old_number = seen[key]
            errors.append(
                f"{path.relative_to(ROOT)}:{number}: 与 "
                f"{old_path.relative_to(ROOT)}:{old_number} 重复"
            )
        else:
            seen[key] = (path, number)

    return errors


def validate_rules(paths: list[Path]) -> tuple[list[str], int]:
    policies = configured_policies()
    errors: list[str] = []
    seen: dict[tuple[str, str], tuple[Path, int]] = {}
    count = 0

    for path in paths:
        errors.extend(validate_blank_lines(path))
        for number, line in meaningful_lines(path):
            count += 1
            errors.extend(validate_rule_line(path, number, line, policies, seen))

    section = ""
    for number, line in meaningful_lines(CONFIG):
        if line.startswith("[") and line.endswith("]"):
            section = line[1:-1].strip().lower()
            continue
        if section == "filter_local":
            count += 1
            errors.extend(validate_rule_line(CONFIG, number, line, policies, seen))

    return errors, count


def rule_content(path: Path) -> list[str]:
    return [line for _, line in meaningful_lines(path)]


def validate_adblock_sync() -> list[str]:
    if not CANONICAL_ADBLOCK.is_file():
        return [f"{CANONICAL_ADBLOCK.relative_to(ROOT)}: 广告规则文件不存在"]
    if not COMPAT_ADBLOCK.is_file():
        return []
    if rule_content(CANONICAL_ADBLOCK) != rule_content(COMPAT_ADBLOCK):
        return ["adblock.list 与 rules/Advertising/Advertising.list 的有效规则不一致"]
    return []


def text_files() -> list[Path]:
    return [
        path
        for path in ROOT.rglob("*")
        if path.is_file()
        and ".git" not in path.parts
        and path.suffix.lower() in TEXT_SUFFIXES
    ]


def validate_old_username() -> list[str]:
    errors: list[str] = []
    for path in text_files():
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if OLD_USERNAME.lower() in line.lower():
                errors.append(
                    f"{path.relative_to(ROOT)}:{number}: 仍包含旧用户名 {OLD_USERNAME}"
                )
    return errors


def clean_url(value: str) -> str:
    return value.rstrip(".,;:]").split(",", 1)[0]


def validate_repository_urls() -> list[str]:
    errors: list[str] = []
    for path in text_files():
        content = path.read_text(encoding="utf-8")
        for match in URL_RE.findall(content):
            url = clean_url(match)
            parsed = urlparse(url)
            if parsed.netloc != "raw.githubusercontent.com":
                continue
            parts = tuple(part for part in parsed.path.split("/") if part)
            if len(parts) < 4 or parts[:2] != REPOSITORY_PATH:
                continue
            local_path = ROOT.joinpath(*parts[3:])
            if not local_path.is_file():
                errors.append(
                    f"{path.relative_to(ROOT)}: Raw 地址指向不存在的文件 "
                    f"{local_path.relative_to(ROOT)}"
                )
    return sorted(set(errors))


def validate_generated_readmes(paths: list[Path]) -> list[str]:
    errors: list[str] = []
    for path in paths:
        readme = path.parent / "README.md"
        if readme.is_file() and readme.read_text(encoding="utf-8") != render_service_readme(path):
            errors.append(f"{readme.relative_to(ROOT)}: 规则统计不是最新状态")
    if ROOT_README.read_text(encoding="utf-8") != render_root_readme(paths):
        errors.append("README.md: Rules 表格不是最新状态")
    return errors


def external_config_urls() -> list[str]:
    urls: set[str] = set()
    for match in URL_RE.findall(CONFIG.read_text(encoding="utf-8")):
        url = clean_url(match)
        parsed = urlparse(url)
        if parsed.netloc == "raw.githubusercontent.com" and tuple(
            part for part in parsed.path.split("/") if part
        )[:2] == REPOSITORY_PATH:
            continue
        if "example.com" not in parsed.netloc:
            urls.add(url)
    return sorted(urls)


def validate_external_urls() -> list[str]:
    errors: list[str] = []
    for url in external_config_urls():
        request = urllib.request.Request(
            url,
            headers={"User-Agent": "QuantumultX-Rules-validator/1.0", "Range": "bytes=0-0"},
        )
        try:
            with urllib.request.urlopen(request, timeout=15) as response:
                if response.status >= 400:
                    errors.append(f"外部地址返回 HTTP {response.status}: {url}")
        except (urllib.error.URLError, TimeoutError) as error:
            errors.append(f"外部地址不可访问: {url} ({error})")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check-external-urls",
        action="store_true",
        help="联网检查 full.conf 中的外部地址",
    )
    args = parser.parse_args()

    paths = discover_rule_files()
    errors = validate_layout(paths)
    rule_errors, rule_count = validate_rules(paths)
    errors.extend(rule_errors)
    errors.extend(validate_adblock_sync())
    errors.extend(validate_old_username())
    errors.extend(validate_repository_urls())
    errors.extend(validate_generated_readmes(paths))
    if args.check_external_urls:
        errors.extend(validate_external_urls())

    if errors:
        print("检查失败：")
        for error in errors:
            print(f"- {error}")
        return 1

    print(
        f"检查通过：{rule_count} 条规则，{len(paths)} 个服务，"
        f"{len(configured_policies())} 个策略组。"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
