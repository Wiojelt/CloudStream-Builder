# Browser DevTools → CloudStream provider: reproducible workflow

This playbook is a tested *reasoning process*, not a promise that one site's selectors or endpoints will work on other sites. It was distilled from a 63:43 screen-recorded tutorial plus CSBuilder's existing extraction patterns. User-accessible/authorized sites only. Never commit sessions, personal cookies, passwords, signed URLs or device tokens.

## 1. Establish the source contract

1. Open the site's home, one movie, one series (preferably two seasons), and a search result. Record **real** category href, pagination, title, poster, plot, and episode selectors. Test page 1 **and** page 2.
2. Identify where lazy imagery resides. `class="media media-cover"` matches CSS `div.media.media-cover`; **not** `div.media media-cover`. Posters may be a `div[data-src]`, not `img[src]`.
3. Separate the source's actual movie, series and anime page templates. Avoid fabricating missing rating, cast, runtime, episodes, seasons or 'coming soon' flags.
4. Do not treat all `/film/`-missing URLs as series. Prefer observed episodes, structured metadata and verified route markers.

## 2. Inspect the playback request chain

1. Open Network with **Preserve log**. Record the response URL, method, content type, necessary *non-secret* headers, and the shape of request/response data.
2. Compare requests **before and after Play**. Ad/tracker XHRs, marketing scripts, an empty `<div id="movie-video">`, and HTTP 200 HTML are **not** playable media.
3. Source selectors sometimes have a selected `a[data-embed]` plus separate `button[data-embed]` mirrors. Query actual child nodes, not a parent `div` with no ID attribute. Preserve first/middle/last sources, language and host labels; drop blank IDs and duplicate selected IDs.
4. Reproduce only observed requests. In the tutorial's **site-specific example**, the ID was form-posted to `/ajax/embed` with a page `Referer`, `X-Requested-With: XMLHttpRequest`, and a form-encoded `id` field. Its response was HTML containing an iframe, **not** an M3U8.
5. Resolve each iframe with a validated HTTP(S) URL, correct response-relative base and host-specific Referer, following the allowed chain as needed. Do not turn a missing `iframe[src]` into the literal string `"null"`. Unsupported/failed hosts must not prevent other mirrors from being tried.
6. Prefer registered `loadExtractor` for supported hosts; write a narrow extractor only when the host contract is observed and repeatable. Preserve external subtitles and audio-language variants.

## 3. Release gates

- `getMainPage`, `search`, `load`, episode responses and `loadLinks` must be checked as **separate** functions. A homepage result does not certify episode parsing or playback.
- Reject `loadLinks` TODO stubs and false-positive `return true` results when no playable-link callback is emitted.
- Test two seasons, repeated episode numbers, empty unannounced release pages, and explicit coming-soon pages. Do not default missing `data-season` to 1 without evidence.
- **Mandatory:** when an authentic HLS master exists, emit **exactly one** `ExtractorLinkType.M3U8` source per server/audio variant. 1080p/720p/480p appear under the player's **Parçalar / Video Tracks**, *not* separate Sources. Do not call `M3u8Helper.generateM3u8` on a master. If only fixed resolutions exist and no maintained authorized master, offer one verified link per server/audio and report the limitation; MP4 is not HLS.
- `BUILD SUCCESSFUL`, HTTP 200, an iframe, an emulator spinner or even a recorded tutorial's playback claim are not **current** playback verification. Record representative manifest + segments, real app playback, and separate catalog/hash/size/install-chain checks.

References: [movie-series.md](movie-series.md), [playback.md](playback.md), [hls-master.md](hls-master.md), [verification-and-release.md](verification-and-release.md), [extractor library](../extractors/INDEX.md).