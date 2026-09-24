package dev.wiojelt.turksinema.vendor.saloo_filmmakinesi.com.keyiflerolsun

import android.util.Base64
import android.util.Log
import com.lagradost.cloudstream3.SubtitleFile
import com.lagradost.cloudstream3.app
import com.lagradost.cloudstream3.utils.ExtractorApi
import com.lagradost.cloudstream3.utils.ExtractorLink
import com.lagradost.cloudstream3.utils.ExtractorLinkType
import com.lagradost.cloudstream3.utils.Qualities
import com.lagradost.cloudstream3.utils.newExtractorLink

class CloseLoad : ExtractorApi() {
    override val name = "CloseLoad"
    override val mainUrl = "https://closeload.filmmakinesi.to"
    override val requiresReferer = true

    override suspend fun getUrl(
        url: String,
        referer: String?,
        subtitleCallback: (SubtitleFile) -> Unit,
        callback: (ExtractorLink) -> Unit
    ) {
        val userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"
        val headers2 = mapOf(
            "User-Agent" to userAgent,
            "Referer" to "$mainUrl/",
            "Origin" to mainUrl
        )

        try {
            val response = app.get(url, referer = mainUrl, headers = headers2)
            val html = response.text

            val realUrl = decryptNative(html)

            if (!realUrl.isNullOrBlank() && realUrl.startsWith("http")) {
                callback.invoke(
                    newExtractorLink(
                        source = this.name,
                        name = this.name,
                        url = realUrl,
                        type = ExtractorLinkType.M3U8
                    ) {
                        quality = Qualities.P1080.value
                        headers = mapOf(
                            "Referer" to "$mainUrl/",
                            "User-Agent" to userAgent
                        )
                    }
                )
            } else {
                Log.e("Kekik_${this.name}", "CloseLoad URL deşifre edilemedi.")
            }

            processSubtitles(html, subtitleCallback)

        } catch (e: Exception) {
            Log.e("Kekik_${this.name}", "Hata: ${e.message}")
        }
    }

    private fun decryptNative(html: String): String? {
        return try {
            val ahkMatch = Regex("""var\s+[a-zA-Z0-9_]+\s*=\s*["']([a-zA-Z0-9]{15,35})["']""").find(html)
            val uwkdMatch = Regex("""var\s+[a-zA-Z0-9_]+\s*=\s*["']([a-zA-Z]{2,8})["']""").find(html)
            val arrMatch = Regex("""\(\[((?:["'][^"']+["'],?\s*)+)\]\)""").find(html)

            if (ahkMatch == null || uwkdMatch == null || arrMatch == null) {
                Log.w("Kekik_${this.name}", "Regex eşleşmedi: ahk=${ahkMatch != null}, uwkd=${uwkdMatch != null}, arr=${arrMatch != null}")
                return null
            }

            val ahk = ahkMatch.groupValues[1]
            val uwkd = uwkdMatch.groupValues[1]
            val parts = arrMatch.groupValues[1].split(",").map {
                it.trim().replace("\"", "").replace("'", "").replace("\\/", "/")
            }

            var whm = parts.joinToString("")
            var qtvy = 0
            var pcn = 0
            for (i in 0 until ahk.length) {
                val c = ahk[i].code
                qtvy = (qtvy * 31 + c) % 251
                pcn = (pcn xor (c + i)) and 255
            }

            val tqinz = (qtvy + pcn) % 256
            val mwb = (qtvy % 13) + 3
            var cgu = ((qtvy * 256 + pcn) % 65521) + 1

            for (i in uwkd.length - 1 downTo 0) {
                val op = uwkd[i]
                when (op) {
                    'b' -> {
                        val pad = whm.length % 4
                        if (pad != 0) whm += "=".repeat(4 - pad)
                        whm = String(Base64.decode(whm, Base64.NO_WRAP), Charsets.ISO_8859_1)
                    }
                    'v' -> {
                        whm = whm.reversed()
                    }
                    else -> {
                        val qth = (26 - ((op.code - 64) % 26)) % 26
                        val sb = StringBuilder(whm.length)
                        for (ch in whm) {
                            val code = ch.code
                            if (code in 65..90) {
                                sb.append(((code - 65 + qth) % 26 + 65).toChar())
                            } else if (code in 97..122) {
                                sb.append(((code - 97 + qth) % 26 + 97).toChar())
                            } else {
                                sb.append(ch)
                            }
                        }
                        whm = sb.toString()
                    }
                }
            }

            val y1su9 = whm.length
            val uo75 = IntArray(y1su9)
            for (i in y1su9 - 1 downTo 1) {
                cgu = (cgu * 75 + 74) % 65537
                uo75[i] = cgu % (i + 1)
            }

            val a44f = whm.toCharArray()
            for (i in 1 until y1su9) {
                val canf = uo75[i]
                val mkuhn = a44f[i]
                a44f[i] = a44f[canf]
                a44f[canf] = mkuhn
            }
            whm = String(a44f)

            var nfn = tqinz
            val u32d8 = StringBuilder(whm.length)
            for (i in 0 until whm.length) {
                val e1b1j = whm[i].code
                nfn = (nfn + mwb) % 256
                u32d8.append((e1b1j xor nfn).toChar())
                nfn = (nfn + e1b1j) % 256
            }

            val decoded = u32d8.toString()
            Log.d("Kekik_${this.name}", "Decoded URL: $decoded")
            decoded
        } catch (e: Exception) {
            Log.e("Kekik_${this.name}", "Deşifre hatası: ${e.message}")
            null
        }
    }

    private fun processSubtitles(html: String, subtitleCallback: (SubtitleFile) -> Unit) {
        try {
            val tracksMatch = """tracks\s*:\s*(\[.*?\])""".toRegex(RegexOption.DOT_MATCHES_ALL).find(html)
            tracksMatch?.groupValues?.get(1)?.let { tracksJson ->
                val trackPattern = """\{[^}]*\}""".toRegex()
                val fileRegex = """"file"\s*:\s*"([^"]+)"""".toRegex()
                val labelRegex = """"label"\s*:\s*"([^"]+)"""".toRegex()

                trackPattern.findAll(tracksJson).forEach { match ->
                    val block = match.value
                    val file = fileRegex.find(block)?.groupValues?.get(1)?.replace("\\/", "/")
                    val label = labelRegex.find(block)?.groupValues?.get(1) ?: "Altyazı"

                    if (!file.isNullOrBlank() && file.startsWith("http")) {
                        subtitleCallback.invoke(SubtitleFile(label, file))
                    }
                }
            }
        } catch (e: Exception) {
            Log.e("Kekik_${this.name}", "Altyazı hatası: ${e.message}")
        }
    }
}
