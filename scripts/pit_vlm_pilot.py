"""Pilot: measure real tree-pit (escocell) size in Porta from Mapillary street photos with a local VLM (Ollama).

Why: no open source gives pit size per tree; the repo only has the 2011 guide minimum (pit_min_m2 in
databases/barcelona/porta_sidewalk_width.csv). This pilot tests whether street photos can do better, on ~50 trees.
Scale trick: Barcelona sidewalks are paved with 20 x 20 cm "panot" tiles, so the model counts tiles along each pit
side instead of guessing metres (ASSUMPTION: the paving around the pit is standard 20 cm panot; the model reports it).

Run on the OMEN (the cloud cannot reach Mapillary). Needs:
  - env var MAPILLARY_TOKEN (client token "MLY|...", never written to any file)
  - Ollama running with a vision model, e.g. `ollama pull qwen2.5vl:7b`
Steps (each writes to databases/barcelona/raw/mapillary/, gitignored; Mapillary images are CC BY-SA 4.0):
  python scripts/pit_vlm_pilot.py coverage          # photos near each Porta tree -> coverage.csv, counts by year
  python scripts/pit_vlm_pilot.py download [N=50]   # best photo per sampled tree, cropped toward the tree
  python scripts/pit_vlm_pilot.py vlm [model]       # ask the model; -> pit_vlm_pilot.csv
"""
import base64, io, json, math, os, pathlib, sys, time
import numpy as np, pandas as pd, requests
from pyproj import Transformer

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "databases/barcelona/raw/mapillary"
API = "https://graph.mapillary.com/images"
FIELDS = "id,computed_geometry,captured_at,compass_angle,is_pano,thumb_2048_url"
NEAR_M = 10.0        # ASSUMPTION: a photo within 10 m can show the pit
FACING_DEG = 60.0    # ASSUMPTION: for non-panoramic photos the tree must be within ±60° of the camera heading
CELL_DEG = 0.002     # bbox cell for API queries (~170 x 220 m)
TO_LL = Transformer.from_crs(25831, 4326, always_xy=True)
TO_XY = Transformer.from_crs(4326, 25831, always_xy=True)

PROMPT = """This street photo was cropped toward one street tree in Barcelona. Look at the tree pit (the opening in the
pavement around the trunk of the tree closest to the centre of the image).
Barcelona sidewalks use square paving tiles of 20 x 20 cm. Count how many tiles fit along each side of the pit opening.
Answer ONLY with JSON: {"pit_visible": true/false, "shape": "square|rectangle|circle|continuous|grate|none",
"tiles_side_a": number or null, "tiles_side_b": number or null, "paving_is_20cm_tiles": true/false,
"confidence": "low|medium|high", "note": "max 15 words"}"""


def trees():
    t = pd.read_csv(ROOT / "exchange/to_gh/porta_trees_lidar.csv")
    o = json.loads((ROOT / "exchange/site_origin.json").read_text())
    t["X"], t["Y"] = t.x + o["origin_x"], t.y + o["origin_y"]
    w = pd.read_csv(ROOT / "databases/barcelona/porta_sidewalk_width.csv")[["tree_id", "size_class", "pit_min_m2", "pit_basis"]]
    return t[["tree_id", "species", "street", "X", "Y"]].merge(w, on="tree_id")


def token():
    tk = os.environ.get("MAPILLARY_TOKEN")
    if not tk:
        sys.exit("set MAPILLARY_TOKEN first (setx MAPILLARY_TOKEN \"MLY|...\", then reopen the terminal)")
    return tk


def coverage():
    t, tk = trees(), token()
    lon, lat = TO_LL.transform(t.X.values, t.Y.values)
    rows = []
    for a in np.arange(lon.min() - 1e-4, lon.max() + 1e-4, CELL_DEG):
        for b in np.arange(lat.min() - 1e-4, lat.max() + 1e-4, CELL_DEG):
            r = requests.get(API, params=dict(access_token=tk, fields=FIELDS, limit=2000,
                                              bbox=f"{a},{b},{a + CELL_DEG},{b + CELL_DEG}"), timeout=60)
            r.raise_for_status()
            rows += r.json().get("data", [])
            time.sleep(0.2)
    im = pd.DataFrame(rows).drop_duplicates("id")
    if im.empty:
        sys.exit("no Mapillary images in Porta")
    im["lon"] = im.computed_geometry.map(lambda g: g["coordinates"][0])
    im["lat"] = im.computed_geometry.map(lambda g: g["coordinates"][1])
    im["IX"], im["IY"] = TO_XY.transform(im.lon.values, im.lat.values)
    im["year"] = pd.to_datetime(im.captured_at, unit="ms").dt.year
    out = []
    for tr in t.itertuples():
        d = np.hypot(im.IX - tr.X, im.IY - tr.Y)
        near = im[d <= NEAR_M].assign(dist=d[d <= NEAR_M])
        brg = np.degrees(np.arctan2(tr.X - near.IX, tr.Y - near.IY)) % 360      # camera -> tree, from north
        off = ((brg - near.compass_angle.fillna(0) + 180) % 360) - 180
        ok = near[near.is_pano.fillna(False) | (off.abs() <= FACING_DEG)].assign(offset=off)
        if len(ok):
            best = ok.sort_values(["year", "dist"], ascending=[False, True]).iloc[0]
            out.append(dict(tree_id=tr.tree_id, n_photos=len(ok), image_id=best.id, year=best.year, dist_m=round(best.dist, 1),
                            offset_deg=round(best.offset, 1), is_pano=bool(best.is_pano)))
    c = t.merge(pd.DataFrame(out, columns=["tree_id", "n_photos", "image_id", "year", "dist_m", "offset_deg", "is_pano"]),
                on="tree_id", how="left")
    OUT.mkdir(parents=True, exist_ok=True)
    c.to_csv(OUT / "coverage.csv", index=False)
    print(f"{len(im)} images in Porta; {c.image_id.notna().sum()} of {len(c)} trees have a usable photo")
    print("best photo year:", c.year.dropna().astype(int).value_counts().sort_index().to_dict())


def download(n=50):
    tk = token()
    c = pd.read_csv(OUT / "coverage.csv").dropna(subset=["image_id"])
    s = c.groupby("pit_basis", group_keys=False).apply(lambda g: g.sample(min(len(g), n // 2), random_state=0))
    from PIL import Image
    (OUT / "img").mkdir(parents=True, exist_ok=True)
    for r in s.itertuples():
        f = OUT / "img" / f"{r.tree_id}.jpg"
        if f.exists():
            continue
        meta = requests.get(f"https://graph.mapillary.com/{int(r.image_id)}",
                            params=dict(access_token=tk, fields="thumb_2048_url"), timeout=60).json()
        im = Image.open(io.BytesIO(requests.get(meta["thumb_2048_url"], timeout=120).content)).convert("RGB")
        if r.is_pano:   # equirectangular, image centre = compass_angle (ASSUMPTION): keep a 90° sector centred on the tree
            W, H = im.size
            cx = (0.5 + r.offset_deg / 360.0) * W
            im = Image.fromarray(np.roll(np.asarray(im), int(W / 2 - cx), axis=1)).crop((3 * W // 8, H // 4, 5 * W // 8, 3 * H // 4))
        im.save(f, quality=92)
    s.to_csv(OUT / "sample.csv", index=False)
    print(f"{len(s)} trees sampled; images in {OUT / 'img'}")


def vlm(model="qwen2.5vl:7b"):
    s = pd.read_csv(OUT / "sample.csv")
    out = []
    for r in s.itertuples():
        img = base64.b64encode((OUT / "img" / f"{r.tree_id}.jpg").read_bytes()).decode()
        resp = requests.post("http://localhost:11434/api/generate", timeout=600, json=dict(
            model=model, prompt=PROMPT, images=[img], stream=False, format="json", options=dict(temperature=0)))
        try:
            a = json.loads(resp.json()["response"])
        except (KeyError, ValueError):
            a = {"note": "unparsed"}
        ta, tb = a.get("tiles_side_a"), a.get("tiles_side_b")
        m2 = round(ta * 0.2 * tb * 0.2, 2) if isinstance(ta, (int, float)) and isinstance(tb, (int, float)) else None
        out.append(dict(tree_id=r.tree_id, pit_min_m2=r.pit_min_m2, pit_basis=r.pit_basis, year=r.year, pit_vlm_m2=m2, **a))
        print(r.tree_id, a)
    pd.DataFrame(out).to_csv(OUT / "pit_vlm_pilot.csv", index=False)


if __name__ == "__main__":
    step = sys.argv[1] if len(sys.argv) > 1 else ""
    if step == "coverage":
        coverage()
    elif step == "download":
        download(int(sys.argv[2]) if len(sys.argv) > 2 else 50)
    elif step == "vlm":
        vlm(*sys.argv[2:3])
    else:
        sys.exit(__doc__)
