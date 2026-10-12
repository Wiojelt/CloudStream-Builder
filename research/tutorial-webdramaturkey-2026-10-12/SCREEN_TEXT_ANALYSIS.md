# Görüntüye gömülü Türkçe açıklama/altyazı analizi

## Teknik gerçek

Video `AAC stereo` akışı içerir ancak dijital sessizdir (FFmpeg max/mean -91 dB). Buna karşılık H.264 karelerin **alt bandında büyük beyaz Türkçe yazılı açıklamalar/altyazılar** vardır. Bu yazılar ayrı `srt` veya altyazı stream'i değildir, resmin pikselleridir.

Bu nedenle:
- **Sesli konuşmanın kelimesi kelimesine dökümü:** mevcut değil, konuşma kaydı yok.
- **Görüntüdeki Türkçe anlatım:** görsel okuma gerektirir. 15 saniyelik kanıt karelerine ek olarak videonun tüm 63:43 süresinden **her saniyede bir toplam 3.824 adet 1200×110 alt bant görüntüsü** alındı.
- 1 FPS alt bant dizini tüm aralıktaki Türkçe yazıları okumaya yardımcı olur fakat **tam harfi harfine transkript olarak iddia edilemez** (bir saniyeden kısa görünümler ve yazı doğrulama eksikliği).
- Saniyelik görsel arşiv `CSBuilder_Turkce_EkranYazilari_1s_2026-10-12.zip` adıyla sohbet dosyası olarak verilir. Repo içinde yalnız araştırma notları tutulur; 3.824 JPEG burada barındırılmaz.

## Kaynak ekranlardan gözle doğrulanan küçük örnekler

- Yaklaşık 00:00:45: “Sağ tıklayıp rename diyip ismini değiştir”
- Yaklaşık 00:01:45: “kategorileri almak için türlere gittim”
- Yaklaşık 00:02:00: “bunları kopyalayıp boş bir html dosyasının içine yapıştırıyorum”
- Yaklaşık 00:10:00: “nokta koymayı unutmuşuz”

Örnekler tam transkript değildir. Anlam/sözcükleri tahmin ederek metin tamamlamayın; kanıtı resimden yeniden okuyun.

## Skill açısından güvenilir bilgi

Bu video adım adım HTML ve DOM örnekleri, Kotlin CloudStream `MainAPI` işleyişi, hata ayıklama ve AJAX oyuncu çözümlemesi gösterir. `BUILD SUCCESSFUL` oynatma kanıtı değildir. İkinci kaynak listesi/kalite variantları videoya dayandırılarak evrensel kural yapılamaz; `SKILL.md` içindeki zorunlu HLS invariantı geçerlidir: **aynı sunucu ve ses varyantından tek master M3U8, kalite yalnız Parçalar/Video Tracks menüsünde.**
