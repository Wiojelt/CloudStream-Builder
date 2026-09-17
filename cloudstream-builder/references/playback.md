# Playback, trailers, and subtitles

## Extraction ladder

Resolve each source using the narrowest observed mechanism:

1. Emit direct chunked `.m3u8` (`ExtractorLinkType.M3U8`) manifests as first priority. Even when fixed resolution choices (1080p, 720p, 480p) are provided by a site or API, map and separate them into chunked HLS streams with explicit `quality` tags. Only fall back to monolithic `.mp4` (`ExtractorLinkType.VIDEO`) when no HLS manifest exists.
2. Use `loadExtractor` for a supported host iframe.
3. Add a focused extractor for an unsupported player host.
4. Reproduce the site's AJAX/API request when the player is generated dynamically.

Do not emit an iframe page, HTML endpoint, expired token, empty URL, or trailer as a video link. These commonly surface as CloudStream error 2004 or “bağlantı bulunamadı”. A 200 HTML response is not playable-media evidence. All emitted streams must specify target player `Referer` and `User-Agent` headers.

## Headers and session state

Preserve required `Referer`, `Origin`, user agent, and session cookies across the exact request chain. Do not hard-code personal cookies or device tokens. If access requires a user session, keep it on-device and document the prerequisite.

Resolve relative URLs against the response URL or an effective `<base>` tag, not blindly against the original home page.

## Multiple sources and extractor priority

Keep all observed server choices and language variants. Label results with the site's source name and quality. Catch a failure per source so one dead mirror does not suppress working mirrors. Use bounded concurrency only for independent requests; preserve order where a token or cookie is produced sequentially.

Sort fast direct CDN extractors (e.g. Vidmoly 1080p, Morencius HLS, Fastly) at the top of the emission queue. Slow, rate-limited, or P2P/iframe hosts (e.g. OKRU, Sibnet) should be emitted secondarily. Emitting slow hosts first causes CloudStream's internal player to stall during initial buffering.

For live IPTV streams with freeze/stalling issues on Android/TV devices, advise users to configure CloudStream internal player buffer: Video arabellek boyutu ~70MB, uzunluğu ~3dk, and disk cache set to High/Very High to eliminate playback interruptions without external players.

## Trailers

Put YouTube or other trailer URLs in `addTrailer`. Exclude them from player candidates and from `loadLinks`. A trailer iframe proves only trailer availability.

## Subtitles

Inspect player JSON, track tags, manifests, and player API responses. Emit every observed subtitle with a human-readable language/label and an absolute URL. Resolve escaped JSON URLs before callback. Do not report subtitle support merely because a player UI has a subtitle button.

## Playback evidence

For HTTP smoke checks, record final URL, status, content type, and whether the body is a manifest or media response. For CloudStream verification, record provider, item, selected source, outcome, and timestamp in `status.json`. Only the app playback attempt can set `playbackVerified` to true.
