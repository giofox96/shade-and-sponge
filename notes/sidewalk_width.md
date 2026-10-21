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
