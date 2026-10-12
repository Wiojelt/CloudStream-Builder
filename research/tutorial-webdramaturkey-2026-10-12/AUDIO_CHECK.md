# Ses dosyasının kelimesi kelimesine dökümü: neden boş?

Yüklenen MP4 bir AAC stereo akış içerir ancak akışın ses örnekleri sessizliktir.

- Tam 63:43.605 boyunca FFmpeg `volumedetect` çıktısı: `mean_volume: -91.0 dB`, `max_volume: -91.0 dB` (dijital sıfır).
- Kayıttan 00:00, 10:00, 25:00, 50:00 ve 61:40 civarı iki saniyelik PCM örnekler alındı: tüm örnekler **0**.
- Hiçbir duyulabilir konuşma, sesli altyazı veya diyalog bulunmadığı için gerçek bir kelimesi kelimesine **ses transkripti üretilemez**.

| Zaman | Konuşma |
|---|---|
| 00:00:00–01:03:43.605 | Yok; dijital sessizlik |

**Not:** Ekrandaki kod editörü ve yazılı sohbet içerikleri sesli konuşma değildir. Ekran metinlerinin birebir çıkarılması ayrı görsel okuma görevidir. 114.594 kare sayısal olarak incelenmiş olmasına rağmen bütün ekran metinlerinin tamamı kelimesi kelimesine aktarılmış değildir; 15 saniyelik kanıt kareleri ve görsel değişim anları kaynakla karşılaştırma amacıyla saklanmıştır.
