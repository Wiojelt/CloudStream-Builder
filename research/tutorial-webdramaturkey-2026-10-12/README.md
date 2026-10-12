# Video kaynak araştırması — WebDramaTurkey (2026-10-12)

Kaynak: kullanıcının yüklediği yaklaşık 63 dk 43 sn, 1280×720, 30 FPS MP4.

**Durum: İNCELEME / KARAR BEKLİYOR.** Bu klasördeki notlar araştırma malzemesidir; `cloudstream-builder/SKILL.md` veya çalışan sağlayıcılar henüz değiştirilmedi.

## Bulgular

Video, `WebDramaTurkey` adlı Kotlin / CloudStream sağlayıcısının site inceleme, CSS selector, katalog/arama, film-dizi/anime detayı, bölüm listesi, `data-embed` kaynak düğmeleri, DevTools Network, AJAX POST, iframe, emulator/logcat testi ve Gradle paketleme akışını gösteriyor. Kaynak sitenin kayıttaki örnek alan adı `webdramaturkey.org`; **bugün çalıştığı doğrulanmamıştır**.

Önemli ayrım: videodaki Gradle `BUILD SUCCESSFUL` ve emülatörde ayrıntı/bölüm ekranlarının açılması **oynatma doğrulaması değildir**. Videonun sonlarına doğru bazı iframe konaklarında yükleme/hata durumları da görülüyor. Video bilgileri `playbackVerified=true` kanıtı olarak kullanılamaz.

## Dosyalar

- [TIMELINE.md](TIMELINE.md): zaman damgalarına dayalı gözlem ve öğretici akış.
- [SKILL_PROPOSAL.md](SKILL_PROPOSAL.md): eklenebilecek kalıplar, olumsuz örnekler, test matrisi ve kullanıcı kararı bekleyen değişiklikler.

### Yöntem ve kapsam

30 saniyelik aralıklarla ekran örneklemesi yapıldı, ek olarak 1 dakikalık temas sayfaları ve kritik noktalardaki çözünürlükte görüntüler incelendi. Bu döküm **tam ses transkripti veya 114.594 karenin tek tek denetimi değildir**. Ses parçası bulunsa da bu araştırmada güvenilir otomatik Türkçe konuşma transkripsiyonu kullanılmadı. Ekranda görünen kod/yazı ile daha ileri doğrulama gerektiren yorumlar ayrı tutulur.

Güvenlik: gerçek kullanıcı çerezleri, bearer tokenlar, cihaz ID’leri, kısa ömürlü medya imzaları, kişisel bilgiler ve kaynak sayfanın geçici konak adresleri raporlara alınmadı. Kayıttaki reklam/izleme kodu referans olarak kopyalanmamalıdır.
