#!/usr/bin/env python3
"""Create a compact, deterministic trait inventory for CloudStream source trees."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


TRAITS = {
    "movie": ("TvType.Movie", "newMovieLoadResponse"),
    "series": ("TvType.TvSeries", "newTvSeriesLoadResponse"),
    "live": ("TvType.Live", "newLiveStreamLoadResponse"),
    "search": ("override suspend fun search",),
    "ajax_or_post": ("app.post(", ".post("),
    "extractor_dispatch": ("loadExtractor(",),
    "custom_extractor": ("ExtractorApi",),
    "subtitles": ("subtitleCallback", "SubtitleFile("),
    "trailers": ("addTrailer(",),
    "dynamic_domain": ("DomainResolver", "lastGood", "domains.json"),
    "settings_ui": ("openSettings", "SourceSettings", "DomainUpdateUi"),
    "country_filter": ("selectedCountries", "CountryFilter"),
    "multiple_sources": ("players", "sources", "Kaynak ${"),
    "hls": ("#EXTM3U", ".m3u8"),
    "dash": ("ExtractorLinkType.DASH", ".mpd"),
    "concurrency": ("supervisorScope", "awaitAll()", "async {"),
    "artwork_cache": ("ChannelArtwork", "cacheDir"),
    "remote_catalog": ("raw.githubusercontent.com", "CATALOGUE"),
}


def source_groups(repo: Path) -> list[tuple[str, Path]]:
    groups: list[tuple[str, Path]] = []
    vendor_roots = list(repo.glob("*/src/main/kotlin/**/vendor"))
    for vendor in vendor_roots:
        for child in sorted(p for p in vendor.iterdir() if p.is_dir()):
            if any(child.rglob("*.kt")):
                groups.append((f"vendor:{child.name}", child))
    for child in sorted(p for p in repo.iterdir() if p.is_dir()):
        src = child / "src"
        if src.is_dir() and any(src.rglob("*.kt")):
            groups.append((child.name, src))
    if not groups and any(repo.rglob("*.kt")):
        groups.append((repo.name, repo))
    seen: set[tuple[str, str]] = set()
    unique: list[tuple[str, Path]] = []
    for name, path in groups:
        key = (name, str(path.resolve()))
        if key not in seen:
            seen.add(key)
            unique.append((name, path))
    return unique


def analyze(name: str, root: Path) -> dict:
    files = sorted(root.rglob("*.kt"))
    text = "\n".join(p.read_text(encoding="utf-8", errors="ignore") for p in files)
    traits = [trait for trait, needles in TRAITS.items() if any(needle in text for needle in needles)]
    return {
        "name": name,
        "path": str(root),
        "kotlinFiles": len(files),
        "traits": traits,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Inventory CloudStream provider implementation traits")
    parser.add_argument("repos", nargs="+", type=Path)
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()
    output = []
    missing = False
    for repo in args.repos:
        repo = repo.resolve()
        if not repo.is_dir():
            print(f"WARN missing repository: {repo}")
            missing = True
            continue
        output.append({
            "repository": str(repo),
            "providers": [analyze(name, path) for name, path in source_groups(repo)],
        })
    if args.as_json:
        print(json.dumps(output, ensure_ascii=False, indent=2))
    else:
        for item in output:
            print(f"\n# {item['repository']}")
            for provider in item["providers"]:
                traits = ", ".join(provider["traits"]) or "unclassified"
                print(f"- {provider['name']} ({provider['kotlinFiles']} kt): {traits}")
    return 2 if missing else 0


if __name__ == "__main__":
    raise SystemExit(main())
