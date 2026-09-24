# 🧩 CloudStream Builder Unified Extractor Library

Bu kütüphane, CloudStream eklentisi (plugin/provider) geliştirirken video oynatıcıları, gömülü iframe'leri ve video hostlarını otomatik veya doğrudan çözmek için hazır Kotlin ve JSON extractor'ları içerir.

---

## 📁 Dizin Yapısı

- **`oce/kotlin/`** — OCE (`byimam2nd/oce`) deposundan derlenen 50 adet bağımsız Kotlin Extractor sınıfı.
- **`oce/configs/`** — 43 adet bildirimsel JSON tabanlı extractor kuralı (`AbyssPlayer`, `BloggerVideo`, `Dailymotion`, `Rumble`, `Voe`, `Krakenfiles`, vb.).
- **`oce/core/`** — `ConfigDrivenExtractor`, `ExtractorConfigParser`, `ExtractorRegistry` ve `ExtractorFallback` motorları.
- **`oce/docs/`** — Detaylı extractor geliştirme ve regex mimarisi rehberi (`OCE_EXTRACTION_GUIDE.md`).
- **`turk/`** — TurkSinema, TurkSpor ve Wio platformuna ait 36 adet özel yerli/yabancı host extractor'ı.

---

## ⚡ 1. Yerli ve Popüler Hostlar (`extractors/turk/`)

| Extractor | İlgili Hostlar / Domainler | Açıklama |
|---|---|---|
| `CloseLoadExtractor.kt` / `HCCloseLoadExtractor.kt` | `closeload.com`, `closeload.fat`, `closeload.top` | FilmMakinesi & HDFilmcehennemi ana HLS oynatıcısı |
| `HCRapidrameExtractor.kt` / `RapidVidExtractor.kt` | `rapidvid.net`, `rapidrame.com` | Rapidrame şifreli video akışları |
| `VidRameExtractor.kt` | `vidrame.org`, `vidrame.pro` | HDFilmizle ana player'ı |
| `FirePlayerExtractor.kt` | `fireplayer.net`, `fireplayer.org` | NetFilmizle HLS/MP4 çözücüsü |
| `VidmixiExtractor.kt` | `vidmixi.org`, `vidmixi.net` | Sinemakolik ve dizi platformları |
| `SetPlayExtractor.kt` / `FastPlayExtractor.kt` | `setplay.org`, `fastplay.to` | SetFilmizle özel player'ları |
| `DiskYandexComTrExtractor.kt` | `disk.yandex.com.tr`, `yadi.sk` | Yandex Disk video oynatıcı API'si |
| `DzenExtractor.kt` | `dzen.ru` | Yandex Dzen video akışları |
| `VkExtractor.kt` | `vk.com`, `vkvideo.ru` | VKontakte video çözücü |
| `SibNetExtractor.kt` | `video.sibnet.ru` | Sibnet video akış çözücüsü |
| `PixelDrainExtractor.kt` | `pixeldrain.com` | Pixeldrain dosya/video indirme/akış |
| `HDMomPlayerExtractor.kt` | `dizimom`, `hdplayer` | DiziMom HLS çözücü |
| `PlayerKoreaExtractor.kt` / `VideoSeyredExtractor.kt` | Kore dizileri ve yerli player'lar | Gömülü iframe akışları |
| `CizgiDuoExtractor.kt` / `CizgiPassExtractor.kt` | ÇizgiMax & animasyon player'ları | Yerli çizgi dizi hostları |

---

## 🌐 2. Uluslararası ve Global Hostlar (`extractors/oce/kotlin/` & `configs/`)

| Extractor | Desteklenen Platformlar |
|---|---|
| `DailymotionExtractor.kt` | `dailymotion.com`, `dai.ly` |
| `RumbleExtractor.kt` | `rumble.com` |
| `KrakenfilesExtractor.kt` | `krakenfiles.com` |
| `VoeExtractor.kt` | `voe.sx`, `voe-network.net` |
| `LuluStreamExtractor.kt` | `luluvdo.com`, `lulustream.com` |
| `OdnoklassnikiExtractor.kt` | `ok.ru`, `odnoklassniki.ru` |
| `BloggerVideoExtractor.kt` | `blogger.com/video.g` |
| `WishfastExtractor.kt` | `wishfast.top`, `fastwish.com` |
| `StreamRubyExtractor.kt` | `streamruby.com`, `rubystream.net` |
| `StreamHGExtractor.kt` | `streamhg.com` |
| `VideoplayerVipExtractor.kt` | `videoplayer.vip` |
| `VidguardtoExtractor.kt` | `vidguard.to`, `vgfplay.com` |
| `GdplayerExtractor.kt` | `gdplayer.tv`, Google Drive proxy'leri |
| `AbyssPlayerExtractor.kt` | `abysscss.com` |
| `DhcplayExtractor.kt` | `dhcplay.com` |

---

## 🛠️ 3. Yeni Bir Eklentiye Extractor Ekleme (Nasıl Kullanılır?)

### Yöntem A: Doğrudan Kotlin Dosyasını Eklenti Modülüne Dahil Etme
1. `extractors/turk/` veya `extractors/oce/kotlin/` altındaki ilgili extractor `.kt` dosyasını eklentinizin `src/main/kotlin/...` dizinine kopyalayın.
2. Provider'ınızın `loadLinks` metodunda `loadExtractor` çağrısı yapın:
```kotlin
loadExtractor(
    url = playerUrl,
    referer = mainUrl,
    subtitleCallback = subtitleCallback,
    callback = callback
)
```

### Yöntem B: JSON Konfigürasyon Tabanlı Oynatıcı Kullanma
1. `extractors/oce/core/ConfigDrivenExtractor.kt` motorunu dahil edin.
2. `extractors/oce/configs/<HostName>.json` konfigürasyonunu yükleyip dinamik olarak çalıştırın:
```kotlin
val extractor = ConfigDrivenExtractor(config)
extractor.getUrl(url, referer, subtitleCallback, callback)
```
