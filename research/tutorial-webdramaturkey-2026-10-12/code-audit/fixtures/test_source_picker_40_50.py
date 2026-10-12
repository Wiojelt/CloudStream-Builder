"""18 offline synthetic assertions; video 40:00–50:00 DOM problem.
No network calls or real tokens. Requires beautifulsoup4.
"""
from pathlib import Path
from bs4 import BeautifulSoup
import unittest
D = Path(__file__).parent
P = BeautifulSoup((D/"source_picker_40_50.html").read_text(encoding="utf-8"),"html.parser")
A = BeautifulSoup((D/"ajax_embed_response_40_50.html").read_text(encoding="utf-8"),"html.parser")

def sources():
    nodes = P.select(".nav-player-select a[data-embed], .nav-player-select button[data-embed]")
    out,seen=[],set()
    for e in nodes:
        id=e.get("data-embed","").strip()
        if not id or id in seen: continue
        seen.add(id)
        name = e.select_one(".name") or e.select_one("span")
        label = name.get_text(" ",strip=True) if name else ""
        if not label or e.name=="a" and "Kaynak" in label:
            b=P.select_one(f'button[data-embed="{id}"] .name')
            if b: label=b.get_text(" ",strip=True)
        lang=e.select_one(".language") or P.select_one(f'button[data-embed="{id}"] .language')
        out.append((id,label,lang.get_text(" ",strip=True) if lang else None))
    return out

class SourceContract(unittest.TestCase):
    def test_01_div_present(self): self.assertIsNotNone(P.select_one("div.nav-player-select"))
    def test_02_div_no_attribute(self): self.assertIsNone(P.select_one("div.nav-player-select[data-embed]"))
    def test_03_anchor_selected(self): self.assertEqual(P.select_one("a.dropdown-toggle")["data-embed"],"101")
    def test_04_button_selected(self): self.assertEqual(P.select_one("button.selected")["data-embed"],"101")
    def test_05_raw_count(self): self.assertEqual(len(P.select("[data-embed]")),4)
    def test_06_unique_count(self): self.assertEqual(len(sources()),3)
    def test_07_first(self): self.assertEqual(sources()[0][0],"101")
    def test_08_middle(self): self.assertEqual(sources()[1][0],"102")
    def test_09_last(self): self.assertEqual(sources()[-1][0],"103")
    def test_10_labels(self): self.assertEqual([s[1] for s in sources()],["VK","UPN (Reklamlı)","Okru"])
    def test_11_languages(self): self.assertEqual({s[2] for s in sources()},{"Türkçe Altyazı"})
    def test_12_button_count(self): self.assertEqual(len(P.select("button.dropdown-source")),3)
    def test_13_ajax_html(self): self.assertIsNotNone(A.select_one("html"))
    def test_14_ajax_iframe(self): self.assertEqual(A.select_one("iframe[src]")["src"],"https://player.example.invalid/video/101")
    def test_15_no_direct_media(self): self.assertIsNone(A.select_one("video[src],source[src],a[href$='.m3u8']"))
    def test_16_wrong_parent_attr(self): self.assertEqual(P.select_one("div.nav-player-select").get("data-embed",""),"")
    def test_17_keep_selected(self): self.assertIn("101",[s[0] for s in sources()])
    def test_18_no_duplicate(self): self.assertEqual(sum(s[0]=="101" for s in sources()),1)

if __name__=="__main__": unittest.main(verbosity=2)
