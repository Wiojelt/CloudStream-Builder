# Proven repository patterns

These patterns were extracted from the current TurkSinema and TurkSpor source trees. They are decision aids, not proof that every provider in either repository is currently reachable. Recheck the target source and run the repository's build/tests before reuse.

## Choose an architecture

| Need | Proven pattern | Representative implementation |
|---|---|---|
| One website, one provider | Self-contained `MainAPI` plus focused extractors | TurkSinema: HDFilmizleBest, NetFilmizle, Sinemakolik |
| Site-specific source chooser/AJAX | Store player identifiers in load data and reproduce the POST in `loadLinks` | TurkSinema: JetFilmizle |
| Authorized application API | Typed response models, configuration bootstrap, runtime resolution | TurkSinema: ClipBox, InatBox, CNCVerse |
| Many upstream providers in one package | Delegate plugins from one aggregate entry and forward lifecycle | TurkSinema aggregate plugin |
| One upstream plugin registers several providers, but one `.cs3` is required | Snapshot `APIHolder.allProviders`, load delegate, retain the selected provider, attach common UI | TurkSinema generated entry wrappers |
| Several sites share channel/player behavior | `SourceSpec` plus shared catalogue, domain, playback, branding, and settings components | TurkSpor shared modules |
| Large remote channel catalogue | Remote JSON with schema validation, short cache, stable IDs, and a minimal bundled fallback | TurkSpor NetVGold |
| Country-heavy channel directory | Persist a country filter and expose it through provider settings | TurkSpor DaddyLive and NTVStream |
| Provider supplies several mirrors | Resolve mirrors independently, discard failed manifests, label and emit every working source | TurkSpor NetVGold and shared `SportsProvider` |

## TurkSinema methods

### Detail-first web provider

The useful web-provider shape separates four concerns:

1. Home/search selectors return canonical detail URLs and clean titles.
2. `load` classifies film versus series from real episode evidence and stores episode-specific playback data.
3. Trailer discovery calls `addTrailer` only.
4. `loadLinks` handles direct media, supported hosts, custom extractors, and site-specific AJAX without returning HTML pages as video.

HDFilmizleBest, NetFilmizle, and Sinemakolik demonstrate broad iframe/data-attribute discovery plus direct HLS/DASH/video handling. JetFilmizle demonstrates a stronger source-button contract: retain content ID, source index, player type, season, and episode; send the observed POST with its required Origin/Referer/User-Agent; then dispatch the returned iframe to the correct extractor. Use this only when the target request shape matches.

### Custom extractor boundary

Create an `ExtractorApi` when a host has a reusable player protocol independent of one catalogue site. Keep catalogue parsing in `MainAPI` and player parsing in the extractor. TurkSinema examples include host-specific JSON, packed scripts, track/subtitle extraction, and a second request that exchanges a page ID for media.

Do not create a generic extractor from one coincidental regex. Confirm at least two player examples or keep the logic private to the provider until the contract is stable.

### API/application provider

ClipBox, InatBox, and CNCVerse show that application sources are not HTML providers. Preserve typed models and the actual configuration/content request sequence. Separate reusable crypto/config parsing from catalogue presentation. Resolve short-lived links at playback time. Never store a user's account token, device identifier, or captured personal cookie in source.

### Aggregate and individual packages

The TurkSinema aggregate forwards plugin filename, `load`, and reverse-order `beforeUnload` to delegates. Individual modules use a wrapper entry so an upstream plugin can be isolated and common domain/support UI attached.

Use an aggregate only when the user wants one installation containing many providers. Use individual packages for independent enable/disable and updates. Do not pretend duplicated catalogue metadata creates real independent `.cs3` files; each package must have one active `@CloudstreamPlugin` entry and its own build output.

### Domain update UI

Persist only a normalized HTTPS origin. Candidate order can include a signed/maintained manifest, last-known-good origin, provider-advertised canonical/redirect target, and current source URL. A response code alone is insufficient: validate provider-specific title, catalogue, or API markers before replacing the last-known-good value. A manual domain must be validated and rolled back on failure.

## TurkSpor methods

### Spec-driven rotating domains

`SourceSpec`, `Channels`, and `DomainResolver` separate host-family rules from parsing. The resolver uses a mutex and time-based cache, limits candidate attempts, validates HTTPS and allowed host patterns, follows provider-owned announcements, and updates `lastGood` only when semantic markers and a non-empty channel list pass.

Numeric domain increments are a last candidate source and apply only to families proven to use that convention. Never increment arbitrary domains.

### Stable catalogue, late playback resolution

Search and home cards use a stable synthetic URL containing the channel ID. `load` re-resolves that ID against the current catalogue. `loadLinks` resolves current player/media URLs only when playback begins. This prevents expiring stream URLs from becoming permanent card data.

Keep channels grouped by meaningful categories and deduplicate by stable ID while merging their player mirrors. A grouped provider such as AslanTV is a product choice; do not generalize it when the user asks for separate channels or packages.

### Player strategy families

The shared sports provider demonstrates explicit player modes rather than one giant fallback regex:

- WordPress-style channel page → player data attribute → embed → session/API exchange.
- Royal-style page → advertised domain endpoint → JSON base URL plus channel ID.
- Direct/inter-style catalogue → already validated HTTPS stream.
- Next.js-style page → parse serialized application state → resolve embed or stream endpoint.

Add a mode only after observing its full request chain. Bound page size, identifier length, host/scheme, number of candidates, and decode work. Preserve coroutine cancellation while isolating ordinary mirror failures.

### HLS quality and audio

Fetch a candidate playlist before labeling it successful. If it is a master playlist, resolve relative variants, parse resolution/bandwidth, and emit quality-sorted links. Keep the master URL when separate `EXT-X-MEDIA` audio renditions could be lost by selecting only a video variant.

### Multi-source and fallback catalogues

NetVGold demonstrates independent source probing with `supervisorScope`, bounded timeouts, per-source labels, and manifest validation. Remote catalogues should have a small validated schema and stable IDs. A bundled fallback is for catalogue availability, not permission to hard-code stale or unrelated streams; keep it minimal and revalidate it.

### Settings, filters, and artwork

Provider settings can display last check status, force refresh, accept a validated manual domain, and persist country choices. Do not expose internal endpoint lists unnecessarily. Status text must distinguish changed, unchanged, and failed.

For channel-heavy sources, use original logos when reliable. TurkSpor's artwork layer downloads with strict timeouts, limits concurrency, caches rendered cards, uses an atomic temporary file, and falls back to readable text. Never block the main thread while preparing art.

Remote channel rules can hide or remap known bad entries without rebuilding, but must be size-limited, cached, schema-checked, and fail closed to the last usable state.

## Known repository-specific behavior not to turn into a universal rule

- Daily support notices, author contact labels, WARP buttons, and aggregate-vs-individual packaging are product choices, not requirements for every plugin.
- Obfuscated or encrypted bootstrap data is not automatically safer and must not contain credentials. Use it only when the authorized source requires non-public endpoint presentation.
- `HTTP 200`, a successful Gradle build, or a parsed channel count does not prove CloudStream playback.
- Existing duplicated filters, broad catch blocks, stale fallback URLs, or response-code-only domain checks are implementation debt, not patterns to copy.

## Local reference roots

When available in the owner's workspace, inspect current code rather than relying on this summary:

- TurkSinema: `C:/Users/root/Documents/Codex/2026-09-01/c/outputs/TurkSinema`
- TurkSpor: `C:/Users/root/Documents/Codex/2026-08-31/i/outputs/TurkSpor`

Run the scanner before a broad repository comparison:

```powershell
python C:/Users/root/.codex/skills/cloudstream-builder/scripts/scan_provider_patterns.py `
  C:/Users/root/Documents/Codex/2026-09-01/c/outputs/TurkSinema `
  C:/Users/root/Documents/Codex/2026-08-31/i/outputs/TurkSpor
```
