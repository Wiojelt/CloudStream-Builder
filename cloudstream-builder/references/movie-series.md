# Movie and series providers

## Catalog contract

Discover navigation categories and home-page sections separately. Include a section only when its cards have a stable title, detail URL, and poster or an intentional fallback. A category name without cards must not be presented as a working row.

Use the site's visible category names. Prefer canonical category/archive URLs over inventing query paths. Test page 1 and page 2 before adding pagination.

Clean card and detail titles from the most specific title node. Remove only demonstrated site suffixes such as `izle`, `film izle`, language labels, and the year already stored separately. Do not apply a universal word blacklist that can damage real titles.

## Detail contract

For a film, collect title, poster, plot, year, tags, actors, rating, recommendations, and trailer when available. For a series, additionally collect season and episode numbers and preserve the episode-specific playback payload.

Classify media from concrete evidence in this order:

1. Episode/season controls or episode URLs.
2. Structured metadata such as `VideoObject`, `Movie`, or `TVSeries`.
3. Stable URL/category markers observed on the site.

Do not infer every card under a `Dizi` category is a film or vice versa. Inspect one representative of each advertised shape.

## Proven patterns worth checking

- Server buttons may store `source_index`, `player_type`, content ID, season, or episode in data attributes. Keep these values in the `data` payload passed to `loadLinks`.
- A detail page may contain only a shell; player HTML can arrive through a same-origin POST. Reproduce the method, fields, headers, and referer exactly.
- Player URLs may be written into inline scripts or lazy attributes such as `data-src`, `data-vsrc`, and `data-video_url`.
- When sources are independent, resolve them concurrently with a small bounded set so one slow server does not block all results. Preserve deterministic labels and isolate failures per source.
- Search results can use a different card layout than home pages. Give search its own verified selectors.

Known local references are implementation examples, not templates to copy blindly:

- `C:/Users/root/Documents/Codex/2026-09-01/c/work/TurkStreamTest/providers/Jetfilmizle`
- `C:/Users/root/Documents/Codex/2026-09-01/c/work/TurkStreamTest/providers/HDFilmizleBest`
- `C:/Users/root/Documents/Codex/2026-09-01/c/work/TurkStreamTest/providers/NetFilmizle`
- `C:/Users/root/Documents/Codex/2026-09-01/c/work/TurkStreamTest/providers/Sinemakolik`

Use a reference only after comparing the current detail page, source buttons, and player network shape.
