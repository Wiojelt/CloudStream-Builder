# Video kod ve ekran incelemesi — 20:00–30:00

**Kanıt:** Kullanıcının yüklediği 63:43, 1280×720 eğitim videosunun 20:00–30:00 aralığından 5 saniyede bir **120 orijinal kare** ve 20 temas sayfası incelendi; kritik IDE/Logcat/emülatör kareleri ayrıca yakınlaştırıldı. Bu döküm tam kaynak `.kt` dosyası değildir. Ayrıntılı görüntü paketi sohbet dosyası olarak saklandı.

## Zaman kodlu karşılaştırma

| Zaman | Videodaki gerçek uygulama | Durum/CSBuilder dersi |
|---|---|---|
| 20:00–21:15 | `div.episodes a` üzerinden `bHref` ve `div.episode` üzerinden `bNum` çıkarılıyor. | Bölüm URL'si, numarası ve sezon ayrı doğrulanmalı. |
| 20:35–21:35 | `bSeason = bHref?.substringBefore("-sezon")?.substringAfterLast("/")?.toIntOrNull()`; `bNum` için `substringBefore(...).toIntOrNull()`. | URL'deki `N-sezon` biçimi hedef siteye özel; parser biçimi doğrulanmalı. |
| 21:35 | `newEpisode(bHref) { this.episode = bNum; this.season = bSeason; this.name = "Bölüm" }` | Bir sezonda ve diğer sezonda `1. Bölüm` tekrar edebilir; birlikte tekilleştirilmeli. |
| 22:20–23:25 | Film `newMovieLoadResponse` ile ayrılıyor; dizi `newTvSeriesLoadResponse` ile yazılıyor. İlk taslakta dizinin `TvType.Movie` ve `episodes=url` hataları var, sonra `episodes=bolumler` yapılıyor. | Kaynak videodaki **ara durumlar çalışma kodu değildir**; cevap türü/API veri modeli eşleşmeli. |
| 23:25 | `loadLinks`: `// TODO`, yorum satırında `loadExtractor(...)`, sonra `return true`. | **Oynatma doğrulanmadı.** Callback'e medya vermeden `return true` başarı kanıtı değildir. |
| 23:30–24:20 | Emülatörde film detay ekranı; bazı içeriklerde `Çok yakında…`. Kotlin'e `Log.d` ekleniyor. | Boş bölüm yüzünden otomatik scraper hata teşhisi konulmaz. |
| 24:30–26:25 | Logcat'te bölüm HTML'i, href'ler, `bNum`, `bSeason` karşılaştırılıyor; bazısında kaynak tarafında bölümler yok. | Gerçekten boş sayfa ile başarısız CSS selector ayrımı yapılmalı; kişisel token loglanmamalı. |
| 26:55–27:15 | Emülatörde `Watashi no Otto to Kekkon Shite` ayrıntısında bölüm listesi görünüyor. Bazı başka detaylarda yenileme/bağlantı ekranları var. | Bazı **bölüm listelerinin görünmesi** olumlu kanıt; gerçek video oynatıldığı kanıtı değil. |
| 27:35–28:10 | Kaynak sitenin dizi/anime sayfaları ve URL/menü biçimi inceleniyor. | `/anime/` ayrımı yalnız o kaynağa özgü; universal sınıflandırma değil. |
| 28:15–29:35 | `newAnimeLoadResponse(..., TvType.Anime, comingSoonIfNone = true)` taslağı, altyazılı/dublaj bölümleri. | `comingSoonIfNone` her boş dizi için zorunlu değil; dil kanıtı gerekli. |
| 29:45–29:55 | `episodes = mutableMapOf(...)` kodu hâlâ yazım hâlinde; IDE hata/uyarı göstergeleri var. | Anime dalının bu noktada derlendiği veya tüm bölümleri gösterdiği doğrulanmamış. |

## Görünen Kotlin kodunun seçili yapısı (tam kaynak değildir)

```kotlin
val bolumler = document.select("div.episodes a").map { bolum ->
    val bHref = fixUrlNull(bolum.attr("href"))
    val bNum = bolum.selectFirst("div.episode")?.text()
        ?.substringBefore(".")?.toIntOrNull()
    val bSeason = bHref?.substringBefore("-sezon")
        ?.substringAfterLast("/")?.toIntOrNull()
    newEpisode(bHref) {
        this.episode = bNum
        this.season = bSeason
        this.name = "Bölüm"
    }
}
```

Videoda `substringBefore` argümanı geliştirme boyunca değişiyor; burada yalnız sonlara doğru okunabilen biçim gösterildi. Boş/null hata denetimleri ve gerçek sayfa varyasyonları tamamlanmış değildir. Ayrıca `return if (url.contains("/film/"))` sınıflaması kaynak URL yapısına bağlıdır.

## Zorunlu doğrulama ayrımı

1. **Source data**: film/dizi/anime sınıfı, title/plot/poster ve gerçek episode URL'leri.
2. **Episode parse**: iki sezonlu örnek; `(season,episode,url)` eşsizliği; `1. Bölüm` nokta ayrıştırma.
3. **Empty result**: site henüz bölüm yayınlamadıysa boş liste doğru olabilir; `comingSoon` yalnız açık kaynak durumuna dayanmalı.
4. **LoadLinks**: TODO/stub veya `return true` medya oynatma kanıtı değildir. Gerçek link, manifest/segment ve CloudStream playback ayrıca doğrulanmalı.
5. **Anime**: Subbed/Dubbed bilgisi kaynak ses/altyazı kanıtı ile işaretlenmeli.
6. **HLS**: **tek gerçek master M3U8 per sunucu/ses**, kaliteler yalnız **Parçalar** menüsünde. Master kalite varyantları ayrı Sources olamaz.

## Fixture ve testler

Sentetik iki sezonlu HTML, explicit coming-soon ve unknown-empty vakaları: [fixtures/episodes.html](fixtures/episodes.html). Testler: [fixtures/test_episode_contract.py](fixtures/test_episode_contract.py). Bağımsız Python/BeautifulSoup **16 offline unittest geçti** (canlı siteye veya CloudStream'e erişmeden). Bunlar oynatmayı kanıtlamaz.

Görsel raporun tüm video kareleri ve seçilmiş orijinal ekran kanıtları bu sohbette hazırlanmış ZIP içindedir; GitHub'a büyük video veya kişisel oturum bilgileri koyulmadı.

**Sıradaki aralık:** 30:00–40:00: film detay/h1 seçici onarımı, farklı açıklama şablonları, oynatıcı kaynaklarının statik HTML'de neden bulunmadığı.
