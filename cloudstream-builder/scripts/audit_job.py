#!/usr/bin/env python3
"""Structural audit for a TurkStream Studio job. Does not claim playback success."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def read_json(path: Path, errors: list[str]):
    if not path.is_file():
        errors.append(f"missing: {path.name}")
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"invalid {path.name}: {exc}")
        return None


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit a TurkStream Studio provider job")
    parser.add_argument("job", type=Path)
    args = parser.parse_args()
    job = args.job.resolve()
    errors: list[str] = []
    warnings: list[str] = []

    if not job.is_dir():
        print(f"FAIL job directory not found: {job}")
        return 2

    review = read_json(job / "review.json", errors)
    spec = read_json(job / "spec.json", errors)
    decisions = read_json(job / "decisions.json", errors)
    status = read_json(job / "status.json", errors)

    if review:
        sections = review.get("sections") or []
        if not sections:
            errors.append("review.json has no discovered sections")
        unconfirmed = [str(x.get("title") or x.get("selector") or "unnamed") for x in sections if x.get("include") and x.get("role") not in {"media", "text", "ignore"}]
        if unconfirmed:
            errors.append("unconfirmed included sections: " + ", ".join(unconfirmed))
        if not any(x.get("include") and x.get("role") == "media" for x in sections):
            errors.append("no included media section")

    if decisions is None:
        errors.append("catalog decisions were not approved")

    provider_name = ""
    if spec:
        provider_name = str(spec.get("name") or "").strip()
        if not provider_name:
            errors.append("spec.json has no provider name")
        if not str(spec.get("baseUrl") or spec.get("base_url") or "").strip():
            warnings.append("spec.json base URL could not be identified")

    kotlin_files = list(job.rglob("*.kt"))
    if not kotlin_files:
        errors.append("no Kotlin source found")
    else:
        combined = "\n".join(path.read_text(encoding="utf-8", errors="ignore") for path in kotlin_files)
        for required in ("load(", "loadLinks("):
            if required not in combined:
                errors.append(f"Kotlin source has no {required}")
        if "youtube" in combined.lower() and "addTrailer" not in combined:
            warnings.append("YouTube reference found without addTrailer; check trailer isolation")

    if status:
        built = bool(status.get("built"))
        cs3 = Path(str(status.get("cs3") or ""))
        source_zip = Path(str(status.get("zip") or ""))
        if built and not cs3.is_file():
            errors.append("status says built but cs3 is missing")
        if built and not source_zip.is_file():
            errors.append("status says built but source ZIP is missing")
        if status.get("playbackVerified") and not status.get("playbackEvidence"):
            errors.append("playbackVerified is true without playbackEvidence")
        if not status.get("playbackVerified"):
            warnings.append("actual CloudStream playback is not verified")

    label = provider_name or job.name
    for item in warnings:
        print(f"WARN {item}")
    for item in errors:
        print(f"FAIL {item}")
    if errors:
        print(f"RESULT {label}: failed ({len(errors)} errors, {len(warnings)} warnings)")
        return 1
    print(f"RESULT {label}: structural audit passed ({len(warnings)} warnings)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
