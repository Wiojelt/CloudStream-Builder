# Playback, trailers, and subtitles

## Extraction ladder

Resolve each source using the narrowest observed mechanism:

1. Emit direct `.m3u8`, `.mpd`, or `.mp4` media with the correct `ExtractorLinkType`, referer, headers, and quality.
2. Use `loadExtractor` for a supported host iframe.
3. Add a focused extractor for an unsupported player host.
4. Reproduce the site's AJAX/API request when the player is generated dynamically.

Do not emit an iframe page, HTML endpoint, expired token, empty URL, or trailer as a video link. These commonly surface as CloudStream error 2004 or “bağlantı bulunamadı”. A 200 HTML response is not playable-media evidence.

## Headers and session state

Preserve required `Referer`, `Origin`, user agent, and session cookies across the exact request chain. Do not hard-code personal cookies or device tokens. If access requires a user session, keep it on-device and document the prerequisite.

Resolve relative URLs against the response URL or an effective `<base>` tag, not blindly against the original home page.

## Multiple sources

Keep all observed server choices and language variants. Label results with the site's source name and quality. Catch a failure per source so one dead mirror does not suppress working mirrors. Use bounded concurrency only for independent requests; preserve order where a token or cookie is produced sequentially.

## Trailers

Put YouTube or other trailer URLs in `addTrailer`. Exclude them from player candidates and from `loadLinks`. A trailer iframe proves only trailer availability.

## Subtitles

Inspect player JSON, track tags, manifests, and player API responses. Emit every observed subtitle with a human-readable language/label and an absolute URL. Resolve escaped JSON URLs before callback. Do not report subtitle support merely because a player UI has a subtitle button.

## Playback evidence

For HTTP smoke checks, record final URL, status, content type, and whether the body is a manifest or media response. For CloudStream verification, record provider, item, selected source, outcome, and timestamp in `status.json`. Only the app playback attempt can set `playbackVerified` to true.
