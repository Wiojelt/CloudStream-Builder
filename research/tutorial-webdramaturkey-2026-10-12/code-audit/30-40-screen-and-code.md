# Video görüntüsü / gerçek Kotlin / HTML incelemesi — 30:00–40:00

**Kanıt seviyesi:** Kullanıcının 63:43 süren 1280×720 ekran videosundan 30:00–40:00 arasında **120 tam kare (5 sn arayla), 10 temas sayfası** ve kritik kare yakınlaştırmaları incelendi. Bu çalışma yalnız ekran altyazısı değil; IDE'deki *kod değişikliklerini*, Firefox Inspector/sayfa kaynağını ve Android emülatörünü karşılaştırır. Orijinal `.kt` dosyasının tam hâli elimizde olmadığı için ara durumların çalışır/derlenir olduğu varsayılmaz.

## Zamanlı gerçek ekran gözlemleri

| Zaman | Film/HTML/IDE'de görünen | Öğrenilen |
|---|---|---|
| 30:00–31:40 | Kotlin `load` yanıtları, animeler/diziler/film kartları emülatörde sınanıyor; farklı detay ve bölüm ekranları görülüyor | Katalog + detay + bölüm görünmesi playback kanıtı değil |
| 31:45–32:35 | Bir film sayfasının DOM'u Inspector ile karşılaştırılıyor, `div.pl-md-4 h1` başlık seçicisi kontrol ediliyor | Aynı sağlayıcıda film/dizi HTML şablonları farklı olabilir |
| 33:15 | Film başlığı daha geniş `h1` ile alınmış; IDE'de **ardışık iki `val description`** tanımı görünür | Kod hâlâ **ara düzenleme** durumunda, nihai kaynak değil |
| 34:05 | İkinci açıklama `movDescription` oluyor, ayrıca `movYear` alanı ekleniyor | Film için farklı `video-attr`, dizi/anime için başka DOM alanları |
| 34:15 | Film `this.plot=movDescription`, `this.year=movYear`; anime `this.plot=description`, `this.year=year` | Alanları uygun `LoadResponse` dalına bağla |
| 35:00 | `tags=div.categories a`, `movTags=div.category a` aynı fonksiyonda görülüyor | Genre seçicileri de şablona göre değişiyor |
| 35:30–36:30 | Şablondan önerilerin geri alınması ve emülatör katalog/detail kontrolleri | Geniş `div.col` tüm kartları öneri sanabilir |
| 37:00–38:20 | Play alanı/sayfa kodu inceleniyor. `view-source` içinde **boş `<div id="movie-video"></div>`** ve JS scriptleri görünür | Bu, oynatılabilir iframe/medya manifesti değildir |
| 38:45–39:55 | `embed`, `iframe`, `src` için kaynak HTML aranıyor; hazır video URL bulunamadığı belirtiliyor | Sonraki adım Play sonrası DevTools Network/XHR zincirini doğrulamak |

## Ekranda görülen seçilmiş Kotlin kodu (tam kaynak veya başarılı çalışan sürüm değildir)

```kotlin
// Düzeltme öncesi, 32:35
val title = document.selectFirst("div.pl-md-4 h1")?.text()?.trim() ?: return null
// Düzeltme sonrası, 33:15
val title = document.selectFirst("h1")?.text()?.trim() ?: return null

// 34:05–35:00 film/dizi metadata ayrımı
val description = document.selectFirst("div.text-content")?.text()?.trim()
val movDescription = document.selectFirst("div.video-attr:nth-child(4) > div:nth-child(2)")?.text()?.trim()
val year = document.selectFirst("div.featured-attr:nth-child(1) > div:nth-child(2)")?.text()?.trim()
val movYear = document.selectFirst("div.video-attr:nth-child(3) > div:nth-child(2)")?.text()?.trim()
val tags = document.select("div.categories a").map { it.text() }
val movTags = document.select("div.category a").map { it.text() }
```

```kotlin
// Videodaki film response içinden görülen kısmi alan atamaları
newMovieLoadResponse(title, url, TvType.Movie, url) {
    this.plot = movDescription
    this.year = movYear
}
// Anime yanıtında this.plot=description, this.year=year görülüyor
```

**Ara hata kanıtı:** 33:15'te iki `val description` kod satırı var; daha sonra değişkenler ayrılıyor. Eğitimin tamamlanmamış kodu doğrudan şablona kopyalanmamalı. Video içindeki `comingSoonIfNone=true` evrensel kural değildir.

## CSBuilder için doğru mühendislik sonucu (videonun aynen kodu değil)

1. **Şablon seçici testi:** Film/dizi/anime için ayrı pozitif DOM fixtürleri; `div.pl-md-4 h1` filmde başarısız, `h1` örnekte çalışır. Genel `h1` gerçek sayfada özgül detay konteyneriyle sınırlandırılmalı.
2. **Metadata mapping:** Birden fazla film şablonu olabileceğinden `description`/`movDescription`, `year`/`movYear` gibi alanlar yalnız kanıtlanan eşleşmelerle film veya dizi yanıtına bağlanmalı; sahte rating/oyuncu türetilmemeli.
3. **Kırılgan nth-child:** Videodaki `div.video-attr:nth-child(4)` DOM sıra değişiminde bozulabilir. Sitedeki gerçek label/DOM ilişkisiyle doğrulama ve regression fixture tercih edilmeli.
4. **Öneri yalıtımı:** `div.col` gibi genel selector'lar yerine gerçek öneri bölümündeki doğrulanmış kartlar kullanılsın.
5. **Video shell != stream:** `<div id="movie-video"></div>` ve dış scriptler medya kanıtı değildir. Ağ eylemi; `Play → Network/XHR → response → iframe/host extractor → gerçek manifest/segment → cihaz playback` şeklinde ayrı kanıtlanmalı. Reklam/telemetri scriptleri medya değildir.

## Yeniden üretilebilir test verisi

`fixtures/movie_detail_30_40.html`, `fixtures/series_detail_30_40.html` ve `fixtures/test_detail_30_40.py` araştırma için **sentetik** veri/fixture'dir; videodan birebir HTML kopyası değildir. Orijinal kod çalıştırılmadı. Yerel karşılığında **15/15 offline BeautifulSoup testi geçti**: başlık seçici farkı, iki metadata DOM'u, poster/tür ve boş player'ın oynatma kanıtı olmaması. 120 tam ekran kare ve seçilmiş yakın planlar sohbet ZIP paketinde; repo içine dev video veya token/cookie eklenmedi.

**Doğrulama sınırı:** 40. dakikaya kadar medya oynatımı kanıtı yok; `loadLinks`in AJAX/iframe çalışma örneği sonraki 40:00–50:00 bölümündedir. `main` değiştirilmedi; araştırma dalı. **HLS invariant:** aynı sunucu/ses için tek gerçek master M3U8, kalite yalnız oynatıcı **Parçalar/Tracks**.
