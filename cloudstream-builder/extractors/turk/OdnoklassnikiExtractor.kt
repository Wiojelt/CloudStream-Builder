// ! Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.
package dev.wiojelt.turksinema.vendor.saloo_belgeselx.com.keyiflerolsun
import android.util.Log
import com.lagradost.cloudstream3.*
import com.lagradost.cloudstream3.utils.*
import com.fasterxml.jackson.annotation.JsonProperty
import com.fasterxml.jackson.core.type.TypeReference
import com.fasterxml.jackson.databind.ObjectMapper

open class Odnoklassniki : ExtractorApi() {
    override val name            = "Odnoklassniki"
    override val mainUrl         = "https://odnoklassniki.ru"
    override val requiresReferer = false

    override suspend fun getUrl(url: String, referer: String?, subtitleCallback: (SubtitleFile) -> Unit, callback: (ExtractorLink) -> Unit) {
        Log.d("Kekik_${this.name}", "url » $url")

        val userAgent = mapOf("User-Agent" to "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36")

        val rawVideoReq = app.get(url, headers=userAgent).text.replace("\\&quot;", "\"").replace("\\\\", "\\")
        val unicodePattern = java.util.regex.Pattern.compile("\\\\u([0-9A-Fa-f]{4})")
        val unicodeMatcher = unicodePattern.matcher(rawVideoReq)
        val decodedBuffer = StringBuffer()
        while (unicodeMatcher.find()) {
            unicodeMatcher.appendReplacement(
                decodedBuffer,
                java.util.regex.Matcher.quoteReplacement(Integer.parseInt(unicodeMatcher.group(1), 16).toChar().toString())
            )
        }
        unicodeMatcher.appendTail(decodedBuffer)
        val videoReq = decodedBuffer.toString()
        val videosStr = Regex(""""videos":(\[[^]]*])""").find(videoReq)?.groupValues?.get(1) ?: throw ErrorLoadingException("Video not found")
        val videos: List<OkRuVideo> = runCatching {
            ObjectMapper().readValue(videosStr, object : TypeReference<List<OkRuVideo>>() {})
        }.getOrElse { throw ErrorLoadingException("Video not found") }

        for (video in videos) {
            Log.d("Kekik_${this.name}", "video » $video")

            val videoUrl  = if (video.url.startsWith("//")) "https:${video.url}" else video.url

            val quality   = video.name.uppercase()
                .replace("MOBILE", "144p")
                .replace("LOWEST", "240p")
                .replace("LOW",    "360p")
                .replace("SD",     "480p")
                .replace("HD",     "720p")
                .replace("FULL",   "1080p")
                .replace("QUAD",   "1440p")
                .replace("ULTRA",  "4k")

            callback.invoke(
                newExtractorLink(
                    source = this.name,
                    name = this.name,
                    url = videoUrl,
                    type = INFER_TYPE
                ) {
                    headers = userAgent
                    this.quality = getQualityFromName(quality)
                }
            )
        }
    }

    data class OkRuVideo(
        @JsonProperty("name") val name: String,
        @JsonProperty("url")  val url: String,
    )
}
