import requests
from bs4 import BeautifulSoup
from pathlib import Path

URL = "https://www.scrapethissite.com/pages/simple/"
OUT_PATH = Path("data/raw_blob.txt")

def extract_blob(url: str = URL) -> str:
    headers = {"User-Agent": "Mozilla/5.0 (compatible; TextExtractor/1.0)"}
    r = requests.get(url, headers=headers, timeout=15)
    r.raise_for_status()

    soup = BeautifulSoup(r.text, "html.parser")
    main = soup.select_one("main") or soup

    # strip boilerplate
    for tag in main.find_all(["script", "style", "nav", "footer", "header", "form", "noscript", "aside"]):
        tag.decompose()

    # intro text
    intro = [el.get_text(" ", strip=True) for el in main.select("h1, h2, p.lead")]

    # country cards
    countries = []
    for card in main.select(".country"):
        name = card.select_one(".country-name")
        capital = card.select_one(".country-capital")
        pop = card.select_one(".country-population")
        area = card.select_one(".country-area")
        line = (
            f"{name.get_text(strip=True)} — "
            f"Capital: {capital.get_text(strip=True)} | "
            f"Population: {pop.get_text(strip=True)} | "
            f"Area: {area.get_text(strip=True)} km²"
        )
        countries.append(line)

    return "\n\n".join(t for t in [*intro, *countries] if t)

blob = extract_blob()

# ensure data/ exists and save
OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
OUT_PATH.write_text(blob, encoding="utf-8")

print(f"Saved {len(blob)} characters to {OUT_PATH.resolve()}")