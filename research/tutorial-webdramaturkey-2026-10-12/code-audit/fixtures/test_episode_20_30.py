"""Offline, synthetic DOM test based on video's 20:00–30:00 coding example."""
from pathlib import Path
from urllib.parse import urljoin, urlsplit
import re
import unittest
from bs4 import BeautifulSoup

HTML = BeautifulSoup(Path(__file__).with_name("episodes_20_30.html").read_text(encoding="utf-8"), "html.parser")
BASE = "https://example.invalid/"

def season_from_url(url):
    for part in urlsplit(url).path.strip("/").split("/"):
        m = re.fullmatch(r"(\d+)-sezon", part, flags=re.I)
        if m:
            return int(m.group(1))
    return None

def number_from_label(label):
    m = re.fullmatch(r"\s*(\d+)\s*\.?\s*Bölüm\s*", label, flags=re.I)
    return int(m.group(1)) if m else None

def parse(section):
    results = []
    for a in section.select(".episodes a[href]"):
        url = urljoin(BASE, a["href"])
        e = a.select_one("div.episode")
        n = number_from_label(e.get_text(" ",strip=True)) if e else None
        s = season_from_url(url)
        if n is None or s is None:
            continue
        t = a.select_one("div.name")
        title = t.get_text(" ",strip=True) if t else ""
        results.append((s,n,title or f"{n}. Bölüm",url))
    return results

def classify_empty(section):
    if parse(section):
        return "episodes_present"
    status = section.select_one(".status")
    if status and status.get_text(" ",strip=True).lower() == "çok yakında":
        return "coming_soon_explicit"
    return "empty_unclassified"

class EpisodeContract(unittest.TestCase):
    def setUp(self):
        self.rows = parse(HTML.select_one('[data-media="drama"]'))
    def test_four_links(self): self.assertEqual(len(self.rows),4)
    def test_two_seasons(self): self.assertEqual({r[0] for r in self.rows},{1,2})
    def test_repeated_first_number(self): self.assertEqual(sum(r[1]==1 for r in self.rows),2)
    def test_unique_season_episode(self): self.assertEqual(len({(r[0],r[1]) for r in self.rows}),4)
    def test_absolute_urls(self): self.assertTrue(all(r[3].startswith(BASE) for r in self.rows))
    def test_fallback_title(self): self.assertEqual(self.rows[0][2],"1. Bölüm")
    def test_real_title(self): self.assertEqual(self.rows[1][2],"İlk Adım")
    def test_parse_3_sezon(self): self.assertEqual(season_from_url(BASE+"dizi/a/3-sezon/12-bolum"),3)
    def test_no_fake_sezon(self): self.assertIsNone(season_from_url(BASE+"dizi/a/sezon-3/12-bolum"))
    def test_num_dot(self): self.assertEqual(number_from_label("1. Bölüm"),1)
    def test_num_no_dot(self): self.assertEqual(number_from_label("10 Bölüm"),10)
    def test_reject_draft(self): self.assertIsNone(number_from_label("Yeni bölüm yakında"))
    def test_fragile_split(self): self.assertEqual("1. Bölüm".split(" ")[0],"1.")
    def test_coming_soon_evidence(self): self.assertEqual(classify_empty(HTML.select_one('[data-media="coming-soon"]')),"coming_soon_explicit")
    def test_unknown_empty_not_coming(self): self.assertEqual(classify_empty(HTML.select_one('[data-media="empty-unknown"]')),"empty_unclassified")
    def test_playback_not_implied(self): self.assertEqual(classify_empty(HTML.select_one('[data-media="drama"]')),"episodes_present")

if __name__ == "__main__": unittest.main(verbosity=2)
