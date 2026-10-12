"""24 offline tests for the tutorial's source IDs, AJAX HTML, nested iframe and HLS invariants.
No real HTTP, credentials, DRM, or playback check; requires beautifulsoup4.
"""
from bs4 import BeautifulSoup
from pathlib import Path
from urllib.parse import urljoin, urlparse, urlencode
from collections import OrderedDict
import unittest

D=Path(__file__).parent
BASE="https://site.example.invalid"
def soup(n): return BeautifulSoup((D/n).read_text(encoding="utf-8"),"html.parser")
def safe_url(raw,base):
    if not raw or not raw.strip() or raw.strip().lower()=="null": return None
    u=urljoin(base,raw.strip());p=urlparse(u)
    if p.scheme not in ("http","https") or not p.netloc: return None
    return u
def iframe_target(html,base):
    tag=html.select_one("iframe[src]")
    return safe_url(tag.get("src") if tag else None,base)
def picker():
    found=OrderedDict()
    for el in soup("source_choice_50_60.html").select(".nav-player-select [data-embed]"):
        key=el["data-embed"].strip()
        if not key: continue
        host=el.get("data-host") or el.get_text(" ",strip=True)
        language=el.get("data-lang") or "unknown"
        if key not in found: found[key]={"id":key,"host":host,"lang":language}
        elif found[key]["lang"]=="unknown" and language!="unknown": found[key]["lang"]=language
    return list(found.values())
def one_master(items):
    return [x["url"] for x in items if x["kind"]=="hls-master"][:1]

class OfflineContract(unittest.TestCase):
    def test_01(self): self.assertEqual(len(picker()),3)
    def test_02(self): self.assertEqual(picker()[0]["id"],"101")
    def test_03(self): self.assertEqual(picker()[-1]["id"],"103")
    def test_04(self): self.assertEqual(len(set(x["id"] for x in picker())),3)
    def test_05(self): self.assertNotIn("",[x["id"] for x in picker()])
    def test_06(self): self.assertEqual(picker()[0]["lang"],"tr")
    def test_07(self): self.assertEqual(picker()[1]["lang"],"en")
    def test_08(self): self.assertEqual(picker()[2]["host"],"Host C")
    def test_09(self): self.assertEqual(urlencode({"id":"101"}),"id=101")
    def test_10(self): self.assertIn("x%2By",urlencode({"id":"x+y"}))
    def test_11(self): self.assertEqual(iframe_target(soup("ajax_a_50_60.html"),BASE+"/watch"),BASE+"/player/a?opaque=REDACTED")
    def test_12(self): self.assertIsNone(iframe_target(soup("ajax_empty_50_60.html"),BASE))
    def test_13(self): self.assertEqual(safe_url("../x",BASE+"/path/page"),BASE+"/x")
    def test_14(self): self.assertEqual(iframe_target(soup("nested_a_50_60.html"),BASE+"/player/a"),"https://media.example.invalid/embed/abc")
    def test_15(self): self.assertIsNone(iframe_target(soup("nested_bad_50_60.html"),BASE))
    def test_16(self): self.assertIsNone(safe_url("",BASE))
    def test_17(self): self.assertIsNone(safe_url("null",BASE))
    def test_18(self): self.assertIsNone(soup("ajax_a_50_60.html").select_one("video[src],source[src]"))
    def test_19(self): self.assertIsNone(iframe_target(soup("host_error_50_60.html"),BASE))
    def test_20(self): self.assertIsNone(safe_url("data:text/html,test",BASE))
    def test_21(self): self.assertIsNone(safe_url("file:///etc/passwd",BASE))
    def test_22(self): self.assertEqual(one_master([{"kind":"hls-master","url":BASE+"/m.m3u8"},{"kind":"variant","url":BASE+"/720.m3u8"}]),[BASE+"/m.m3u8"])
    def test_23(self): self.assertEqual(one_master([{"kind":"mp4","url":BASE+"/x.mp4"}]),[])
    def test_24(self): self.assertFalse(bool(soup("nested_a_50_60.html").select("video[src],source[src]")))

if __name__=="__main__": unittest.main(verbosity=2)
