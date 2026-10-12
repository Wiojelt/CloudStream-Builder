# WebDramaTurkey — gerçek ekran/kod analizi 60:00–63:43

Kaynak: kullanıcının 01:03:43.605, 1280×720 sessiz ses kanallı eğitim videosu. Son 3:43, **4 saniyede bir 56 tam kare**, 5 temas sayfası ve 12 seçilmiş yüksek çözünürlüklü ek kareyle incelendi. Bu bir IDE/Gradle/Git ekran analizi; gerçek CloudStream yeniden derlemesi veya güncel site oynatma testi değil.

## Zaman damgalı kanıtlar

| Zaman | Görüntüden doğrulanan | Sonuç |
|---|---|---|
| 60:00–60:40 | Emülatörde farklı detaylar; Logcat'te iframe çözümleme çıktıları | Tüm kaynakların çalıştığı kanıtlanmadı |
| 60:44–61:08 | Proje ağacında WebDramaTurkey.kt, WebDramaTurkeyPlugin.kt, AndroidManifest.xml, build.gradle.kts | Kotlin/manifest/Gradle uyumu kontrol edilmeli |
| 61:08–61:40 | Eğitmen Gradle metadata düzenini unuttuğunu söylüyor ve build.gradle.kts açıyor | Önceki BUILD SUCCESSFUL mesajı son metadata için yeniden derleme kanıtı değil |
| 61:45–62:05 | version=1, authors, language=tr, description, status=1, tvTypes görülüyor | Eğitimdeki Gradle alanları mevcut SDK ile ayrıca doğrulanmalı |
| 61:50–62:08 | tvTypes içinde AsianDrama, Movie, Anime var | İlan edilen tüm medya şekillerinde load ve oynatma kanıtı gerekir |
| 62:12–62:30 | Favicon aracı kullanılıyor, iconUrl üçüncü taraf hizmetten alınıyor | Kalıcı, kontrol edilen erişilebilir HTTPS ikon tercih edilmeli |
| 62:45–63:05 | Description kısaltılıp Web Drama Turkey - Kore, Çin, Japon Dizileri, Filmleri ve Animeler oluyor | Metadata içerikle uyumlu olmalı |
| 63:15–63:33 | IntelliJ Commit panelinde dört dosya: AndroidManifest.xml, build.gradle.kts, WebDramaTurkey.kt, WebDramaTurkeyPlugin.kt; commit mesajı WebDramaTurkey | Videoda .cs3/repo.json/plugins.json paketi görünmüyor |
| 63:36–63:42 | **4 files committed: WebDramaTurkey** ve son karede **Pushed 1 commit to origin/master** | Git push eğitim kaydında gerçekleşmiş; dağıtılmış .cs3 kurulumunu ispatlamaz |

## Gerçek ekrandaki Gradle metadata biçimi

```kotlin
version = 1
cloudstream {
    authors = listOf("kraptor")
    language = "tr"
    description = "Web Drama Turkey - Kore, Çin, Japon Dizileri, Filmleri ve Animeler"
    status = 1
    tvTypes = listOf("AsianDrama", "Movie", "Anime")
    iconUrl = "<third-party favicon URL omitted>"
}
```

Video içindeki açıklamada durum kodları 0=Down, 1=OK, 2=Slow, 3=Beta only. Bu tarihsel örnektir; güncel CloudStream SDK semantiğinin doğrulaması değildir. Icon URL de canlı çalışırlığı test edilmemiş örnektir.

## CSBuilder için gerekli kontroller

1. Kotlin MainAPI supportedTypes, load yanıtları, Gradle tvTypes ve plugin/manifest kayıtlarını eşleştir.
2. Metadata değiştikten sonra yeni Gradle build çalıştır; gerçek .cs3 manifestini incele.
3. Git commit/push ile .cs3 üretimini ayrı kapılar say. repo.json → katalog/plugins.json → gerçek indirilebilir .cs3 sürümü, SHA-256, dosya boyutu ve kaynak ZIP'i doğrula.
4. Status/version alanını eski videoya bakarak körlemesine değiştirme. Repo politika ve SDK sürümünü doğrula.
5. Sahibi tarafından barındırılan 128×128+ halka açık provider logo ve gerçek HTTP erişimi kullan; favicon proxy URL'sini hazır prod logo sayma.
6. Wiojelt depo özel commit mesajı ve builds/main işleyişini koru; videodaki commit mesajı o politikayı değiştirmez.
7. **Zorunlu HLS:** aynı host/ses için Sources'da tek gerçek master M3U8; 1080p/720p seçenekleri yalnız oynatıcının Parçalar/Tracks menüsünde.

## Yerel test kapsamı

19 sentetik offline metadata/release kanıt testi geçti. Gerçek CloudStream derlemesi, GitHub video deposu canlı erişimi veya güncel cihaz oynatma testi yapılmadı. Orijinal kareler sohbet ZIP paketinde; kişisel/dinamik token içerebilecek ekranlar doğrudan GitHub'da yayınlanmıyor.

## Main dalı ile uyumluluk uyarısı

Son karşılaştırma araştırma dalını main'den **82 commit ileride, 30 commit geride** ve toplam 54 dosya farkıyla **diverged** gösteriyor. Main dalındaki SKILL.md ve HLS referansı daha yeni. Bu araştırma dalını doğrudan merge edip main'in mevcut kurallarını ezme. Güncel main'den yeni temiz entegrasyon dalı aç; video vaka çalışmasını ve yalnız eklemeli referansları taşı; test ve kullanıcı incelemesinden sonra birleştir.

Önceki code-audit bölümleri: [00–10](00-10-screen-and-code.md), [10–20](10-20-screen-and-code.md), [20–30](20-30-screen-and-code.md), [30–40](30-40-screen-and-code.md), [40–50](40-50-screen-and-code.md), [50–60](50-60-screen-and-code.md).