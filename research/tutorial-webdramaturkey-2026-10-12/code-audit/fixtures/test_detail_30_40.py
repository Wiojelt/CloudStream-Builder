"""15 offline assertions over anonymized synthetic HTML.
Does not prove live CloudStream playback or actual source-site availability.
Requires beautifulsoup4.
"""
from pathlib import Path
from bs4 import BeautifulSoup
import unittest

P = Path(__file__).parent

def soup(n):
    return BeautifulSoup((P/n).read_text(encoding="utf-8"),"html.parser")

def labeled(root, label):
    for element in root.select("div.video-attr"):
        lab, value = element.select_one(".label"),element.select_one(".value")
        if lab and value and lab.get_text(strip=True).casefold()==label.casefold():
            return value.get_text(" ",strip=True)
    return None

def detail(root):
    t = root.select_one("h1")
    pl = root.select_one("div.text-content")
    yr = root.select_one("div.featured-attr > div:nth-child(2)")
    cover = root.select_one("div.media.media-cover")
    return dict(title=t.get_text(strip=True) if t else None,
        plot=pl.get_text(" ",strip=True) if pl else labeled(root,"Genel Bakış"),
        year=yr.get_text(strip=True) if yr else labeled(root,"Yayın yılı"),
        poster=cover.get("data-src") if cover else None,
        category=[x.get_text(strip=True) for x in root.select("div.categories a")])

class TwoTemplates(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.movie=soup("movie_detail_30_40.html")
        cls.series=soup("series_detail_30_40.html")
        cls.m,cls.s=detail(cls.movie),detail(cls.series)
    def test_01_old_selector_missing_movie(self): self.assertIsNone(self.movie.select_one("div.pl-md-4 h1"))
    def test_02_movie_title(self): self.assertEqual(self.m["title"],"The Match")
    def test_03_series_title(self): self.assertEqual(self.s["title"],"Örnek Dizi")
    def test_04_movie_plot(self): self.assertEqual(self.m["plot"],"Film için gözlenen ayrı açıklama şablonu")
    def test_05_series_plot(self): self.assertEqual(self.s["plot"],"Dizi şablonunda özet buradan geliyor.")
    def test_06_movie_year(self): self.assertEqual(self.m["year"],"2024")
    def test_07_series_year(self): self.assertEqual(self.s["year"],"2025")
    def test_08_movie_poster(self): self.assertTrue(self.m["poster"].endswith("the-match.jpg"))
    def test_09_series_poster(self): self.assertTrue(self.s["poster"].endswith("series.jpg"))
    def test_10_movie_genre(self): self.assertEqual(self.m["category"],["Dram"])
    def test_11_series_genre(self): self.assertEqual(self.s["category"],["Romantik"])
    def test_12_player_shell_not_iframe(self):
        for document in (self.movie,self.series):
            self.assertIsNotNone(document.select_one("#movie-video"))
            self.assertIsNone(document.select_one("#movie-video iframe[src]"))
    def test_13_script_is_not_media(self):
        self.assertEqual(self.movie.select_one("script[src]").get("src"),"/static/player-init.js")
        self.assertIsNone(self.movie.select_one("video[src],source[src],iframe[src]"))
    def test_14_no_fabricated_rating(self): self.assertIsNone(self.movie.select_one(".rating"))
    def test_15_no_playback_evidence(self):
        self.assertFalse(bool(self.movie.select("video[src],source[src],iframe[src],a[href$='.m3u8']")))

if __name__=="__main__":
    unittest.main(verbosity=2)
