# Sidewalk width at each tree position: how to extract it (plan, 21 Oct 2026)

**Why it is needed.** v6 turns the 2011 sizing rule into a constraint: the sidewalk width at a position sets the tree size class planted there (`notes/topic_decision.md` §9.7). The rule (2011 guide pp. 22–23):

| Sidewalk width | Tree size class (one per sidewalk type) |
|---|---|
| < 2.5 m | none |
| < 3.5 m | small |
| 3.5–6 m | medium |
| > 6 m | large |

The city inventory (`arbrat_viari.csv`) has **no sidewalk-width field**. Its columns were checked on 21 Oct: `categoria_arbrat` is a trunk-size class, not a street class.

## Sources found (21 Oct)

| Source | What it has | Format, licence | Use |
|---|---|---|---|
| **Mapa base topogràfic 1:1000** (Ajuntament, open data `mapa-base-topografic`, modified 8 Apr 2025) | City-wide vector topography. WMS layer names include *Línies construccions façanes* (façade lines) and *Línies comunicacions* (road lines, where the kerbs should be) | `MTM_GPKG.zip`, **652 MB**, GeoPackage, **CC BY 4.0**, from CartoBCN (`https://w20.bcn.cat/CartoBCN/getFile.ashx?prod=131.BARCELONA.42`) | **Primary.** Width = kerb-to-façade distance at each tree |
| Mapa base de vialitat (open data `mapa-base-de-vialitat`) | WMS only. Its description lists block façade, park, pavement and road-separator contours | WMS image, CC BY 4.0 | Visual check only; its description suggests the topographic layers hold kerbs |
| ICGC LiDAR 2021 (already in the repo) | Building points (class 6) and ground points (a kerb step; its height in Porta is an `ASSUMPTION` to measure) | LAZ, CC BY 4.0 | Fallback and cross-check |
| OSM | Some sidewalks as separate ways; `width` tags are rare | ODbL | Not recommended |
| Parcs i Jardins | May hold widths internally | — | Asked in `notes/email_parcs_i_jardins.md`, question 5 |

## Method (primary)

1. **Download and clip.** Download `MTM_GPKG.zip` once (652 MB, **needs your OK**) to `databases/barcelona/raw/` (gitignored). Clip to Porta + 30 m.
2. **Find the right features.** Read the feature codes in *Línies comunicacions* to isolate the **kerb lines** (*vorada*), and take the **façade lines** as they are. Expect to map a few code values once by hand, on one street, against the WMS image.
3. **Measure each tree.**
   - Snap the tree to the nearest kerb segment and take that segment's normal.
   - Cast a ray from the kerb, through the tree, away from the carriageway.
   - Width = distance from the kerb to the first façade line the ray hits.
   - Cap the ray at 30 m. If it hits no façade, flag the tree as an "open side" (square, median, park edge).
4. **Assign the class.** Turn each width into the guide's size class, using the table above. The guide gives one class per sidewalk type; allowing smaller classes on wider sidewalks would be an `ASSUMPTION`, to be run as a variant.
5. **Handle the special cases.**
   - Trees on medians or boulevards, and trees with no façade within 30 m, get the class "large, check by hand".
   - Planes on large avenues are kept by the city (§9.7.2), but whether Av. Meridiana counts is open (email question 2).
6. **Quality check.**
   - Measure 20 random trees by hand on the 1:1000 WMS: target agreement ±0.3 m.
   - Compare the façade distance with LiDAR building points.
   - Report the share of trees in each class.

**Output:** `databases/barcelona/porta_sidewalk_width.csv` (tree_id, width_m, method, flag, size_class). The tool then reads `size_class` as a per-position filter on the palette.

## Risks

- **Kerb codes.** If *Línies comunicacions* mixes kerbs with other road lines under one code, step 2 needs a geometric rule (for example, the line parallel to the façade and closest to the tree).
- **Legacy trees.** Many existing planes may stand on sidewalks narrower than the rule allows for their size. That is a result to report (the rule forces downsizing), not an error.
- **Few options per position.** If most positions allow only one or two species, the optimisation shrinks (`notes/topic_decision.md` §9.8). Count this first.

## Result v1 (21 Oct): done through the WMS, not the GeoPackage

The 652 MB download failed twice from the script and once in the user's browser. The server resets the connection halfway and does not support resuming. **So the same map was read through its WMS as SVG vectors, in 250 m tiles.** This is the same source and the same licence (CC BY 4.0), with exact line coordinates (0.1 m per SVG unit).
- **Script:** `scripts/porta_sidewalk_width.py` → `databases/barcelona/porta_sidewalk_width.csv`.
- **Raw tiles:** cached in `databases/barcelona/raw/topo_1000/svg/` (gitignored).

**How each tree is measured.** From the nearest façade line, a ray runs through the tree to the first long road line (≥ 4 m). Three cases follow:
- **ok:** the ray reaches a kerb with no road line in between. Width = façade-to-kerb distance.
- **median:** the ray crosses a road line *before* the tree. The tree stands on a median or across a carriageway, so the façade does not bound its sidewalk.
- **no_facade / no_kerb:** no façade within 30 m, or no kerb beyond the tree.

Tree points may sit up to 1 m past the kerb line (they mark the pit), so that is the tolerance. It is an `ASSUMPTION`.

| Flag | All 2,825 trees | 832 planes |
|---|---|---|
| ok | 1,545 | 400 |
| median | 569 | 206 |
| no_facade | 571 | 196 (160 on Av. Meridiana) |
| no_kerb | 140 | 30 |

**Size class of the 400 measured planes** (2011 guide, one class per sidewalk type):

| Size class | Planes |
|---|---|
| large (> 6 m) | 259 |
| medium (3.5–6 m) | 126 |
| small (< 3.5 m) | 14 |
| none (< 2.5 m) | 1 |

Widths of all ok trees: median 6.65 m, interquartile range 4.76–10.03 m.

**What the numbers mean.**
- **Few narrow streets.** Under the literal rule (narrow sidewalk → small → *Pyrus* only), only 15 plane positions face a one-species choice.
- **Most measured positions are open.** 259 of the 400 measured planes would take the large group (Celtis, Tipuana, Jacaranda), and 126 the medium group (Melia, *Styphnolobium*, Brachychiton).
- **The optimisation is not reduced to nothing.** The risk in `notes/topic_decision.md` §9.8 is smaller than feared, at least for the measured half.

**Checked by eye, not by a formal sample.** Six 80–100 m windows (Malgrat, Valldemossa, Lluc, Rio de Janeiro ×2, Andreu Nin) were plotted with the lines, rays and widths; two are saved:
- `notes/figures/sidewalk_width_qa_lluc.png`;
- `notes/figures/sidewalk_width_qa_rio_de_janeiro.png`.

On ordinary streets the widths match the map (Malgrat ≈ 2.4 m, Lluc ≈ 3.3–3.5 m). Widths over 15 m are real wide pedestrian areas facing a plaza; for the rule they only mean "large". The ±0.3 m 20-tree check of the plan above was **not** done.

**Still open.**
- **The 432 plane positions flagged median, no_facade or no_kerb** (194 of them on Av. Meridiana) need a kerb-to-kerb width for medians, or a rule. Medians and boulevards are likely "large" (to check).
- **Whether the city keeps the Meridiana planes at all** is open (§9.7.2; email question 2).
