#!/usr/bin/env python3
"""Unit tests for conservative static preflight, Python stdlib only."""
import sys
import tempfile
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from audit_provider_contracts import analyze_source, function_ranges, mask_noncode, scan_paths

def rules(src):
    return {f.rule for f in analyze_source(src, "Provider.kt")}

class VideoLessons(unittest.TestCase):
    def test_hls_generator(self):
        self.assertIn("HLS_SPLIT_REVIEW", rules("M3u8Helper.generateM3u8(n, master, r)"))
    def test_unqualified_hls_generator(self):
        self.assertIn("HLS_SPLIT_REVIEW", rules("generateM3u8(n, master, r)"))
    def test_direct_master_allowed(self):
        self.assertNotIn("HLS_SPLIT_REVIEW", rules('newExtractorLink(name, name, master, type = ExtractorLinkType.M3U8)'))
    def test_comment_ignored(self):
        self.assertEqual(rules('// M3u8Helper.generateM3u8(name, url, ref)'),set())
    def test_string_ignored(self):
        self.assertEqual(rules('val tutorial = "M3u8Helper.generateM3u8(n,u,r)"'),set())
    def test_true_only(self):
        self.assertIn("LOADLINKS_TRUE_WITHOUT_PROOF",rules('override suspend fun loadLinks(data: String): Boolean { return true }'))
    def test_true_after_extractor(self):
        src='override suspend fun loadLinks(data: String): Boolean { loadExtractor(data, ref, subs, cb); return true }'
        self.assertIn("LOADLINKS_TRUE_WITHOUT_PROOF",rules(src))
    def test_callback_count_return(self):
        src='override suspend fun loadLinks(data: String): Boolean { var n=0; loadExtractor(data, ref, subs) { cb(it); n++ }; return n>0 }'
        self.assertNotIn("LOADLINKS_TRUE_WITHOUT_PROOF",rules(src))
    def test_executable_todo(self):
        self.assertIn("LOADLINKS_TODO",rules('override suspend fun loadLinks(x: String): Boolean { TODO("unfinished"); return true }'))
    def test_commented_todo(self):
        self.assertNotIn("LOADLINKS_TODO",rules('override suspend fun loadLinks(x: String): Boolean { // TODO("unfinished")\n return false }'))
    def test_wrong_parent(self):
        self.assertIn("SOURCE_ID_PARENT",rules('document.select("div.nav-player-select").attr("data-embed")'))
    def test_wrong_parent_variable(self):
        src='val playerlar = document.select("div.nav-player-select")\n val id = playerlar.attr("data-embed")'
        self.assertIn("SOURCE_ID_PARENT",rules(src))
    def test_child_correct(self):
        src='document.select("div.nav-player-select button[data-embed]").map { it.attr("data-embed") }'
        self.assertNotIn("SOURCE_ID_PARENT",rules(src))
    def test_null_iframe_string(self):
        self.assertIn("NULL_IFRAME_URL",rules('val src = response.selectFirst("iframe")?.attr("src").toString()'))
    def test_iframe_elvis(self):
        self.assertNotIn("NULL_IFRAME_URL",rules('val src = response.selectFirst("iframe[src]")?.attr("src") ?: return false'))
    def test_page_ignored(self):
        src='override suspend fun getMainPage(page: Int, request: MainPageRequest): HomePageResponse { val doc = app.get(mainUrl).document; return newHomePageResponse(emptyList()) }'
        self.assertIn("HOMEPAGE_IGNORES_PAGE",rules(src))
    def test_page_used(self):
        src='override suspend fun getMainPage(page: Int, request: MainPageRequest): HomePageResponse { val doc = app.get(request.data + "?page=" + page).document; return newHomePageResponse(emptyList()) }'
        self.assertNotIn("HOMEPAGE_IGNORES_PAGE",rules(src))
    def test_nested_code_balancing(self):
        src='override suspend fun loadLinks(x: String): Boolean { val msg="{ }"; if (x.isNotBlank()) { cb(x) }; return false }'
        self.assertEqual(len(function_ranges(mask_noncode(src),"loadLinks")),1)
    def test_scan_directory(self):
        with tempfile.TemporaryDirectory() as t:
            root=Path(t); (root/"src").mkdir()
            (root/"src"/"Bad.kt").write_text("M3u8Helper.generateM3u8(n,u,r)",encoding="utf8")
            (root/"src"/"Ignored.txt").write_text("M3u8Helper.generateM3u8(n,u,r)",encoding="utf8")
            self.assertEqual([f.rule for f in scan_paths([root])],["HLS_SPLIT_REVIEW"])

if __name__=="__main__":
    unittest.main(verbosity=2)
