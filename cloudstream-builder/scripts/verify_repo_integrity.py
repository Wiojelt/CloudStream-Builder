#!/usr/bin/env python3
"""Verify every local CloudStream catalog against its packaged .cs3 files.

Use --fix before publishing, then run again without --fix. HTTP checks of the
published repo.json -> catalog -> package chain remain a separate release step.
"""

import argparse
import hashlib
import json
import sys
import zipfile
from pathlib import Path
from urllib.parse import unquote, urlparse


DEFAULT_REPOS = [
    Path(r"C:\Users\root\Downloads\cloudstream-work\TurkSinema-deploy"),
    Path(r"C:\Users\root\Downloads\cloudstream-work\TurkSpor"),
    Path(r"C:\Users\root\Downloads\cloudstream-work\WioSpor-builds"),
    Path(r"C:\Users\root\Downloads\cloudstream-work\WioSinema"),
    Path(r"C:\Users\root\Downloads\cloudstream-work\test"),
]


def package_path(repo: Path, entry: dict) -> Path:
    filename = unquote(Path(urlparse(entry.get("url", "")).path).name)
    candidates = [repo / filename, repo / f"{entry.get('internalName', '')}.cs3"]
    return next((path for path in candidates if path.is_file()), candidates[0])


def audit_catalog(repo: Path, catalog: Path, fix: bool, selected: set[str]) -> tuple[int, int, int]:
    try:
        entries = json.loads(catalog.read_text(encoding="utf-8"))
        if not isinstance(entries, list):
            raise ValueError("catalog must be a JSON array")
    except (OSError, ValueError) as error:
        print(f"[ERROR] {catalog}: {error}")
        return 1, 0, 0

    unresolved = changed = checked = 0
    for entry in entries:
        if not isinstance(entry, dict):
            print(f"[ERROR] {catalog}: non-object entry")
            unresolved += 1
            continue
        name = entry.get("internalName") or entry.get("name") or "<unnamed>"
        if selected and name not in selected:
            continue
        checked += 1
        package = package_path(repo, entry)
        if not package.is_file():
            print(f"[MISSING] {catalog}: {name}: {package.name}")
            unresolved += 1
            continue
        try:
            with zipfile.ZipFile(package) as archive:
                manifest = json.loads(archive.read("manifest.json"))
            version = manifest["version"]
        except (OSError, ValueError, KeyError, zipfile.BadZipFile) as error:
            print(f"[INVALID] {package}: {error}")
            unresolved += 1
            continue
        data = package.read_bytes()
        digest = hashlib.sha256(data).hexdigest()
        expected = {"version": version, "fileSize": len(data), "fileHash": f"sha256-{digest}"}
        if "hash" in entry:
            expected["hash"] = digest
        mismatches = [key for key, value in expected.items() if entry.get(key) != value]
        if "filesize" in entry:
            mismatches.append("filesize (obsolete)")
        if mismatches:
            print(f"[MISMATCH] {catalog}: {name}: {', '.join(mismatches)}")
            if fix:
                entry.update(expected)
                entry.pop("filesize", None)
                changed += 1
            else:
                unresolved += 1

    if fix and changed:
        catalog.write_text(json.dumps(entries, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"[SAVED] {catalog}: {changed} corrected")
    print(f"[AUDIT] {catalog}: {checked} checked, {unresolved} unresolved")
    return unresolved, changed, checked


def audit_repo(repo: Path, fix: bool, selected: set[str]) -> tuple[int, int, int]:
    catalogs = [path for path in [repo / "plugins.json", *repo.glob("catalogs/**/plugins.json")] if path.is_file()]
    if not catalogs:
        print(f"[ERROR] {repo}: no plugins.json catalog found")
        return 1, 0, 0
    results = [audit_catalog(repo, catalog, fix, selected) for catalog in catalogs]
    return tuple(sum(result[index] for result in results) for index in range(3))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repos", nargs="*", type=Path, help="local builds checkout directories")
    parser.add_argument("--fix", action="store_true", help="synchronize catalog metadata with packages")
    parser.add_argument("--all", action="store_true", help="audit all existing default repository paths")
    parser.add_argument("--only", action="append", default=[], metavar="INTERNAL_NAME")
    args = parser.parse_args()
    repos = [repo for repo in DEFAULT_REPOS if repo.exists()] if args.all or not args.repos else args.repos
    if not repos:
        print("[ERROR] no repositories found")
        return 1
    results = [audit_repo(repo.resolve(), args.fix, set(args.only)) for repo in repos]
    unresolved, changed, checked = (sum(result[index] for result in results) for index in range(3))
    print(f"SUMMARY: {checked} catalog entries checked, {changed} corrected, {unresolved} unresolved")
    return 1 if unresolved else 0


if __name__ == "__main__":
    sys.exit(main())
