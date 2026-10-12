# Browser DevTools to CloudStream provider: observed-request playbook

Source: uploaded WebDramaTurkey 63:43 tutorial, timecoded research, and visually verified Turkish on-screen writing. A case study, not a verified working extractor.

1. Verify public/authorized access and inspect the current site; do not record personal cookies, tokens or credentials.
2. Collect site navigation URLs. Normalize base and relative URLs, and verify pagination with real page 1 and 2.
3. Inspect cards for movie, series and anime separately: title, detail URL, poster src/data-src, media classification. The video's div.col selector is site-specific. **Do a DOM-backed CSS selector fixture check:** `class="media media-cover"` matches `div.media.media-cover`, NOT `div.media media-cover` (which looks for a descendant tag). Lazy posters can be on a `div[data-src]`, not `img[src]`; verify poster render on emulator after build. See [code-screen case study](../../research/tutorial-webdramaturkey-2026-10-12/code-audit/00-10-screen-and-code.md) and the adjacent fixture/test.
4. Preserve a minimal DevTools Network trace: request role, method, safe headers, POST field names, response content type, session ordering and response shape.
5. Implement and separately test getMainPage, search, load and loadLinks.
6. Source buttons may carry an ID such as data-embed. Preserve each observed source ID, host label and language; never silently choose only the first host.
7. In the demonstrated site an ID form POST was sent to /ajax/embed and the returned HTML exposed iframe[src]. Only reproduce this when the current site Network responses support it. If requests are absent in static HTML or on initial page load, **press Play and then inspect new Network requests**. Distinguish ad/tracker network traffic from player requests by inspecting response payload, resulting iframe, manifest, or actual media. Do not presume the first new request is the stream.
8. Resolve each iframe with a proven host loadExtractor or a narrow custom extractor; HTML and iframe pages are not playable ExtractorLink values.
9. **Mandatory HLS master policy:** emit ONE authentic master M3U8 per server/language in Sources. Never split master variants into independent Sources. Let CloudStream's Parçalar (Tracks) menu expose resolutions and renditions. Never label MP4 as HLS.
10. Verify separately: build, catalog, search, detail, episodes, source resolution, manifests/segments and real CloudStream playback.
11. Optional metadata must be evidence-based: do not invent rating, duration, cast, or recommendations absent from the source. Investigate live DOM, page HTML, and multiple representative detail pages, not only one screen.
12. For serialized content, test at least one two-season title; inspect the true episode container, href links and season markers, and parse `1. Bölüm`-style labels using tested formats. A fixed `substringBefore` split is fragile; preserve episode-specific URLs and season/episode numbers in `newEpisode` payloads. Build success and HTTP 200 do not prove playback.

Additional real-screen evidence is recorded in the [10:00–20:00 code audit](../../research/tutorial-webdramaturkey-2026-10-12/code-audit/10-20-screen-and-code.md). It shows why stale template metadata selectors must be replaced from DOM evidence, and why a two-season episode list needs a season-aware parser instead of a raw text split. Synthetic fixture tests validate selector assumptions, **not** live website playback.

### Source-code review gate from filmed 20:00–30:00 lesson

A `loadLinks` implementation with a `// TODO` / commented-out `loadExtractor` and `return true` **does not prove any playable link was delivered**. Treat it as a missing implementation and fail playback verification until the callback emits validated media and CloudStream actually plays it. Likewise, a series response accidentally using `TvType.Movie` or the page URL as the `episodes` parameter is an intermediate coding error, not a working reusable pattern.

When a source provides `1-sezon`-style episode URLs, parse and validate both season and episode and test a series containing at least two seasons. An empty page may be an accurate source-side condition: never equate empty with `comingSoon` without explicit evidence. Anime `Subbed/Dubbed` labels require source evidence. See the [20:00–30:00 IDE/Logcat visual audit](../../research/tutorial-webdramaturkey-2026-10-12/code-audit/20-30-screen-and-code.md) and [16-case offline fixture](../../research/tutorial-webdramaturkey-2026-10-12/code-audit/fixtures/test_episode_20_30.py).

### Video audit (30:00–40:00): HTML player shell vs actual media

The video contains a visible empty `<div id="movie-video"></div>` in `view-source`, while site JavaScript (including advertising/telemetry scripts) is present. Neither is an `ExtractorLink`. Verify whether a click on **Play** triggers a site-specific XHR/POST and whether its response contains a playable host iframe or real media. Discard tracking/ad scripts from the media evidence chain. The [actual-screen audit](../../research/tutorial-webdramaturkey-2026-10-12/code-audit/30-40-screen-and-code.md) documents when the author realizes no ready media URL appears in page source; the AJAX/source-ID result belongs to the *next* video segment, not this one.

## Failure diagnosis

| Symptom | Check |
|---|---|
| Empty catalog | Validate selectors, response HTML, JavaScript/XHR and real item cards |
| Empty episodes | Inspect episode container, IDs, classification and release status |
| HTML in Sources | Continue iframe/host resolution to media |
| HTTP 200 but no playback | Check error HTML, content type, headers, expiring tokens, HLS manifests and media segments |
| Many quality links from one HLS host | Return original master only, verify Tracks in player |
| One server fails | Handle errors independently, retain other mirrors |

## Evidence safeguards

Video includes fixes, unsuccessful host resolution, emulator experiments, and AI-generated proposals. At approximately 59:53 the tutorial author reports playback success on the recorded emulator; treat this as a historical demonstration, not proof of present-day playback on a fresh device. Mark unresolved playback as unverified. Its AAC audio is silent; narration is rendered on-screen Turkish text, NOT a spoken-word transcript. Do not turn site-specific shortcuts, URL, CSS or AJAX into universal rules.

See [movie-series.md](movie-series.md), [playback.md](playback.md), [hls-master.md](hls-master.md), [verification-and-release.md](verification-and-release.md).