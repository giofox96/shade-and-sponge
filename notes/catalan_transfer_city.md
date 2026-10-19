# The Catalan fallback transfer city: screening of 18+ municipalities

*18 Oct 2026; design rainfall added 19 Oct (§5b). Fallback to Florence (`notes/firenze_lidar_request.md`), whose point cloud must be requested. Criteria and their severity order from `notes/transferability.md` §2–3. Everything below was established by opening the document, the API or the point cloud itself; status marks as in the inventories.*

## Verification status (18 Oct 2026) — READ FIRST
A six-domain adversarial fact-check was run in full (two domains first, four after the account limit reset). Outcome per section:

| Section | Status |
|---|---|
| §0, §2 — ACA pluvial | ✅ **verified.** All 40 per-city figures reproduce exactly against Annex 8 Taula 1 and Annex 6 Apèndix. Nine framing corrections applied |
| §1 — LiDAR flight dates | ✅ **verified and independently reproduced.** Badalona re-clipped at six separate spots: 100% 2021-09-26, ASPRS-classified, 11.1–14.8 pts/m². **But two rows were mislabelled** (Castelldefels/El Prat, Figueres) and the sampling caveat is now stated honestly |
| §3 — tree inventories | ⚠️ **corrected.** Badalona and Reus are *not* unreachable; "verified absent" held for only 8 of 11; the "never geometry" claim was too strong |
| §4 — dual hazard | ⚠️ **corrected.** A wrong rainfall figure, two merged Badalona events, and Badalona's 2025 event re-measured as a low-intensity winter frontal event |
| §5 — policy drivers | ⚠️ **heavily corrected.** The DIBA/Santamour attribution was wrong, Sabadell's figures are a conference deck not an approved plan, Girona's denominator was wrong |
| §6 — recommendation | ❌ **re-derived twice.** Badalona no longer leads; after §5b, Mataró leads outright |
| §3b — Mataró tree data | ⚠️ **verified first-hand, but NOT second-passed.** The independent fact-check could not run (account session limit). Everything load-bearing was checked directly — the GeoPackage queried, the geojson profiled, both table pages read, the four arithmetic checks, the `capes.js` wiring and the `mataro.cat/ca/legal` text — but this section has not had the adversarial second reading that corrected §5b. **Second pass completed 19 Oct**: the arithmetic held (all 59 page-33 rows re-read, the GeoPackage, geojson and overlap numbers reproduced), but it corrected the OSM claim, the Escapos framing, the inventory-universe comparison and four wording errors, all applied below |
| §5b — design rainfall | ✅ **verified, then fact-checked a second time (19 Oct).** All Mataró and Barcelona figures reproduce against PDCLAM '03, the 1999 monograph and the repo's PDISBA table; the Meteocat, XEMA and CAUMAX bullets were re-derived independently. **Six corrections applied**: the duration-factor attribution (the "two" formulas are the same formula), "no extrapolation", the T = 1 scope, the climate-uplift claim, the daily-basis gap, and the method/climate share. Two unsourced claims removed |

**§1, §2 and §5b are citable to the tutor. §3–§6 are now corrected but thinner than the first draft claimed.**

*One caveat even in §5b: Barcelona's daily quantile comes from the 1999 monograph's SQRT-ET max table while Mataró's is Gumbel, so the harmonised comparison is like-for-like in its duration factor but not in its frequency law. Stated in §5b; not yet fixed.*

## 0. The headline, including the bad news
**Criterion 2 fails for the whole of Catalonia.** The ACA's 3rd-cycle pluvial product, approved 15 July 2026, is a **list of 44 municipalities** whose ARPSI polygon **is the administrative boundary** — Annex 8 §3.3, verbatim: *"les ARPSI pluvials no es defineixen a partir de criteris hidrològics (conques) o hidràulics (eixos de drenatge), sinó a partir dels límits administratius del municipis"* (the missing *s* is the source's own typo) — with no extent, no depth and no return period. No 3rd-cycle MAPRI exists — ACA says MAPRI and PGRI *"es troben actualment en fase d'elaboració"*; a 2027 date for homologated **inundable-zone** (not pluvial) cartography comes from press coverage of a parliamentary committee statement of 12 Nov 2025, **not from any ACA document**. The one pluvial ARPSI that ever had a modelled depth map (CRT Vila-seca i Salou, 8.54 km², HEC-HMS 3.3 + IBER 2.2) is **proposed for deletion** in the APRI phase, though its maps still stand. The **2018 (2nd-cycle)** fluvial-pluvial classification rested on a quantitative layer — the ZDD, *zones de dificultat de drenatge* — taken from an *"estudi inèdit de TRAGSATEC"* and never published (2nd-cycle APRI Annex 05 §3.2.1 and footnote 4). The 3rd cycle instead derives its "Pluvial-fluvial" typology simply from the presence of a fluvial TRI.

**So Barcelona's RESCCUE depth model is the only city-wide pluvial depth model found in Catalonia**, and no Catalan transfer city can reproduce the hotspot-targeting half of the method from open data. (The one other published ACA pluvial depth product covers **8.54 km² at the CRT Vila-seca i Salou** — MAPRI 2019, with modelled depth classes <40 cm / 41 cm–1 m / >1 m from IBER 2D — and it remains **current**, since no 3rd-cycle MAPRI exists to supersede it; Annex 8 only *proposes* deleting the ARPSI. Mataró's municipal drainage model is reported to exist but is not open.) That is itself a finding for the thesis: it sharpens why Porta was the right calibration site, and it is a concrete instance of the transferability argument.

The 44-list is still worth a lot: it is an authoritative, euro-quantified **pre-filter** with per-municipality damages and two risk indices, and a citable justification that pluvial flooding is a real municipal problem in the chosen city.

**Recommendation: Mataró** (§6), on three independent pillars — it is in the ACA 44, it has a leaf-on classified cloud, and after the 19 Oct design-rainfall check (§5b) it is the only finalist with a **published city design storm**. One user-side check remains, on its tree inventory.

## 1. LiDAR flight dates and classification — the most valuable result
Criterion 1 decided more here than anywhere else, and it could be settled **exactly**. The ICGC per-sheet metadata carries only the flight *year*, but every point stores absolute GPS time. Via the ICGC's own clip service the screening read the per-point date and classification over 22 city centres. **Control: the Porta clip returned 2021-09-26 for 100% of 867,739 points, reproducing the date the repo had already derived independently** (`databases/data_inventory_barcelona.md` §G) — so the method is cross-checked against our own ground truth.

Density is given excluding the class-12 overlap strips, comparable to Porta's ≥8 pts/m².

| City | Flight date | Leaf-on? | Classified | pts/m² |
|---|---|---|---|---|
| **Badalona** | **2021-09-26** | ✅ **same mission as Porta** | ✅ | 12.3–15.7 |
| **Santa Coloma de Gramenet** | **2021-09-26** | ✅ same mission as Porta | ✅ | ~12 |
| **Sant Cugat del Vallès** | **2021-09-26** | ✅ same mission as Porta | ✅ | 13.5 |
| Reus | 2021-09-17 (+ 08-01 south) | ✅ | ✅ | 11.8–14.1 |
| Vilanova i la Geltrú | 2021-08-01 | ✅ | ✅ | 12.0 |
| Tarragona | 2021-07-27 | ✅ | ✅ | 11.7+ |
| Igualada | 2021-07-21 | ✅ | ✅ | 12.3 |
| **Terrassa** | 2021-07-20 | ✅ | ✅ | **14.2–17.9 (densest sampled)** |
| **Sabadell** | 2021-07-20 | ✅ | ✅ | 10.3–14.0 |
| **Mataró** | 2021-07-20 | ✅ | ✅ | ~12.5–13.6 |
| Rubí | 2021-07-20 / 09-26 split | ✅ both | ✅ | ~12 |
| Granollers | 2021-06-26 / 07-20 split | ✅ both | ✅ | ~12 |
| Tortosa | 2021-07-19 | ✅ | ✅ | 11.9 |
| L'Hospitalet de Llobregat | 2022-06-01 | ✅ (different year) | ✅ | 11.7 |
| Cornellà de Llobregat | 2022-06-01 | ✅ (different year) | ✅ | 12.7 |
| Lleida | 2022-05-23 | ✅ (different year) | ✅ | 14.3 |
| **Castelldefels** | 2022-10-01 | ✅ **leaf-on** (corrected) | ✅ | 12.8 |
| El Prat de Llobregat | 2022-10-01 | ✅ leaf-on (corrected) | ✅ | 12.1 |
| Girona | 2021-08-26 | ✅ by date | ❌ **unclassified in the clip** | — |
| Vic | 2023-07-19 | ✅ by date | ❌ unclassified in the clip | — |
| Manresa | 2021-11-18 | ❌ **leaf-off** | ❌ unclassified | — |
| Figueres | 2021-04-24 (+ a second mission 2021-05-04) | ✅ leaf-on for 6 of 8 palette species | ❌ **unclassified — this is what excludes it** | — |

**Two corrections the fact-check forced, both from the project's own tables.** "Marginal" was wrong for the 1 October 2022 flights: `databases/traits/phenology_palette.csv` gives **m10 = 1 for all eight palette species** (only November drops to 0.5), and `databases/barcelona/storm_months.csv` puts **October at 22% of intense convective days, the second-highest month**. So 1 October is full leaf-on *and* inside the storm season by our own sourced data. That mislabel is load-bearing: it is what kept **Castelldefels** — the second-highest-damage municipality in §2 — out of the shortlist. Its real criterion-1 cost is only the flight *year* (2022 vs 2021). Likewise Figueres is excluded by its **unclassified** return, not by phenology (m04 = 1 for six of the eight palette species).

**Sampling caveat, stated honestly:** this table is built from **one 150×150 m clip per city** (two for Reus), i.e. 0.0225 km² samples in municipalities of 10–100+ km², through the ICGC clip service rather than the published `datacloud` tiles, and the coordinates and script are not yet committed. The table's own data shows why one spot is not a city: Rubí and Granollers split missions *inside a single clip*, Reus splits over ~1 km, a second Figueres clip adds a mission, and a mission boundary runs through Porta's own tile (see the §G correction in `databases/data_inventory_barcelona.md`). Read the column as **"flight date at the sampled city-centre clip"**. Before relying on it for the chosen city, download the actual 1×1 km LAZ over the study district and histogram date and class over the full extent.

**The control is weaker than first stated:** the Porta clip was reported as "100% of 867,739 points", but the stated origin box yields 445,319 and no clip extent was recorded, so the figure cannot be re-derived. What does hold: the Porta polygon plus buffer returns 2021-09-26 across eight clips, agreeing with the date the repo derived by a different delivery route from the same ICGC product — agreement, not independence.

## 2. The ACA 44 (criterion 2 pre-filter)
Source: ACA, *Revisió i actualització de l'APRI del DCFC — 3r Cicle, Annex 8*, v3, Taula 1 pp. 8–9, `https://info.aca.gencat.cat/ca/aca/informacio/web/plans-programes/PGRI/3cicle/APRI/ca/01_08_00_Annex_8_ARPSI_Pluvials_v3.pdf` (accessed 18 Oct 2026); damages and IRM values from Annex 6, Apèndix Taula 1, `.../01_06_01_Annex_6_AP_Proposta_incorporacio_municipis_v2.pdf`.

**Selection required three things, not one:** flood damages ≥ €500,000 in 2005–2023; a determination that the origin was **pluvial rather than fluvial**; and a **DGPC obligation to hold a municipal flood action plan (PAM)** — the third gate is why several high-damage municipalities are absent. Viladrau and Riells i Viabrea were admitted despite failing it.

Rows below are sorted by **recorded damages**, which is ACA's own highest-weighted criterion (Annex 6 §4d). **IRM AMC = 0 does not mean low risk**: it means no indirect hazard indicator passed its threshold and the municipality is not among the 146 above ACA's risk threshold. ACA ranks this index the *most uncertain* of its three and weights it *least*.

| In the 44 | ARPSI code | Type | Damages 2005–23 | IRM AMC |
|---|---|---|---|---|
| **Tarragona** | ES100P080_010 | Pluvial-fluvial | **€44,302,252** | 0 |
| Castelldefels | ES100P800_010 | Pluvial | €6,826,265 | 23.68 |
| Reus | ES100P913_010 | Pluvial-fluvial | €5,102,433 | 37.73 |
| Rubí | ES100P200_080 | Pluvial | €4,935,265 | 0 |
| Terrassa | ES100P200_070 | Pluvial-fluvial | €2,424,305 | 93.98 |
| Sant Cugat del Vallès | ES100P060_060 | Pluvial | €2,052,625 | 31.47 |
| Sabadell | ES100P060_040 | Pluvial-fluvial | €1,661,493 | 67.80 |
| Manresa | ES100P200_020 | Pluvial-fluvial | €1,415,038 | 36.00 |
| **Mataró** | ES100P700_030 | Pluvial-fluvial | €1,363,419 | 32.09 |
| **Badalona** | ES100P700_050 | **Pluvial** | **€658,154 — the lowest here, just over the €500k threshold** | 100.00 (the scale maximum) |

**Not in the 44:** Girona, Lleida (outside the ACA district entirely — Ebro/Segre), Santa Coloma, L'Hospitalet, Cornellà, Vilanova, Granollers, El Prat. ACA types Girona's and L'Hospitalet's risk as **fluvial**.

## 3. Open tree inventories (criterion 3)
**Found and opened — six municipalities:** Girona (**32,824 trees, 181 scientific names, CC BY, annual series 2014–2025** — the cleanest in Catalonia), L'Hospitalet (37,947 trees, 224 species, but **CC BY-ND**), Lleida (41,270, 233 name values, a `VIARI` street flag and height/perimeter classes, **no licence stated**), Sant Boi (18,728, 202 species, CC BY-NC-ND), Manlleu (5,822, CC BY 4.0), Olesa de Montserrat (4,617, licence unspecified).

**Not published in the catalogues queried — eight confirmed, three not:** confirmed by full AOC package listings (Tarragona 40 datasets, Santa Coloma 34, Vilanova 41, Granollers 18, Manresa 59, Rubí 30, Castelldefels 25, El Prat 39) plus zero public ArcGIS Online items. **Untested:** Sant Cugat (only 2 datasets on AOC, so absence proves nothing), **Terrassa** (its portal is Cloudflare-blocked, so the "126 datasets federated" claim is unverified) and Cornellà. Note this means "not in the catalogue I queried", **not** "the municipality holds no inventory".

**Corrected after fact-check — only two are actually unreachable.** **Mataró** and **Sabadell** are proxy-blocked. **Mataró is now largely resolved — see §3b**: its species composition and its tree positions are both published, but in two separate files, and the joined per-tree table sits on the one host this container cannot reach. **Badalona and Reus are reachable**, and the answer for Badalona is now a near-negative rather than an unknown: its public GeoServer lists **161 WMS layers with no tree or green layer**, it has **no AOC CKAN organisation**, and `www.badalona.cat/dades-obertes` returns 404 (not the 403 recorded earlier), while its `seu-e.cat` page answers 200. So: **no open tree inventory found for Badalona.**

**No numeric DBH and no crown diameter anywhere**, and only Lleida has a height attribute — but three of the six do carry a **coarse size class**: Girona's `mida_tronc` is a trunk-perimeter band (20–50 / 50–80 / 80–120 / >120 cm; n = 12,662 / 11,276 / 6,498 / 2,313), Sant Boi has `MIDA` (petit/mitjà/gran/exemplar) plus a growth stage, Lleida a perimeter class 0–4. The conclusion survives in its proper form: **the point cloud stays the binding input for LAI and crown geometry at every site**, because a size band cannot give either.

## 3b. Mataró's tree data — criterion 3 reopened and largely resolved (19 Oct)

§3 recorded Mataró as **proxy-blocked, therefore unknown**. That was right at the time and is now superseded.
A six-route sweep found that **Mataró's data is split in two**, and the split is what matters:

| Asset | Species? | Coordinates? | Records | Verified here |
|---|---|---|---|---|
| Pla Director de l'arbrat viari, Nov 2016 | ✅ Latin binomial | ❌ none | **17,204 street trees, 117 species** | ✅ opened, four checks |
| ICGC *Referencial Topogràfic Local* 1:1000, **2D** edition (GeoPackage) | ❌ **none** | ✅ EPSG:25831 | **79,748 tree points** | ✅ downloaded, queried |
| `melia.geojson` (allergy-map extract) | ✅ | ✅ WGS84 | **1,064 trees, one species** | ✅ downloaded, profiled |
| `T_C_ARBRAT` (ORDS REST, the joined table) | ✅ | ✅ | unknown | ❌ **host unreachable from here** |

**The joined inventory exists** — verified first-hand in the viewer's own source. `GeoMat/visor/js/parts/capes.js`
line 8254 reads `afegirCapaServeiWeb("https://apex.mataro.org/ords/sig/geodades/T_C_ARBRAT", …)`, and that function
(line 545) fetches with a plain `$.getJSON` and parses the response through `new Wkt.Wkt()` — **no key, no auth
header, WKT geometry**. Line 8244 wires the monumental-tree layer the same way. From this container the request dies in a tunnel failure (`ws_closed_mid_exchange`,
1006 after ~13 s), so its contents and field list remain **unknown**. Two honest limits on that sentence: the
same failure kind was logged the same day for several hosts that are certainly up, so it is **evidence of a
relay-side failure, not evidence that Mataró is serving**; and `apex` is not uniquely unreachable —
`adminweb.mataro.cat` was refused by policy and `datacloud.icgc.cat` also failed, while `www.mataro.cat` and
`serveisweb.mataro.cat` both answer 200. "No key" is verified from the client code; **"public" is an inference**
— nobody has received a response, and the endpoint could be referrer- or session-scoped. Nobody has seen
`T_C_ARBRAT`'s schema.

**What was verified first-hand in this session**, not taken from an agent report:
- **The GeoPackage.** `gpkg2d.zip` (92 MB, Last-Modified 14 Oct 2026) → `topografia-local-v1r0-mataro-2d-2022.gpkg`.
  Layer `_260_cobertes_sol_n`: **79,748 rows, all `tipus='arb'`**, and the columns are exactly
  `id, geom, tipus, nivell, visible` — **no species, no height, no DBH**. All **24 feature layers** are
  **EPSG:25831, the same CRS as Porta** (the other 35 tables are non-spatial lookups). Also present for the DTM:
  `_280_relleu_n` 114,317 relief points, `_580_relleu_l` 44,532 contours. One caveat before relying on
  completeness: **every one of the 79,748 tree rows carries `nivell = 'nec'`**, which the file's own lookup
  decodes as *"no contemplat en l'encàrrec"* — not covered by the survey commission. The field is not a constant
  elsewhere (`_280_relleu_n` splits 72,695 `nap` / 41,622 `nec`).
- **The 1,064-tree joined sample.** 1,064 `Melia azedarach` points, CRS84, with `TIPUS_UG` = **Viari 822 /
  Zona verda 242** (an explicit street-vs-park flag), `CATEGORIA` trunk-girth band, `ESTAT` condition, street and
  neighbourhood. `ALCADA` is null throughout, and `DIAMETRE`, `PERIMETRE` and `ALCARIA` are **zero-filled** — present as columns, carrying no measurement.
- **The 2016 composition table**, pp. 33–34 → `databases/mataro/mataro_street_tree_species_2016.csv`. Page 34 came
  from the PDF text layer; page 33 is a raster, so species and counts were transcribed from a 190 dpi render and
  the green/yellow/red suitability column was sampled programmatically at 300 dpi. Four independent checks, all
  exact: units **16,338 + 866 = 17,204** (the plan's printed Total); **59 + 58 = 117** species (its stated count);
  suitability **15 apte / 51 restriccions / 51 evitar** (its stated split); and every row's percentage equals
  units/17,204. Note the 117 are **table entries including cultivars** (and the plan itself says two are repeated);
  merged to parent binomials they are **108 distinct species**. The colour sampling corrected two rows a visual read had wrong (*Populus simonii* and
  *Olea europaea* are `evitar`, not `restriccions`).

### Where to re-download these (nothing large is in the repo)

The two reachable assets were opened in a cloud container and are **not** committed — only the derived CSVs are.
To get them on a local machine:

| Asset | URL | Size |
|---|---|---|
| ICGC RTL 1:1000 **2D** GeoPackage (79,748 tree points + relief + contours, EPSG:25831) | `https://serveisweb.mataro.cat/visorSIG/images/RecursosVisor/SSIT/minisite/descarrega_productes/Cartografia_Topografica_1_1000_3D/gpkg2d.zip` | 92 MB zip → 215 MB `.gpkg` |
| 3D edition of the same (not opened here) | same path, `gpkg3d.zip` | ~270 MB |
| `melia.geojson`, the 1,064-tree joined sample | `https://serveisweb.mataro.cat/GeoMat/visor/geojsons/arbrat_alergies/melia.geojson` | 759 kB |
| PDCLAM '03 sewer master plan (the IDF table, §5b) | `https://oficinavirtual.aiguesmataro.com/api/doc/F2104/pla-dir-clavegueram` | 676 kB, 71 pp |
| The viewer source that wires `T_C_ARBRAT` | `https://serveisweb.mataro.cat/GeoMat/visor/js/parts/capes.js` | 410 kB |

The 2016 *Pla Director de l'arbrat viari* PDF (the composition table) was found through the mataro.cat site
search; its extracted table is committed as `databases/mataro/mataro_street_tree_species_2016.csv`, so the PDF
itself is only needed to re-verify a row. Raw downloads belong in a gitignored `databases/mataro/raw/`.

### Species overlap with Porta — Mataró beats Florence

Running Mataró through the existing `scripts/transfer_species_overlap.py` (top-30, same `MIN_N = 5` bar):

| | species matched | on ≥ 5 Porta trees | genus matched |
|---|---|---|---|
| **Mataró** | 20 species, **63.6%** | **52.2%** | **92.9%** |
| Florence | 15 species, 63.5% | 43.5% | 74.0% |
| Barcelona (ceiling) | 27 species, 97.9% | 90.5% | 97.9% |

The headline species line up closely: *Platanus* × *acerifolia* 21.4% of Mataró's **identified** street trees (20.85% of the full 17,204, the plan's own printed figure) against 29.3% of
Porta's, *Celtis australis* 10.9% against 10.5%, *Melia azedarach* 5.9% against 5.9%, *Tipuana tipu* 4.9% against
4.9%. Largest gaps where Porta has not even the genus: *Washingtonia filifera* 2.0%, *Albizia julibrissin* 1.3%,
*Quercus ilex* 1.0%. **Mataró looks the better transfer on this measure — but the margin is inflated and must not
be quoted bare.** The three inventories are not the same universe: Mataró's 17,204 and Barcelona's 140,404 are
**street trees**, Florence's 82,226 is **all public trees, parks included**. Porta, the reference, is street trees.
So Mataró is compared like-for-like and Florence is not: its top-30 is diluted by park and landscape species, and
its two largest genus gaps — *Quercus ilex* 8.5% and *Olea europaea* 6.2% — are exactly the species a Mediterranean
park contributes and a street does not. The direction of the conclusion probably survives; **the size of the gap
is not measured**, and closing it properly means extracting Florence's street subset.

**A second caveat on the species shares.** These are the **2016** street figures. A **2024** composition exists
(PDIVM Diagnòstic, Safetree data, ~25,300 trees, all trees rather than street-only) and differs materially:
*Platanus* × *acerifolia* **16.4%** (4,145) rather than 21.4%, *Celtis australis* 9.3% (2,340), and *Pinus pinea*
(1,705) and *Quercus ilex* entering the top ten. The 2016 plan is the right universe for a street-to-street
comparison with Porta, so it is used here — but the "headline species line up closely" claim rests on the 2016
shares, and the 2024 numbers move the largest of them by five points. Say which vintage any quoted figure is from.

### What this means for the module

**It can run — in a degraded form, and the degradation must be declared.** Crown, height and LAI come from the
LiDAR, not from the inventory, and Mataró has leaf-on classified ICGC cover plus 79,748 open positions in Porta's
own CRS. So an S0 baseline is buildable today, species-blind. What breaks without `T_C_ARBRAT`:
1. **Per-tree species** drives `s·LAI` interception and the leaf-on month. Without it, species must be assigned
   probabilistically from the published composition — which turns a *species-level* transfer test into a
   *composition-weighted* one. That is a real loss of independence, and an `ASSUMPTION` to label as such.
2. **No usable numeric DBH or height exists for Mataró.** Not in the RTL layer, not in the 2016 plan, and only as a
   4-class band in the Melia extract. OSM is the one partial exception and it is too thin to help: of **6,322
   `natural=tree` nodes** in the municipality, **121 carry a numeric `height`** (values 2–10 m) and 68 a species,
   with **no girth or crown tag at all** — 1.9% coverage on a self-reported field. So the LiDAR crown/LAI proxy
   **cannot be validated against inventory measurements in Mataró**. *(An earlier draft called this "the second
   failure after Escapos" and "a pattern". That is withdrawn — the two failures are unrelated. Escapos does carry
   real `dbh_cm`, `h_m` and `crn_w_m`; only its `lai` column is synthetic. Florence's inventory carries continuous
   trunk circumference, so the crown/height half of the proxy remains validatable there. Two unlike failures are
   not a pattern.)* Worth noting separately: those 6,322 OSM positions, 4,397 of them within 10 m of a street, are
   a **second open positional source** for Mataró.
3. **RTL has no street-vs-park flag**, so the street subset must be derived by buffering the road layer. The Melia
   extract's real `TIPUS_UG` is the obvious way to check that derivation — that is its highest value.

### Licence: UNKNOWN, and the default is unfavourable

**No Mataró dataset carries a verified licence**, and the municipal terms are explicitly restrictive. Read
first-hand at `mataro.cat/ca/legal`: *"no es permet la reproducció parcial o total del portal, ni el seu
**tractament informàtic**, sense el permís previ i per escrit dels seus propietaris"*, and, more decisively,
*"L'Ajuntament de Mataró **no atorga cap llicència o autorització d'ús de cap classe** sobre els seus drets de
propietat intel·lectual o industrial, o sobre qualsevol altre dret relacionat amb el portal o el seu contingut."*
That is not silence about reuse — it is an explicit refusal to grant any licence. The open-data portal is a separate
host whose terms nobody has read. **Do not record CC BY for any Mataró asset.** The composition CSV in this repo is
cited, not redistributed in bulk; before publishing anything derived from the GeoPackage or `T_C_ARBRAT`, get a
licence statement in writing from the Servei de Sistemes d'Informació i Telecomunicacions.

### Open — one browser session in Windows settles it

These are **blocked, not absent** (see `notes/todo_manual.md`):
1. `https://apex.mataro.org/ords/sig/geodades/T_C_ARBRAT?limit=50000` — **the gate**. Does it return one object per
   tree with `ESPECIE` and a WKT point, and are `ALCADA`/`DIAMETRE`/`PERIMETRE` populated for species other than Melia?
2. `https://apex.mataro.org/dadesobertes` — **the licence**, and whether a packaged CSV/GeoJSON exists. Equal priority:
   without it the data is unusable even if it downloads.
3. `https://apex.mataro.org/ords/rest/dobertes/elements` — the dataset-list API; shows what else is published.

If all three fail, the fallback is a data request for the Safetree extract. **Which unit to ask was wrong in an
earlier draft**: the contact block (`bustia@ajmataro.cat`, `planoldelaciutat@ajmataro.cat`, +34 93 758 21 91,
Mon–Fri 08:00–15:00) comes from the *plànols* / GeoMat page footer and belongs to the **Servei en Sistemes
d'Informació i Telecomunicacions**, not the **Àrea d'Ecologia Urbana** — which exists (the PDIVM credits it) but is
not the source of those details. The addresses are real; the attribution was not. Confirm the right unit on
mataro.cat before writing.

## 4. Dual hazard (criterion 4)
No Catalan municipality outside Barcelona has a single document mapping both hazards; the evidence comes from different institutions.
- **Granollers** — strongest heat product: its own ICGC TASI-600 thermal flight (night 27–28 Sept 2021, **4 m pixel**, street-level UHI > 4.5 °C, LCZ layers, two greening simulations). **Rainfall figures corrected** from Meteocat XEMA station YM Granollers (validated daily statistics, dataset `7bvh-jvq2`): 5 Oct 2026 = **108.1 mm, max 30 min 37.7 mm, max 1 h 74.8 mm** — *not* "50 mm in ~30 min". And the episode was **multi-day with antecedent saturation** (83.2 / 164.7 / 108.1 mm on 3, 4, 5 Oct), with the intensity maximum on **4 Oct** (94.1 mm/h, 65.0 mm/30 min). Citing 5 Oct as flash-flood evidence would apply a laxer standard than the one used to disqualify Bologna ("rain on saturated soils, which trees cannot meaningfully affect"); cite 4 Oct, with the saturation caveat. No tree inventory, and not in the 44.
- **Mataró** — the best-balanced dossier: its 2003 *Pla Director de Clavegueram* was written expressly to solve frequent flooding, heat is named in its own PAESC, and 16 Sept 2022 brought 120 mm (90 mm in one hour) — a **leaf-on, high-intensity September** event, i.e. the right kind for this thesis. **Two corrections:** it is **not unique** (Badalona's own *Pla Director de Clavegueram* is under update, with four retention tanks totalling 150,000 m³ and a modelled 523 ha catchment), and it is **not a pluvial hazard model**: PDCLAM-03 §§1.7.3.2–1.7.3.6 describe a **level-III 1D sewer-network model with Keifer-Chu design storms** — pipe capacity, not surface depth or extent. So it does not contradict §0's "only city-wide pluvial *depth* model".
- **Badalona** — **materially weaker than first written.** The heat flight is a **nocturnal December 2017** one (ICGC TASI, 4 m, *Revista Catalana de Geografia* 60, 2020) with **no published UHI magnitude for Badalona**. Two December 2025 events were merged and must be split: **20 Dec 2025** (XEMA WU Badalona-Museu 76.6 mm; 76.4 mm as reported by 3Cat) is the ground-floor and Plaça de la Vila flooding; the **Gorg metro closure belongs to 16 Dec 2025** (45.5 mm). Crucially, re-measured intensity for 20 Dec: **max 1 h = 18.9 mm, max 30 min = 11.1 mm** — a long-duration, low-intensity **winter frontal** event in a **leaf-off** month, against Granollers' 94.1 mm/h and Mataró's reported 90 mm/h. **This is the same season conflict that downgraded Lisbon in `notes/city_transfer_candidates.md`**, and it applies to Badalona too.
- **Sabadell** — heat mapping only, from a nocturnal **December 2017** flight. On the pluvial side: no city-specific pluvial study or drainage model located, **beyond its ACA standing recorded in §2** (ES100P060_040, Pluvial-fluvial, €1,661,493, IRM AMC 67.80) — and since ACA selection required a DGPC obligation to hold a municipal flood action plan, "no pluvial evidence" would contradict §2 and is withdrawn.
- Heat only: L'Hospitalet, Cornellà, Manresa. Pluvial episodes only: Tarragona, Vilanova. Nothing found: Reus, Lleida.

## 5. Policy driver (criterion 6) — stronger than expected
**Corrected after fact-check — the earlier framing was wrong three ways.** The DIBA *Guia per a la selecció d'espècies de verd urbà: arbrat viari* (2012, 135 pp) **never mentions Santamour, 10%, or the 10-20-30 rule**. Its only threshold is a **non-binding "criteri de referència"** of *"un percentatge raonable d'un 15%"* for one species in a municipality's **whole tree inventory** (not street trees as a separate denominator), and the same section calls diversity *"una estratègia de supervivència del sistema o com un recurs del disseny més que el producte d'una norma"*. Nothing links Barcelona's own 15% cap (Pla director de l'arbrat 2017–2037) to that guide, so **"provincial guidance" asserted a lineage with no source**. DIBA's remit is also the **province of Barcelona only**, so it cannot reach Girona — whose 2025 plan explicitly rejects a uniform 15% (*"es proposa per al conjunt de la ciutat imposar la proporció 5-10-15"*). And DIBA does **not commission** tree master plans: its 2026 *Catàleg de serveis* offers applied-for technical support, preferentially to municipalities over 10,000 inhabitants. The Santamour lineage belongs where the municipal plans actually cite it: L'Hospitalet (1990) and Girona (1991).

- **Sabadell — still the closest match, but it is a proposal, not policy.** The source is a **33-slide conference deck** (Parcs i Jardins, APEVC, 18 Feb 2021); **no plenary or Junta de Govern approval is traceable**, so it *proposes* rather than caps or commits. It states the objective *"que cap espècie superi el 15% del total"*, records **Platanus at 23.95% of 30,238 street trees**, and would reduce the remaining plane alignments from 13.95% to **5%**. **The "~2,700 positions" figure is derived, not stated, and rests on an assumption:** 2,706 = (13.95% − 5%) × 30,238 reads those percentages as shares of *all street trees*, but the slide labels them *"del total de plàtans"* — on the literal reading the figure is **≈ 650**. Same for "17 historic plane axes = 10% of the stock": the deck says *"10% del total de plàtans"*. What stands unqualified is the useful part: its municipal 16-parameter, 74-species *índex d'idoneïtat* scores shade only as a qualitative class and contains **no interception, runoff or thermal-comfort metric at all** — precisely the gap this thesis fills.
- **L'Hospitalet** — the only formally approved one: *Pla Director del Verd Urbà 2018–2028* (532 pp, Junta de Govern Local, April 2019), states the 15% maximum, records *Platanus × hispanica* at 17.07% and *Ulmus* at 15.94% of 16,448 street trees (both over the cap). Four of the thesis's seven palette species are already in its top ten.
- **Girona** — newest and most demanding: *Pla Director de l'Arbrat Urbà*, definitive 9 May 2025, imposes 5-10-15 city-wide with 10-20-30 per neighbourhood, restricts *Celtis australis* (its commonest species) and classes **7,497 positions = 20% of the whole inventory** (EV 3,084 / AV 4,413) as Low or Very Low suitability — of which the **4,413 street trees are 32% of the street-tree stock** (13% in green spaces). The earlier note applied the 32% to the wrong denominator.

## 5b. Design rainfall / IDF (criterion 5) — checked 19 Oct, and it decides the city

This was the last open hole in §7. Four routes were checked for both finalists: the ACA, Meteocat, the
municipal drainage master plans, and the Spanish national route. **Mataró has a complete published design
storm; Badalona has none.** That is a third independent pillar for Mataró, and the only one that bears
directly on the runoff module's inputs rather than on its calibration data.

### What each route gives

| Route | Badalona | Mataró | Shortest duration |
|---|---|---|---|
| ACA, *Guia tècnica* 2003 | method only | method only | 1 h published (Fig. 2.18 is dimensionless, 0–24 h, no table). The guide's Tc ≥ 0.25 h floor is a limit on the **rational method** (§3.2c), not on the IDF curve |
| Meteocat *Corbes IDF municipal* | ✅ table, T = 2–500 | ✅ table, T = 2–500 | **60 min** — Meteocat states the method "tan sols permet obtenir la relació IDF a una resolució temporal màxima d'una hora" |
| Municipal master plan | ❌ none public | ✅ **PDCLAM '03, full numeric table** | **5 min** |
| Spanish national (1999 + 5.2-IC) | derivable | derivable | 60 min anchored; below that is extrapolation |

**Mataró — PDCLAM '03** (CLABSA for Aigües de Mataró, 2003, Memòria p. 28) prints intensities in mm/h for
durations 5–120 min in 5-min steps × T = 1/2/5/10/50/100/500/1000, so the module's 10/20/30/60 min grid can be
read straight off a published municipal document, and it goes finer than Barcelona's own PDISBA table, which
stops at 10 min. **This is availability, not independent measurement:** those sub-hourly values are themselves
the Témez extrapolation below the 1 h anchor, pre-computed by CLABSA rather than by us (see the second
constraint below). The plan prints its construction — Gumbel on annual daily maxima (quantiles on p. 26) plus
the Témez/5.2-IC duration factor with I1/Id = 11 — so the curve can be *regenerated* at any duration rather than
interpolated: `scripts/make_mataro_idf.py` reproduces all 48 checked printed cells to within **0.0107%**.
One wrinkle to carry: the plan prints the duration factor with denominator **0.4**, a rounding of the exact
Témez value 28^0.1 − 1 = 0.3954549 (ACA *Guia tècnica* eq. 2.9, citing MOPU 1990). The two differ by 2.2–4.2%,
so whichever is used must be used at **both** ends of any city comparison.
→ `databases/mataro/mataro_idf_city.csv`.

**Badalona has no design rainfall of its own.** Neither its Pla Director de Clavegueram, its memòria nor any
environmental assessment could be found published. (An agent report described the plan as "mid-revision"; no
source on disk supports that, so it is not asserted here.) The one peer-reviewed study of Badalona's own
calibrated 1D/2D model (Martínez-Gomariz et al., *Water* 2019, 11(12):2658, CC BY 4.0, BINGO project) drives it
with **Barcelona's Fabra IDF curves**, justified by proximity. That is a citable precedent, but it makes a
transfer test partly circular: we would be "transferring" to a city whose design rainfall is by assumption the
one we started from. And the candidate values for Badalona's T = 10 / 60 min disagree badly: **38.2 mm/h** from
our own Gumbel fit to its in-town XEMA station, **62.5** if Barcelona's PDISBA is adopted wholesale, and **74.0**
from Meteocat's municipal IDF — a spread of **1.94×** over which there is no principled choice.

### Two constraints this puts on the module

**1. T = 1 yr is not obtainable for any candidate transfer city on any route checked.** Meteocat starts at
T = 2 and the 1999 monograph's Tabla 7.1 starts at T = 2. (Barcelona's PDISBA *does* have a T = 1 column — which
is the problem: the module's cheapest storm is the one no transfer city can match.) And PDCLAM's column headed
"T = 1" is really the Gumbel **T = 1.001** limit (P24h = 13.41 mm, verified against the plan's own quantile
table) — 15.99 mm/h at 10 min against Barcelona's 51.6, i.e. 0.27–0.31× where T = 2 and T = 10 sit at a
plausible 0.68–0.85×. **It must not be fed to the module.** So: either run the transfer test at T = 2 and
T = 10 only, or construct T = 1 for *both* cities from partial-duration series by the same route — never read it
off a published table for one city only. "Not obtainable" means not published; it does not mean underivable.
The CSV encodes that column as `T_years = 1.001`, not `1`, so it cannot be picked up by accident.

**2. Published Mataró numbers must not be put straight next to published Porta numbers.** The two are not the
same kind of quantity:

- PDISBA's `design_intensity_mmh` is an across-gauge **envelope** (at T = 10 / 60 min: design 62.53 vs
  across-gauge mean 50.57 mm/h, i.e. **+24%**), derived from actual pluviograph records. In the repo CSV it is
  `min(max, normal95)` at all 20 rows — an envelope, not a climate adjustment. *(An earlier draft of this note
  said it "carries a climate uplift"; that is withdrawn. PDISBA's climate-adjusted design storms are a separate
  product, per `data_inventory_barcelona.md` §B2.)*
- Mataró's is a **central** estimate: Gumbel on daily maxima from the 1993 preliminary plan *"ampliades amb"* a
  later Maresme *rieres* study, with the sub-daily shape supplied analytically, and the plan states it assumes
  stationarity (*"s'assumeix l'estacionarietat a llarg termini de les mitjanes de precipitació"*). PDCLAM's
  Pd(T10) = 99.28 mm is **15.0% below** Meteocat's 24 h T10 for Mataró (116.8 mm) — but much of that is an
  artefact: PDCLAM's Pd is a **calendar-day** maximum while Meteocat's is a **sliding 24 h** maximum, worth
  roughly 13%, which leaves only ~4% of genuine difference. Do not quote the 15% as ageing.

Compared raw, Mataró looks **19–32%** drier than Porta, and **duration-dependently so** — which reads exactly
like a real climatological difference:

| T = 10 yr | 10 min | 20 min | 30 min | 60 min |
|---|---|---|---|---|
| Mataró published (mm/h) | 118.38 | 82.62 | 66.15 | 44.28 |
| Barcelona PDISBA design (mm/h) | 146.83 | 117.69 | 97.96 | 62.53 |
| ratio, raw | 0.81 | 0.70 | 0.68 | 0.71 |
| ratio, like-for-like | **0.93** | **0.93** | **0.93** | **0.93** |
| of the raw gap, share that is method | 66% | 78% | 80% | 77% |

**Read the bottom rows carefully — the flat 0.93 is not a discovery, it is an identity.** Rebuild Barcelona's
design storm by the same duration factor used for Mataró (from the 1999 monograph's published Barcelona point
values P̄ = 68 mm/day, Cv = 0.46, Tabla 7.1 Yt(0.46, T10) = 1.564) and the duration dependence vanishes
*necessarily*: both cities sit in the same I1/Id = 11 region, so f(D) is literally the same number at both ends
of the ratio and cancels. Any two cities in that region would give a flat line. What the comparison legitimately
shows is the **top** rows — that the raw duration-dependence (0.81 → 0.68 → 0.71) cannot be climate, because a
genuine climatological difference would not reverse direction with duration. It is the estimator mismatch.

On that reading, **most of the apparent gap is method, not climate**: 66% at 10 min, 77–80% at 20–60 min. (An
earlier draft said "roughly two-thirds of the ~30% gap"; that mispairs the numbers — two-thirds holds only at
10 min, where the gap is 19%, not 30%.)

Three consequences, and the last two are uncomfortable:

- **Harmonise before comparing, and say which construction was used** — including which denominator, 0.4 or
  0.3954549, since mixing them reintroduces a 2–4% duration drift that looks like signal. Recommended: rebuild
  Barcelona's storm the Mataró way and run the transfer on that pair, reporting PDISBA as a sensitivity case.
- **The two daily legs are still not the same distribution.** Mataró's Pd is **Gumbel**; the Barcelona Pd above
  comes from Tabla 7.1, captioned *"Cuantiles Y_t, de la Ley **SQRT-ET max**"*. So even the harmonised comparison
  is like-for-like in its *duration factor* but not in its *frequency law*. Fixing this properly means refitting
  Barcelona's daily maxima with Gumbel rather than reading the monograph's table.
- **Under harmonisation the sub-hourly comparison carries no information beyond the daily one.** If f(D) cancels,
  the entire 10/20/30/60 min transfer test reduces to the ratio of daily depths — 0.93 at T = 10, 1.00 at T = 2.
  No sub-hourly observation from Mataró enters anywhere; its shape comes from the single regional constant
  I1/Id = 11. For Barcelona the sub-hourly curve is empirical (pluviograph records, PDISBA §2.6 *"IDF
  empíriques"*); for the transfer city it is an assumption. State this plainly rather than burying it — it is
  one of the most concrete costs of transfer the thesis can name.

*(Note on scope: `databases/barcelona/pdisba_idf_city.csv` is a **city-wide** Barcelona table, not Porta-specific.
"Porta's design storm" throughout this repo means the city curve applied at Porta.)*

### Smaller findings worth keeping

*Provenance: these began as agent reports and were then **independently re-derived in the 19 Oct fact-check** against the Meteocat comarca PDFs, the XEMA station metadata and annual-maxima series, and the CAUMAX v3.0 rasters. They are now verified, with the corrected figures below.*

- Meteocat's municipal IDF tempts you to extrapolate below 1 h with its published β exponent. **Do not.** Tested
  against PDISBA at Barcelona (β = −0.80375, I(1 h) = 63.4 mm), the error is **+1.4%** at 60 min, **+13.0%** at
  30 min, **+30.3%** at 20 min and **+82.3%** at 10 min (T = 10). The method downscales *from* 24 h, so the
  Mediterranean convective sub-hourly peak is not in it.
- **Station coverage favours Badalona**, for what it is worth: XEMA *WU "Badalona – Museu"* sits 0.2 km from the
  centre (0.24 km from Pl. de la Vila; `data_inici` 2005-09-21, so 2006–2025 = 20 complete years), while Mataró's
  own station *YV* only opened **11 Jun 2025** and any Mataró fit needs an inland proxy. This is the one design-rainfall criterion Badalona wins, and it is outweighed by having no
  published design storm at all.
- A **large unexplained discrepancy at Badalona**, and it is real rather than an apples-to-oranges slip: Meteocat's
  municipal IDF gives T10 / 1 h = **74.0 mm**, against **38.19 mm** from a Gumbel fit to its own in-town station
  (XEMA WU variable 1303, *"Precipitació màxima en 1 h (diària)"*, annual maxima 2006–2025, n = 20, mean 26.17,
  sd 9.22) — the same quantity, 1.9× apart. Meteocat also puts Badalona well above Barcelona (63.4) and Mataró
  (61.2) at T = 10 while the three T = 2 values are effectively identical (36.3 / 36.2 / 36.0). Unresolved;
  another reason not to build on Badalona.
- Mataró's printed *hyetograph* table (Taula 1.7.3.3.4, p. 32) has a **broken T = 2 column**: its peak 5-min pair
  reads 43.36 mm/h where the IDF gives 72.271 at 10 min. It is not noise — the whole column is a flat **0.600×**
  of T = 10, against the correct Pd ratio 60.6091 / 99.2804 = **0.6105**. Every other column (T = 1, 5, 10, 50,
  100, 500, 1000) reproduces the IDF exactly. Use the IDF table and regenerate hyetographs.
- PDCLAM '03 states **no reuse licence**. Cite it as a document; keep the PDF out of the repo.
- CEDEX's CAUMAX v3.0 (Feb 2025) national 500 m grid is **NoData over the whole Catalan internal basins** —
  nearest valid `t10` cell **66.9 km** from Badalona and **77.7 km** from Mataró (`t2…t500`, `i1id` and `p0` are
  all NoData at Badalona, Mataró, Barcelona and Porta; only `mdt` has values). The convenient modern product has a
  hole exactly here — which is also why I1/Id = 11 has to be cited from the ACA *Guia tècnica* §2.8.2 (*"a Catalunya
  es pot considerar un valor mitjà d'11, d'acord amb MOPU (1990)"*) rather than read off the national grid.

## 6. Recommendation — re-derived after the fact-check

**Changed twice. After the fact-check, Badalona lost the lead and the two were joint-first. After the 19 Oct design-rainfall check (§5b), Mataró leads outright: it is the only finalist with a design storm of its own, and Badalona's only route to one is to borrow Barcelona's, which makes the transfer test circular.** The tree-inventory portal check is now the single remaining gate, and it is a gate on Mataró rather than a tie-breaker between two.

The first draft put Badalona first on two pillars. The fact-check left one standing and knocked the other down:

| Criterion | Badalona, on verified evidence |
|---|---|
| 1 — leaf-on classified cloud | ✅ **Confirmed, and harder than before**: re-clipped at **six separate spots** across the municipality, 100% 2021-09-26, ASPRS-classified, 11.1–14.8 pts/m² |
| 2 — pluvial standing | ⚠️ **€658,154, the lowest of the ten**, just over ACA's threshold; the IRM AMC that made it look best is not a pluvial index (§2) |
| 3 — tree inventory | ❌ **Probably none.** Not "unknown": its GeoServer lists 161 layers with no tree layer, and it has no AOC CKAN organisation |
| 4 — dual hazard | ❌ **Weakest of the four.** A December midnight thermal flight with no published UHI value, and a 2025 event re-measured at **18.9 mm/h in a leaf-off month** — the Lisbon objection, applied to Badalona |
| 6 — policy driver | ❌ None of its own, and the DIBA fallback is mis-sourced (§5) |

**And the mission-day argument was overrated.** "Zero season, sensor or year difference" reads as decisive but is a *convenience*, not a validity condition: Mataró, Sabadell, Terrassa and Castelldefels are **also leaf-on, also classified, also 10–14 pts/m²**, just on other 2021 mission days. (The "same 10 km block 4358" detail is also wrong — northern Badalona sits above y = 4,590,000, in block 4359. Same date there, so the substance survives.)

**Mataró, on the same evidence:** in the 44 (€1,363,419, Pluvial-fluvial), leaf-on July 2021 classified tiles, a documented **calibrated level-III municipal drainage model**, a **leaf-on high-intensity September event** (120 mm, 90 mm/h — the right storm type for this thesis), and heat named in its own PAESC. Since 19 Oct it also has the only published design storm of any candidate (§5b) and a resolved tree-data picture (§3b), including the best species overlap with Porta of any transfer candidate — **52.2% on ≥5 Porta trees against Florence's 43.5%, and 92.9% at genus against 74.0%**.

**So:**
1. **Mataró is the transfer city** unless its licence forbids it. §3b resolved criterion 3: the inventory exists, its composition is published (17,204 street trees, 117 species) and 79,748 positions are downloadable in Porta's own CRS. What remains is **three browser URLs** (§3b) — the decisive one being whether `T_C_ARBRAT` joins species to position, and the licence, which is currently **UNKNOWN and unfavourable by default**.
2. **Then Sabadell** (`https://dadesobertes.sabadell.cat/ca/dataset?q=arbrat`) — weakest on hazard, strongest on the decision problem, though now known to be a proposal rather than policy.
3. **Badalona drops to last among the finalists.** It leads on nothing except mission-day convenience and XEMA station coverage, its inventory is probably absent, and §5b shows it has no design rainfall of its own — the one input the runoff module cannot assume. Keep it only if Mataró's inventory check fails *and* a tree layer turns up behind its geoportal, and if so, state the circularity explicitly.
4. **Castelldefels re-enters the comparison**, having been wrongly excluded by the "marginal" leaf-on label: it is the **second-highest-damage municipality** (€6,826,265, typed plainly *Pluvial*) on leaf-on October tiles. Its real blocker is criterion 3 — **no tree dataset among its 25 AOC datasets** — and a 2022 rather than 2021 flight year.

**Do not pick Girona or L'Hospitalet** despite theirs being the only inventories downloadable today: L'Hospitalet is not in the 44 and ACA types it fluvial; Girona's clip came back unclassified, it is not in the 44 either, and its only heat map is 300 m per pixel.

## 7. Holes this screening did not close
- ~~Criterion 5 (design rainfall / IDF) was never checked for any Catalan city.~~ **Closed 19 Oct — see §5b.** Mataró has a full published design storm, Badalona has none, and the Porta/Mataró comparison needs harmonising before it means anything.
- **The licence of the ACA GIS layers is unknown.** `https://sig.gencat.cat/ows/AIGUA/wms` (layer `AIGUA_PLUVIAL_ARPSI`) rejects this container's user agent; open it locally.
- **The four unclassified clips** (Girona, Vic, Manresa, Figueres) may be an artefact of the clip service; re-check against the published `datacloud` tile before treating them as unclassified.
- **Correction to carry forward:** Sabadell's street-tree master plan is documented in a **2021** municipal presentation (APEVC, 18 Feb 2021), **not approved in 2019** — an earlier note in this repo said 2019 and that is withdrawn.
