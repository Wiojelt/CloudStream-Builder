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

---

## 8. CloudStream Önbellek Temizleme (Cache Cleaner) Mimarisi
- **Kullanıcı Verisini Korumalı Temizlik:**
  - CloudStream eklentilerinde Ayarlar UI'ına eklenen önbellek temizleme butonu veritabanını (`databases/`), ayarları (`shared_prefs/`) veya giriş oturumlarını silmemelidir.
  - `context.cacheDir.listFiles()` taranarak yalnızca geçici dosyalar (`cache/` dizini içeriği) silinir.
  - `app.baseClient.cache?.evictAll()` tetiklenerek OkHttp ağ istek önbelleği boşaltılır.
  - İşlem sonrasında `Toast` mesajı ile kullanıcıya temizlenen boyut MB/KB cinsinden anında bildirilir.

---

## 9. Spor Tekrarları & OK.RU İkili Periyot Çıkarıcı Mimarisi
- **Çoklu Periyot / Yarım Ayrıştırma (Basketball Video & Basketball Replays):**
  - Maç tekrarı sitelerinde (NBA, EuroLeague) maçlar tek bir video yerine "1. Yarı / 2. Yarı" veya "Q1, Q2, Q3, Q4" şeklinde farklı iframe/oynatıcılar altında barındırılır.
  - Her oynatıcı iframe'i (OK.RU, Dailymotion, Netu, Streamtape vb.) `newEpisode` olarak ayrıştırılmalı ve `season` / `episode` bilgisine periyot adı eklenmelidir.
  - OK.RU mobil iframe (`//ok.ru/videoembed/...`) doğrudan `OkRuExtractor` veya regex ile HLS/MP4 video kaynaklarına çözülür.

---

## 10. Mini Dizi / Dikey Drama & NetShort Hibrit RSA+AES Kilit Açma Mimarisi
- **Next.js RSC (React Server Component) Akış Çözümleme:**
  - `netshort.com` gibi Next.js modern web siteleri sayfa içeriğini HTML gövdesine değil, `self.__next_f.push([1, "..."])` JS akış bloklarına gömer.
  - Bu bloklar regex ile yakalanıp unescape edildiğinde (`\"` -> `"`, `\\` -> `\`), ham JSON veri dizilerine doğrudan erişilir.
- **NetShort API RSA-2048 + AES-128 Hibrit Güvenlik Mimarisi:**
  - **İstek Güvenliği:** 32 baytlık statik veya dinamik AES anahtarı (`5k3KYTOO9jnO0CeyGhdHc3pIjGnVgrMN`), NetShort RSA public key ile şifrelenip HTTP `encrypt-key` başlığına eklenir. JSON gövdesi AES-128/ECB/PKCS5Padding ile şifrelenir.
  - **Yanıt Çözümleme:** Sunucudan dönen `encrypt-key` başlığı JS istemci paketinden sızdırılan RSA private key ile çözülür, ardından dönen şifreli gövde bu anahtar ile AES-ECB deşifre edilir.
  - **VIP / Reklam Kilidi Açma (Unlock Ad Episode):**
    - Ziyaretçi token'ı `/web/auth/visitor_login` üzerinden alınır (`Authorization: Bearer <token>`).
    - Kilitli bölümler için `/user/shortPlay/userBase/unlock_ad_episode_v3` uç noktasına `shortPlayId`, `shortPlayEpisodeId`, `shortPlayEpisodeNo` şifreli olarak gönderilir.
    - İstek başarılı olunca `/web/v4/short_play/episode_info` çağrılır ve kilitli bölümün doğrudan CDN video URL'si (`playVoucher`) ve Türkçe altyazıları çekilir.

---

## 11. Bysesukior (JWPlayer) AES-256-GCM Deşifreleme & Dailymotion HLS & Test Deposu Kuralı
- **Bysesukior / JWPlayer AES-256-GCM:**
  - `bysesukior.com/api/videos/<code_id>` uç noktası `playback` nesnesi döner.
  - Anahtar Türetimi: `version` (1-indexed), `idx1 = version - 1`, `idx2 = 31 - version`. `key_parts[idx1]` ve `key_parts[idx2]` Base64URL decode edilip birleştirilerek 32 baytlık AES anahtarı elde edilir.
  - Şifre Çözümü: `Cipher.getInstance("AES/GCM/NoPadding")` ile `GCMParameterSpec(128, ivBytes)` ve `SecretKeySpec(keyBytes, "AES")` kullanılarak `payloadBytes` deşifre edilir. Elde edilen JSON içindeki `sources` dizisinden doğrudan HLS `.m3u8` master manifesti alınır.
- **Dailymotion HLS Ayrıştırma:**
  - `https://www.dailymotion.com/player/metadata/video/<video_id>` uç noktasına `Referer: https://geo.dailymotion.com/` başlığıyla GET isteği atılır.
  - Dönen JSON'daki `qualities.auto[0].url` doğrudan yüksek hızlı HLS `.m3u8` akışını sunar.
- **Test Deposu Dağıtım Kuralı:**
  - Kullanıcı tarafından açıkça ana / prodüksiyon depolara (`TurkSinema`, `TurkSpor`, `WioSinema` vb.) dağıtılması emredilmedikçe, yeni geliştirilen tüm eklentiler varsayılan olarak GitHub test deposuna (`Wiojelt/test`) yüklenir.

---

## 12. HLS / M3U8 Zorunluluğu ve Parçalı Akış Kuralı
- **Temel Prensip:**
  - Tüm eklentilerde kaynaklar öncelikle parçalı HLS formatında (`ExtractorLinkType.M3U8`) sunulmalıdır.
  - Kaynaklarda sabit çözünürlükler (1080p, 720p, 480p) bulunsa bile, CloudStream'in ExoPlayer tamponlama mekanizmasının ve anlık ileri/geri sarmasının kesintisiz çalışması için bunlar doğrudan HLS manifestolarına ve parçalı stream formatına aktarılmalıdır.
  - MP4 ve statik tek parça video dosyaları özellikle Android TV ve düşük RAM'li cihazlarda donmalara ve çöküşlere yol açtığından M3U8 önceliklendirilmelidir.
  - Her akış bağlantısına mutlaka hedef oynatıcı domainiyle eşleşen `Referer` ve `User-Agent` başlıkları eklenmelidir.

---

## 13. DiziAsya Çoklu Sağlayıcı & Next.js Görsel Çözümleme Mimarisi
- **Next.js Optimize Görseller (`/_next/image?url=...`):**
  - Modern web sitelerinde (DiziAsya gibi) afişler `/_next/image?url=https%3A%2F%2Fapi.diziasya.com...&w=...` şeklinde göreceli optimize parametrelerle sunulur.
  - CloudStream içerisinde afişlerin boş çıkmaması için `url=` parametresindeki şifreli URL `URLDecoder.decode(..., "UTF-8")` ile çözülmeli ve mutlak `api.diziasya.com/v2/images/posters/...` formatında CloudStream'e teslim edilmelidir.
- **DiziAsya Sağlayıcı Deşifreleri:**
  - **Diziasya2, 4Me, P2P, ABStr (Vidstack SPA):** URL hash'i (`#...`) ve AES-128-CBC (`Key: kiemtienmua911ca`, `IV: 1234567890oiuytr`) algoritması ile JSON ayrıştırılır, Cloudflare CDN üzerindeki doğrudan `cfNative` / `source` HLS (`.m3u8`) akışı elde edilir.
  - **Abyss:** HTML içerisindeki `datas` şifreli metni ayrıştırılır, `https://enc-dec.app/api/dec-abyss` uç noktasına POST edilerek çözülmüş akış kaynakları alınır.
  - **EV (Morencius):** JS packer ile paketlenmiş kod `getAndUnpack` ile açılarak doğrudan HLS `.m3u8` akışına erişilir.
  - **Vidmoly & LULU:** CloudStream standart extractor'ları ile HLS formatında çözümlenir.
  - **OKRU:** Kullanıcı talimatı gereği DiziAsya kaynaklarından tamamen filtrelenir/hariç tutulur.

---

## 14. SupportNotice Pop-up UI & Sıklık Yönetimi
- **UI Standartları:**
  - Sabit dar genişlikler (`340dp`) yerine yatay ve TV ekranlarında `450dp`'ye kadar uzanan dinamik genişlik (`minOf((screenWidth * 0.52f).toInt(), dp(450))`) kullanılmalıdır.
  - MaterialButton bileşenlerinde varsayılan 6dp dikey insets metin kırpılmasına sebep olduğundan `insetTop = 0`, `insetBottom = 0`, `height = 48dp`, `gravity = Gravity.CENTER` tanımlanmalıdır.
  - Köşe yuvarlamaları `20dp`, iç boşluklar (`24dp, 22dp, 24dp, 18dp`) ile modern koyu cam teması korunmalıdır.
- **Sıklık ve Senkronizasyon:**
  - Birden fazla eklentinin ardı ardına pop-up açmasını engellemek için tek bir paylaşımlı `wio_global_support_notice` tercihi ve oturum içi bellek kilidi (`isShownThisSession`) uygulanır.
  - Günlük veya periyodik gösterimlerde zaman damgası kontrolü (`System.currentTimeMillis() - lastTime > interval`) ile kullanıcıyı boğmayacak şekilde aralıklı tetikleme yapılır.

---

## 15. BingeBang (bingebang.tv) & Özel Şifre Çözme / Çoklu Sunucu Mimarisi
- **Script XOR Ticket Çözümü:**
  - Sayfadaki inline script `var k=[...], d=[...]` dizilerini içerir. `(d[i] xor k[i % k.size]).toChar()` ile deşifre edilerek dinamik `ticket` ve metadata (`imdb`, `season`, `episode`) elde edilir.
- **Özel SHA-256 CTR Akış Şifresi (Kritik Sayaç Hatası):**
  - Anahtar Türetme: `SHA256(salt + ticket)` (`salt = "9e2b7c41a0f6d85b3c1e7a94f25d0b86"`).
  - IV: Base64Url çözümlenmiş ham şifreli verinin ilk 16 baytı. Ciphertext: 16. bayttan sonrası.
  - **Sayaç Başlangıcı (`counter`):** Standart CTR gibi 1'den değil, **kesinlikle 0'dan** başlar (`counter = 0`). 1'den başlatıldığında ilk 32 bayt ve tüm müteakip bloklar yanlış deşifre edilerek bozuk JSON ve "bağlantı bulunamadı" hatası verir.
  - Blok Girdisi: `Key[32] + IV[16] + Counter_UInt32_BE[4]` (52 bayt). Keystream = `SHA256(blok_girdisi)`.
- **8 Sunucu Eşzamanlı Çözümleme (`amap`):**
  - BingeBang 8 farklı sunucu döndürür (`Aldebaran`, `Rigel`, `Sirius (4K)`, `Yildun`, `Vega`, `Polaris`, `Nashira`, `Fomalhaut`).
  - Seri döngü yerine `serverList.amap { ... }` ile paralel sorgulanarak tüm sunucular 1-2 saniye içinde HLS M3U8 (`ExtractorLinkType.M3U8`) olarak teslim edilir.
- **Kapsamlı Altyazı Desteği:**
  - Hem sunucunun resolve yanıtından dönen `.vtt` altyazıları (`subArr`), hem de script'ten ayrıştırılan IMDb ID üzerinden OpenSubtitles API (`opensubtitles-v3.strem.io`) sorgulanarak Türkçe ve İngilizce altyazılar CloudStream'e aktarılır.

---

## 16. Spor ve Maç Tekrarı Portallarında (BasketballVideo vb.) Afiş Çözümleme
- **Tuzak:**
  - Haber ve maç video sitelerinde afiş görseli (`<div class="poster"><a href="..."><img ...></a></div>`) ile başlık metni (`<h3><a href="...">Maç Başlığı</a></h3>`) ayrı kardeş etiketlerde yer alır.
  - `doc.select("a[href*='replay']")` ile doğrudan linkler dönüldüğünde, resim linkinde metin olmadığı için atlanır; metin linkinde ise resim bulunmadığı için afişler boş kalır.
- **Çözüm:**
  - Kart kapsayıcısı seçilmelidir (`.short_item`, `[id^='entryID']`, `.inf_raited`, `table tr`).
  - Başlık kapsayıcı içindeki `h3` veya başlıktan, afiş ise `.poster img, .full_img img, img` seçicilerinden çekilerek eksiksiz afişli arama ve ana sayfa yanıtı oluşturulmalıdır.

---

## 17. Kesin Depo ve Dağıtım Ayrımı (Wio vs Turk Depoları)
- **WioSinema Kuralı (Sağlayıcı Mimarisi):**
  - WioSinema toplu bir sağlayıcı toplayıcıdır (`StreamAggregator`).
  - Yeni film/dizi kaynakları WioSinema'ya bağımsız `.cs3` eklentisi olarak DEĞİL; `StreamAggregator.kt` içindeki `directTmdbProviders` veya `scraperProviders` listesine dahili bir `MainAPI` sağlayıcısı olarak eklenir. `WioSinema.cs3` derlenip doğrudan `Wiojelt/WioSinema` reposuna yüklenir.
- **TurkSinema Kuralı (Eklenti Mimarisi):**
  - TurkSinema modüler bir eklenti deposudur (`Wiojelt/TurkSinema`).
  - Burada her kaynak (`BingeBang`, `DiziAsya`, vb.) bağımsız bir eklenti (`.cs3`) olarak derlenir ve `TurkSinema/plugins.json` listesine ayrı bir girdi olarak eklenir.
- **TurkSpor vs WioSpor Ayrımı:**
  - Basketbol (`BasketballReplays`, `BasketballVideo`) ve benzeri branş/tekrar eklentileri **YALNIZCA TurkSpor** reposuna yüklenir.
  - `WioSpor` reposuna **ASLA** yüklenmez.
- **Test Deposu Temizleme Prensibi:**
  - `Wiojelt/test` deposu sadece geliştirme ve ön test aşamasındaki eklentiler içindir.
  - Bir eklenti test edilip onaylandıktan sonra ana depolara (`TurkSinema`, `WioSinema`, `TurkSpor`) taşınır ve test deposundan (`test/plugins.json` ve `.cs3` dosyaları) anında temizlenir.

---

## 18. CloudStream "Hata / İndirilemedi" Önleme Kuralı (Bütünlük Kilidi) ve Eklenti Logoları
- **Kök Neden (Neden "Hata" Verir?):**
  - CloudStream bir eklentiyi indirirken `plugins.json` içindeki `fileHash` (format: `sha256-<küçük_harf_hex>`), `hash` ve `fileSize` alanlarını indirilen `.cs3` dosyasının gerçek SHA-256 özeti ve bayt boyutuyla katı şekilde kıyaslar.
  - En ufak bir uyuşmazlıkta (örneğin `.cs3` yeniden derlenip versiyon arttırıldığında `fileHash` eski kaldığında ya da başka bir eklentinin boyutu kopyalandığında) CloudStream yüklemeyi keser ve kullanıcıya hiçbir detay vermeden "Hata" / "İndirilemedi" der.
- **Bütünlük Kilidi (Zorunlu Dağıtım Adımı):**
  - Her `.cs3` derlemesi veya `plugins.json` güncellemesinden önce ve sonra dosya boyutu ve SHA-256 hash'i KESİNLİKLE script ile otomatik doğrulanmalı ve düzeltilmelidir:
    ```bash
    python cloudstream-builder/scripts/verify_repo_integrity.py <repo_yolu> --fix
    # Veya tüm depoları tek seferde denetlemek için:
    python cloudstream-builder/scripts/verify_repo_integrity.py --all
    ```
  - Bu komut listedeki her eklentinin `.cs3` dosyasının fiziksel varlığını, bayt boyutunu ve SHA-256 özetini okur; `plugins.json` içindeki `fileSize`, `fileHash` (`sha256-<hex>`) ve `hash` alanlarıyla birebir eşitler. Sıfır hata raporlanmadan push atılamaz.

- **Eklenti Logosu ve iconUrl Kuralı:**
  - Her eklentinin kendine özel, yüksek çözünürlüklü şeffaf bir logosu (`.png` / `.webp`, tercihen minimum 128x128 kare) bulunmalıdır.
  - Özel depolar (`*-Source`) gizli olduğundan logolar buradan çekilemez (404 verir).
  - Logolar genel erişime açık ana depoların (`TurkSinema`, `TurkSpor` vb.) `main` dalındaki `assets/providers/<EklentiAdı>.png` dizinine kaydedilmeli ve `iconUrl` buna yönlendirilmelidir (`https://raw.githubusercontent.com/Wiojelt/<Repo>/main/assets/providers/<EklentiAdı>.png`).
  - Genel logo (`assets/logo.png`) yalnızca geçici yer tutucu olarak kullanılabilir; nihai sürümde asla genel logo bırakılmamalıdır.

---

## 19. Tek ve Ortak Ayarlar UI Mimarisi (WioSinema & WioSpor Bütünlüğü)
- **Problem & İhtiyaç:**
  - WioSinema ve WioSpor ayarlarının birbirinden kopuk olması ve birinde yapılan UI iyileştirmelerinin (örneğin "Önbelleği Temizle" ve "Kaydet ve Kapat" butonlarının tepeye taşınması, modern cam teması vb.) diğerine yansımaması engellenmelidir.
- **Tek Merkez Mimarisi (`WioCoreSettingsDialog`):**
  - Hem WioSinema hem de WioSpor ayar ekranı için tek bir ortak çekirdek UI bileşeni kullanılır: `WioCoreSettingsDialog`.
  - Hiçbir eklenti bağımsız, eski/özel kırmızı ayar bottom sheet'i (`WioSettings.kt`) barındırmaz. `WioSettings.show` çağrısı doğrudan `WioCoreSettingsDialog.show(context, config)` yapısına delege edilir.
- **Otomatik Gradle Senkronizasyon Kancası (`syncCommonUi`):**
  - İki ayrı Git deposu bulunduğu için, Gradle derleme sürecine (`preBuild` / `prepareBundleSources`) otomatik senkronizasyon görevi (`syncCommonUi`) entegre edilmiştir.
  - `WioCoreSettingsDialog.kt` üzerinde yapılan herhangi bir tasarım/UI değişikliği, derleme anında paket ismi (`package dev.wiojelt.turksinema.common` <-> `package turkspor.common`) otomatik dönüştürülerek diğer depoya da senkronize edilir.






