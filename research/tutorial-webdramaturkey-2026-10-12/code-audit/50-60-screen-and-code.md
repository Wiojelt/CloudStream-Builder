# Video gerçek ekran, Kotlin ve Logcat analizi — 50:00–60:00

**Kanıt:** Kullanıcının 63:43, 1280×720 video kaydı. Bu aralıkta her 5 saniyeden alınan **120 gerçek tam ekran kare**, 10 zaman kodlu temas sayfası, 18 özel zamanlı kare ve 18 büyütülmüş kod/ekran bölgesi incelendi. Kaynak dosyanın tamamı sağlanmadığı için görünen satırlar **ara geliştirme** niteliğindedir. Video AAC ses kanalı sessiz; ekranda Türkçe yazılı açıklamalar var. Hash içeren iframe URL'leri GitHub araştırmasına alınmadı.

## Kanıt zinciri

| Zaman | Ekranda doğrulanan | Sonuç |
|---|---|---|
| 50:00–51:55 | ChatGPT önerisi sonrası `loadLinks` içinde `document.select("[data-embed]").mapNotNull { it.attr("data-embed") }` | Üst kapsayıcı yerine doğru iç elemanlar hedefleniyor; `mapNotNull` **boş string** elemez |
| 52:00–54:15 | DevTools Request Headers, IntelliJ `app.post("$mainUrl/ajax/embed", referer=data, headers=..., data=...)` | Siteye özgü POST form alanı `id`, `X-Requested-With: XMLHttpRequest`, `Content-Type: application/x-www-form-urlencoded; charset=UTF-8` |
| 54:20–55:15 | `.distinct()` ile seçili kaynak tekrarları eleniyor ve `for(id in embedIds)` POST döngüsü oluşturuluyor | İlk kaynak + diğer hostlar ayrıştırılıyor; host/dil bilgilerini de kaydetmek gerek |
| 55:20–55:55 | Logcat cevabı `iframe.embed-responsive-item[src]`; farklı cevaplarda yan öğeler/reklam alanları var | İlk AJAX yanıtı HTML, medya manifesti değil |
| 56:00–56:45 | `.selectFirst("iframe")?.attr("src").toString()` | İlk iframe URL'sini buluyor; eksik iframe varsa yanlışlıkla `"null"` metni oluşabilir |
| 56:50–58:45 | `app.get(iframe, referer=data).document` ardından başka `iframe[src]` okunuyor | **İki katlı iframe**: AJAX HTML → iframe sayfası → ikinci host embed |
| 58:45–59:15 | Logcat'te birden fazla harici player hostu ve bir hostta kullanılamama/telif uyarısı görünüyor | Her mirror bağımsız sınanmalı; bir iframe bulunması başarılı oynatma sayılmaz |
| 59:20–59:40 | `loadExtractor(iframeSon, "$mainUrl/", subtitleCallback, callback)` etkin; `BUILD SUCCESSFUL`; emülatörde video yükleme simgesi | Başarı sadece derleme/deneme; hosta uygun referer ayrıca doğrulanmalı |
| 59:45–59:55 | Emülatörün yatay player UI'si ve anlatıcının “video oynuyor” yazısı | **Eğitimde raporlanan oynatma**, güncel sitede bağımsız doğrulama değil |

## Videoda görünen önemli Kotlin satırları (final tam kod olarak kullanmayın)

```kotlin
val embedIds = document.select("[data-embed]")
    .mapNotNull { it.attr("data-embed") }
    .distinct()
for (id in embedIds) {
    val response = app.post(
        url = "$mainUrl/ajax/embed",
        referer = data,
        headers = mapOf(
            "X-Requested-With" to "XMLHttpRequest",
            "Content-Type" to "application/x-www-form-urlencoded; charset=UTF-8"
        ),
        data = mapOf("id" to id)
    ).document
    val iframe = response.selectFirst("iframe")?.attr("src").toString()
    val iframeGet = app.get(iframe, referer = data).document
    val iframeSon = iframeGet.selectFirst("iframe")?.attr("src").toString()
    loadExtractor(iframeSon, "$mainUrl/", subtitleCallback, callback)
}
```

**Eksiklikler:** `attr` yoksa boş dize döndürebilir; `mapNotNull` boş dizeyi atmaz. `?.attr("src").toString()` bir iframe bulunamadığında gerçek HTTP adresi olmayan `"null"` dizesi üretme riski taşır. İlk iframe göreli ise doğru yanıt URL'sine göre mutlaklaştırılmalıdır. İkinci iframe için ana sitenin kökünü zorunlu referer varsaymak doğru değildir. Mevcut kayıtta tüm hostların başarılı olduğu ispat edilmedi.

## CSBuilder teknik çıkarımı

1. Seçili `a[data-embed]` ve diğer `button[data-embed]` kimliklerini topla; trim, boş değer eleme ve host/language bazında tekilleştirme uygula. İlk, orta ve son kaynağın çıktığını test et.
2. Network'teki AJAX sözleşmesini alan adından değil gözlenen method/content-type/request body/headers/response sırasından öğren; geçici token/çerezleri loglama.
3. HTML dönen `POST` → birinci iframe GET → ikinci iframe veya gerçek medya. Her seviyede URL şeması, boş cevap, döngü ve uygun referer kontrol et. Yanlış, reklam veya kullanılamayan hostu medya gibi döndürme.
4. Her host ayrı hata yalıtımıyla çözümlensin; sunucu kimliklerini ve dilleri rastgele bir araya getirme.
5. **Değişmez kural:** Bir sunucu/ses varyantı için bir gerçek master M3U8 Source; farklı 1080p/720p varyantlar ayrı Sources değil, oynatıcının **Parçalar/Tracks** menüsünde.
6. `return true`, terminal build, Logcat iframe kaydı ve emülatör spinner'ı gerçek cihazda oynatmaya eşdeğer değildir. Eğitmenin tarihsel başarı ifadesini açıkça ayrı etiketle.

## Test kanıtı

Yerel pakette `fixtures/test_ajax_iframe_50_60.py` ile **24/24 offline unittest PASS**. Testler kaynak ID'si/dil/tekrar, form encoding, ilk ve ikinci iframe, boş/hatalı yanıtlar, `javascript:`/`file:`/`data:` URL reddi, reklam/error HTML'nin medya olmaması ve master M3U8 tek Source politikası için sentetik HTML üzerinden çalışır. **Bu test gerçek CloudStream veya site erişimini doğrulamaz.**

**Depo durumu:** Çalışma bu araştırma dalında belgeleniyor; `main` ya da çalışan sağlayıcı değiştirilmedi. Video içindeki tam kare ekran görüntüleri büyük ve tokenized URL içerebildiği için GitHub'a yüklenmemiş, kullanıcıya özel ZIP içinde sağlanmıştır.

**Sonraki bölüm:** 60:00–63:43 — Gradle metadata, sürüm, TV türleri, ikon ve GitHub'a gönderim.