# Ekran, Kotlin, HTML ve DevTools analizi — 10:00–20:00

Kaynak: kullanıcının 01:03:43 süren 1280×720 video kaydı. Bu aralık 5 saniyede bir toplam **120 tam kare** ve kritik anlardaki yakın planlarla incelendi. Önceki Türkçe altyazı dökümünün tekrarı değildir; IDE kodunun önceki/sonraki hâlleri ve tarayıcı DOM'u karşılaştırıldı. **Orijinal sağlayıcı projesinin tam kaynak dosyası elimizde yoktur.** Kısmi video kodunu çalışan nihai kaynak olarak kullanmayın.

## 10:00–15:00 — load() ve gerçek metadata seçicileri

| Zaman | Ekran kanıtı | Mühendislik sonucu |
|---|---|---|
| 10:00–10:20 | Önceki poster seçici düzeltmesi; emülatör ve terminaldeki kontrol | Kartın görünmesi detay sayfasını doğrulamaz |
| 10:25–10:55 | \`load(url: String)\`, \`app.get(url).document\`; şablondan \`h1\`, \`div.poster img\`, \`div.wp-content p\`, \`div.sgeneros a\`, \`span.dt_rating_vgs\`, \`span.runtime\`, \`div.srelacionados article\` alanları | Bunlar **başlangıç şablonu**, hedef sitede doğrulanmadan kopyalanmamalı |
| 11:00–12:00 | Just Wanna Be with You film detayında Firefox Inspect, poster ve açıklama DOM'u | Poster için \`div.media.media-cover[data-src]\`; açıklama için \`div.text-content\` araştırılıyor |
| 12:00–13:15 | Başlık ve kategori HTML blokları inceleniyor | Daha sonra \`div.pl-md-4 h1\`, \`div.categories a\`, \`div.extra span.c a\` gibi siteden öğrenilmiş seçiciler deneniyor |
| 13:45–15:00 | Rating/duration kaynak sayfalarda bulunamadığı için kaldırılıyor | Eksik metadata yerine sahte/0 değer konulmamalı |
| 15:00–15:55 | Oyuncu ve öneriler farklı içerik sayfalarında aranıyor | Bir örnekte yok diye evrensel alan silme kararı verilmez |

Görüntüdeki **ilk şablon (10:55)**, seçilmiş satırlar:
\`\`\`kotlin
val title = document.selectFirst("h1")?.text()?.trim() ?: return null
val poster = fixUrlNull(document.selectFirst("div.poster img")?.attr("src"))
val description = document.selectFirst("div.wp-content p")?.text()?.trim()
val tags = document.select("div.sgeneros a").map { it.text() }
val rating = document.selectFirst("span.dt_rating_vgs")?.text()?.trim()?.toRatingInt()
\`\`\`

**17:40'a kadar geliştirilen görünür alternatifler**, tam kaynak değil:
\`\`\`kotlin
val title = document.selectFirst("div.pl-md-4 h1")?.text()?.trim() ?: return null
val poster = fixUrlNull(document.selectFirst("div.media.media-cover")?.attr("data-src"))
val description = document.selectFirst("div.text-content")?.text()?.trim()
val tags = document.select("div.categories a").map { it.text() }
\`\`\`
Aynı karede \`year\` için \`div.featured-attr:nth-child(1) > div:nth-child(2)\`, \`actors\` için \`span.valor a\`, \`trailer\` için embed regex denemesi okunuyor. Bu satırların **tam doğruluğu ve gerçek karşılıkları kanıtlanmış değil**; bazıları hâlâ şablon artığı olabilir. Fragman oynatma kaynağı yerine \`addTrailer\` ile taşınmalı.

## 15:00–20:00 — iki sezon, bölüm HTML'i ve newEpisode

| Zaman | Ekranda gözlenen | CSBuilder uyarısı |
|---|---|---|
| 16:00–16:35 | İki sezonlu örnek aranıyor; Spy × Family seçiliyor | Tek sezonla test etmeyin |
| 16:35–17:00 | Browser Inspector'da \`div.episodes\`, \`id="season-2"\`, \`class="tab-pane"\`, \`a[href]\`, \`div.episode\`, boş \`div.name\` | Aynı numara farklı sezonda tekrar edebilir |
| 17:40–18:35 | \`document.select("div.episodes a").map { bolum -> ... }\`, \`bolum.attr("href")\`, \`bolum.selectFirst("div.episode")?.text()\` | Her bölüm URL'sini koruyun |
| 18:45–19:20 | \`substringBefore(" ")\` ile \`1. Bölüm\` metnini bölme denemesi | \`"1. Bölüm".substringBefore(" ")\` sonucu \`"1."\` olur; Int değildir |
| 19:15–19:55 | \`newEpisode(bHref)\` ve \`this.episode\` ataması; sezon ayrı atanmamış ara geliştirme | Tamamlanmış/derlenmiş çalışan liste gibi sunulamaz |

Anonimleştirilmiş **DOM ilişki örneği** (sitenin birebir HTML dökümü değil):
\`\`\`html
<div class="episodes"><div id="season-2" class="tab-pane">
<a href="/anime/spy-x-family/2-sezon/7-bolum">
  <div class="episode">7. Bölüm</div><div class="name"></div>
</a></div></div>
\`\`\`

Videodaki **KISMİ geliştirme**:
\`\`\`kotlin
val bolumler = document.select("div.episodes a").map { bolum ->
    val bHref = bolum.attr("href")
    val bNum = bolum.selectFirst("div.episode")?.text()?.substringBefore(" ")
    newEpisode(bHref) {
        // IDE ekranında this.episode atanıyor; sezon henüz doğrulanmamış.
    }
}
\`\`\`

**Geliştirme önerisi, video kodu DEĞİL:** bölüm numarasını \`(\d+)\s*\.?\s*Bölüm\` benzeri doğrulanmış formatlardan sayıya ayır, URL'yi mutlaklaştır, \`season-1/season-2\` kapsayıcısını veya canonical URL sezona aitse onu kullan, boş isim için \`N. Bölüm\` etiketi üret, kayıtlarda \`(season, episode, url)\` kimliğini koru. URL eşleşmeleri örnek sayfada test edilmeli. Eski \`substringBefore\` kuralı evrenselleştirilmemeli.

## Test fixtürü

- [two_season_episodes.html](fixtures/two_season_episodes.html) — video DOM ilişkilerinden kurulan **sentetik** iki sezon/dört bölüm örneği.
- [test_episode_selector.py](fixtures/test_episode_selector.py) — \`BeautifulSoup\` ile **10 kontrol başarılı**: bağlantı, sezon grubu, \`1. Bölüm\` sayısı, boş isim, iki sezondaki tekrar eden bölüm, URL tekilliği ve kırılgan bölme kontrolü.
- Yerel ZIP içinde 10 özgün video karesi ve 4 yakın çekim bulunmaktadır; medya dosyaları büyük olduğundan GitHub kaynak klasörüne yüklenmedi.

## Kanıt düzeyi ve güvenlik

Bu rapor yalnız 10:00–20:00 aralığında **görülmüş** kod/HTML/UI için geçerlidir; film/dizi \`load\` çağrılarının bu noktada başarıyla derlendiği ya da gerçek yayının oynatıldığı kanıtlanmadı. 20. dakikadan sonraki dizi türü ve sezon parsing düzeltmelerini henüz bu rapora nihai sonuç olarak dahil etmedik. Kişisel çerezler, dinamik medya tokenları ve cihaz ID'leri paylaşılmamalı.

**Değişmez HLS kuralı:** her sunucu/ses için tek gerçek master M3U8 Sources girişidir; 1080p/720p gibi kalite seçenekleri yalnız **Parçalar/Tracks** menüsündedir.
