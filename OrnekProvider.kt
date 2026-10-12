package com.ornek

import com.lagradost.cloudstream3.*
import com.lagradost.cloudstream3.utils.*
import org.jsoup.nodes.Document

class OrnekProvider : MainAPI() {
    override var mainUrl = "https://www.ddizi.im/"
    override var name = "Örnek Site"
    override val hasMainPage = true
    override var lang = "tr"
    override val supportedTypes = setOf(
        TvType.Movie,
        TvType.TvSeries
    )

    // Ana sayfa kategorileri ve içerik çekimi
    override suspend fun getMainPage(page: Int, request: MainPageRequest): HomePageResponse {
        val document = app.get(mainUrl).document
        val items = mutableListOf<HomePageList>()

        // Örnek selector: Site HTML yapısına göre güncellenmelidir
        val latestMovies = document.select("div.movie-item").mapNotNull {
            it.toSearchResult()
        }

        if (latestMovies.isNotEmpty()) {
            items.add(HomePageList("Son Eklenenler", latestMovies))
        }

        return newHomePageResponse(items)
    }

    private fun org.jsoup.nodes.Element.toSearchResult(): SearchResponse? {
        val title = this.selectFirst("h2.title")?.text() ?: return null
        val href = fixUrl(this.selectFirst("a")?.attr("href") ?: return null)
        val posterUrl = fixUrlNull(this.selectFirst("img")?.attr("src"))

        return newMovieSearchResponse(title, href, TvType.Movie) {
            this.posterUrl = posterUrl
        }
    }

    // Arama fonksiyonu
    override suspend fun search(query: String): List<SearchResponse> {
        val searchUrl = "$mainUrl/?s=$query"
        val document = app.get(searchUrl).document

        return document.select("div.search-result-item").mapNotNull {
            it.toSearchResult()
        }
    }

    // Film / Dizi detay sayfası
    override suspend fun load(url: String): LoadResponse {
        val document = app.get(url).document
        val title = document.selectFirst("h1.entry-title")?.text()?.trim() ?: "Bilinmeyen Başlık"
        val poster = fixUrlNull(document.selectFirst("div.poster img")?.attr("src"))
        val plot = document.selectFirst("div.description")?.text()?.trim()

        // Tür belirleme (Film mi Dizi mi)
        val isTvSeries = document.select("div.seasons-wrapper").isNotEmpty()

        return if (isTvSeries) {
            val episodes = mutableListOf<Episode>()
            document.select("div.episode-item").forEach { ep ->
                val epHref = fixUrl(ep.selectFirst("a")?.attr("href") ?: return@forEach)
                val epName = ep.selectFirst(".ep-name")?.text() ?: "Bölüm"
                val seasonNum = ep.attr("data-season").toIntOrNull() ?: 1
                val epNum = ep.attr("data-episode").toIntOrNull() ?: 1

                episodes.add(
                    newEpisode(epHref) {
                        this.name = epName
                        this.season = seasonNum
                        this.episode = epNum
                    }
                )
            }

            newTvSeriesLoadResponse(title, url, TvType.TvSeries, episodes) {
                this.posterUrl = poster
                this.plot = plot
            }
        } else {
            newMovieLoadResponse(title, url, TvType.Movie, url) {
                this.posterUrl = poster
                this.plot = plot
            }
        }
    }

    // Oynatıcı video bağlantılarını ayıklama (Extractors)
    override suspend fun loadLinks(
        data: String,
        isCasting: Boolean,
        subtitleCallback: (SubtitleFile) -> Unit,
        callback: (ExtractorLink) -> Unit
    ): Boolean {
        val document = app.get(data).document

        // Sayfa içindeki iframe veya embed kaynaklarını tara
        document.select("iframe").forEach { iframe ->
            val iframeUrl = fixUrl(iframe.attr("src"))
            // Desteklenen hazır extractor'lara yönlendir (m3u8, Rapidstream, Vidmoly vb.)
            loadExtractor(iframeUrl, data, subtitleCallback, callback)
        }

        return true
    }
}
