# Görsel KOD ve HTML analizi — 00:00–10:20

## Yöntem / kapsam
Video 01:03:43, 1280×720. **İlk 10 dk boyunca 5 saniyede bir toplam 120 tam ekran kare**, 09:54–10:26 arasında ayrıca her saniye 32 kare incelendi. Alt yazı değil **IDE dosyası, HTML kaynak kodu, CSS selector, terminal ve emülatör ekranı** esas alındı. Bu, her karenin manuel transkripsiyonu değildir. Yerel teknik pakette ekran görüntüleri ve örnek fixture/test mevcuttur; kaynak sitenin bugün çalıştığı doğrulanmadı.

## Kare/kod karşılaştırması

| Zaman | Ekranda görülen işlem / kod | Doğruluk ve ders |
|---|---|---|
| 00:20–01:00 | Terminalde `cp -r __Temel WebDramaTurkey`, IntelliJ **Rename/Refactor** ile `Temel` ve `TemelPlugin` değiştirme | Sınıf + referans + plugin kaydı/Gradle metadata birlikte güncellenmeli |
| 01:08–01:30 | `class WebDramaTurkey : MainAPI()`, `mainUrl`, `name`, `lang="tr"`, `hasMainPage=true`, `supportedTypes` ve `mainPageOf` | İlk görünen satırlarda şablon kalıntıları da var; bunlar nihai kod sayılmaz |
| 01:50–03:15 | Tarayıcı kaynak HTML'den `/tur/...` linklerini `anizm.html` geçici dosyasında toplu düzenleme | `"\${mainUrl}/tur/aksiyon" to "Aksiyon"` gibi kategori çiftleri, `request.data` URL / `request.name` başlık |
| 04:15–04:35 | Kategori sayfasında `?page=` gözlemi → `app.get("\${request.data}?page=$page")` | İki sayfada test et; mevcut query parametresi varsa `&` kullanılmalı |
| 04:35–05:05 | İlk şablon `div.items article` seçicisi, gerçek site için `div.col` ile değiştirilir | Eski `MainAPI` şablon kodu başka siteye kopyalanamaz |
| 05:05–06:10 | Gerçek HTML: `div.col > div.list-movie`; başlık `a.list-title`; poster `div.media.media-cover[data-src]` | Poster normal `img[src]` içinde **değil**, kapak `data-src` niteliği ile taşınıyor |
| 06:50–07:45 | `title`, `href`, `posterUrl`, `tvType` alanlarından `newMovieSearchResponse` | Film için `href.contains("/film/")` yapılıyor; diğer her şeyi `TvType.AsianDrama` kabul etmek genel kural olamaz |
| 08:10–09:00 | Arama URL'si `/arama/`; `search(query)` ve `div.col` seçicisi | Query encode edilmeli ve arama HTML'i ayrıca test edilmeli |
| 09:10–09:55 | `:WebDramaTurkey:deployWithAdb`, `BUILD SUCCESSFUL`; emülatörde başlıklar var, posterler eksik | Derleme/ADB dağıtımı işlevsel kataloğun doğrulanması değildir |
| 09:58–10:06 | **Gerçek hata:** `div.media media-cover` → `div.media.media-cover` | Boşluk torun etiketi demektir; iki class aynı elementteyse arka arkaya `.` gerekir |
| 10:10–10:20 | Loglar ve emülatör kontrolü; video yazısı “loglarımıza göre düzeldi” | Eğitmenin yerel test sonucu, güncel site/cihaz doğrulaması değildir |

## Gerçek HTML'ye dayalı anonymize fixture

```html
<div class="col"><div class="list-movie">
  <a class="list-media" href="/diziler/ornek-dizi">
    <div class="media media-cover" data-src="https://example.test/cover/ornek.jpg"></div>
  </a>
  <div class="list-caption">
    <a class="list-title" href="/diziler/ornek-dizi">Örnek Dizi</a>
  </div>
</div></div>
```

Eğitim sitesindeki somut görünen örnek: **Love Beyond the Curse**, `/dizi/love-beyond-the-curse`, `/public/upload/cover/love-beyond-the-curse.jpg`. Bunun gelecekte de aynı şekilde bulunacağı iddia edilmez.

## Görünen Kotlin yapı taşları (nihai kaynak kopyası değil)

```kotlin
// Video: getMainPage içindeki fikir
val document = app.get("${request.data}?page=$page").document
val home = document.select("div.col").mapNotNull { it.toMainPageResult() }

// Video: kart parselleme
val title = this.selectFirst("a.list-title")?.text() ?: return null
val href = fixUrlNull(this.selectFirst("a")?.attr("href")) ?: return null
val posterUrl = fixUrlNull(this.selectFirst("div.media.media-cover")?.attr("data-src"))

// Video: arama
val document = app.get("${mainUrl}/arama/${query}").document
return document.select("div.col").mapNotNull { it.toSearchResult() }
```

## Reproducible CSS test

Local `fixtures/test_css_contract.py` and anonymized `fixtures/lazy_poster_card.html` pass **6 assertions** using BeautifulSoup: the bad `div.media media-cover` selector finds no element; `div.media.media-cover` successfully returns the `data-src` poster.

## Skill'e alınması gereken özgün dersler

1. **Template-diff audit** — önce şablon seçicilerinin kaynak DOM ile gerçekten eşleştiğini kanıtla; hatalı çalışan örneği kopyalama.
2. **Selector evidence** — her CSS selector için gerçek HTML örneği ve en az bir pozitif test bulundur. `data-src`, `src`, `data-original` gibi lazy alanları öğe türüne göre kontrol et.
3. **CSS class semantics** — `class="media media-cover"` → `div.media.media-cover` (aynı element), `div.media media-cover` (alt etiket) değildir.
4. **Result auditing** — Gradle build başarılı, liste başlıkları var ama posterler eksikse sağlayıcı hazır sayılmayacak.
5. **Template type & query caveats** — URL'den tüm film dışı içerikleri tek `TvType` altında toplama; `search(query)` URL encoding ve bağımsız selector testi gerektirir.
6. **HLS değişmez kural** — tek gerçek master M3U8 / sunucu-ses; çözünürlükler Parçalar/Tracks içinde, ayrı Sources bağlantıları değil.

**Kısıt:** Kodun tamamı video karelerinden kurtarılamaz; burada yalnız okunabilen yöntem/satırlar ve açıkça adlandırılmış örnekler var. `load`, `loadLinks`, AJAX ve extractor ekranları sonraki bölümlerin konusudur.
