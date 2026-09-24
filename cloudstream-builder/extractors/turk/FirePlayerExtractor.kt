package dev.wiojelt.turksinema.vendor.test_netfilmizle.com.wiojelt.turkstream.netfilmizle
import com.lagradost.cloudstream3.*
import com.lagradost.cloudstream3.utils.*

class FirePlayerExtractor(override val mainUrl: String) : ExtractorApi() {
    override val name = "FirePlayer"
    override val requiresReferer = true

    override suspend fun getUrl(url: String, referer: String?, subtitleCallback: (SubtitleFile) -> Unit, callback: (ExtractorLink) -> Unit) {
        val pageUrl = url.substringBefore('?').trimEnd('/')
        val id = pageUrl.substringAfterLast('/')
        app.get(pageUrl, referer = referer ?: mainUrl)
        val response = app.post(
            "$pageUrl?do=getVideo",
            headers = mapOf("Referer" to pageUrl, "X-Requested-With" to "XMLHttpRequest"),
            data = mapOf("data" to id, "do" to "getVideo"),
        ).text
        val source = Regex(""""videoSrc"\s*:\s*"([^"]+)"""").find(response)?.groupValues?.get(1)?.replace("\\/", "/")
            ?: throw ErrorLoadingException("FirePlayer kaynağı bulunamadı")
        loadExtractor(source, pageUrl, subtitleCallback, callback)
    }
}
