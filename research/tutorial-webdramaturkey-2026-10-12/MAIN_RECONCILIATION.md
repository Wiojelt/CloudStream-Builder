# CSBuilder video research: safe integration into current main

GitHub comparison 2026-10-12: investigation branch is **diverged** from main, **82 commits ahead / 30 commits behind**; 54 changed files. Current main SKILL.md (~9.1 KB) is newer/larger than the investigation branch copy (~8.6 KB); main hls-master.md (~2.1 KB) is newer/larger than the investigation copy (~1.7 KB). Do **not** merge/replace those files blindly.

## Preserve non-negotiable current behavior

- Exactly **one authentic HLS master M3U8 per server/audio variant**, resolutions in the player **Parçalar/Tracks** menu rather than separate Sources.
- Existing integrity checks for compiled .cs3, version, fileHash, fileSize, source ZIP and public repo.json -> catalog -> download chain.
- Wiojelt repository-specific naming, branch/builds, blank commit-message and minimal-safe-change rules.

## Safe additive changes to port

1. New `cloudstream-builder/references/browser-devtools-to-provider.md` practical Network/XHR -> source ID -> AJAX -> nested iframe -> extractor playbook.
2. Research archive `research/tutorial-webdramaturkey-2026-10-12/` including both Turkish onscreen captions and **actual IDE/HTML/Logcat** audits. Keep only anonymized synthetic fixtures in GitHub.
3. Add **one cross-reference** to the new guide inside the current **main** SKILL.md, rather than copying the old research SKILL.md.
4. Apply narrow additive amendments to current main movie-series.md, playback.md, and verification-and-release.md for proven selector/metadata/episode/release-false-positive lessons.
5. Preserve **current main hls-master.md** without replacing it with older research text.

## Recommended workflow

Create a **new clean branch from latest main** (e.g. docs/csbuilder-video-playbook-2026-10-12), copy new research docs, apply cherry-picked **text additions only**, run fixture test suite, check Markdown links and YAML header, review diff for unintended code or publishing changes, and open a reviewable PR. Do not merge into production main without user review/approval.

## Boundaries

The video ends with an observed `Pushed 1 commit to origin/master` on the instructor's project, not CloudStream .cs3 release proof. Screen-caption text is sampled, not guaranteed frame-by-frame word-perfect; full 114,594-frame pixel scan does not establish human transcription of each frame. See [60:00–63:43 screen/code audit](code-audit/60-63-screen-and-code.md).