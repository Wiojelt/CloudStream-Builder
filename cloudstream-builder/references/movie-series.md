# Movie and series providers

## Catalog contract

Discover navigation categories and home-page sections separately. Include a section only when its cards have a stable title, detail URL, and poster or an intentional fallback. A category name without cards must not be presented as a working row.

For series and anime providers, always provide dedicated "Son Eklenen Bölümler" (Latest Episodes) and "Son Eklenen Filmler" (Latest Movies) sections on the main page (`mainPage`) whenever the source website exposes newly published releases. This guarantees direct discovery of recent episode broadcasts without requiring manual searches.

Use the site's visible category names. Prefer canonical category/archive URLs over inventing query paths. Test page 1 and page 2 before adding pagination.

Clean card and detail titles from the most specific title node. Remove only demonstrated site suffixes such as `izle`, `film izle`, language labels, and the year already stored separately. Do not apply a universal word blacklist that can damage real titles.

## Detail contract

For a film, collect title, poster, plot, year, tags, actors, rating, recommendations, and trailer **only when the site actually exposes them**. Do not invent ratings, runtimes, cast, or recommendations to fill empty optional fields. Check HTML source, the live DOM, and representative detail pages before concluding that a field is absent. For a series, additionally collect season and episode numbers and preserve the episode-specific playback payload.

**Episode selector audit (video case study):** Inspect a representative two-season series, locate the actual episode grouping and its `a[href]` nodes, verify both season containers, and preserve canonical episode URLs. Extract episode/season numbers from observed patterns such as `1. Bölüm`; do not assume that `substringBefore(" ")` works for all whitespace, punctuation, or localized numbering. When episode labels lack a title, display a truthful season/episode label instead of inventing an episode title. Verify empty seasons and multiple templates independently. See [DevTools-to-provider tutorial](browser-devtools-to-provider.md).

Classify media from concrete evidence in this order:

1. Episode/season controls or episode URLs.
2. Structured metadata such as `VideoObject`, `Movie`, or `TVSeries`.
3. Stable URL/category markers observed on the site.

Do not infer every card under a `Dizi` category is a film or vice versa. Inspect one representative of each advertised shape.

## Proven patterns worth checking

- Server buttons may store `source_index`, `player_type`, content ID, season, or episode in data attributes. Keep these values in the `data` payload passed to `loadLinks`.
- A detail page may contain only a shell; player HTML can arrive through a same-origin POST. Reproduce the method, fields, headers, and referer exactly.
- Player URLs may be written into inline scripts or lazy attributes such as `data-src`, `data-vsrc`, and `data-video_url`.
- In REST/GraphQL API backends (e.g. DiziAsya), fetch chapter and episode details directly by chapter UUID/ID (`$apiUrl/chapters/$id`) rather than scraping multi-nested index arrays.
- In ongoing series, filter out future unreleased drafts (`publishDate > currentTimeMillis`) that appear in episode schedules but yield 404 or empty stream links.
- When sources are independent, resolve them concurrently with a small bounded set so one slow server does not block all results. Preserve deterministic labels and isolate failures per source.
- Search results can use a different card layout than home pages. Give search its own verified selectors.

Known local references are implementation examples, not templates to copy blindly:

- `C:/Users/root/Documents/Codex/2026-09-01/c/work/TurkStreamTest/providers/Jetfilmizle`
- `C:/Users/root/Documents/Codex/2026-09-01/c/work/TurkStreamTest/providers/HDFilmizleBest`
- `C:/Users/root/Documents/Codex/2026-09-01/c/work/TurkStreamTest/providers/NetFilmizle`
- `C:/Users/root/Documents/Codex/2026-09-01/c/work/TurkStreamTest/providers/Sinemakolik`

Use a reference only after comparing the current detail page, source buttons, and player network shape.
