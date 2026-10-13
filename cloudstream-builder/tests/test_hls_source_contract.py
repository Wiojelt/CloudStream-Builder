"""Code-shape regression for host examples changed to preserve HLS masters.

This checks Kotlin source text only; it is NOT a media playlist or device test.
"""
import unittest
from pathlib import Path

EXTRACTORS = (
    Path(__file__).resolve().parents[1] / "extractors" / "turk" / "Extractors.kt"
)
SOURCE = EXTRACTORS.read_text(encoding="utf-8")


def class_body(start: str, following: str) -> str:
    return SOURCE.split(start, 1)[1].split(following, 1)[0]


class HlsSourceContract(unittest.TestCase):
    def test_supervideo_emits_single_m3u8_callback(self):
        block = class_body("open class SuperVideo :", "class Kwik :")
        self.assertNotIn("generateM3u8(", block)
        self.assertIn("newExtractorLink(name, name, m3u8, ExtractorLinkType.M3U8)", block)

    def test_supervideo_ignores_blank_link(self):
        block = class_body("open class SuperVideo :", "class Kwik :")
        self.assertIn("if (m3u8.isBlank()) return", block)

    def test_supervideo_keeps_referer(self):
        block = class_body("open class SuperVideo :", "class Kwik :")
        self.assertIn('this.referer = "$mainUrl/"', block)

    def test_akamaicdn_preserves_master_url(self):
        block = class_body("class Akamaicdn :", "class Cloudorchestranova :")
        self.assertNotIn("generateM3u8(", block)
        self.assertIn("newExtractorLink(name, name, m3u8, ExtractorLinkType.M3U8)", block)
        self.assertIn("/master.txt?s=1", block)

    def test_akamaicdn_preserves_headers(self):
        block = class_body("class Akamaicdn :", "class Cloudorchestranova :")
        self.assertIn("this.headers = headers", block)
        self.assertIn("this.referer = mainUrl", block)


if __name__ == "__main__":
    unittest.main(verbosity=2)
