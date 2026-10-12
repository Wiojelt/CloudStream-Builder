# Browser DevTools to CloudStream provider: observed-request playbook

Source: uploaded WebDramaTurkey 63:43 tutorial, timecoded research, and visually verified Turkish on-screen writing. A case study, not a verified working extractor.

1. Verify public/authorized access and inspect the current site; do not record personal cookies, tokens or credentials.
2. Collect site navigation URLs. Normalize base and relative URLs, and verify pagination with real page 1 and 2.
3. Inspect cards for movie, series and anime separately: title, detail URL, poster src/data-src, media classification. The video's div.col selector is site-specific.
4. Preserve a minimal DevTools Network trace: request role, method, safe headers, POST field names, response content type, session ordering and response shape.
5. Implement and separately test getMainPage, search, load and loadLinks.
6. Source buttons may carry an ID such as data-embed. Preserve each observed source ID, host label and language; never silently choose only the first host.
7. In the demonstrated site an ID form POST was sent to /ajax/embed and the returned HTML exposed iframe[src]. Only reproduce this when the current site Network responses support it.
8. Resolve each iframe with a proven host loadExtractor or a narrow custom extractor; HTML and iframe pages are not playable ExtractorLink values.
9. **Mandatory HLS master policy:** emit ONE authentic master M3U8 per server/language in Sources. Never split master variants into independent Sources. Let CloudStream's Parçalar (Tracks) menu expose resolutions and renditions. Never label MP4 as HLS.
10. Verify separately: build, catalog, search, detail, episodes, source resolution, manifests/segments and real CloudStream playback.
11. Optional metadata must be evidence-based: do not invent rating, duration, cast, or recommendations absent from the source. Investigate live DOM, page HTML, and multiple representative detail pages, not only one screen.
12. For serialized content, test at least one two-season title; inspect the true episode container, href links and season markers, and parse `1. Bölüm`-style labels using tested formats. A fixed `substringBefore` split is fragile; preserve episode-specific URLs and season/episode numbers in `newEpisode` payloads. Build success and HTTP 200 do not prove playback.

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

Video includes fixes, unsuccessful host resolution, emulator experiments, and AI-generated proposals. Mark unresolved playback as unverified. Its AAC audio is silent; narration is rendered on-screen Turkish text, NOT a spoken-word transcript. Do not turn site-specific shortcuts, URL, CSS or AJAX into universal rules.

See [movie-series.md](movie-series.md), [playback.md](playback.md), [hls-master.md](hls-master.md), [verification-and-release.md](verification-and-release.md).