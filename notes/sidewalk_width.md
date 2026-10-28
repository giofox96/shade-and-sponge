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

**Checked by eye first (21 Oct).** Six 80–100 m windows (Malgrat, Valldemossa, Lluc, Rio de Janeiro ×2, Andreu Nin) were plotted with the lines, rays and widths; two are saved:
- `notes/figures/sidewalk_width_qa_lluc.png`;
- `notes/figures/sidewalk_width_qa_rio_de_janeiro.png`.

Widths over 15 m are real wide pedestrian areas facing a plaza; for the rule they only mean "large".

## QA and fact-check (21 Oct, second session)

**Reproducibility.** Re-running `scripts/porta_sidewalk_width.py` on the cached tiles gives the committed CSV exactly (every column, every row). All the counts above match it.

**Corrections from the fact-check.**
- **Malgrat is ≈ 3.7 m, not ≈ 2.4 m.** That was the earlier by-eye reading. The script gives 31 ok trees, median 3.68 m (range 3.40–3.86), so Malgrat is "medium", not "small".
- **Lluc.** The median is 3.48 m (IQR 3.39–4.92), so "≈ 3.3–3.5 m" holds.
- **Meridiana.** The unmeasured planes on Av. Meridiana are **176**, not 194. Av. Meridiana holds 194 planes in all; 18 of them are measured ("ok"). The 176 unmeasured are 160 no_facade, 13 no_kerb and 3 median.

**20-tree check** (`scripts/sidewalk_width_qa.py` → `databases/barcelona/sidewalk_width_qa.csv`, `notes/figures/sidewalk_width_qa_20.png`):
- **Sample.** 20 random ok trees (seed 21), each plotted in a 50 m window with the façade lines, road lines, the measuring ray and LiDAR buildings.
- **Visual verdict.** In 18 of 20 the ray runs façade → tree → kerb across the sidewalk as intended. In 2, the tree stands at a street corner and the ray runs diagonally to a building corner: #7 C/ Arnau d'Oms (10.75 m) and #14 Pg Verdum (8.12 m). Corner widths are overestimated, but both trees stay "large" on a plain reading of the map.
- **The ±0.3 m target cannot be tested with the data in hand.** The only independent source is the LiDAR 2021 (0.5 m), and it resolves neither line at that precision:
  - **Façades.** LiDAR building edges lie a median 0.60 m streetward of the map façade, and more than 1 m in 8 of 20 trees. These are roof overhangs and balconies, which LiDAR sees and the map's façade line does not.
  - **Kerbs.** A 12–15 cm kerb step is smoothed out in the 0.5 m DTM. Searching it for an 8 cm drop found a step within 1 m of the map kerb in only 3 of 20 trees.
  - So the map, which is the city's own 1:1000 survey, stays the reference. A ±0.3 m check would need the orthophoto (ICGC, 25 cm) or a site visit.
- **Class uncertainty.** What matters for the constraint is the size class, not the centimetre. 32 of the 400 measured planes (8%) lie within 0.3 m of a class threshold (2.5, 3.5 or 6 m), so their class could flip. For all ok trees it is 280 of 1,545.

## Rule for the 432 unmeasured planes (21 Oct)

**A kerb-to-kerb width was tried.** `strip_width_m` in the CSV is the distance between the road lines on either side of the tree, along the perpendicular to the nearest one. A visual check of 16 cases found:
- **Plausible on wide medians and boulevards.** Meridiana 26–32 m, Doctor Pi i Molist 17 m, Valldaura 8 m and Andreu Nin 4 m.
- **Wrong where the tree stands on a road line inside a narrow band.** Pl Jardins d'Alfàbia gave 1.9 m ("none") for four trees on a tree-pit/parking band next to a wide sidewalk.

So `strip_width_m` is kept as information only. `size_class` stays "check" for these positions.

| Unmeasured planes | Strip class: large | medium | small | none | n/a (no line on the other side) |
|---|---|---|---|---|---|
| Av. Meridiana (176) | 55 | 0 | 0 | 0 | 121 |
| Elsewhere (256) | 63 | 70 | 5 | 21 | 97 |

**Rule used by the tool (`ASSUMPTION`).**
- **"check" positions get no size-class filter.** Every palette species is allowed, subject only to the existing crown–building clearance (`layout.fits`). The reasoning is that medians, boulevards and plaza edges have no façade, so the guide's façade-driven sizing does not bind them. They are reported separately so that results can be shown with and without them.
- **Av. Meridiana stays in the decision set by default.** A switch drops all its 194 planes as "kept by the city" (2011 guide p. 17: planes are kept on large avenues). Which setting is right is question 2 of the email to Parcs i Jardins.

**Still open.**
- **The orthophoto check (±0.3 m).** It needs the ICGC WMS, which is reachable only from the user's PC.
- **The two corner cases.** A rule that skips the ray at corners (for example, the façade foot within 2 m of a façade vertex) is a possible refinement.

## OSM check: can OpenStreetMap give widths outside Porta? (26 Oct)

User, 26 Oct: cross the data with OpenStreetMap for the sidewalks. `scripts/osm_sidewalks.py` → `databases/barcelona/osm_sidewalk_check.csv`. Source: BBBike extract "Barcelona" (ODbL), downloaded 26 Oct. Overpass and Geofabrik were unreachable from the cloud.

**What OSM has in Barcelona:**
- 1,663 km of sidewalk lines (`footway=sidewalk`), but only 21 km of them carry a width tag.
- No street way in the extract carries a sidewalk width tag (`sidewalk:*:width`): 0 of 85,819 (osmium count, 26 Oct).
- The extract (wider than the municipality) has 61,658 crossing nodes and 9,092 bus stops. These are the obstacles the planting spots do not model yet (`scripts/porta_planting_spots.py`).

**Test on Porta's 1,545 façade-bounded measured trees (flag ok):**

| Proxy | Coverage | Median error | Within 1 m | Size class agrees |
|---|---|---|---|---|
| A: tree → nearest OSM building + 0.69 m | 100% | −0.13 m | 65% | **76%** |
| B: 2 × (OSM sidewalk line → building) | 90% | +1.53 m | 24% | 59% |
| Baseline: every tree "large" | — | — | — | 56% |

**Reading:**
- **The OSM sidewalk lines do not give the width.** They are not drawn at the centre of the sidewalk, so B is barely above the baseline.
- **The tree's distance to the building does (proxy A).** It gets the class right in about 3 trees out of 4.
  - Most of A's errors are between neighbouring classes: 127 large read as medium, 35 small read as none.
  - Its mean absolute error (3.15 m) comes from a heavy tail: the median absolute error is 0.51 m, but 14% of trees are off by more than 5 m.
  - It needs a tree position, so it works for **existing trees (replacement)**, not for new spots.
- **Caveat:** the test covers only the façade-bounded trees. Medians and boulevards ("check") are where every method struggles.

**Proposal for the city scale (§6.2 step 4 of `notes/citywide_plan.md`):**
- City screening: use proxy A for the size class of existing trees, labelled "approximate (OSM)".
- Project areas: keep the 1:1000 map, which stays the reference.
- New spots: use the OSM crossings and bus stops as exclusions with the 2011 guide's clearances, which removes part of the "upper bound" caveat. Not done yet.

## OSMnx check: a width without a tree (26 Oct)

User, 26 Oct: try OSMnx. `scripts/osmnx_street_width.py` → `databases/barcelona/osmnx_street_width_check.csv`.
- Overpass is unreachable from the cloud, so OSMnx reads an OSM XML cut of Porta plus margin. The cut comes from the BBBike extract.
- On a PC, `graph_from_polygon` works directly; `site.py` already uses OSMnx online for green areas.

**Why:** proxy A (above) needs an existing tree. New planting spots need a width estimated from the street itself.

**Method:**
1. Take the nearest drivable street centreline (OSMnx graph).
2. Cast a ray from the centreline through the point to the first OSM building outline. Call its length D.
3. Width = D − lanes × 3.0 m / 2 − parking.

Lanes are tagged on 90% of the 2,782 drivable edges in the cut. Parking is tagged on 1%, so whether a street has a parking lane is unknown. All three values (3.0 m per lane, the default lane counts, the parking width) are `ASSUMPTION`.

| On 1,182 measured trees (77% of 1,545; the rest have no building hit on the ray) | Median error | Within 1 m | Size class agrees |
|---|---|---|---|
| C, no parking | +1.13 m | 41% | 66% |
| C, 1.1 m (half a parking lane, a midpoint) | +0.03 m | 43% | 66% |
| C, 2.2 m parking everywhere | −1.07 m | 31% | 56% |
| Baseline: every tree "large" | — | — | 50% |

**Reading:**
- **OSMnx gives a usable width without a tree: 66% class agreement, against 50% for always guessing "large".**
- It is weaker than proxy A (76%), which uses the tree itself. The main error is the unknown parking lane, worth ±1.1 m.
- OSMnx also gives, in the same cut, the obstacles the spots need:
  - 1,388 crossings and 125 bus stops;
  - 1,574 sidewalk ways;
  - 3,649 OSM tree nodes, which could cross-check the inventory.

**Proposal:**
- For city screening: proxy A for existing trees, proxy C for new spots. Both labelled "approximate (OSM)".
- Use the OSMnx crossings and bus stops to drop spots too close to them, with the 2011 guide's clearances (next step).
- The 1:1000 map stays the reference for project areas.

## Spot exclusions from OSM street furniture (26 Oct)

`scripts/porta_spot_exclusions.py` adds `excluded_by` to `databases/barcelona/porta_planting_spots.csv`, and `layout.planting_spots()` drops those spots. Clearances, measured to the OSM point or line:

| Obstacle (OSM tags) | Clearance | Basis |
|---|---|---|
| Traffic signals (`highway=traffic_signals`) | 3 m | 2011 guide: > 3 m from traffic lights and signs (`notes/tree_master_plan.md` §5) |
| Crossings (`highway=crossing` points, `footway=crossing` lines) | 3 m | `ASSUMPTION`: the guide's sign clearance, since crossings carry signs and need sight lines |
| Parking entrances (`amenity=parking_entrance`) | 3 m | `ASSUMPTION`: the guide's > 1 m from driveways plus half of a ~4 m driveway |
| Bus stops (`highway=bus_stop`, `public_transport=platform`) | 8 m | `ASSUMPTION`: keeps about 16 m of kerb free for the shelter and the doors; no source yet |

**Result:**
- 267 → **232 spots** (122 small, 42 medium, 68 large).
- Excluded: 31 by crossings, 2 by parking entrances, 1 by a traffic signal, 1 by a bus stop.
- **Sensitivity:**
  - crossings 2 / 3 / 5 m and bus stops 5 / 8 / 15 m: **209–243 kept**;
  - crossings 5 m alone: 213;
  - bus stops 15 m alone: 227.

**Still an upper bound:**
- Lamps (only 4 mapped in the Porta cut), signs, driveways without a parking entrance, underground services and balconies are not in OSM here.
- A dropped spot does not free its neighbours from the spacing rule, so a few valid spots may be missing.
