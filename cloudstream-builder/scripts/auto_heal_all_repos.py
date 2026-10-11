#!/usr/bin/env python3
"""Auto-heals and verifies CloudStream repository catalogs across all Wio repositories.

1. Audits live downloadable .cs3 packages for every entry in plugins.json.
2. Fixes hash, size, version, and cache-buster query mismatches.
3. Updates cache busters in repo.json.
4. Auto-commits and pushes fixes to git remotes.
5. Verifies end-to-end installation health.
"""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import subprocess
import sys
import time
import urllib.request
import zipfile
from pathlib import Path

REPOS_CONFIG = [
    {
        "name": "WioSinema",
        "path": Path(r"C:\Users\root\Downloads\cloudstream-work\WioSinema"),
        "branch": "main",
        "repo_json": "https://raw.githubusercontent.com/Wiojelt/WioSinema/main/repo.json",
    },
    {
        "name": "WioAnime",
        "path": Path(r"C:\Users\root\Downloads\cloudstream-work\WioAnime"),
        "branch": "main",
        "repo_json": "https://raw.githubusercontent.com/Wiojelt/WioAnime/main/repo.json",
    },
    {
        "name": "WioDrama",
        "path": Path(r"C:\Users\root\Downloads\cloudstream-work\WioDrama"),
        "branch": "main",
        "repo_json": "https://raw.githubusercontent.com/Wiojelt/WioDrama/main/repo.json",
    },
    {
        "name": "WioKids",
        "path": Path(r"C:\Users\root\Downloads\cloudstream-work\WioKids"),
        "branch": "main",
        "repo_json": "https://raw.githubusercontent.com/Wiojelt/WioKids/main/repo.json",
    },
    {
        "name": "WioCinema",
        "path": Path(r"C:\Users\root\Downloads\cloudstream-work\WioCinema"),
        "branch": "main",
        "repo_json": "https://raw.githubusercontent.com/Wiojelt/WioCinema/main/repo.json",
    },
    {
        "name": "WioAsya",
        "path": Path(r"C:\Users\root\Downloads\cloudstream-work\WioAsya"),
        "branch": "main",
        "repo_json": "https://raw.githubusercontent.com/Wiojelt/WioAsya/main/repo.json",
    },
    {
        "name": "TurkSinema-deploy",
        "path": Path(r"C:\Users\root\Downloads\cloudstream-work\TurkSinema-deploy"),
        "branch": "builds",
        "repo_json": "https://raw.githubusercontent.com/Wiojelt/TurkSinema/builds/repo.json",
    },
    {
        "name": "TurkSpor",
        "path": Path(r"C:\Users\root\Downloads\cloudstream-work\TurkSpor"),
        "branch": "builds",
        "repo_json": "https://raw.githubusercontent.com/Wiojelt/TurkSpor/builds/repo.json",
    },
    {
        "name": "test",
        "path": Path(r"C:\Users\root\Downloads\cloudstream-work\test"),
        "branch": "builds",
        "repo_json": "https://raw.githubusercontent.com/Wiojelt/test/builds/repo.json",
    },
]


def git_cmd(repo_path: Path, args: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git"] + args,
        cwd=repo_path,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )


def fetch_bytes(url: str, timeout: int = 15) -> bytes | None:
    try:
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "CloudStream/3 AutoHealer",
                "Cache-Control": "no-cache",
            },
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read()
    except Exception as e:
        print(f"  [HTTP ERR] {url} -> {e}")
        return None


def heal_catalog(catalog_path: Path, local_repo: Path, fix: bool) -> tuple[int, int, int]:
    try:
        entries = json.loads(catalog_path.read_text(encoding="utf-8"))
        if not isinstance(entries, list):
            return 1, 0, 0
    except Exception as e:
        print(f"  [ERROR] Cannot parse {catalog_path}: {e}")
        return 1, 0, 0

    checked = changed = unresolved = 0

    for entry in entries:
        if not isinstance(entry, dict):
            continue
        name = entry.get("internalName") or entry.get("name") or "<unnamed>"
        checked += 1
        url = entry.get("url", "")

        pkg_bytes = None
        # Priority 1: Fetch from live URL (exact bytes downloaded by Cloudstream clients)
        if url:
            pkg_bytes = fetch_bytes(url)

        # Priority 2: Fallback to local files if URL failed
        if not pkg_bytes:
            candidate_names = [
                f"{name}.cs3",
                f"{entry.get('name', '')}.cs3",
                Path(url).name.split("?")[0] if url else "",
            ]
            for c in candidate_names:
                if not c:
                    continue
                p = local_repo / c
                if p.is_file():
                    pkg_bytes = p.read_bytes()
                    break

        if not pkg_bytes:
            print(f"  [MISSING] {name}: Cannot retrieve package locally or via URL")
            unresolved += 1
            continue

        raw_digest = hashlib.sha256(pkg_bytes).hexdigest()
        actual_size = len(pkg_bytes)
        actual_hash = f"sha256-{raw_digest}"

        actual_version = entry.get("version", 1)
        try:
            with zipfile.ZipFile(io.BytesIO(pkg_bytes)) as z:
                if "manifest.json" in z.namelist():
                    manifest = json.loads(z.read("manifest.json").decode("utf-8"))
                    actual_version = manifest.get("version", actual_version)
        except Exception:
            pass

        mismatches = []
        if entry.get("fileSize") != actual_size:
            mismatches.append(f"fileSize ({entry.get('fileSize')} -> {actual_size})")
        if entry.get("fileHash") != actual_hash:
            mismatches.append(f"fileHash ({entry.get('fileHash')} -> {actual_hash})")
        if entry.get("version") != actual_version:
            mismatches.append(f"version ({entry.get('version')} -> {actual_version})")

        if mismatches:
            print(f"  [MISMATCH] {name}: {', '.join(mismatches)}")
            if fix:
                entry["fileSize"] = actual_size
                entry["fileHash"] = actual_hash
                entry["version"] = actual_version
                if "hash" in entry:
                    entry["hash"] = raw_digest
                entry.pop("filesize", None)

                # Update query param ?v= if present to bust client/worker caches
                if url and "workers.dev" in url and "?v=" in url:
                    base_url = url.split("?")[0]
                    entry["url"] = f"{base_url}?v={raw_digest[:12]}"

                changed += 1
            else:
                unresolved += 1

    if fix and changed > 0:
        catalog_path.write_text(json.dumps(entries, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"  [FIXED] {catalog_path.name}: {changed} entries updated.")

    return unresolved, changed, checked


def update_repo_cache_buster(repo_path: Path):
    repo_json_path = repo_path / "repo.json"
    if not repo_json_path.is_file():
        return
    try:
        data = json.loads(repo_json_path.read_text(encoding="utf-8"))
        lists = data.get("pluginLists", [])
        ts = int(time.time())
        new_lists = []
        for l in lists:
            base = l.split("?")[0].replace("/refs/heads/", "/")
            new_lists.append(f"{base}?t={ts}")
        data["pluginLists"] = new_lists
        repo_json_path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"  [CACHE BUSTER] Updated {repo_json_path.name} timestamp: {ts}")
    except Exception as e:
        print(f"  [WARN] Failed to update repo.json cache buster: {e}")


def process_repo(config: dict, fix: bool, push: bool) -> tuple[int, int, int]:
    repo_path: Path = config["path"]
    name: str = config["name"]
    branch: str = config.get("branch", "main")

    if not repo_path.is_dir():
        print(f"\n[SKIP] {name}: Directory does not exist: {repo_path}")
        return 0, 0, 0

    print(f"\n========================================")
    print(f"AUDITING REPO: {name} ({repo_path})")
    print(f"========================================")

    # Pull latest commits from origin if present
    pull_res = git_cmd(repo_path, ["pull", "--ff-only", "origin", branch])
    if pull_res.returncode != 0 and pull_res.stderr.strip():
        print(f"  [GIT PULL NOTICE] {pull_res.stderr.strip()}")

    catalogs = [p for p in [repo_path / "plugins.json", *repo_path.glob("catalogs/**/plugins.json")] if p.is_file()]
    if not catalogs:
        print(f"  [WARN] No plugins.json found in {name}")
        return 0, 0, 0

    total_unresolved = total_changed = total_checked = 0
    for cat in catalogs:
        unres, chg, chk = heal_catalog(cat, repo_path, fix)
        total_unresolved += unres
        total_changed += chg
        total_checked += chk

    if fix and total_changed > 0:
        update_repo_cache_buster(repo_path)
        if push:
            print(f"  [GIT] Committing and pushing {name}...")
            git_cmd(repo_path, ["add", "-A"])
            commit_res = git_cmd(repo_path, ["commit", "-m", f"chore(catalog): auto-heal package hashes and sizes ({total_changed} fixed)"])
            print(f"  [GIT COMMIT] {commit_res.stdout.strip()}")
            push_res = git_cmd(repo_path, ["push", "origin", branch])
            if push_res.returncode == 0:
                print(f"  [GIT PUSH] Pushed to origin/{branch} successfully.")
            else:
                print(f"  [GIT PUSH ERR] {push_res.stderr.strip()}")

    return total_unresolved, total_changed, total_checked


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fix", action="store_true", help="Auto-fix discrepancies in plugins.json")
    parser.add_argument("--push", action="store_true", help="Auto-push fixes to Git remotes")
    parser.add_argument("--only", type=str, default="", help="Run only on specific repository name")
    args = parser.parse_args()

    repos = [r for r in REPOS_CONFIG if not args.only or r["name"].lower() == args.only.lower()]
    total_unresolved = total_changed = total_checked = 0

    for r in repos:
        unres, chg, chk = process_repo(r, args.fix, args.push)
        total_unresolved += unres
        total_changed += chg
        total_checked += chk

    print(f"\n========================================")
    print(f"GLOBAL AUDIT COMPLETE:")
    print(f"  Total Checked:    {total_checked}")
    print(f"  Total Corrected:  {total_changed}")
    print(f"  Total Unresolved: {total_unresolved}")
    print(f"========================================\n")

    return 1 if total_unresolved > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
