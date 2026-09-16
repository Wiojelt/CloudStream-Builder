# CSBuilder Geliştirme ve Mimari Notları

Bu dosya, tamamlanan her CloudStream eklentisi ve altyapı geliştirmesinden sonra biriktirilen pratik yöntemleri, mimari kalıpları ve extractor çözümlerini içerir. PR talimatı verildiğinde bu notlar cloudstream-builder skill dokümanlarına ve referanslarına aktarılacaktır.

---

## 1. Ortak UI ve Ayarlar Mimarisi (WioCoreSettingsDialog)
- **Sorun:** BottomSheetDialog içinde dikey liste kaydırılırken diyalog aşağıya doğru sürüklenip kapanıyordu (dismiss).
- **Çözüm:** 
  - NestedScrollView kullanımı ve davranış kontrolü:
    val behavior = (dialog as BottomSheetDialog).behavior
    behavior.isDraggable = false
    behavior.skipCollapsed = true
    behavior.state = BottomSheetBehavior.STATE_EXPANDED
- **Responsive Çoklu Sütun:** Ekran genişliği 580dp üzeri cihazlarda veya TV ekranlarında 2 sütunlu grid, dikey telefonlarda tek sütun.
- **TV Box / Düşük Donanım Tespiti:**
  - ActivityManager.isLowRamDevice kontrolü
  - UI_MODE_TYPE_TELEVISION kontrolü
- **Modern Alan Adı Düzenleme Penceresi:** Ham AlertDialog yerine koyu cam kart temalı (#161B22), altın vurgulu çerçeveli (#FFC107), yuvarlatılmış MaterialButton içeren özel Dialog.

---

## 2. Otomatik Alan Adı Atlama Motoru (Auto-Domain Engine)
- **Kullanım Yeri:** DiziPal, DiziBox gibi sık engellenen sağlayıcılar.
- **Yöntem:**
  - Mevcut domain HTTP 403 / 404 / ConnectionError verdiğinde regex ile domain sonundaki sayıyı ayrıştırma (dizipal1581.com -> 1581).
  - Sırayla +1, +2, +3 adreslerine HEAD / GET isteği atıp HTTP 200 dönen adresi yakalama.
  - Bulunan yeni adresi SharedPreferences / Plugin Key-Value Storage'a kaydetme ve çalışma anında mainUrl değişkenini güncelleme.

---

## 3. Eklenti İncelemeleri ve Çözüm Kalıpları

### A. CineCat (cinecat.eu)
- **Yapı:** TMDB tabanlı dizi/film portalı.
- **Yöntem:**
  - TMDB API / dahili katalog arama motoru ile Türkçe ve global meta veri senkronizasyonu.
  - Video oynatıcı iframe'lerinden VidSrc / SuperEmbed / FastX türevi akışları Regex ile çekme.
  - Kalite seçeneği (1080p, 720p, 480p) ve Türkçe dublaj/altyazı track'lerini ayrıştırma.

### B. DiziAsya (diziasya.com)
- **Yapı:** Kore, Japon, Çin dizileri ve Asya sineması.
- **Sorun & Çözüm:**
  - Dizi bölümleri HTML tablosundan ve ajax bölüm listesinden parse edildi.
  - Video kaynağında Okru (Odnoklassniki) ve RapidVid iframeleri yer alıyor.
  - Okru kaynaklarında User-Agent ve Referer başlıklarının CloudStream standart niceHttp istemcisine tam uyumlu geçilmesi zorunludur; aksi takdirde HTTP 403 / Bağlantı bulunamadı hatası alınır.

### C. DMAX (dmax.com.tr)
- **Yapı:** Discovery / Warner Bros bünyesindeki resmi programlar ve Canlı TV.
- **Yöntem:**
  - Canlı TV: HLS (.m3u8) akış manifestosu, token yenileme ve dinamik stream URL ayrıştırma.
  - Kategoriler: Programlar, Belgeseller, Popüler içerikler API üzerinden sayfalanarak 5'li gruplar halinde CloudStream ana sayfasına (HomePageList) dizildi.

### D. Yeşilçam TV & PowerSinema
- **Yapı:** Klasik Türk Sineması arşivi.
- **Yöntem:**
  - Direct MP4 ve YouTube resolver entegrasyonu.
  - Tek çatıda toplanarak gereksiz extractor yükü optimize edildi, düşük FPS / takılma sorunları doğrudan akış linki verilerek çözüldü.

### E. RecTV & InatBox
- **Yapı:** Şifreli ve açık spor kanalları, ulusal yayınlar.
- **Yöntem:**
  - InatBox v59 sunucu protokolü ve saat eşitleme (time-sync token) mekanizması.
  - RecTV spor alternatifleri (beIN Sports, S Sport, Tivibu) yedekli stream adresleri ile yapılandırıldı.

---

## 4. Multi-Provider Gradle Mimarisi
- common/src/main/kotlin dizini tüm alt projelere (subprojects) kaynak kümesi (sourceSets.getByName('main').java.srcDirs += rootProject.file('common/src/main/kotlin').path) olarak bağlanır.
- Böylece UI, ağ yardımcıları ve extractor'lar tek bir noktadan güncellendiğinde tüm bağımsız .cs3 eklentileri otomatik olarak yeni mimariye kavuşur.
### F. TurkAnime (turkanime.tv) - Film ve Dizi Ayrıştırma Mimarisi
- **Yapı:** Türkiye'nin en büyük anime portalı. Hem bölümlü anime serileri hem de tekil anime filmleri barındırır.
- **Film ve Dizi Arasındaki Kritik Farklar:**
  1. **Detay Sayfası Ayrımı (`load`):**
     - Diziler: `div#animedetay` metninde `Kategori:TV`, `Kategori:OVA`, `Kategori:ONA` içerir. Bölüm sayısı `220 / 220`, `12 / 12` gibidir.
     - Filmler: `Kategori:Movie` veya `Kategori:Film` içerir ve Bölüm Sayısı `1 / 1` dir.
  2. **Bölüm Listesi (`ajax/bolumler`):**
     - Dizilerde `li a[href*='/video/']` başlığında `(\\d+)\\.\\s*Bölüm` yer alır. Çoklu `newEpisode` oluşturularak `newTvSeriesLoadResponse` ile döndürülür.
     - Filmlerde başlıkta bölüm numarası yer almaz (örn: `Kimi no Na wa.`). Bu durumda tekil video linki yakalanıp CloudStream'de tek tıkla izleme sunan `newMovieLoadResponse(..., TvType.AnimeMovie, movieVideoUrl)` döndürülür.
  3. **Video Çözümleme (`loadLinks`):**
     - Video sayfasında fansub butonları (`AnimeWho-BD`, `AniSekai`, `AoiSubs` vb.) `IndexIcerik('ajax/videosec&b=...&f=...')` AJAX çağrıları içerir.
     - Her fansub içinde varsayılan Alucard oynatıcısı ve diğer video barındırıcılar (`OK.RU`, `HDVID`, `DOODSTREAM`, `VOE`, `UQLOAD`, `MAIL.RU` vb.) yer alır.
     - **AES Şifre Çözümü:** İframe adresi `embed/#/url/` içeriyorsa Base64 decode edilerek JSON (`ct`, `iv`, `s`) elde edilir ve `AesHelper.cryptoAESHandler` (AES-256-CBC, OpenSSL EVP MD5 anahtar türetimi) ile çözülür.
     - **Doğrudan İframe Fallback:** Bazı sunucular (örn: DOODSTREAM, MAIL.RU) şifresiz doğrudan `<iframe>` verir; bu yüzden şifresiz link kontrolü şarttır.
     - **Paralel Çözümleme:** Senkron döngü yerine Kotlin Coroutines (`coroutineScope`, `async`/`awaitAll`) ile ilk 3-4 fansub ve sunucuları eşzamanlı taranır; bekleme süresi 30 saniyeden 1-2 saniyeye indirilir.
