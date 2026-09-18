# CloudStream Builder Mimari Referans Notları

> **Not:** Antigravity / Codex skill motorunun ana giriş noktası `cloudstream-builder/SKILL.md` ve altındaki `references/` dizinidir. Bu belge, geliştirme süreçlerinde kazanılan genel mühendislik kalıplarını ve yetenek hafızasını (pattern memory) saklayan teknik referans kılavuzudur.

---

## 1. Genel UI ve Ayarlar Mimarisi
- **Tam Ekran & Kaydırma Kararlılığı:**
  - Ayar ve kontrol pencerelerinde `BottomSheetBehavior.STATE_EXPANDED` ile birlikte `skipCollapsed = true` ve `isDraggable = false` uygulanmalıdır.
  - Sürükleme kapatıldığında (`isDraggable = false`), dokunma ve kaydırma hareketleri `NestedScrollView` bileşenine devredilir; bu sayede liste kaydırılırken pencerenin kazara kapanması engellenir.
- **TV & D-Pad Odak Yönetimi:**
  - Tüm tıklanabilir elemanlar (`MaterialButton`, `SwitchMaterial`, kart kapsayıcıları) `isFocusable = true` ve belirgin odak kenarlığı (`focusedBorder`) ile donatılmalıdır.
- **Düğme Düzeni Standardı:**
  - Hızlı aksiyon butonları ("Önbelleği Temizle", "Kaydet ve Kapat") pencerenin üst kısmında yer almalı, kullanıcıyı uzun listelerin altına inmek zorunda bırakmamalıdır.

---

## 2. Otomatik Alan Adı Atlama Motoru (Auto-Domain Engine)
- **Kural & Mekanizma:**
  - Kapanan veya engellenen web siteleri için alan adı doğrulaması yapılırken yalnızca HTTP yanıt koduna (200) güvenilmez.
  - Başlık veya anasayfa HTML'i içinde sağlayıcıya özgü anlamsal belirteçler (meta etiketler, anahtar API yanıtları) aranmalıdır.
  - Başarılı olan yeni adres `SharedPreferences` üzerinde saklanmalı ve müteakip isteklerde dinamik olarak kullanılmalıdır.

---

## 3. TMDb & IMDb Meta Veri Standardı
- **Güvenli Eşleştirme:**
  - Arama sorguları ve katalog verileri TMDb / IMDb API ile zenginleştirilirken, yerel ve yabancı başlıklar normalize edilmeli (`cleanTitle`).
  - Yıl ve sezon/bölüm bilgileri eşleştirmede teyit unsuru olarak kullanılmalıdır.
- **Fragman İzolasyonu:**
  - Fragman linkleri kesinlikle `loadLinks` içine video kaynağı olarak konulmamalı; yalnızca CloudStream'in yerleşik `addTrailer` alanına aktarılmalıdır.

---

## 4. HLS / M3U8 Parçalı Akış Zorunluluğu
- **Kesin Kural:**
  - Eklentiden döndürülen tüm video kaynakları öncelikle parçalı HLS formatında (`ExtractorLinkType.M3U8`) teslim edilmelidir.
  - Kaynak sunucuda sabit çözünürlükler (1080p, 720p, 480p) ayrık halde bulunsa bile, her biri CloudStream'e bağımsız parçalı akış (chunked HLS stream) olarak aktarılmalıdır.

---

## 5. Gelişmiş Şifre Çözme ve Ayrıştırma Kalıpları (Yetenek Hafızası)
- **Dinamik Script XOR Ayrıştırma:**
  - Sayfa içine gömülü paralel tamsayı dizileriyle gizlenmiş bilet ve oturum anahtarları, `(d[i] xor k[i % k.size]).toChar()` mantığıyla anında deşifre edilir.
- **Özel CTR Akış Şifreleri (Counter Senkronizasyonu):**
  - Hash tabanlı anahtar akışı (keystream) üreten akış şifrelerinde sayaç başlangıç indeksinin (0-based vs 1-based) doğru ayarlanması hayati önem taşır; 0 tabanlı CTR akışlarında ilk 32 bayt `counter = 0` ile deşifre edilmelidir.
- **Çoklu Sunucu Paralel Çözümleme (`amap`):**
  - Birden fazla video sunucusu (mirror/host) döndüren kaynaklarda seri döngü yerine paralel eşzamanlı sorgulama (`amap`) uygulanarak tüm linkler 1-2 saniye içinde teslim edilmelidir.
- **Spor / Çok Parçalı Yayın Çıkarıcı:**
  - İki yarı veya çoklu periyot şeklinde yüklenen maç kayıtlarında her periyot bağımsız oynatma seçeneği olarak sunulmalıdır.

---

## 6. Depo Dağıtım Bütünlük Kilidi (Anti-"Hata" ve Anti-"Eski Sürüm" Kilidi)
- **Kök Neden:**
  - CloudStream, `plugins.json` içindeki `version`, `fileHash` (`sha256-<hex>`), `hash` ve `fileSize` alanlarını indirilen `.cs3` arşiviyle katı şekilde karşılaştırır.
  - Kodda/Gradle'da sürüm artsa bile `plugins.json` içinde sürüm güncellenmezse kullanıcı cihazında güncelleme butonu görünmez ("v1'de kaldı" hatası).
  - 1 baytlık boyut veya en ufak hash uyuşmazlığı ise kurulumda sessiz "Hata / İndirilemedi" uyarısına yol açar.
- **Zorunlu Dağıtım Adımı:**
  - Her dağıtım ve güncelleme öncesinde otomatik doğrulama ve düzeltme aracı çalıştırılmalıdır:
    ```bash
    python cloudstream-builder/scripts/verify_repo_integrity.py --all --fix
    ```
  - Bu araç `.cs3` arşivinin içindeki `manifest.json` dosyasından derlenmiş gerçek sürüm numarasını (`version`), arşivin fiziksel boyutunu (`fileSize`) ve SHA-256 özetini (`fileHash`/`hash`) okuyarak `plugins.json` ile otomatik eşitler. Sıfır hata raporlanmadan depolara push yapılamaz.

---

## 7. Eklenti Logoları ve Dış Kaynak Güvenliği
- **Logo Standardı:**
  - Her eklenti için genel erişime açık depolarda barındırılan, minimum 128x128 çözünürlükte şeffaf bir logo (`.png` / `.webp`) tanımlanmalıdır.
  - Özel (private) kaynak depolarına yönlendiren URL'ler (404 döneceği için) kullanılmamalıdır.
- **Bağış & Destek Yönlendirmeleri:**
  - Tüm destek bildirimleri, ayar ekranı butonları ve depo sayfalarında tek standart bağış adresi `https://kreosus.com/wiojelt` olarak kullanılır.
