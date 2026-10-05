# Verification and release

## Required gates

Before delivery, confirm:

- `review.json` decisions exist and no included section is unconfirmed.
- Film and series detail paths were inspected when both are advertised.
- Search, detail, and playback return useful results for representative items.
- Trailers are isolated from playback sources.
- Multiple servers and subtitles are retained when observed.
- Gradle produced the intended `.cs3` and the source ZIP matches its version.
- Every local catalog integrity check passes: run `python scripts/verify_repo_integrity.py <repo_dir> --fix` and then again without `--fix`. This includes `plugins.json` and `catalogs/**/plugins.json`; version, byte size, `fileHash`, and optional `hash` must match each physical `.cs3`.
- `status.json` distinguishes build, HTTP smoke checks, and actual playback verification.

Run `python C:/Users/root/.codex/skills/cloudstream-builder/scripts/audit_job.py JOB`. Run `python scripts/verify_repo_integrity.py <repo_dir>` before push. Treat missing job artifacts, mismatched hashes, and contradictory verification flags as failures. The audit is structural; it cannot prove a site's current playback.


## Device verification

Use `artemis-android` only when requested or when live app verification is part of the task. Check `adb devices -l` first. If multiple devices are online, ask the user which serial to use. Validate the visible provider, catalog/detail screen, and one playback flow. Record the actual result rather than inferring it from build output.

## Packaging

Deliver the `.cs3` and source ZIP produced by the same build. Scan the bundle/source for secrets and machine-specific paths. Keep logs outside the bundle unless they are explicitly requested and sanitized.

## GitHub

Do not push without authorization. When authorized, verify repository and branch before mutation. For the user's TurkStream repositories, use a completely blank commit message. After pushing, run `node scripts/verify_remote_repo.mjs <public-repo.json-URL>` to check each linked catalog and package URL for HTTP 200, byte count, and SHA-256. GitHub raw URLs can briefly serve cached catalog content, so update the `repo.json` catalog URL query when necessary and confirm the new chain. An immutable commit URL is suitable for an intentionally frozen release; a rolling catalog should keep a branch URL so later packages remain discoverable.
