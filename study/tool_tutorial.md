# Tool tutorial: how `shade_sponge` works, how to use it, how to explain it (state of 20 Oct 2026)

This file teaches **the tool**. For the thesis around it (problem, site, gap, RQ, hypotheses), use `study/guide.md` (on `main`).
It describes the tool as of 20 Oct: main's tool (7-species city palette, photo-based leaf calendar, 15 Oct) merged with the web app, the Barcelona shortlist and the diversity floor, re-run on 20 Oct and published online the same day. **What changed since 12 Oct** is in the box below. Source of every number: `shade_sponge/README.md`, `notes/methodology.md` §4b and §6, `web/README.md`, `exchange/README.md`, unless another file is named. Numbers in "Worked example" boxes were computed for this tutorial from the tool's own formulas and parameters.

**Three parts, used in this order:**
- **A. Learn** (§1–§11): what each module does, the idea, the maths, the assumptions. Each chapter ends with a one-sentence version you should be able to say.
- **B. Use** (§12–§17): run it in Python, read the outputs, use the web app, bring results into Grasshopper.
- **C. Explain** (§18–§21): a spoken demo script with stage directions, a technical walkthrough, likely questions, and the limits to state yourself before anyone else does.

Study it like the guide: read a chapter, close it, answer **Check yourself** aloud, then open the answers.

> **What changed since 12 Oct (learn these first)**
> 1. **Seven species in the city palette:** *Styphnolobium japonicum* was added (user, 14 Oct). Porta has only 5 measured trees, so its crown and LAI come from a city-wide LiDAR sample (367 trees on 25 streets; `site.CITY_LIDAR`), in both palettes.
> 2. **Photo-based leaf calendar (15 Oct):** 170 dated Barcelona iNaturalist photos showed that **Jacaranda is mostly in leaf in January** (f = 0.8), not bare as the Valencia phenology study suggested. Tipuana is in leaf in January and half-leafed in February–March (`notes/decisions/leaf_state_inat.md`).
> 3. **So the "free" winter gain mostly went away:** summer-only → balanced now cuts winter shade by only **2.3%** (was 9–10% with the old calendar), and the swap vanishes in 3 of 8 sensitivity variants. The real summer–winter trade-off beyond the balanced layout is still **robust**, now carried by the winter-bare *Pyrus* and *Styphnolobium*.
> 4. **Heat metric decided (19 Oct):** the thesis's heat objective is the **mean UTCI over 12–17 h on a hot design day** (`notes/topic_decision.md` §8). The proxy still uses 15 July, 12–17 h CEST; aligning it to the decided window and calibrating it against Ladybug is the next step (§4).
> 5. **H3 withdrawn (19 Oct):** "the runoff benefit shrinks as storms grow" is true by construction of the bucket model, so it is now a **declared validity boundary**, not a hypothesis (§6).

---

# A. Learn

## 1. The tool in one picture

**One sentence:** *for each of Porta's 832 plane-tree positions, the tool picks a replacement species so that summer shade goes up, winter shade goes down and runoff towards flood hotspots goes down, within the city's 15% cap per species, and it shows what you trade when you favour one goal.*

```
 DATA                         SITE BUNDLE (1 m grid)          PER-POSITION POTENTIALS       OPTIMISER                 OUTPUTS
 street trees + LiDAR  ──►    roofs, sealed, pervious (CN)    shade_summer[i, j]            weighted-sum LP (HiGHS)   summary CSV (scores)
 DTM + building heights ──►   terrain + buildings  ─► topo ─► shade_winter[i, j]  ───────►  15 weight sets     ───►   layouts CSV (Grasshopper)
 flood-hazard index    ──►    flood hotspots                  water[i, j]                   + caps, façade fit        positions CSV (Grasshopper)
 IDF curves, storm months ──► design storm, leaf calendar     (i = position, j = species)   + optional diversity      web app data
                                                                                            ▼
                                                              FULL RE-SCORING of every layout (raster models, crown overlaps) → Pareto front
```

**The five ideas to remember**
1. **One decision:** which species goes at each plane position. Positions do not move; the other trees stay.
2. **Three objectives:** summer shade (benefit), winter shade (cost: people want winter sun), runoff that reaches flood hotspots (cost).
3. **Fast proxies, not full simulations:** a shade proxy instead of UTCI, a bucket + curve-number model instead of a hydraulic model. They are fast enough to score thousands of species–position pairs.
4. **Exact optimisation:** the problem is shaped so that a linear program finds the true best layout for given weights, in seconds.
5. **Honest re-scoring:** every chosen layout is scored again with the full raster models (with crown overlaps) before any number is reported.

**Package map** (`shade_sponge/`)
| File | Job | Chapter |
|---|---|---|
| `site.py` | Builds the site bundle on a 1 m grid and caches it (`cache/site_porta.npz`) | §2 |
| `topo.py` | Where surface water flows (routing on terrain + buildings) | §3 |
| `heat.py` | Sun position, building shadows, crown shadows, shade metric | §4 |
| `season.py` | Leaf calendar per species, storm months | §5 |
| `runoff.py` | Design storm, canopy bucket, SCS curve number | §6 |
| `layout.py` | Palette, caps, façade fit, potentials, optimiser, Pareto | §7–§9 |
| `__main__.py` | The run: `python -m shade_sponge` | §12 |
| `web_export.py` | Writes the web app's data | §15 |

---

## 2. The site bundle (`site.py`)

**Question it answers:** what does the tool need to know about Porta, cell by cell?

**Idea:** everything becomes a raster on one **1 m grid** in EPSG:25831 (metres). Rasters can be added, masked and filtered quickly, so every later step is array maths.

**Layers in the bundle**
| Layer | Meaning | From |
|---|---|---|
| `domain` | Inside Porta | Neighbourhood boundary (Open Data BCN) |
| `roof` | Building footprint | OSM footprints |
| `cn` | Curve number: 98 roofs and sealed ground, 74 pervious | NDVI 2017 ≥ 0.3 with LiDAR canopy < 2 m, or OSM park/garden/grass |
| `dtm`, `bldg_h` | Ground height; building height above ground | ICGC LiDAR (flown 26 Sept 2021) |
| `background` | Canopy that is not a street tree (parks, private), fixed in every layout, LAI 2.3 | LiDAR canopy ≥ 2 m minus street crowns |
| `hot` | Flood hotspot: Resilience Atlas hazard index ≥ 40 | Barcelona Regional |
| `acc`, `dist_hot` | Water convergence and flow distance to a hotspot | `topo.py` (§3) |

Porta's surfaces: **roofs 29%, sealed open space 52%, pervious 19%** of 83.7 ha.

The trees come from `exchange/to_gh/porta_trees_lidar.csv`: **2,825 street trees** (2,600 with a LiDAR crown, `flag == ok`); **832 of them are plane positions**, the decision variables.

**Site-agnostic by design:** a new site needs only a `build_<site>()` and `trees_<site>()` returning the same keys and columns. Nothing else in the package knows it is Porta.

> **Say it:** "The tool first turns the site into one 1-metre grid (roofs, sealed and green ground, terrain, buildings, flood hotspots), so everything after that is fast array maths, and a new city only needs a new data adapter."

---

## 3. Topography: where the water goes (`topo.py`)

**Question:** if rain falls on this cell, where does the water flow, and does it reach a flood hotspot?

**Idea:** water flows downhill, cell to cell. Each cell sends its water to **one of its 8 neighbours**. Buildings are added to the terrain as walls, so water flows around them. Pits (small dips in the DTM) would trap water forever, so the **Priority-Flood** algorithm (Barnes et al. 2014, *to add*) fills them on the fly: it floods the grid from the edges inward, lowest cell first, and every cell's receiver is the neighbour that flooded it.

Two results:
- **Water convergence** (`acc`): how much open ground drains through each cell (m²). High values = natural gutters and low points.
- **Flow distance to a hotspot** (`dist_hot`): metres along the flow path to the first hotspot cell.

**Key assumption, `CAPTURE_M` = 100 m:** runoff counts towards a hotspot only if its path reaches one within 100 m. This stands in for the sewer inlets that take water on the way. Without a limit, 97% of open ground would drain to some hotspot and position would stop mattering. Test range 50–200 m (not run yet).

**Limits:** no sewer network, no inflow from outside the grid (Porta's bounding box). The map shows where surface water *would converge*, not where it ends up.

**Checked against RESCCUE flood depths (15 Oct, `scripts/compare_resccue_runoff.py`; `notes/methodology.md` §4):** the routing finds the main convergence points, but it is not a flood map.
- Overall, upstream area barely separates RESCCUE wet from dry cells (ROC AUC 0.52 in all four scenarios).
- But the cells with the largest upstream area do get wet: of the top 0.5% of open ground, 58% (T10 present) to 80% (T100) are wet, 1.7–2.6 times the random rate.
- 44% of the atlas high-hazard cells the tool uses are wet at T10 present, vs 23% of all open ground.
- Likely reasons (from the map, not tested): RESCCUE floods the perimeter avenues with water from outside Porta and from the sewer, which the routing lacks; depression filling gives plazas and the sports ground large upstream areas that RESCCUE leaves dry.
- **Consequence:** hotspots stay tied to the atlas index (or RESCCUE depth, licence pending), as the tool already does; the routing only decides which ground drains to them.

> **Say it:** "The terrain and buildings tell us where water converges; ground whose runoff reaches a flood hotspot within 100 metres counts more, so trees there are worth more for flooding."

---

## 4. The heat proxy (`heat.py`)

**Question:** how much useful shade does a tree give pedestrians, in summer and in winter?

**Why a proxy and not UTCI:** UTCI with Ladybug in an optimisation loop costs 20–25 min per layout for 42 trees (Shaamala et al. 2025); Porta has 832 positions. The proxy is fast and must later be **calibrated against Ladybug UTCI** on a sub-area (not done yet).

**Four steps**
1. **Sun position** for each design hour (NOAA solar equations).
   - Summer: **15 July, 12–17 h CEST**, sun ≈ 47–70° high.
   - Winter: **15 January, 10–15 h CET**, sun ≈ 15–27° high. (Both days are ASSUMPTIONS.)
   - **Not yet aligned with the decided heat metric** (19 Oct: mean UTCI over 12–17 h EPW standard time = 13–18 h CEST on a hot design day; `notes/decisions/heat_objective.md` §1). Moving the summer window to that day and those hours changes every shade number, so it is done together with the Ladybug calibration.
2. **Is the pedestrian in the sun?** For each cell, at 1.1 m (pedestrian height), march towards the sun over terrain + buildings. If a building is in the way, the cell is already shaded, and a tree there adds nothing.
3. **Crown shadow:** each crown is an **ellipsoid** (diameter D, from crown base Hb to height H). Its shadow at 1.1 m is an **ellipse**: as wide as the crown across the sun direction, longer along it when the sun is low, and shifted away from the sun by (crown-centre height − 1.1 m) / tan(altitude). Winter shadows are long and far from the trunk.
4. **Opacity** (how much sun the crown blocks):
   - In leaf: **1 − exp(−0.5·LAI)** (Beer–Lambert, k = 0.5 as in Peng et al. 2026).
   - Leafless: **OP_BARE = 0.35** (ASSUMPTION; leafless crowns cut ~35% of sunlight, McPherson 1984; up to ~54% for London plane, Heisler 1982/84; both cited in Thayer & Maeda 1985). Test range 0.25–0.54.
   - Mixed months: f·(leaf value) + (1 − f)·0.35, with f = leaf fraction of the month (§5).

**Metric:** effective shade (m²·h) = sum over design hours of (opacity × area) of crown shadow falling on **sunlit open ground**. Where shadows overlap, the darker one counts (no double counting).
- **Summer shade = benefit** (heat stress).
- **Winter shade = cost** (sun access for cold-season comfort). This is what creates a real trade-off (§10).

> **Worked example: Jacaranda vs Tipuana** (median Porta crowns: Jacaranda D = 7.33 m, LAI 2.91; Tipuana D = 8.01 m, LAI 2.20)
> - Leaf opacity: Jacaranda 1 − e^(−0.5×2.91) = **0.77**; Tipuana 1 − e^(−0.5×2.20) = **0.67**.
> - Summer, rough (crown footprint only): 0.77 × 42.2 m² ≈ 32 vs 0.67 × 50.4 m² ≈ 34. **Almost equal**: the denser Jacaranda canopy makes up for its smaller crown.
> - January, photo-based calendar: Jacaranda is 80% in leaf (opacity 0.8 × 0.77 + 0.2 × 0.35 = **0.68**), Tipuana fully in leaf (0.67). Rough winter shadow: 0.68 × 42.2 ≈ 29 vs 34, **only ~14% less**, and mostly because Jacaranda's crown is smaller.
> - With the old calendar (Jacaranda bare, opacity 0.35) it was 15 vs 34, less than half. That difference was the whole "no-regret swap"; the photos shrank it (§10).

> **Say it:** "Heat is a shade proxy: crowns are ellipsoids that cast elliptical shadows, as dark as their leaf density allows, and only shade that falls where buildings leave people in the sun counts; summer shade is good, winter shade is a cost."

---

## 5. Seasons: leaf calendar and storm months (`season.py`)

**Question:** a deciduous tree has no leaves in winter. When does that matter?

**Leaf calendar:** `databases/traits/phenology_palette.csv` gives, per species and month, the leaf fraction f (1 = full leaf, 0 = bare, 0.5 = leafing out or dropping), with a source per species; months that come from a leaf-habit class default are marked ASSUMPTION. Examples: Celtis, Melia, Pyrus, Styphnolobium bare Dec–Feb (class default); **Jacaranda 80% in leaf in January, 70% in February, 50% in March–April** and **Tipuana in leaf in January, 50% in February–April** (Dec–Mar from 170 dated Barcelona iNaturalist photos, adopted 15 Oct; Tipuana's April = ASSUMPTION); Brachychiton evergreen. The older Valencia value (Jacaranda bare Jan–Mar, Gandía-Ventura et al. 2025) is kept as a sensitivity variant.

**LAI in month m** = LAI measured by LiDAR (26 Sept, full leaf) × (R_OFF + (1 − R_OFF)·f(m)).
**R_OFF = 0.5** (ASSUMPTION, test 0.3–0.7): a leafless crown still holds about half the water of a full one (branches and bark). Anchors: Herbst et al. 2008; Xiao et al. 2000.

**Storm months:** intense storm days in the Barcelona area (Esbrí, Rigo & Llasat 2026, Fig. 4; `databases/barcelona/storm_months.csv`). **78% fall in May–Oct**, peaking in September (29%) and October (22%). The runoff objective is the **expected runoff over the storm months**.

> **Worked example: does leaf fall matter for runoff?** Season-weighted leaf factor in storms (1 = full leaf in every storm): deciduous species (incl. Styphnolobium) **0.93**, Jacaranda **0.98**, Tipuana **0.99**, Brachychiton **1.00**. Storms come when every species is in leaf, so for **runoff** the leaf calendar barely matters. For **winter shade** it matters a lot (§4).

> **Say it:** "Each species has a monthly leaf calendar: it changes winter shade a lot, but runoff very little, because Barcelona's intense storms come in late summer and autumn, when every tree is in leaf."

---

## 6. Runoff (`runoff.py`)

**Question:** for a design storm, how many m³ of water run off Porta, and how much of it heads to flood hotspots?

**Step 1: design storm.** From the PDISBA city IDF curves (`databases/barcelona/pdisba_idf_city.csv`): **T = 2 years, 1 hour → 31.9 mm**. (Runoff v1 also reports T = 1 and 10 yr.)

**Step 2: canopy bucket.** Under each crown (not over roofs: roof water goes down the pipes anyway), the crown stores **S = s·LAI** mm of rain before any reaches the ground. Interception I = min(P, S); the ground gets P − I (= max(P − S, 0)).
- **s = 1.75 mm per unit LAI**, calibrated on the open field data of Anys & Weiler (2024): 16 urban lime and maple trees, 51 events. Lower bound for sensitivity: 0.86 mm (surface storage only, Xiao & McPherson 2016).
- Same s for every species (limit): species differ only through crown size and LAI.

**Step 3: SCS curve number** on the rain that reaches the ground:
- S_cn = 25.4·(1000/CN − 10) mm (how much the surface can absorb)
- Ia = 0.2·S_cn (initial abstraction: what is lost before runoff starts)
- Q = (P − Ia)² / (P − Ia + S_cn) if P > Ia, else 0

> **Worked example: one 1 m² cell, P = 31.9 mm**
> | Cell | S_cn | Ia | Runoff Q |
> |---|---|---|---|
> | Sealed (CN 98), no tree | 5.2 mm | 1.0 mm | **26.4 mm** (83% of the rain) |
> | Sealed, under a crown with LAI 2.3 (S = 4.0 mm) | 5.2 mm | 1.0 mm | **22.5 mm** |
> | Pervious (CN 74), no tree | 89.2 mm | 17.8 mm | **1.9 mm** |
>
> A crown over asphalt removes ~3.9 mm per m². An 8 m crown (~50 m²) over sealed ground ≈ **200 litres per storm**. Over green ground the soil already does most of the work; over a roof it does nothing in this model.

**Outputs per layout:** `runoff_m3` (whole site), `runoff_hot_m3` (from open ground that drains to a hotspot within 100 m), `interception_m3`; season-weighted (§5), plus `*_leafon` columns at full leaf.

**Size of the effect:** Porta's current street trees cut runoff by **1.85%** at T2-60 (open space only: 2.9%; range 0.4–4.0% across s and T). That is the same order as field measurements (3.5–4%, Selbig et al. 2021; Coville et al. 2022). The benefit shrinks as storms get bigger. This is a **declared validity boundary**, not a hypothesis: in the bucket model every crown is full at every design storm, so the falling percentage follows from I = min(P, S) by construction (H3 withdrawn on 19 Oct, `notes/topic_decision.md` §8). Say it that way: "consistent with the declared boundary", never "supports H3".

**Checks so far:** reproduces `runoff_scenarios.csv` of runoff v1 exactly (S0, T2-60, full leaf: 17,649.6 m³); the calibration of s is against field data. No local runoff measurements in Porta.

> **Say it:** "Each crown is a small bucket of s times LAI millimetres; the rest of the 2-year, 1-hour storm goes through the curve-number equation; trees cut Porta's runoff by about 2%, the same order as field studies, so for flooding the tool is about where the water goes, not big volumes."

---

## 7. Palette and constraints (`layout.palette`, `layout.fits`)

**Question:** which species may go where, and how many of each?

**Two palettes**
| Palette | Species | Traits from | Run flag |
|---|---|---|---|
| **City** (default) | **7**: the 6 the city names as plane replacements (*Celtis australis, Melia azedarach, Pyrus calleryana, Jacaranda mimosifolia, Tipuana tipu, Brachychiton populneus*) + *Styphnolobium japonicum* (added by the user, 14 Oct) | Median LiDAR crown of each species' trees **in Porta**; Styphnolobium from a city-wide sample (367 trees on 25 streets), because Porta has only 5 | none |
| **Barcelona shortlist** | **34** species with ≥ 500 street trees in Barcelona (established in the city's climate, ASSUMPTION), no planes, no listed invasives; ≥ 20 LiDAR-measured trees each (`MIN_LIDAR`, ASSUMPTION) | Medians from Porta + 3 ICGC tiles (one of them Porta's own tile); Styphnolobium as in the city palette | `--palette=barcelona` |

Species traits used: crown diameter, height, crown base, LAI proxy (all medians), leaf calendar.

**Constraints**
- **Cap (15%):** no species above 15% of all street trees in Porta (tree master plan). Cap of a species = floor(0.15 × 2,825) = 423, minus its trees that are kept. Changeable in the web app.
- **Façade clearance:** a species fits at a position only if its crown radius ≤ the distance to the nearest building (ASSUMPTION: no extra margin). If nothing fits, the smallest crown is allowed.
- **Diversity floor (optional, §9).**
- Not modelled yet: maintenance, roots and paving, allergens, pests. Invasive behaviour is flagged in the shortlist (*Robinia, Ulmus pumila, Ligustrum lucidum*) but not excluded.

> **Say it:** "The designer chooses among the city palette's seven species or a 34-species Barcelona shortlist, with sizes measured by LiDAR on real trees in the city, within the 15% cap and only where the crown clears the façades."

---

## 8. Per-position potentials (`layout.shade_potential`, `layout.water_potential`)

**Question:** before optimising, what would each species deliver at each position, on its own?

For every position i and species j the tool pre-computes three numbers:
- `shade_summer[i, j]`: m²·h of effective summer shade on sunlit open ground (§4), using the species' median crown;
- `shade_winter[i, j]`: the same on the winter day (cost);
- `water[i, j]`: m³ intercepted over open ground **that drains to a hotspot**, season-weighted (§5–6).

**Shortcut:** each potential treats the tree **alone** (no overlap with neighbours), and uses a box filter (the share of sunlit or hotspot-draining ground in a square the size of the shadow or crown). This is what makes the problem linear: a layout's score = the sum of its positions' potentials.

**Why it matters for the defence:** the shortcut is checked, not trusted. Every final layout is re-scored with the full raster models (§9). And there is a known gap: hotspot runoff after re-scoring **does not follow the runoff weight** (the water potential predicts it poorly; to investigate: crown overlap with kept trees, the box filter).

> **Say it:** "For each of the 832 positions and each species, the tool pre-computes what that tree alone would give in summer shade, winter shade and intercepted hotspot runoff; that table is what the optimiser works on."

---

## 9. The optimiser (`layout.assign`, `layout.sweep`)

**Question:** given weights for the three goals, what is the best species at every position?

**Weighted sum:** each potential table is divided by its maximum (so the three are comparable, 0–1), then
score[i, j] = w_summer·summer − w_winter·winter + w_runoff·water (+ a 0.1% share of the unweighted sum to break ties).

**The linear program (a "transportation problem")**
- Variables x[i, j] = 1 if species j goes at position i.
- Each position gets exactly one species: Σ_j x[i, j] = 1.
- Each species stays under its cap: Σ_i x[i, j] ≤ cap_j.
- x[i, j] = 0 where the species does not fit (façade).
- Maximise Σ score[i, j]·x[i, j].

It is solved with **HiGHS** (via `scipy.optimize.linprog`). For this problem shape the best solution comes out whole (0 or 1) by itself, so there is no rounding: **it is the exact optimum for the given weights**, in seconds.

**The sweep:** weights on a 0.25 grid over the triangle (summer, winter, runoff) → **15 weight sets**, e.g. `S4_s0.50_w0.25_r0.25` = balanced. Corners are the single-objective layouts: (1, 0, 0) = summer-only (the methodology's S2), (0, 0, 1) = runoff-only (S3).

**Diversity floor (optional, `--diversity=N`):** keep at least N **effective species** among the replanted positions. Effective species = exp(Shannon H), the measure SylvCiT uses (Nicol et al. 2026). With proportions p_j: H = −Σ p_j·ln p_j; 6 species in equal numbers give exactly 6. H is curved, so the tool replaces each species' term by straight segments that lie just under the curve (a conservative floor) and makes only the 6–34 species counts whole numbers. The problem stays fast (1–5 s in the browser). N is a designer choice, not a sourced threshold. With the city palette (7 species) a floor of 6 is feasible and costs about 4% of summer shade (browser estimate, 20 Oct); with the old six species it was infeasible.

**Why not NSGA-II (yet):** the weighted-sum LP gives exact, repeatable layouts quickly. The methodology keeps NSGA-II for later, if the weighted-sum front leaves gaps (a weighted sum cannot find points in concave parts of a front).

> **Say it:** "For each set of priorities the tool solves a linear program that gives the exact best species at every position under the caps and façade limits; sweeping the priorities over 15 combinations traces the trade-off."

---

## 10. Scenarios, re-scoring and the Pareto front

**Scenarios in the tool**
| ID in the files | Meaning |
|---|---|
| `S0_current` | Today's trees, mature planes included |
| `S1_random_0…9` | Each plane position gets a random palette species that fits and has room under the cap (a trait-blind replacement); 10 seeds, the mean is the reference |
| `S4_s<summer>_w<winter>_r<runoff>` | The 15 optimised layouts |

Note: the methodology's S1 is "like-for-like in the city's proportions"; the tool's S1 is a random palette under the caps. Say "random palette" when you show the tool.

**Re-scoring:** every layout is evaluated with the full models (crown overlaps, actual shadows, seasonal runoff) → `databases/barcelona/tool_v0_summary.csv`.

**Pareto front:** a layout is on the front if no other layout is at least as good on all three (summer ↑, winter ↓, hotspot runoff ↓) and better on one. Computed among replacement layouts only (S0 keeps mature planes, so it is not a fair competitor).

**Results, city palette, 7 species, photo-based leaf calendar** (`shade_sponge/README.md`, run of 20 Oct; Porta's kept trees of the shortlist species (about 92% of the non-plane trees) now have leaf calendars too, so winter shade is ~28,000 m²·h lower in every layout than in the 15 Oct run; layouts and summer values are identical)
| Layout | Summer shade (m²·h) | Winter shade (m²·h, cost) | Hotspot runoff (m³) |
|---|---|---|---|
| S0 current (mature planes) | 359,310 | 196,218 | 2,682.3 |
| S1 random palette (mean of 10) | 286,656 | 190,332 | 2,698.5 |
| S4 summer only (1, 0, 0) | 332,224 | 205,396 | 2,690.8 |
| **S4 balanced (0.50, 0.25, 0.25)** | **332,342** | **200,750** | 2,688.9 |
| S4 winter-heavy (0, 0.50, 0.50) | 272,596 | 159,790 | 2,691.1 |

**Four findings to know**
1. **Optimised beats random: +15.9% summer shade** (balanced vs random), robust across all 8 sensitivity variants (+15.8 to +15.9%). But it casts *more* winter shade than random (+5.5%): no winter gain.
2. **The "free" gain is small now:** summer-only → balanced cuts winter shade by only **2.3%** at the same summer shade (~90 Tipuana → Jacaranda), and the swap vanishes in 3 of 8 variants. Before the photo-based calendar it was −9%, and the old calendar in today's run still gives −10%: the calendar, not the new species, shrank it (§4 worked example).
3. **The real trade-off is robust:** beyond balanced, more winter sun costs summer shade (winter-heavy: **−20.4% winter shade for −18.0% summer shade**; across variants winter −14 to −23%, summer −17 to −20%). It is carried by the winter-bare *Pyrus* (276, at its cap) and *Styphnolobium* (213–245 in every variant), which replace Tipuana and most Jacaranda.
4. **Placement follows the buildings, partly:** when winter sun counts (winter-heavy layout), the winter-bare Pyrus gets positions in sun 78% of winter hours and Celtis 68%, the evergreen Brachychiton 31%. But the winter-bare Styphnolobium (36%) also sits where buildings already shade the street, so leaf habit does not explain every placement. (Melia's 87% in the balanced layout is mostly summer sun: it holds the same sunny streets when winter has no weight.)

And two honest ones: **runoff barely changes** across layouts (hotspot runoff varies 0.5%; it now mostly follows the runoff weight, Spearman −0.73, but did not in the 8 Oct run, so the water potential is still unverified), and **no city-palette layout reaches today's mature planes** on summer shade (best: −7.5%).

**Barcelona shortlist** (34 species, re-run 20 Oct): optimised layouts **match or beat the mature planes** on summer shade (balanced +0.9%, summer-only +1.7%), and the trade-off is wider (summer-only → balanced: −18% winter shade for −0.8% summer shade). But a few species dominate (balanced: *Ulmus pumila* + *Pinus pinea* = 84% of positions). With **diversity floor N = 10**, those two drop to 52% and the balanced layout loses only **2.0% summer shade** (still +27.5% over the random palette): diversity is cheap here.

> **Say it:** "Every layout is re-scored with the full models; the optimised layout gives 16% more summer shade than a random palette, and asking for winter sun is a real trade: about 20% less winter shade costs about 18% of summer shade. A free winter gain we found first shrank to 2% once Barcelona photos showed Jacaranda keeps its leaves in January."

---

## 11. The two front-ends

**Web app** (`web/`, Vue + MapLibre + deck.gl + ECharts; static site, no server). Online: https://giofox96.github.io/shade-and-sponge/ (published 20 Oct: the same version and numbers as this tutorial, diversity floor included). It is rebuilt automatically whenever `web/` changes on `main` or `claude/web-ui`; a browser may keep the previous version for up to 10 minutes after a deploy, so reload if the numbers look old.
- Shows the saved layouts on a 3D map with exact scores.
- **Live re-optimisation:** the same LP as Python, solved in the browser with HiGHS (WebAssembly) in ~0.1–0.3 s. Checked against Python: same layout at 827–832 of 832 positions for 4 weight sets.
- Live scores are **estimates (≈)**: summed single-tree potentials, corrected by a straight line fitted on the 16 saved layouts (R² shown). Exact scores need a Python run.
- **Add trees:** click open ground; the browser computes each species' potentials at that point (a port of the Python formulas, median difference 0.01% at the plane positions) and recommends the best species. Refuses roofs, ground outside Porta and < 1 m from a building; warns < 4 m from another tree (ASSUMPTION). No sidewalk data: the designer decides where planting is possible.

**Grasshopper** (primary user: the computational designer). For now, through files in `exchange/` (§16); a Hops component is planned. Ladybug UTCI is the check on the shade proxy (Tier 1/Tier 2, methodology §5).

> **Say it:** "One Python core, two front-ends: Grasshopper files for the computational designer, and a web app where anyone can move the priorities and see a new optimised layout in a fraction of a second."

### Check yourself (A)
1. Name the three objectives and say which are costs.
2. Why is winter shade a cost, and which species property makes the trade-off appear? Which species carry it now?
3. What is `CAPTURE_M`, and why can it not be unlimited?
4. Compute runoff on a sealed cell for P = 31.9 mm with and without a crown of LAI 2.3. Which numbers do you need?
5. Why is the LP result exact and not rounded?
6. Why are live web scores marked ≈?
7. What does the diversity floor measure, and what did it cost in the Barcelona balanced layout?
8. Why did the no-regret swap shrink from −9% to −2%, and what evidence changed it?

<details><summary>Answers</summary>

1. Summer shade (benefit), winter shade (cost), runoff reaching flood hotspots (cost).
2. People need winter sun; leaf habit (winter-bare vs winter-leafed crowns) separates species that give similar summer shade. Now the winter-bare Pyrus and Styphnolobium.
3. Runoff counts towards a hotspot only if its flow path reaches one within 100 m (sewer inlets take the rest); unlimited → 97% of open ground would count and position would not matter.
4. CN 98 → S_cn 5.2 mm, Ia 1.0 mm → Q 26.4 mm; with S = 1.75 × 2.3 = 4.0 mm the ground gets 27.9 mm → Q 22.5 mm. Need P, CN, s and LAI.
5. Transportation-problem structure: each position takes exactly one species, each species has a cap, so the LP's optimum is already 0/1.
6. They sum single-tree potentials (no crown overlaps), corrected by a line fitted on the 16 saved layouts.
7. Effective number of species exp(Shannon H) among replanted positions; N = 10 cost 2.0% summer shade.
8. 170 dated Barcelona iNaturalist photos (15 Oct) showed Jacaranda 80% in leaf in January, not bare, so it no longer gives back much more winter sun than Tipuana. The leafless-crown opacity still scales what is left (−3.6% at 0.25, −0.4% at 0.54).
</details>

---

# B. Use

## 12. Run the Python tool

**Where:** the main project folder on your laptop. The run needs `cache/site_porta.npz` or the raw data in `databases/barcelona/raw/`; both are local only (not in git), so cloud sessions cannot do a full run.

**PowerShell** (conda env `shade-and-sponge`):
```powershell
conda activate shade-and-sponge
$env:PATH = "$env:CONDA_PREFIX\Library\bin;$env:PATH"   # GIS DLLs
python -m shade_sponge                                   # city palette, ~4 min
```
If `conda activate` does not work in PowerShell, call the env's Python directly:
```powershell
& "$HOME\miniconda3\envs\shade-and-sponge\python.exe" -m shade_sponge
```
A "GDAL_DATA is not defined" warning is harmless.

**Variants**
```powershell
python -m shade_sponge porta --palette=barcelona                  # 34-species shortlist
python -m shade_sponge porta --palette=barcelona --diversity=10   # + diversity floor
```

**What it prints, in order:** number of positions and storm depth (832, 31.9 mm) and sun altitudes; the palette table (traits, cap, storm leaf factor); the leaf-factor sensitivity; the share of positions where each species fits; then the summary table, one row per layout.

**What it writes**
| File | Content |
|---|---|
| `databases/barcelona/tool_v0_summary<tag>.csv` | One row per layout: scores, species counts, `eff_species` (in runs since 12 Oct), `pareto` |
| `exchange/to_gh/positions_tool_v0<tag>_<date>.csv` | Per position: site context + every species' potentials |
| `exchange/to_gh/layouts_tool_v0<tag>_<date>.csv` | Every saved layout, one row per position, crown sizes |
| `databases/barcelona/tool_v0_storm_leaf_factor<tag>.csv` | Leaf factor in storms per species |

`<tag>` = `_barcelona` and/or `_div<N>` (the leaf-factor file only gets `_barcelona`). The run overwrites tracked CSVs: commit them if the code changed on purpose, otherwise discard them with `git checkout -- <file>`. Exchange files carry the date, so a run on a new day creates new untracked files: delete them if you do not keep the run.

**Figure:** `$env:PYTHONPATH="."; python scripts/plot_tool_v0.py` → `notes/figures/tool_v0.png`.
**Sensitivity (7 variants):** `python scripts/sensitivity_tool_v0.py` → `databases/barcelona/tool_v0_sensitivity.csv`.
**Tests (data-free, ~2 s, also run by CI):** `python -m pytest -q -p no:cacheprovider tests`.

## 13. Read the summary CSV

| Column | Meaning | Better when |
|---|---|---|
| `scenario` | `S0_current`, `S1_random_k`, `S4_s…_w…_r…` | |
| `shade_summer_m2h` | Effective summer shade on sunlit open ground | higher |
| `shade_winter_m2h` | The same on 15 January | lower |
| `runoff_m3`, `runoff_hot_m3` | T2-60 runoff, whole site / towards hotspots, season-weighted | lower |
| `interception_m3` | Rain held by crowns | higher |
| `*_leafon` | The same at full leaf (September LiDAR) | |
| species columns | Trees of each species at the 832 positions | |
| `eff_species` | exp(Shannon H) of the replanted positions (runs since 12 Oct) | |
| `pareto` | On the front among replacement layouts | |

**Exercise:** open `tool_v0_summary.csv`, compute the mean summer shade of the 10 `S1_random` rows, and compare it with `S4_s0.50_w0.25_r0.25`. You should get ≈ +16%.

## 14. Change a parameter and see what happens

Assumptions sit at the top of each module as constants with a comment. To test one:
1. Change it (e.g. `OP_BARE = 0.25` in `heat.py`).
2. Run `python -m shade_sponge` and compare the summary with the previous one.
3. Undo the change (`git checkout -- shade_sponge/heat.py`), or run `scripts/sensitivity_tool_v0.py`, which already does this for 6 variants.

| Constant | File | Value | Status |
|---|---|---|---|
| `CAPTURE_M` | `site.py` | 100 m | ASSUMPTION (test 50–200) |
| `HAZARD_HIGH` | `site.py` | index ≥ 40 | Same as site screening |
| `SEASONS` | `heat.py` | 15 Jul 12–17 h CEST; 15 Jan 10–15 h CET | ASSUMPTION (summer window to align with the decided metric, 13–18 h CEST on a hot design day) |
| `K` | `heat.py` | 0.5 | Peng et al. 2026 |
| `OP_BARE` | `heat.py` | 0.35 | ASSUMPTION, sourced range 0.25–0.54 |
| `R_OFF` | `season.py` | 0.5 | ASSUMPTION (0.3–0.7), anchored |
| `s_mm_per_lai` | `databases/barcelona/runoff_params.json` | 1.75 | Calibrated (Anys & Weiler 2024) |
| CN sealed / pervious | same | 98 / 74 | ASSUMPTION (TR-55 values) |
| `MAX_SHARE` | `layout.py` | 0.15 | Tree master plan |
| `MIN_LIDAR` | `layout.py` | 20 trees | ASSUMPTION |

The cache (`cache/site_porta.npz`) stores the site bundle. If you change something in `build_porta()` (surfaces, routing, hotspot threshold), delete the cache so it is rebuilt (~15 s). `CAPTURE_M` is applied when the site is loaded, so it does not need a rebuild.

## 15. Use the web app

**Online (use this for demos):** https://giofox96.github.io/shade-and-sponge/ (20 Oct version, same numbers as this tutorial; nothing to install).
**Local** (only to see a new Python run before it is published; needs Node.js):
```powershell
python -m shade_sponge.web_export                          # only after a new Python run
python -m shade_sponge.web_export porta --palette=barcelona
cd web; npm install; npm run dev                           # then open the address it prints
```

**Guided tour (10 minutes)**
1. **Header:** palette switch, "City palette (6)" or "Barcelona shortlist".
2. **Layout:** "Current trees" → "Random palette" → "Optimised" (balanced). Watch the **Results** panel: each metric vs current and vs random (green = better).
3. **Map layer** "Winter sun (15 Jan 10–15 h)": the streets that buildings already shade in winter. Then switch to "Optimised" and see where the winter-bare species sit.
4. **Month slider:** move to January. Deciduous crowns become more transparent (opacity follows each leaf calendar).
5. **Priorities triangle:** dots = the 15 exact layouts (blue = on the front). Click a dot: exact scores. Click empty space: live re-optimisation (≈ estimate; the note shows the R² of the estimate).
6. **Trade-off chart:** summer shade vs winter shade for all layouts; current trees and random palettes for reference.
7. **Click a tree:** the inspector shows its sun hours, whether its ground drains to a hotspot, and what every species would deliver there. This answers "why this species here?".
8. **Max share per species:** lower it to 10%, and the optimiser has to spread species out.
9. **Untick a species** (e.g. a pest risk): it is removed and the layout re-optimised.
10. **Diversity floor:** tick it and raise N; watch summer shade drop slightly and the species bar diversify.
11. **Add trees:** click open ground; the tool recommends a species for the current priorities. "Download CSV" exports the new trees in Grasshopper coordinates.

## 16. Bring results into Grasshopper

All rules and Python snippets are in `exchange/README.md`. In short:
- **Coordinates:** Rhino metres, local XY = EPSG:25831 − (430800, 4586800) (`exchange/site_origin.json`). Z = height above ground (`ground_z` gives the terrain height).
- **Buildings:** `porta_buildings.geojson` → extrude footprints by `height_m` (snippet in the README).
- **A layout:** read `layouts_tool_v0_<date>.csv`, filter one `scenario` (e.g. `S4_s0.50_w0.25_r0.25`), build each crown as an ellipsoid centred at z = ground_z + (crown_base_m + height_m)/2, horizontal diameter `crown_diam_m`, vertical extent `height_m − crown_base_m` (ellipsoid snippet).
- **Context maps:** read `positions_tool_v0_<date>.csv` as points and colour them by `sun_share_winter`, `drains_to_hotspot` or any species potential.
- **Back to Python:** export Ladybug UTCI results to `exchange/from_gh/` in long format (`scenario, hour, point_id, x, y, z, utci_C`, writer snippet in the README) and log the EPW and settings in `from_gh/run_log.md`. This is how the shade proxy will be calibrated.

## 17. Hands-on exercises
1. Run the city palette. Which species never reaches its cap in the balanced layout?
2. In the web app, find the weights where Tipuana disappears. What happens to summer shade?
3. Pick a position with `sun_share_winter` < 0.3 in the positions file. Which species does the balanced layout put there, and why does that fit §10, finding 4?
4. Set the max share to 10% in the web app. How do summer shade and the species mix change?
5. Barcelona shortlist, balanced, diversity floor off vs 10: write down the two biggest species before and after.
6. Load the balanced layout in Grasshopper and render it with the buildings. Compare with S0 in a summer-noon sun view.

---

# C. Explain

## 18. The 30-second version (by heart)

> "Barcelona has to replace many plane trees. My tool decides **which species go at each position**. For every street-tree position in Porta it computes what each candidate species would give in **summer shade**, **winter sun** and **rain kept away from flood hotspots**, using LiDAR-measured crowns, the terrain and the buildings. Then an optimiser finds the best layout for the designer's priorities, within the city's 15% rule. In Porta it gives 16% more summer shade than a random choice of the same species, and it shows exactly what you give up when you ask for more winter sun."

## 19. Demo script, web app (≈ 4 min)

`[DO]` = action on screen, **SAY** = what you say. Start on the city palette, "Current trees", map layer off.

**1. The problem (30 s)**
`[DO]` Show the map of Porta with today's trees.
**SAY:** "This is Porta, in Nou Barris. These are its 2,825 street trees; for 2,600 of them LiDAR gives the real crown size. Eight hundred and thirty-two are plane trees, and the city's tree plan caps every species at 15%, so many of them will be replaced. The question is: replaced with what, and where?"

**2. A trait-blind replacement (30 s)**
`[DO]` Click "Random palette". Point at the Results panel.
**SAY:** "If we put the seven candidate species at random, respecting the cap, we lose about a fifth of today's summer shade. Young trees would lose even more, but here I compare mature sizes."

**3. The optimised layout (45 s)**
`[DO]` Click "Optimised". Point at "vs random".
**SAY:** "Now the tool picks the species for each position. For every position and every species it has pre-computed the summer shade on pedestrians, the winter shade, and the rain the crown would hold over ground that drains to a flood hotspot. A linear program then finds the exact best combination under the 15% cap and the façade clearance. Same species, same positions: 16% more summer shade than random."

**4. Why winter matters (45 s)**
`[DO]` In the triangle, click the dot halfway between "winter sun" and "runoff" (winter 0.5, runoff 0.5). Map layer → "Winter sun". Month slider → January. Click a Pyrus in a sunny street, then a Brachychiton in a shaded one.
**SAY:** "Shade is not always good. In January people want sun. When I ask for it, the tool puts the winter-bare Pyrus in streets that get sun 78% of the winter hours, and the evergreen Brachychiton where buildings already block it: 31%. It found that from the geometry; nobody told it. It is a tendency, not a rule: the winter-bare Styphnolobium also ends up in shaded streets."

**5. The trade-off (45 s)**
`[DO]` Point at the trade-off chart, then click the summer-only dot and the balanced dot in the triangle.
**SAY:** "Each dot is the optimum for a different set of priorities. From 'summer shade only' to 'balanced', winter shade drops by only 2%. We first measured 9%, until dated photos from Barcelona showed that Jacaranda keeps most of its leaves in January; the tool lets one data check change a recommendation. Beyond that point it is a real trade-off: asking for winter sun brings in the winter-bare Pyrus and Styphnolobium, and costs roughly as much summer shade, in percent, as it saves winter shade. The designer has to choose."

**6. Live design (30 s)**
`[DO]` Click an empty spot in the triangle; untick one species; tick the diversity floor.
**SAY:** "The designer can set their own priorities, exclude a species, or require a minimum diversity, and the layout is re-optimised in the browser in under a second, or a few seconds with the diversity floor. These live values are estimates; the exact ones come from the Python core."

**7. Honest close (15 s)**
**SAY:** "Two limits. Heat is a shade proxy, which I will calibrate against Ladybug UTCI. And for flooding, street trees remove only about 2% of runoff in a 2-year storm, the same order as field studies, so the tool's job there is to put the trees where the water goes, not to replace the sewer."

## 20. Technical walkthrough (≈ 3 min, for the tutor or a technical jury)

**SAY, step by step (show `notes/figures/tool_v0.png` or the package map in §1):**
1. "Everything sits on a 1-metre grid of Porta: roofs, sealed and green ground with curve numbers, LiDAR terrain and building heights, and the flood-hazard hotspots."
2. "For water, I route surface flow over terrain plus buildings with Priority-Flood. Ground whose runoff reaches a hotspot within 100 metres counts; 100 metres is an assumption standing in for sewer inlets."
3. "For heat, I compute the sun for a July and a January design day, mark where buildings leave pedestrians in the sun, and cast each crown as an ellipsoid with Beer–Lambert opacity from its LAI, or 35% when it is leafless. The heat objective we decided is mean UTCI from 12 to 17 h on a hot design day; aligning the proxy's window to it is part of the Ladybug calibration."
4. "Runoff is a canopy bucket of 1.75 millimetres per unit LAI, calibrated on open field data, then the SCS curve number, season-weighted because 78% of intense storms fall from May to October."
5. "Per position and species, these give three potentials. The optimiser is a weighted-sum transportation LP solved exactly with HiGHS, with the 15% cap, façade clearance and an optional Shannon diversity floor. Fifteen weight sets trace the front."
6. "Every layout is then re-scored with the full raster models, with crown overlaps. Sensitivity over eight variants: the 16% summer gain and the summer–winter trade-off are robust; the free winter gain shrank from 9 to 2% with the photo-based leaf calendar and is not robust."
7. "Next: calibrate the proxy on Ladybug UTCI in a sub-area, test the 100-metre capture distance, add a species storage factor and young versus mature crowns, then transfer to Sant Antoni and Florence."

## 21. Questions you will get, and short answers

| Question | Answer (≈ 20 s) |
|---|---|
| Why not compute UTCI directly? | Too slow in the loop (Ladybug: 20–25 min per layout for 42 trees, Shaamala et al. 2025). The proxy ranks layouts; Ladybug checks the final ones and calibrates the proxy. |
| Is the proxy valid? | Not yet calibrated: that is the next step (Tier 1 UTCI on a sub-area). Its parts are standard (sun geometry, Beer–Lambert with k = 0.5 as Peng et al. 2026). |
| Why a weighted sum and not NSGA-II? | For a linear problem it gives the exact optimum in seconds and is repeatable. NSGA-II stays for later, if the front has gaps a weighted sum cannot reach. |
| Doesn't it just pick the biggest trees? | With shade and runoff only, almost: in the first run (no winter objective) every weight gave nearly the same big-crown layout, and the front collapsed to a point. Winter sun is the criterion that makes leaf habit and position matter. |
| Runoff hardly changes: why keep it? | It is honest: trees remove ~2% at T2-60, the same order as field studies (3.5–4%). The method keeps it so the trade-off is visible, and targets hotspots. Tree pits (infiltration) are the next lever and are not modelled yet. |
| Does hotspot runoff follow the runoff weight? | In the 15 Oct run mostly yes (Spearman −0.73), in the 8 Oct run no; it only varies 0.5%, so the per-position water potential is still unverified (suspects: overlap with kept trees, the box filter). |
| Your first result changed: why trust it? | That is the point of the sensitivity runs. The leaf state of Jacaranda was the uncertain input; 170 dated Barcelona photos fixed it, the free gain shrank from 9% to 2%, and the robust results kept their sign and rough size (summer gain vs random +14 → +16%; trade-off −11% winter for −16% summer → −20% for −18%). |
| Does the proxy match the decided heat metric? | Not yet: the metric is mean UTCI over 12–17 h standard time (13–18 h CEST) on a hot design day (decided 19 Oct); the proxy uses 15 July 12–17 h CEST. Aligning the window and calibrating on Ladybug Tier 1 is the next step. |
| Where do species values come from? | LiDAR crowns of real trees of each species in Barcelona (medians); leaf calendars from sources per species; class defaults marked ASSUMPTION. |
| Young trees? | Not in v0: crowns are mature medians. Runoff v1 shows young replacements lose ~37% of today's street-tree runoff benefit; a young/mature horizon is planned. |
| Does it work elsewhere? | The core is site-agnostic: a new site needs a data adapter (`build_<site>`, `trees_<site>`). Validated only for Porta; Florence is the transfer test. |
| What about diversity, pests, allergens, roots? | 15% cap and optional Shannon floor now; species can be excluded in the web app. Pests, allergens, roots and paving are not scored. |

**Limits to say first (tool-specific)**
- Heat = shade proxy, not UTCI; no transpiration cooling; the summer window (15 July, 12–17 h CEST) is not yet aligned with the decided metric (12–17 h standard time = 13–18 h CEST, on a hot design day).
- Runoff = event volume only: no sewer, no ponding, no peak flow; same storage per LAI for every species; tree pits not modelled.
- LiDAR LAI proxy is uncalibrated and probably low → storage underestimated.
- Potentials ignore crown overlaps (fixed by re-scoring, but the hotspot-runoff mismatch remains).
- Façade clearance has no margin; no sidewalk or utilities data.
- Mature crowns only.

---

## Glossary (tool terms)
| Term | Meaning |
|---|---|
| Site bundle | All site rasters on one 1 m grid, cached in `cache/site_<name>.npz` |
| Priority-Flood | Flow routing that fills pits while flooding from the edges, so every cell drains somewhere |
| Water convergence | Upstream open area draining through a cell (m²) |
| `CAPTURE_M` | Max flow distance (100 m) for runoff to count towards a hotspot |
| Effective shade (m²·h) | Opacity × shadow area on sunlit open ground, summed over design hours |
| Beer–Lambert | Light through a canopy falls as exp(−k·LAI) |
| `OP_BARE` | Share of sunlight blocked by a leafless crown (0.35) |
| Leaf factor | Share of full-leaf LAI in a month (or season-weighted over storms) |
| Canopy bucket | Crown storage S = s·LAI mm, filled before rain reaches the ground |
| SCS curve number | Empirical runoff equation: CN 98 sealed, 74 pervious |
| Potential | What one species alone gives at one position (shade or water) |
| Transportation LP | Assign each position one species, under per-species caps; exact optimum |
| Weighted sum | One score from the three normalised objectives and the designer's weights |
| Effective species | exp(Shannon H): the number of equally common species with the same diversity |
| Pareto front | Layouts that no other layout beats on every objective |
| Re-scoring | Evaluating a chosen layout with the full raster models, overlaps included |

## Key numbers (tool)
| Number | Value | Source |
|---|---|---|
| Street trees in Porta / with LiDAR crown / plane positions | 2,825 / 2,600 / 832 | `exchange/README.md` |
| Grid | 1 m, EPSG:25831, 83.7 ha | `notes/methodology.md` §4b |
| Roofs / sealed / pervious | 29% / 52% / 19% | same |
| Design storm T2-60 | 31.9 mm | `databases/barcelona/pdisba_idf_city.csv` |
| Canopy storage | s = 1.75 mm per unit LAI | `notes/methodology.md` §4b |
| Street-tree runoff reduction (T2-60) | 1.85% | same |
| Intense storms in May–Oct | 78% | `shade_sponge/README.md` |
| Weight sets / random layouts | 15 / 10 | `shade_sponge/__main__.py` |
| City palette | 7 species (6 named by the city + Styphnolobium) | `shade_sponge/layout.py` |
| Balanced vs random, summer shade | +15.9% | `shade_sponge/README.md` |
| Free winter gain (summer-only → balanced) | −2.3% (was −9% with the old leaf calendar; not robust across variants) | same |
| Trade-off, winter-heavy vs balanced | −20.4% winter shade for −18.0% summer shade | same |
| Barcelona balanced vs mature planes, summer | +0.9% | same |
| Diversity floor N = 10, cost in summer shade (Barcelona balanced) | 2.0% | same |
| Live LP in the browser | ~0.1–0.3 s | `web/README.md` |
