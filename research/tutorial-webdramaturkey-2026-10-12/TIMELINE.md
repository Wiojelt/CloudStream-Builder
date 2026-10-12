# Zaman kodlu inceleme — WebDramaTurkey sağlayıcı eğitimi

> Zamanlar yaklaşık bölüm başlangıçlarını gösterir, saniye saniye anlatımın aynen deşifresi değildir. Görünen ekran ve test davranışı esas alınmıştır.

| Zaman | Doğrudan gözlem | CSBuilder için anlamı |
|---|---|---|
| 00:00–02:30 | CloudStreamPlugins proje ağacı, yeni WebDramaTurkey Kotlin/Gradle eklenti dosyaları; sayfadaki kaynak koddan kategori bağlantıları alınması | Önce gerçek site ve mevcut sağlayıcı yapısını belirle; yalnız CSS'den isim tahmin etme |
| 02:30–04:30 | HTML `/tur/...` kategori hreflerinin `mainUrl` + görünür kategori isimleriyle eşlenmesi | Kategori URL / başlık sözleşmesi, boş bölümleri filtreleme |
| 04:30–08:30 | `getMainPage`, `app.get(...).document`, `document.select(\"div.items article\")`, `toMainPageResult()`, `selectFirst`, `data-src` ile poster | Ana sayfa kart seçicilerini kart/link/poster üzerinden birlikte test et; göreli URL'leri düzelt |
| 08:30–11:00 | Terminalde `deployWithAdb` ve `BUILD SUCCESSFUL`, emülatörde arama/katalog görünümü, eksik nokta/selector üzerinde düzeltme | Derleme ve yükleme çalışabilir; UI verisini ayrıca doğrula |
| 11:00–16:00 | `search`, `quickSearch`, `load`; sayfa HTML'inde film detayı: başlık, poster, özet, yıl, türler, oyuncular, fragman, öneriler | Arama selector'ı ana sayfadan farklı olabilir; tüm metadata alanları opsiyonel/fallbacklı olmalı |
| 16:00–23:30 | Anime/dizi sayfasında sezon/bölüm linkleri `div.episode` üzerinden toplanıyor; `newEpisode` yapısı deneniyor | Her bölüm için ayrı kararlı `data`, sezon/bölüm ID ve oynatma verisi tutulmalı |
| 23:30–30:30 | Emülatörde bazı dizilerin bölüm listesi boş; loglarla `div.episode` ve sayfa türü işleme revize ediliyor | En az 2 sezonlu bir seri, farklı URL biçimleri ve boş kaynak testi gerekir |
| 30:30–37:00 | Film, anime ve seri sayfalarından HTML farkları inceleniyor; selector/metaveri düzeltmeleri sürüyor | Görünen kart türü / ana sayfa menüsüne bakarak `Movie` etiketleme yapılmamalı |
| 37:00–41:00 | HTML kaynağında `iframe` aranıyor; ham sayfa ve gerçek oynatıcı yüklenmesi arasında fark görülüyor | Statik HTML'de iframe yoksa DOM/script/XHR akışı incelenmeli |
| 41:00–47:30 | Tarayıcı geliştirici araçlarında Network/XHR ve HTML'de kaynak seçim düğmeleri araştırılıyor; `data-embed` ve farklı host etiketleri görülüyor | İstek zincirini id→AJAX→iframe→extractor olarak modelle; ilk hostu bütün kaynak sanma |
| 47:30–51:30 | Kaynak ID seçimi/ilk video ID'si sorunu araştırılıyor; ChatGPT'den kod yardımı isteniyor | AI önerisi kanıt değildir; XHR istek/yanıtıyla doğrula |
| 51:30–55:30 | `loadLinks`, `[data-embed]`, `distinct()` ve `POST /ajax/embed`; `Referer`, `X-Requested-With`, form data `id` ve içerik türü işleniyor | Siteye özgü POST sözleşmesi kayıt altına alınmalı; hata başarısızsa diğer hostlar bağımsız denenmeli |
| 55:30–58:30 | AJAX yanıtı HTML olarak ele alınıp `iframe[src]` aranmaya başlanıyor; Logcat'te yanıt ve iframe adresi inceleniyor | İframe HTML yanıtı oynatılabilir medya değildir; host extractor sonraki zorunlu adımdır |
| 58:30–61:00 | Emülatör ve loglarda çeşitli host iframe adresleri, dönen `null` durumları, yükleme/hata ekranları görülüyor | Gerçek segment/manifest ve cihaz oynatma kontrolü şart; burada başarı kanıtı yok |
| 61:00–63:43 | `build.gradle.kts` içinde `cloudstream` metadata, tvTypes, dil/açıklama, ikon; IDE commit ekranında 4 değiştirilmiş dosya | Paketleme ve metadata kontrol listesine girmeli; videoda tamamlanmış yayın/push kanıtı yok |

## Yüksek güvenli görünür yapı taşları

- Kotlin `MainAPI`/CloudStream eklentisi içinde `getMainPage`, `search`, `load`, `loadLinks` aşamaları ayrı geliştirilmiş.
- Kartlar için gözlenen CSS örnekleri: `div.items article`, başlık bağları, kapak için `data-src`; bunlar **yalnızca gösterilen site için örnek**, genel kural değil.
- Film/seri/anime sayfaları farklı şablonlar kullanabildiğinden tek selector ve tek medya türü yeterli değil.
- Kaynak seçiminde `data-embed` kimliği tespit edilmiş; seçilen kimlik `/ajax/embed` POST gövdesinde `id` olarak kullanılmış; yanıt HTML'inden `iframe[src]` okunmaya çalışılmış.
- Uygulama ve terminal logları boş katalog/bölüm/kaynak sorununu teşhis etmek için kullanılmış; `BUILD SUCCESSFUL` görüntülenmiş fakat bu oynatma kanıtı değil.

## Açık kalanlar

- Videodaki sesin tam Türkçe transkripti bu dosyada mevcut değil.
- Her bir konak için canlı çalışırlık, DRM/yetki kısıtları ve güncel `Referer` ihtiyaçları bağımsız doğrulanmadı.
- Final çalışır .cs3 / canlı yayın / kesintisiz film oynatma doğrulanmadı.
- Video ekranından alınan örnek adımlar eğitimdir, aktif kaynak URL veya kimliği olarak kullanılmamalıdır.
