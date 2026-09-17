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
  4. **URL Şeması Koruması:** `ajax/bolumler` veya `ajax/videosec` gibi görece (relative) AJAX adresleri CloudStream OkHttp/NiceHttp istemcisine doğrudan verilemez (`Expected URL scheme 'http' or 'https'`). Her istek öncesi `fixTurkAnimeUrl` ile mutlak URL'e dönüştürülmelidir.

---

## 5. CloudStream Dağıtım ve UI Kalıpları
- **İndirirken Hata (Download Mismatch) Çözümü:**
  - CloudStream, indirilen `.cs3` içindeki `manifest.json` dosyasındaki `version` değeri ile depodaki `plugins.json` içindeki `version` değerini birebir karşılaştırır. Uyuşmazlık durumunda doğrudan "İndirirken hata" verir.
  - Gradle `version = X` artırıldığında `:make` görevi sonrası üretilen `.cs3` derhal depoya kopyalanmalı, SHA-256 ve dosya boyutu `plugins.json`'a işlenmelidir.
- **IPTV / Kaynak Seçimi Aç-Kapa (Switch) UI Tasarımı:**
  - Klasik `AlertDialog` ve checkbox listesi yerine, Android `Switch` bileşenleri içeren koyu cam kart (`#161B22`) temalı özel `Dialog` tasarımı.
  - Her anahtar (Switch) durumu doğrudan `SharedPreferences.putBoolean` ile saklar; diyalog kapatıldığında anında akış filtreleme motoruna yansır.
- **Depo Önbellekleme:** `repo.json` içindeki `pluginLists` URL'lerinde zaman damgası sorgu parametreleri (`?t=...`) yerine sabit ham GitHub URL'leri kullanılmalı, CDN önbelleği temiz tutulmalıdır.

---

## 6. TMDB & IMDb Meta Veri Güvenliği ve Arama Optimizasyonu
- **TMDB HTTP 500 (Internal Server Error) ve Kademeli İstek Fallback'i:**
  - Bazı dizilerde (örn. Erşan Kuneri - ID 197679) TMDB `append_to_response=videos,credits,recommendations` parametreleriyle çağrıldığında sunucu tarafında 500 hatası üretir ve tüm sayfa yüklemesi çöker.
  - **Çözüm (Çok Kademeli Fallback):**
    1. Kademeli `app.get`: Önce zengin parametrelerle dene, hata alınırsa sadece `append_to_response=external_ids` ile çağır, yine hata alınırsa yalın detay adresine geç.
    2. Eksik IMDb ID'ler için `/external_ids` uç noktasına bağımsız GET isteği at.
- **Cinemeta (Stremio IMDb) Alternatif Meta Veri Katmanı:**
  - TMDB sonuç dönmediğinde veya içerik bulunamadığında Stremio'nun açık Cinemeta API'si (`https://v3-cinemeta.strem.io`) devreye girer.
  - Hem film (`/meta/movie/tt...json`) hem dizi (`/meta/series/tt...json`) bölümleri ve katalog araması (`/catalog/.../top/search=...json`) ile alternatif veri kaynağı sağlanır.
- **Türkçe Karakter / ASCII Arama Normalizasyonu:**
  - Çoğu Türkçe film/dizi sağlayıcısı (Dizilla, DiziBox vb.) başlıkları veritabanında Türkçe karaktersiz (ASCII) indeksler.
  - Arama motorunda `normalizeTr()` fonksiyonu ile `[ş->s, ç->c, ı->i, ğ->g, ü->u, ö->o]` dönüşümü yapılarak sağlayıcılara hem orijinal hem ASCII başlık sorgulanmalı, eşleşme başarısı maksimize edilmelidir.

---

## 7. CloseLoad & Rapidrame Yeni Nesil Şifreleme ve Destek Mimarisi
- **CloseLoad / Rapidrame Modern Deşifre Algoritması:**
  - **Eski Durum:** Sabit fonksiyon adı (`dc_`), sahte JSON-LD `contentUrl` (404 dönen honeypot URL).
  - **Yeni Mekanizma:**
    1. Dinamik fonksiyon adı ve değişkenler: `ahk` (20-30 karakterlik anahtar) ve `uwkd` (işlem sırası dizgisi örn: `bvX`, `bIbvb`).
    2. Operasyon Sırası: Atob (`b`), String ters çevirme (`v`), ROT kaydırma (`qth = (26 - ((code - 64) % 26)) % 26`).
    3. PRNG Dizi Karıştırma (Shuffle): `cgu = (cgu * 75 + 74) % 65537` formülü ile üretilen indis dizisi üzerinden karakter değişimi.
    4. XOR Akümülatör Çözümü: `tqinz` ve `mwb` adımlarıyla `(e1b1j ^ nfn)` üzerinden gerçek akış linkine (`.txt` uzantılı HLS m3u8) ulaşılır.
  - Sahte `master.txt` (playmix.uno) fallback'i tamamen iptal edilerek native algoritma ile %100 doğrudan canlı akış elde edilir.
- **Topluluk / Destek Bildirimi:**
  - Bağımsız gereksiz "Destek" eklentileri (.cs3) depolardan temizlenir; bildirim `SupportNotice` üzerinden günde bir kez açılan şık cam kart arayüzü ile doğrudan Kreosus (`https://kreosus.com/wiojelt`) ve Telegram bağlantılarıyla kullanıcıya sunulur.
