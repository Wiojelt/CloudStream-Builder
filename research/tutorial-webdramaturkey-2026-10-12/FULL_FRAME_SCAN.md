# Her-kare taraması ve kanıt durumu (12 Ekim 2026)

Kaynak video: 01:03:43.605, 1280×720, H.264, 29.970185 fps (ortalama), 114.594 kare.

## Gerçekten tamamlanan işlem

- FFmpeg bütün **114.594 H.264 kareyi** çözdü, **0 kare atlandı**.
- Her karenin 80×45 piksel gri tonlamalı kopyası, önceki kareyle piksel farkı/önemli değişen piksel yüzdesi ve ortalama parlaklık açısından tarandı. **114.594 satırlı** `all_114594_frames_metrics.csv.gz` yerel çalışma paketinde bulunur.
- Piksel farkı ortalaması >4 olan **3.969** kare, >12 olan **1.060** kare saptandı. Bunlar görsel değişim **adaylarıdır**, insan tarafından semantik olarak açıklanmış 1.060 ayrı eylem değillerdir.
- Ayrıca her **15 saniyede bir** alınmış **255 adet** özgün 1280×720 kare, **101 kritik değişim karesi** ve **22 temas sayfası** yerel kanıt paketine eklendi.
- Paket `/mnt/data/CSBuilder_Full_Frame_Analysis_2026-10-12.zip` içinde oluşturuldu; bu dosya GitHub reposunda barındırılmaz, sohbet eki olarak teslim edilir.

**Ek keşif — gömülü altyazılar:** Video görüntüsünün alt bandında Türkçe anlatım cümleleri bulunuyor; AAC sesi sessiz olsa da görünür metin vardır. Bunlar ayrı bir altyazı akışı değil, H.264 görüntü pikselleridir. Her saniyeden alınmış **3.824 alt bant görüntüsü** ve zaman dizini ikinci ZIP paketinde oluşturuldu; böyle bir görüntü dizini bile milisaniyelik metinlerin eksiksiz kelime-kelime transkripti sayılamaz.\n\n**Kesin sınır:** 'Her kareyi sayısal taradık' demek, '114.594 karenin her birinde görünen her kod/sohbet cümlesini tek tek eksiksiz okuyup yazıya geçirdik' demek değildir. Bu ikinci iddia doğrulanamaz. Konuşma transkripti de yoktur; ses kanalı sessizdir.

## Video bilgisine uygulanacak kurallar

Videonun oynatıcı çözümleme yaklaşımı bir DevTools/XHR vaka çalışmasıdır: film/dizi/bölüm verisi → `data-embed` sunucu kimliği → sayfanın izinli AJAX isteği `POST /ajax/embed` → HTML `iframe[src]` → uygun extractor → oynatılabilir manifest/segment → CloudStream doğrulaması. Video kaydında playbackVerified ispatlanmamıştır.

HLS kuralı **bu araştırma dalındaki belgelere** uygulanmıştır (main dalına aktarımı ayrıca doğrulanmalıdır): `cloudstream-builder/SKILL.md`, `references/playback.md`, `references/proven-repository-patterns.md` ve `CSBUILDER_NOTES.md`. **Aynı sunucu/ses için tek master M3U8; kalite yalnız oynatıcının Parçalar menüsünde.** Eski extractor kütüphanesi fonksiyonlarının kodları bu yönergeye göre henüz yeniden yazılmamıştır; farklı konak/codec özel durumları için test gerektirir.

## Yeniden üretilebilirlik

Kaynağı `ffmpeg` ile bütün kareler okunarak 80×45 gri kopyaya dönüştürmek ve birbirini izleyen karelerin ortalama mutlak farkını hesaplamak yeterlidir. Kanıt paketinde `scan_summary.json`, `visual_change_events.json` ve her kareye ait CSV.gz bulunmaktadır. Sayısal kare zamanları FPS bazlı yaklaşık zamanlardır; tam ses transkripti üretilemez.
