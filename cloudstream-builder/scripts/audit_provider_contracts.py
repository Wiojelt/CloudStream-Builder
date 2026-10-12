#!/usr/bin/env python3
"""Conservative static preflight for CloudStream Kotlin providers and extractors.

Finds suspect code patterns. This is NOT a compiler, proof of runtime behavior,
or a replacement for replaying site requests and playing in the CloudStream app.
Uses Python standard library only. Operates on local paths (never network).
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class Finding:
    severity: str
    rule: str
    path: str
    line: int
    detail: str


def mask_noncode(source: str) -> str:
    """Replace comments and quoted content by spaces while preserving offsets."""
    out = list(source)
    n = len(source)
    i = 0

    def blank(a: int, b: int) -> None:
        for k in range(a, b):
            if source[k] not in "\r\n":
                out[k] = " "

    while i < n:
        if source.startswith("//", i):
            end = source.find("\n", i + 2)
            j = n if end == -1 else end
            blank(i, j)
            i = j
        elif source.startswith("/*", i):
            j = i + 2
            depth = 1
            while j < n and depth:
                if source.startswith("/*", j):
                    depth += 1
                    j += 2
                elif source.startswith("*/", j):
                    depth -= 1
                    j += 2
                else:
                    j += 1
            blank(i, j)
            i = j
        elif source.startswith('"""', i):
            end = source.find('"""', i + 3)
            j = n if end < 0 else end + 3
            blank(i, j)
            i = j
        elif source[i] in "'\"":
            quote = source[i]
            j = i + 1
            while j < n:
                if source[j] == "\\":
                    j += 2
                    continue
                if source[j] == quote:
                    j += 1
                    break
                j += 1
            blank(i, min(j, n))
            i = min(j, n)
        else:
            i += 1
    return "".join(out)


def line_at(source: str, offset: int) -> int:
    return source.count("\n", 0, offset) + 1


def function_ranges(masked: str, method: str) -> list[tuple[int, int]]:
    result = []
    for match in re.finditer(r"\bfun\s+" + re.escape(method) + r"\s*\(", masked):
        cursor = masked.find("{", match.end())
        # Kotlin interface methods may be abstract; do not walk into next function.
        next_fun = re.search(r"\b(?:override\s+)?(?:suspend\s+)?fun\s+\w+", masked[match.end():cursor if cursor >= 0 else len(masked)])
        if cursor < 0 or next_fun:
            continue
        depth = 1
        pos = cursor + 1
        while pos < len(masked) and depth:
            if masked[pos] == "{":
                depth += 1
            elif masked[pos] == "}":
                depth -= 1
            pos += 1
        if depth == 0:
            result.append((cursor + 1, pos - 1))
    return result


def analyze_source(text: str, filename: str) -> list[Finding]:
    findings: list[Finding] = []
    code = mask_noncode(text)

    def add(severity: str, rule: str, offset: int, detail: str):
        findings.append(Finding(severity, rule, filename, line_at(text, offset), detail))

    # Master or media playlist type is not statically decidable. Require review.
    for m in re.finditer(r"\b(?:M3u8Helper\s*\.\s*)?generateM3u8\s*\(", code):
        add("warning", "HLS_SPLIT_REVIEW", m.start(),
            "Check argument manifest: a real master must be emitted as ONE M3U8 source; "
            "never expand its resolution variants in Sources.")

    for start, end in function_ranges(code, "loadLinks"):
        body = code[start:end]
        for m in re.finditer(r"\breturn\s+true\b", body):
            add("warning", "LOADLINKS_TRUE_WITHOUT_PROOF", start + m.start(),
                "A literal return true does not prove a playable callback fired. "
                "Count callback emissions and require real-device playback evidence.")
        if re.search(r"\bTODO\s*\(", body):
            add("error", "LOADLINKS_TODO", start,
                "loadLinks still has executable TODO; it cannot be released.")

    # In video the class div.nav-player-select lacks data-embed; children contain it.
    wrong = re.compile(
        r"\bselect(?:First)?\(\s*['\"](?:div\.)?nav-player-select['\"]\s*\)"
        r"\s*(?:\?\s*)?\.attr\(\s*['\"]data-embed['\"]\s*\)",
        re.S,
    )
    for m in wrong.finditer(text):
        if not code[m.start():m.start()+5].strip():
            continue
        add("warning", "SOURCE_ID_PARENT", m.start(),
            "Source IDs are likely on nested a/button[data-embed], not the container.")

    assignment = re.compile(
        r"\b(?:val|var)\s+(\w+)\s*=\s*[^\n;]*?"
        r"\.select\(\s*['\"](?:div\.)?nav-player-select['\"]\s*\)",
    )
    for m in assignment.finditer(text):
        variable = m.group(1)
        later = re.search(r"\b" + re.escape(variable) + r"\s*\.attr\(\s*['\"]data-embed['\"]", text[m.end():])
        if later:
            idx = m.end() + later.start()
            add("warning", "SOURCE_ID_PARENT", idx,
                "Selected parent container read through variable; inspect nested ID nodes.")

    nullable_src = re.compile(
        r"\?\s*\.attr\(\s*['\"]src['\"]\s*\)\s*(?:\?\s*)?\.toString\(\s*\)",
        re.S,
    )
    for m in nullable_src.finditer(text):
        add("warning", "NULL_IFRAME_URL", m.start(),
            "Nullable iframe attr converted to a String; avoid literal 'null' URLs.")

    # Check a function that hardcodes the main URL although page+request exist.
    for start, end in function_ranges(code, "getMainPage"):
        part = text[start:end]
        if "app.get(mainUrl)" in part and "request.data" not in part and "$page" not in part:
            add("info", "HOMEPAGE_IGNORES_PAGE", start,
                "Sample getMainPage reads only mainUrl; verify request.data and pagination.")
    return sorted(findings, key=lambda f: (f.path, f.line, f.rule))


def scan_paths(paths: list[Path]) -> list[Finding]:
    files = []
    for path in paths:
        if path.is_file() and path.suffix == ".kt":
            files.append(path)
        elif path.is_dir():
            files.extend(path.rglob("*.kt"))
    issues = []
    for file in sorted(set(f.resolve() for f in files)):
        try:
            issues.extend(analyze_source(file.read_text(encoding="utf-8"), str(file)))
        except (OSError, UnicodeError) as exc:
            issues.append(Finding("error", "READ_FAILURE", str(file), 1, str(exc)))
    return issues


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("paths", nargs="+", type=Path, help="Kotlin files or directories")
    ap.add_argument("--strict", action="store_true", help="Treat review warnings as release failures")
    ap.add_argument("--json", action="store_true", help="Emit structured results")
    args = ap.parse_args()
    issues = scan_paths(args.paths)
    if args.json:
        print(json.dumps([asdict(f) for f in issues], ensure_ascii=False, indent=2))
    else:
        for f in issues:
            print(f"{f.severity.upper()} {f.rule} {f.path}:{f.line} {f.detail}")
        print(f"Scanned: {len(issues)} findings")
    return 1 if any(f.severity == "error" or (args.strict and f.severity == "warning")
                    for f in issues) else 0


if __name__ == "__main__":
    sys.exit(main())
