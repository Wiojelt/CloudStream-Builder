"""Case study from on-screen WebDramaTurkey video: class vs descendant CSS."""
from pathlib import Path
from bs4 import BeautifulSoup

html = (Path(__file__).parent / "lazy_poster_card.html").read_text(encoding="utf-8")
soup = BeautifulSoup(html, "html.parser")
card = soup.select_one("div.col")
assert card is not None
assert card.select_one("a.list-title").get_text(strip=True) == "Örnek Dizi"
assert card.select_one("a.list-title")["href"] == "/diziler/ornek-dizi"
assert card.select_one("div.media media-cover") is None
cover = card.select_one("div.media.media-cover")
assert cover is not None
assert cover["data-src"].endswith("ornek-dizi.jpg")
assert cover.get("src") is None
print("PASS: incorrect descendant selector fails, two-class selector finds lazy cover")
