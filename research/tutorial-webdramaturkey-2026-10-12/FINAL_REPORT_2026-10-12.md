# CSBuilder video research — consolidated findings (2026-10-12)

## Source and transcription scope

- User-provided 01:03:43.605 H.264 720p screen-recording (audio stream present but decoded PCM is silent).
- Pixel-change metrics computed for **all 114,594 video frames**; **not** identical to a semantic/human transcription of all frames.
- Turkish instruction captions rendered into the video were separately inspected, with roughly 2 FPS in the first 10 minutes, largely 1 FPS thereafter and selected closer inspections.
- **135 distinct caption statements** across 13 interval files (00:00–63:43) are recorded under [transcripts/](transcripts/INDEX.md). They are visually selected samples with approximate timestamps; **NOT guaranteed complete word-for-word text for all frames**.
- Original video was not uploaded to GitHub; screenshots and full metrics are maintained in conversation analysis artifacts, not dumped as binaries into this repo.
- Do not publish cookies, session keys, dynamic signed media URLs, advertising click URLs or device identifiers from the screen recording.

## What the video actually teaches

| Time | Observed process | Stable engineering lesson |
|---|---|---|
| 00:00–10:00 | Kotlin provider template, `mainUrl`, real category href, mainPage, CSS card selector, `data-src` lazy poster, search, emulator | Validate navigation, cards, posters and search independently; a successful build is not a working provider |
| 10:00–15:00 | Film metadata and description extraction; source lacks some ratings and runtimes | Optional fields must not be fabricated |
| 15:00–30:00 | Two-season series, `episodes a[href]`, `newEpisode`, film vs series response; empty episode pages and coming-soon anime | Preserve stable episode-specific data; distinguish missing published content from selector failure |
| 30:00–38:00 | Fix title selector (narrower `h1`), handle alternate descriptions, reintroduce recommendations | Do not assume every detail page uses one heading/description template |
| 38:00–45:00 | Static page source lacks media; click Play; inspect DevTools Network, reject ad-looking requests | Dynamic player sources may appear after a user action; ad/network traffic is not proof of stream |
| 45:00–55:00 | Map source-button IDs to requests; missing first ID; construct request with Referer, form fields | Capture full source chooser contract, isolate first-item indexing errors and enforce safe headers |
| 55:00–60:00 | Decode AJAX HTML response; extract iframe src; resolve through host extractor; emulator tests | Never output HTML/iframe as playable media; test subsequent host/manifest/segment |
| 60:00–63:43 | Metadata in build.gradle, tvTypes, version/status, authors, favicon and commit/push | Distinguish metadata/packaging from player success and validate against plugin schema |

## Reported outcome vs independently verified facts

At approx. **59:53**, the tutorial author states “evet video oynuyor her şey mükemmel”. That is an observation of the recording and can be documented as *author-reported playback in historical demonstration*. The user's CURRENT site, current network, video links, and actual present-day CloudStream playback were not tested in this research. Do not set `playbackVerified=true` based on that statement alone.

## CSBuilder updates prepared on the research branch

- `cloudstream-builder/references/browser-devtools-to-provider.md`: browser Inspector / Network, AJAX, source ID, iframe, extractor and playback verification sequence.
- `cloudstream-builder/references/movie-series.md`: evidence-backed metadata fields and two-season episode testing, absent/not-yet-released episode distinctions.
- `cloudstream-builder/references/verification-and-release.md`: recorded demonstration != current playback verification.
- `cloudstream-builder/SKILL.md`: discoverability for DevTools-to-provider guide.
- HLS documentation reconciled with **mandatory single master M3U8 per server/language** and **Parçalar/Tracks menu** for qualities. Never generate separate 1080p/720p/480p Sources from a master and never mislabel MP4.

## Pending after transcript

1. Validate against existing Gradle/CloudStream plugin API signatures and write test fixtures for alternate selectors, zero episodes and first source ID.
2. Verify source requests on **currently authorized and reachable** sites; no universal endpoint must be inferred from this tutorial.
3. If desired, extend caption inspection to true frame-accurate word-for-word extraction for **every caption transition**; sampled captions do not meet that higher bar.
4. Have user review the research branch diff before merging into `main`. No new live provider release has been produced from this video.

**Status:** time-ranged **sampled transcription finished**, skill research draft completed, full word-for-word all-frame verification **not completed**.


## Görsel kaynak kodu denetimi tamamlandı (ek çalışma)

Ekrandaki yazıların örneklemeli dökümünden **ayrı olarak** IDE, tarayıcı HTML'i, DevTools, Logcat, emülatör, Gradle ve Git ekranları 7 teknik bölüme ayrılarak incelendi: [00–10](code-audit/00-10-screen-and-code.md), [10–20](code-audit/10-20-screen-and-code.md), [20–30](code-audit/20-30-screen-and-code.md), [30–40](code-audit/30-40-screen-and-code.md), [40–50](code-audit/40-50-screen-and-code.md), [50–60](code-audit/50-60-screen-and-code.md), [60–63:43](code-audit/60-63-screen-and-code.md). HTML selector/class, film/dizi metadata, iki sezon, kaynak kimlikleri, AJAX, çift iframe, Gradle ve Git push adımlarında somut hatalar/süreçler belgelendi. **Son karede `Pushed 1 commit to origin/master` görüldü**; canlı `.cs3` yayınlama veya güncel oynatma doğrulanmadı. Sentetik HTML/Python testleri video vaka çalışmasına aittir, canlı Kotlin build'e değil.

### Güvenli main entegrasyonu

[MAIN_RECONCILIATION.md](MAIN_RECONCILIATION.md) belgesini izle: araştırma dalı ve main ayrışmıştır; ana HLS master/Parçalar, mevcut release bütünlüğü ve depo kurallarını koruyarak yeni main-tabanlı dala yalnız eklemeli değişiklikler alınmalı. **Main bu aşamada değiştirilmedi.**
