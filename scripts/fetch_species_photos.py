"""Freely licensed photos for the species cards of the web app (web/src/components/SpeciesCards.vue).

For every species in the exported palettes (web/public/data/*/meta.json) this takes the lead image of its English
Wikipedia article (or the file in FILE below), keeps it only if Wikimedia Commons states a free licence (CC0, public
domain, CC BY, CC BY-SA; never NC or ND), and saves a 640 px thumbnail with its attribution:
web/public/species/<slug>.jpg + web/public/species/photos.json (author, licence, licence URL, source page).
--candidates "Species A" "Species B": instead, save the free-licence results of a Commons search "<species> tree" as
small thumbnails in web/public/species/_candidates/ (not published), to pick a whole-tree photo for FILE.

Wikimedia is not reachable from the cloud containers; run it on the PC: python scripts/fetch_species_photos.py
"""
import html
import io
import json
import pathlib
import re
import sys
import time

import requests
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "web" / "public" / "species"
UA = {"User-Agent": "shade-and-sponge-thesis/0.1 (https://github.com/giofox96/shade-and-sponge)"}
FREE = re.compile(r"^(cc0|public domain|pd\b|cc[ -]by(-sa)?[ -]?\d|cc[ -]by(-sa)?$)", re.I)
TITLE = {}  # species -> Wikipedia title, when the name does not resolve
FILE = {  # species -> Commons file name, to replace a lead image that is not the whole tree
    'Acer monspessulanum': 'Acer monspessulanum trees, Novi Beograd.jpg',
    'Catalpa bignonioides': 'Trompetenbaum Catalpa bignonioides -20201009-RM-170911.jpg',
    'Celtis australis': 'Bad Dürkheim Kurpark Zürgelbaum 001 2021 10 10.jpg',
    'Citrus × aurantium': 'Turunç - Citrus aurantium 05.JPG',
    'Cupressus sempervirens': "Abbazia di Sant'Andrea (Borzone, Borzonasca) - cipresso 2022-06-09.jpg",
    'Fraxinus angustifolia': 'Fraxinus angustifolia 20190614.jpg',
    'Hibiscus syriacus': 'Hibiscus-syriacus-street-tree.JPG',
    'Koelreuteria paniculata': 'Koelreuteria habitus.jpg',
    'Jacaranda mimosifolia': 'Jacaranda tree (Jacaranda mimosifolia) in bloom, Miguel Bombarda Avenue, Lisbon, Portugal julesvernex2.jpg',
    'Magnolia grandiflora': 'Magnolia grandiflora "Sempreverde".jpg',
    'Prunus cerasifera': '2025.08.13 Prunus cerasifera tree Salihorsk Paŭnočnaja 8.jpg',
    'Robinia pseudoacacia': 'Robinia pseudoacacia - Robinie - Mörfelden-Walldorf - Germany - 01.jpg',
    'Tilia x euchlora': 'Tilia x euchlora 5zz.jpg',
}


def slug(s):
    return re.sub(r"[^a-z0-9]+", "_", s.lower()).strip("_")


def api(url, **params):
    for wait in (2, 5, 15, 30):  # Commons sometimes answers with an error body (rate limit): back off and retry
        r = requests.get(url, params=dict(format="json", formatversion=2, **params), headers=UA, timeout=30)
        r.raise_for_status()
        time.sleep(0.5)
        if "query" in r.json():
            return r.json()
        time.sleep(wait)
    raise RuntimeError(f"{url} {params}: {r.text[:300]}")


def lead_file(species):
    title = TITLE.get(species, re.sub(r" x ", " × ", species))
    q = api("https://en.wikipedia.org/w/api.php", action="query", prop="pageimages", piprop="name",
            titles=title, redirects=1)["query"]["pages"][0]
    return q.get("pageimage"), q.get("title")


def free_info(name, width):
    """Commons imageinfo of a file, or None when the licence is not free (NC, ND, fair use) or the file is not on Commons."""
    info = api("https://commons.wikimedia.org/w/api.php", action="query", prop="imageinfo", titles=f"File:{name}",
               iiprop="url|extmetadata", iiurlwidth=width)["query"]["pages"][0]
    if "imageinfo" not in info:
        return None
    ii = info["imageinfo"][0]
    md = {k: v.get("value") for k, v in ii["extmetadata"].items()}
    lic = plain(md.get("LicenseShortName"))
    if not FREE.match(lic) or re.search(r"\b(nc|nd)\b", lic, re.I):
        return None
    return dict(thumb=ii["thumburl"], page=ii["descriptionurl"], author=plain(md.get("Artist")) or "unknown",
                licence=lic, licence_url=md.get("LicenseUrl"))


def save_jpg(url, path, width):
    im = Image.open(io.BytesIO(requests.get(url, headers=UA, timeout=60).content)).convert("RGB")
    im.thumbnail((width, width * 2))
    im.save(path, quality=80, optimize=True)


def plain(s):
    return html.unescape(re.sub(r"<[^>]+>", "", s or "")).strip()


OUT.mkdir(parents=True, exist_ok=True)
if "--candidates" in sys.argv:
    (OUT / "_candidates").mkdir(exist_ok=True)
    found = {}
    for s in sys.argv[sys.argv.index("--candidates") + 1:]:
        hits = api("https://commons.wikimedia.org/w/api.php", action="query", list="search", srnamespace=6, srlimit=15,
                   srsearch=f"{s} tree")["query"]["search"]
        names = [h["title"].removeprefix("File:") for h in hits if h["title"].lower().endswith((".jpg", ".jpeg"))]
        found[s] = []
        for name in names:
            ii = free_info(name, 330)
            if ii and len(found[s]) < 8:
                save_jpg(ii["thumb"], OUT / "_candidates" / f"{slug(s)}_{len(found[s])}.jpg", 300)
                found[s].append(name)
        print(s, found[s])
    (OUT / "_candidates" / "candidates.json").write_text(json.dumps(found, indent=1, ensure_ascii=False), encoding="utf-8")
    sys.exit()

species = sorted({p["species"] for f in (ROOT / "web/public/data").glob("*/meta.json")
                  for p in json.loads(f.read_text(encoding="utf-8"))["palette"]})
credits, missing = {}, []
for s in species:
    name, page = (FILE[s], None) if s in FILE else lead_file(s)
    if not name:
        missing.append(f"{s}: no lead image")
        continue
    ii = free_info(name, 960)
    if not ii:
        missing.append(f"{s}: {name} not free or not on Commons")
        continue
    f = f"{slug(s)}.jpg"
    save_jpg(ii.pop("thumb"), OUT / f, 640)
    credits[s] = dict(file=f, commons=name, wiki=page, **ii)
    print(f"{s}: {name} ({ii['licence']})")
(OUT / "photos.json").write_text(json.dumps(credits, indent=1, ensure_ascii=False), encoding="utf-8")
print(f"\n{len(credits)}/{len(species)} photos -> {OUT}")
print("\n".join(missing))
