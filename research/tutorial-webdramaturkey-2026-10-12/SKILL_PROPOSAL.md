# CSBuilder değişiklik önerisi — onay bekliyor

## Karar: skill'e nerede ve nasıl eklenmeli?

**Önerilen yeni referans:** `cloudstream-builder/references/browser-devtools-to-provider.md`.

`SKILL.md` dosyasına uzun transkript koymak yerine `movie-series.md` ve `playback.md` belgelerinden bu yeni referansa 1–2 satırlık yönlendirme konmalı. Bu video bir *site inceleme / hata ayıklama vaka çalışmasıdır*, evrensel hazır sağlayıcı şablonu değildir.

### Yeni playbook'un kapsamı (öneri)

1. Site türünü ve erişim koşullarını belirle (sitenin kamuya açık / yetkili API olması; oturum verilerini depolama).
2. Browser Inspector ile film/seri/anime kartlarını ve `href` / lazy poster alanlarını ayrı ayrı incele. Her HTML selector için title, canonical URL ve poster kontrol et.
3. `getMainPage`, `search`, `load`, `loadLinks` için ayrı doğrulama çıktısı üret. `quickSearch` yalnız arama sözleşmesini doğruladıktan sonra eklenir.
4. Film/seri/anime ayrımı için bölüm düğmeleri, stabil URL türü ve somut metadata kanıtı kullan. Bölüm `data` içinde sayfa linki ve sezon/bölüm kimliğini koru.
5. Kullanıcının kaynak düğmesine basılınca DevTools Network ile **Method, URL role, content-type, form fields, safe headers, response type** ve gerekli session sırasını yakala. Geçici token/çerez ve kişisel URL'leri loglama.
6. `data-embed` gibi kaynak ID'lerini kullanıcıya gösterilen host/altyazı dili etiketiyle eşleştir; `distinctBy(id,host,language)` uygula. Tüm mirror ve dilleri koru, ilkini rastgele seçme.
7. AJAX `POST` yanıtındaki `iframe[src]` alanını sayfa bağlamında mutlaklaştır. **HTML/iframe doğrudan `ExtractorLink` değildir**; uygun host `loadExtractor` veya doğrulanmış siteye özel extractor kullan.
8. Durum kodu 200 olsa bile HTML `error`, boş iframe, soft 404, kapanmış host, süresi dolmuş token ve anti-bot yanıtı kontrol et.
9. Test kapıları: derleme, katalog, arama, film detayı, çok sezonlu dizi, bölümler, farklı hostlar, altyazı, HTTP medya/manifest, CloudStream cihazında gerçek oynatma. Her testin ayrı durumunu yaz.
10. Logları güvenli ve sınırlı üret: kaynak ID'si için maskeli/anonim kimlik, endpoint yolu/HTTP durum, yanıt türü, test sonucu; asla oturum çerezi veya tam kısa ömürlü akış URL'si değil.

### Görünür videodan alınabilecek kod düşüncesi (çalışır kod olduğu iddia edilmiyor)

```text
GET detail URL
  -> select source buttons [data-embed] + visible host/language label
  -> preserve episode-specific data
  -> POST /ajax/embed (form: id; site-required headers; Referer=detail)
  -> parse response HTML for iframe[src]
  -> normalize iframe URL; identify supported host
  -> loadExtractor(iframe, correctReferer, subtitleCallback, callback)
  -> verify output is real media + test playback
```

## Var olan depodaki çelişki — video dışı ama giderilmeli

`cloudstream-builder/SKILL.md` içindeki **tek sunucu/tek kaynak, HLS master playlist Parçalar** invariantı, aşağıdaki eski notlarla çelişiyor:

- `CSBUILDER_NOTES.md` §4 tüm kaynakların HLS'ye çevrilmesini ve sabit kalitelerin ayrı ayrı sunulmasını savunuyor.
- `references/proven-repository-patterns.md` VixSrc altında `#EXT-X-STREAM-INF` varyantlarını ayrı CloudStream Sources olarak yaymayı, başka yerde masterı korumayı öneriyor.

**Öneri:** `SKILL.md` ana invariantı geçerli tek kaynak olsun; alt metinler bunu açıkça tekrarlasın. Gerçek HLS master mevcutsa tek M3U8 bağlantısı ve oynatıcı içindeki track seçimi. Kaynak yalnız bağımsız sabit çözünürlük veriyorsa ana invariantta tanımlandığı biçimde uygun tek sunucu/kalite politikası. Bir MP4'ü sözde HLS diye sunma; site dışı yeniden paketleme izni/altyapısı yoksa gerçek biçimiyle ifade et. Bu son cümle teknik tutarlılık önerisidir ve kullanıcı onayı ister.

## Hangi konular eklenmemeli?

- Örnek sitenin mevcut domaini, canlı iframe URL'leri, reklam kodları, çevrimiçi erişim tokenları, karakteristik buton ID'leri için statik liste.
- Siteye özel CSS selector'ları doğrulamadan tüm sağlayıcılara dayatan zorunlu kurallar.
- Hatalı/boş kaynakları sırf uygulama listeledi diye başarılı kabul eden kontrol adımları.
- Videoda AI tarafından önerilmiş ama gerçek site yanıtıyla doğrulanmamış kod parçaları.

## Kullanıcı kararı

[A] Yalnız yeni DevTools/AJAX referansı ve SKILL yönlendirmesi.
[B] A + HLS kalite kuralındaki çelişkilerin düzeltilmesi. **Önerilen.**
[C] B + ayrıntılı tekrar üretilebilir test matrisi ve `scripts/` altında gelecekte uygulanacak audit checklist (yeni kod yazılmadan önce mevcut betiklerle çapraz kontrol).

Bu branch araştırma branch'idir. Ana `SKILL.md` ve üretim sağlayıcılarına henüz dokunulmadı.
