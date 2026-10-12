# Kod ve ekran incelemesi — 40:00–50:00

Kaynak: kullanıcı tarafından yüklenen 63:43, 720p, sessiz ses kanallı ekran kaydı. Bu aralıkta 5 saniyelik **120 tam kare**, 10 temas sayfası ve 12 ayrıntılı yakınlaştırma incelendi. Aşağıdaki ara kodlar öğretici sırasında görüntülenen **taslak** sürümler olup çalışan nihai Kotlin sağlayıcısı veya güncel site doğrulaması değildir. Ağ ekranlarının çerezleri, cihaz verisi ve dinamik medya imzaları bu rapora alınmadı.

| Zaman | Ekranda doğrulanan işlem | Çıkarım |
|---|---|---|
| 40:00–40:30 | View Source üzerinde embed/iframe aranıyor | Statik HTML’de medya bulunmaması, dinamik kaynağın yokluğu demek değil |
| 40:35–41:35 | Firefox Network/Headers/Response içinde çok sayıda GET | Reklam, izleme, içerik isteği yanıt türüne göre ayrılmalı |
| 41:40–43:30 | IDE ile ağ yanıtları karşılaştırılıyor; kimi response boş veya reklama ait | 200 durum kodu, iframe veya reklam video linki playback kanıtı değildir |
| 43:45–44:15 | Play'e basılıyor, reklam/promo ve yükleme sonrası yeni istekler izleniyor | Önce/sonra Network farkını kaydet |
| 44:20–44:55 | Yeni yanıtın HTML ve iframe yapısı inceleniyor | HTML iframe gerçek medya manifesti yerine geçirilemez |
| 45:00–45:15 | DevTools'ta **POST /ajax/embed**, HTTP 200, **text/html; charset=UTF-8** | Form ID, gerçek referer ve istek başlıkları bugünkü hedef sitede yeniden teyit edilmeli |
| 45:20–46:10 | Sayfa kaynak kodunda `data-embed` araması; `div.nav-player-select` içinde seçili `a[data-embed]` ve `button.dropdown-source[data-embed]` | Özellik **div'de değil iç bağlantı ve düğmelerde** |
| 46:15–47:10 | Browser Inspector ile seçili ve diğer host düğmeleri inceleniyor | İlk/orta/son host, dil ve isim bilgilerini birlikte yakala |
| 47:15–47:30 | `loadLinks` içinde `document.select("div.nav-player-select").attr("data")` ara denemesi | Yanlış element + yanlış attr |
| 47:35–48:20 | Emülatör ve Logcat, yeni `videoId` logu | Katalog detay ekranı açılması gerçek oynatma kanıtı değil |
| 48:25–49:20 | `val playerlar = document.select("div.nav-player-select")`; `playerlar.attr("data-embed")`; eğitmen 'ilk video idsi gelmiyor' diyor | Dış div'de `data-embed` yok, seçili anchor + kaynak düğmeleri hedeflenmeli |
| 49:40–49:55 | ChatGPT üzerinden kod yardımı isteniyor | AI önerisi mevcut Network/DOM sonuçlarıyla doğrulanana kadar hipotez |

## Önce/sonra ekran bulgusu

Kaynak HTML'de seçili kaynak iki yerde gösteriliyor: `a.dropdown-toggle[data-embed]` ve `button.dropdown-source.selected[data-embed]`. Geriye kalan kaynaklar `button.dropdown-source[data-embed]` düğmeleri. Her düğümde etiket (ör. 'VK', 'UPN (Reklamlı)', 'Okru') ve `Türkçe Altyazı` alanı var. Kimlik ve URL değerleri raporda anonimleştirildi.

**Video ekranındaki yanlış ara kod:**

```kotlin
val document = app.get(data).document
val playerlar = document.select("div.nav-player-select")
val videoId = playerlar.attr("data-embed")
Log.d("kraptor_$name", "videoId = $videoId")
// TODO: loadExtractor(...)
return true
```

Kapsayıcıda özellik olmadığı için bu yaklaşım ilk ID'yi ve diğer seçenekleri doğru çıkaramıyor. `loadExtractor` hâlâ TODO olduğu için `return true` ayrıca oynatılabilir callback sonucu değildir.

**CSBuilder düzeltme örüntüsü (video son hâli değil):**

```kotlin
val ids = mutableSetOf<String>()
val choiceNodes = document.select(
    "div.nav-player-select a[data-embed], div.nav-player-select button[data-embed]"
)
val sourceIds = choiceNodes.mapNotNull { node ->
    val id = node.attr("data-embed").trim()
    id.takeIf { it.isNotEmpty() && ids.add(it) }
}
```

Bu kod seçili ID'nin hem anchor hem seçili button'da tekrar etmesini silerken sıralamayı korur. Gerçek host etiketi, dil varyantı ve yetkilendirilmiş istek zinciri ayrıca korunmalı; `data-embed` siteye özgü gözlem, universal API kuralı değil.

## Oynatma doğrulama sırası

Kaynak seçici `data-embed` → gözlenen **POST /ajax/embed** → HTML yanıtı `iframe[src]` → izinli ve uyumlu host resolver → manifest/segment içeriği → CloudStream cihaz oynatımı. Network'teki reklam/telemetri isteğini 'kaynak bulundu' sayma. Bu videonun 40–50. dakikası gerçek başarılı playback ispatı vermez.

**HLS master zorunluluğu:** sunucu/ses varyantı başına **tek gerçek master M3U8**; kalite yalnız CloudStream **Parçalar/Tracks** menüsünde. Aynı sunucunun 1080p/720p varyantlarını Sources olarak çoğaltma.

## Testler

Anonim/sentetik HTML fixtürü `fixtures/source_picker.html`, AJAX iframe fixtürü `fixtures/ajax_embed_response.html` ve `fixtures/test_source_picker.py`. **18/18 unittest geçti**: parent/child attribute seviyesi, seçili kaynağın tekrarı, ID dedup, ilk/orta/son kaynak, sunucu etiketi, dil, HTML iframe'in medya olmaması. Bunlar yerel DOM testleri olup canlı site veya CloudStream playback testleri değildir.

Orijinal karelerin büyük kopyaları GitHub'a konulmadı; 120 kare, temas sayfaları, seçilmiş ekran kanıtları ve bu belgenin tam metni kullanıcıya ZIP dosyasıyla sağlanır. Sonraki inceleme: 50:00–60:00 AJAX form alanları/headers, iframe parser ve host extractor.
