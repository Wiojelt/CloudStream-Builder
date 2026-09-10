<p align="center">
  <img src="assets/banner.svg" alt="CloudStream Builder" width="100%">
</p>

<p align="center">
  <strong>Bir siteyi yalnızca listeleyen değil, katalogdan gerçek oynatmaya kadar inceleyen CloudStream eklenti üretim sistemi.</strong>
</p>

<p align="center">
  <a href="https://github.com/Wiojelt/TurkSinema">TurkSinema</a> ·
  <a href="https://github.com/Wiojelt/TurkSpor">TurkSpor</a> ·
  <a href="https://github.com/Wiojelt">GitHub @Wiojelt</a> ·
  Telegram: <strong>@wioj3lt</strong>
</p>

---

## Neler yapar?

- Film, dizi ve canlı yayın sağlayıcılarını ayrı akışlarla analiz eder.
- Sitedeki gerçek kategori adlarını, posterleri, detay bilgilerini ve bölümleri çıkarır.
- Kaynak seçici, AJAX oynatıcı, iframe ve doğrudan HLS/DASH bağlantılarını ayırt eder.
- Çoklu kaynakları, kalite etiketlerini ve altyazıları korur.
- Fragmanları oynatma kaynağına karıştırmadan CloudStream'in fragman alanına ekler.
- Derlenmiş `.cs3` ile aynı sürüme ait kaynak paketini üretir.
- Derleme ile gerçek oynatma doğrulamasını birbirinden ayırır.

## Nasıl çalışır?

```text
Site / izinli API
        ↓
Kategori ve örnek içerik keşfi
        ↓
Film + dizi detay ve player isteği analizi
        ↓
CloudStream Kotlin sağlayıcısı
        ↓
Derleme → yapısal denetim → gerçek oynatma testi
        ↓
                  .cs3
```

## Kullanım örneği

Codex içinde:

```text
$cloudstream-builder https://ornek.site için film ve dizi eklentisi oluştur.
```

Beceri; belirsiz bir kartın medya, açıklama veya gereksiz bölüm olup olmadığını gerektiğinde sorar. Sonraki çalışmalarda doğrulanmış site kalıplarından yararlanır, fakat her sitenin oynatıcı isteğini ayrıca kontrol eder.

## Durum

CloudStream Builder aktif olarak geliştiriliyor. Gösterim deposu açıktır; beceri kodu ve geliştirme araçları şimdilik özel kaynak deposunda tutulmaktadır. Bu sayfada çalıştırılabilir kaynak kodu veya gizli yapılandırma bulunmaz.

## İlkeler

- Yalnızca kullanıcının yetkilendirdiği kaynaklar üzerinde çalışır.
- Kişisel çerez, token, parola ve cihaz verisini paketlere eklemez.
- “Derlendi” ile “CloudStream'de oynatıldı” durumlarını ayrı raporlar.
- Kaynakta bulunmayan altyazı, bölüm veya kaliteyi uydurmaz.

---

<p align="center">
  <sub>CloudStream Builder · Wiojelt</sub>
</p>
