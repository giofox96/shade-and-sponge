# Florence LiDAR transfer check (16 Nov 2026)

**Question.** Does the Porta per-tree LiDAR method (`scripts/bcn_lidar_porta.py`) transfer to Florence, and how close are its heights and crown widths to a tree census?

**Data.** Dati LiDAR 2023 forniti da [Comune di Firenze], derivati dal rilievo aereo effettuato sul territorio comunale nel periodo maggio/giugno 2023.
21 LAS tiles clipped to Firenze Nova (EPSG:7791, about 20 pts/m², RGB + NIR, return numbers, **not classified**). Research use only: the cloud and every per-point or per-cell product stay in `databases/florence/raw/` (gitignored); only per-tree values are in the repo.
Reference: Comune di Firenze, "Life Escapos – Alberature pubbliche" (c_d612:D.7840, CC BY-NC 4.0), 1,459 trees with `h_m` and `crn_w_m`. Same CRS as the cloud, so no reprojection.

**Method.** `scripts/florence_lidar_trees.py` → `databases/florence/florence_tree_lidar.csv` (per tree), `florence_lidar_validation.csv`, `florence_lai_vs_porta.csv`, `notes/figures/florence_lidar_validation.png`. Same as Porta (0.5 m CHM, canopy > 2 m, watershed seeded at the census positions, 9 m crown limit, crown diameter = equal-area diameter, LAI proxy = −ln(gap)/K with K = 0.5) except three changes the unclassified cloud forces:
1. **Ground, ASSUMPTION:** 1 m lowest-point grid, grey opening 21 m, 5-cell median. The Comune's 2023 DTM was not fetched.
2. **Vegetation, ASSUMPTION:** NDVI from the point NIR/red > 0.2 replaces classes 3–5 (leaf-on flight); without it buildings and vehicles enter the CHM.
3. **Gap fraction, ASSUMPTION:** "ground" = points < 0.5 m above that DTM, over all points in the crown (Porta: ground class over labelled points).

**Results.** 1,420 of 1,459 trees get a crown (39 `no_crown_detected`).

| | n | bias (LiDAR − census) | MAE | RMSE | Pearson | Spearman |
|---|---|---|---|---|---|---|
| Height (m) | 1,420 | +1.08 | 1.21 | 1.55 | 0.97 | 0.97 |
| Crown width (m) | 1,420 | +0.22 | 1.41 | 2.15 | 0.81 | 0.80 |

Per species (≥ 20 trees, 15 species) in `florence_lidar_validation.csv`. Height: r ≥ 0.96 for 10 of 15 species, weakest *Cedrus libani* (0.74) and *Olea europaea* (0.79); the bias is positive for every species (+0.7 to +1.8 m, largest for *Platanus*). Crown width: good for *Ulmus*, *Quercus robur*, *Platanus*, *Carpinus*, *Liriodendron* (r 0.86–0.98), poor for *Acer campestre*, *Cedrus*, *Olea*, *Pyrus* (r 0.35–0.42).

**Reading.** Height transfers well: it ranks trees almost perfectly, with a systematic +1.1 m offset that a single correction would remove. Crown width is unbiased on average but scatters by ±2 m, so it is usable for groups of trees, not for one tree.

**Limits.**
- **The census height and crown width are almost certainly remote-sensing values, not field measurements (checked 16 Nov on the census file itself).** The dataset page (opendata.comune.fi.it, "Life Escapos – Alberature pubbliche", published 12 Feb 2026) says only that it holds species, DBH, total height and crown width for the trees of the Firenze Nova area that are in the Direzione Ambiente tree database; it gives no survey method, and neither do the LIFE project pages. The file's own numbers settle most of it:
  - `crn_w_m` equals the diameter of a circle of area `canopy_are` for all 1,459 trees (largest difference 4 × 10⁻¹⁵ m), so crown width is computed from a segmented crown polygon, not measured across the crown. Every tree also has its own `seg_id`.
  - `h_m` is not rounded: 10.4% of heights lie within 0.05 m of a whole metre, the share expected at random (10%), and 80% are exact single-precision floats, as values read from a raster canopy height model are. The minimum is 3.00 m, a typical canopy-height cut-off.
  - `dbh_cm` behaves differently: 81% of values lie within 0.05 cm of a whole centimetre (random: 10%). DBH is most likely the field value from the city database, with a small numerical perturbation.
  So r = 0.97 for height and 0.81 for crown width measure agreement between our LiDAR method and another remote-sensing method, possibly on the same 2023 flight; they are not an accuracy against field measurement. The data source and flight behind the census values remain unknown; only the Comune can say (opendata@comune.fi.it). DBH is the one independent field variable in the file.
- Census year unknown (metadata modified Feb 2026); growth between census and flight would explain part of the positive height bias, as would the ground surface (assumption 1).
- May/June is leaf-on, but some deciduous crowns may not be at full size; crowns of neighbouring trees merge in rows and the watershed splits them at the valley, which hits crown width more than height; census points may sit off the crown centre (position error was not measured).

**LAI proxy (no reference).** The Escapos `lai` field is synthetic (`scripts/escapos_lai_check.py`), so nothing validates the proxy here. Medians for the shared species, Florence vs Porta: *Celtis australis* 4.29 vs 2.00, *Tilia* 4.16 vs 1.82, *Pyrus calleryana* 2.26 vs 2.08 (others have < 20 Porta trees). Florence is about twice Porta for the two well-sampled species, which more likely reflects the changed gap definition (assumption 3), point density and the flight season than real foliage: **the proxy is not comparable across the two cities without a common ground classification.**
