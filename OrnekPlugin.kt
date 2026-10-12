package com.ornek

import com.lagradost.cloudstream3.plugins.CloudstreamPlugin
import com.lagradost.cloudstream3.plugins.Plugin
import android.content.Context

@CloudstreamPlugin
class OrnekPlugin: Plugin() {
    override fun load(context: Context) {
        // Provider'ı Cloudstream eklenti sistemine kaydet
        registerMainAPI(OrnekProvider())
    }
}