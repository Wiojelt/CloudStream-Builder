"""Source-shape regression tests for two additional HLS host paths.

These checks do not access the network or replace Kotlin/CloudStream playback tests.
"""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1] / "extractors" / "turk"
MEGA = (ROOT / "Extractors.kt").read_text(encoding="utf-8")
CINE = (ROOT / "CineStreamExtractors.kt").read_text(encoding="utf-8")


class AdditionalMasterContracts(unittest.TestCase):
    def test_megaplay_never_expands_master(self):
        part = MEGA.split("val m3u8 = root.sources?.file", 1)[1].split("root.tracks.forEach", 1)[0]
        self.assertNotIn("generateM3u8(", part)
        self.assertIn("newExtractorLink(serverName, serverName, m3u8, ExtractorLinkType.M3U8)", part)

    def test_megaplay_keeps_required_headers(self):
        part = MEGA.split("val m3u8 = root.sources?.file", 1)[1].split("root.tracks.forEach", 1)[0]
        self.assertIn("this.headers = playbackHeaders", part)
        self.assertIn('this.referer = "$host/"', part)

    def test_hexa_one_master_source_per_server(self):
        part = CINE.split("suspend fun invokeHexa(", 1)[1].split("suspend fun invokeVidlink(", 1)[0]
        self.assertNotIn("generateM3u8(", part)
        self.assertIn("ExtractorLinkType.M3U8", part)
        self.assertIn("server.capitalizeServer()", part)

    def test_hexa_keeps_referer_and_skips_missing(self):
        part = CINE.split("suspend fun invokeHexa(", 1)[1].split("suspend fun invokeVidlink(", 1)[0]
        self.assertIn('this.referer = "https://hexa.su/"', part)
        self.assertIn("if (m3u8.isBlank()) continue", part)


if __name__ == "__main__":
    unittest.main(verbosity=2)
