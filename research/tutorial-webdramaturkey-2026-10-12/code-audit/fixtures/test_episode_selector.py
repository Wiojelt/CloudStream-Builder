"""Illustrative fixture for recorded WebDramaTurkey HTML relation, not live scrape."""
from pathlib import Path
import re
from bs4 import BeautifulSoup
document = BeautifulSoup((Path(__file__).parent / "two_season_episodes.html").read_text(encoding="utf8"), "html.parser")
anchors = document.select("div.episodes a[href]")
assert len(anchors) == 4
result = []
for anchor in anchors:
    group = anchor.find_parent(id=re.compile(r"^season-\d+$"))
    assert group
    season = int(group["id"].split("-")[-1])
    text = anchor.select_one("div.episode").get_text(" ", strip=True)
    number = re.search(r"(?<!\d)(\d+)\s*\.?\s*Bölüm", text, re.I)
    assert number
    episode = int(number.group(1))
    label = anchor.select_one("div.name").get_text(" ", strip=True)
    name = label or f"{episode}. Bölüm"
    result.append((season, episode, name, anchor["href"]))
assert [(s, e) for s, e, *_ in result] == [(1, 1), (1, 2), (2, 1), (2, 7)]
assert result[0][2] == "1. Bölüm"
assert result[1][2] == "Ek Bölüm Adı"
assert len({(s, e) for s, e, *_ in result}) == 4
assert all(path.startswith("/anime/spy-x-family/") for *_, path in result)
assert "1. Bölüm".split(" ")[0] != "1"
print("PASS: verified synthetic two-season episode DOM and text contract")
