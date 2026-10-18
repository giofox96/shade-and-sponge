# The Catalan fallback transfer city: screening of 18+ municipalities

*18 Oct 2026. Fallback to Florence (`notes/firenze_lidar_request.md`), whose point cloud must be requested. Criteria and their severity order from `notes/transferability.md` §2–3. Everything below was established by opening the document, the API or the point cloud itself; status marks as in the inventories.*

## Verification status (18 Oct 2026) — READ FIRST
A six-domain adversarial fact-check was run in full (two domains first, four after the account limit reset). Outcome per section:

| Section | Status |
|---|---|
| §0, §2 — ACA pluvial | ✅ **verified.** All 40 per-city figures reproduce exactly against Annex 8 Taula 1 and Annex 6 Apèndix. Nine framing corrections applied |
| §1 — LiDAR flight dates | ✅ **verified and independently reproduced.** Badalona re-clipped at six separate spots: 100% 2021-09-26, ASPRS-classified, 11.1–14.8 pts/m². **But two rows were mislabelled** (Castelldefels/El Prat, Figueres) and the sampling caveat is now stated honestly |
| §3 — tree inventories | ⚠️ **corrected.** Badalona and Reus are *not* unreachable; "verified absent" held for only 8 of 11; the "never geometry" claim was too strong |
| §4 — dual hazard | ⚠️ **corrected.** A wrong rainfall figure, two merged Badalona events, and Badalona's 2025 event re-measured as a low-intensity winter frontal event |
| §5 — policy drivers | ⚠️ **heavily corrected.** The DIBA/Santamour attribution was wrong, Sabadell's figures are a conference deck not an approved plan, Girona's denominator was wrong |
| §6 — recommendation | ❌ **re-derived.** Badalona no longer leads; see §6 |

**§1 and §2 are citable to the tutor. §3–§6 are now corrected but thinner than the first draft claimed.**

## 0. The headline, including the bad news
**Criterion 2 fails for the whole of Catalonia.** The ACA's 3rd-cycle pluvial product, approved 15 July 2026, is a **list of 44 municipalities** whose ARPSI polygon **is the administrative boundary** — Annex 8 §3.3, verbatim: *"les ARPSI pluvials no es defineixen a partir de criteris hidrològics (conques) o hidràulics (eixos de drenatge), sinó a partir dels límits administratius del municipis"* (the missing *s* is the source's own typo) — with no extent, no depth and no return period. No 3rd-cycle MAPRI exists — ACA says MAPRI and PGRI *"es troben actualment en fase d'elaboració"*; a 2027 date for homologated **inundable-zone** (not pluvial) cartography comes from press coverage of a parliamentary committee statement of 12 Nov 2025, **not from any ACA document**. The one pluvial ARPSI that ever had a modelled depth map (CRT Vila-seca i Salou, 8.54 km², HEC-HMS 3.3 + IBER 2.2) is **proposed for deletion** in the APRI phase, though its maps still stand. The **2018 (2nd-cycle)** fluvial-pluvial classification rested on a quantitative layer — the ZDD, *zones de dificultat de drenatge* — taken from an *"estudi inèdit de TRAGSATEC"* and never published (2nd-cycle APRI Annex 05 §3.2.1 and footnote 4). The 3rd cycle instead derives its "Pluvial-fluvial" typology simply from the presence of a fluvial TRI.

**So Barcelona's RESCCUE depth model is the only city-wide pluvial depth model found in Catalonia**, and no Catalan transfer city can reproduce the hotspot-targeting half of the method from open data. (The one other published ACA pluvial depth product covers **8.54 km² at the CRT Vila-seca i Salou** — MAPRI 2019, with modelled depth classes <40 cm / 41 cm–1 m / >1 m from IBER 2D — and it remains **current**, since no 3rd-cycle MAPRI exists to supersede it; Annex 8 only *proposes* deleting the ARPSI. Mataró's municipal drainage model is reported to exist but is not open.) That is itself a finding for the thesis: it sharpens why Porta was the right calibration site, and it is a concrete instance of the transferability argument.

The 44-list is still worth a lot: it is an authoritative, euro-quantified **pre-filter** with per-municipality damages and two risk indices, and a citable justification that pluvial flooding is a real municipal problem in the chosen city.

**Recommendation: Badalona**, subject to one 30-minute check the user must do (§6).

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

**Corrected after fact-check — only two are actually unreachable.** **Mataró** and **Sabadell** are proxy-blocked. **Badalona and Reus are reachable**, and the answer for Badalona is now a near-negative rather than an unknown: its public GeoServer lists **161 WMS layers with no tree or green layer**, it has **no AOC CKAN organisation**, and `www.badalona.cat/dades-obertes` returns 404 (not the 403 recorded earlier), while its `seu-e.cat` page answers 200. So: **no open tree inventory found for Badalona.**

**No numeric DBH and no crown diameter anywhere**, and only Lleida has a height attribute — but three of the six do carry a **coarse size class**: Girona's `mida_tronc` is a trunk-perimeter band (20–50 / 50–80 / 80–120 / >120 cm; n = 12,662 / 11,276 / 6,498 / 2,313), Sant Boi has `MIDA` (petit/mitjà/gran/exemplar) plus a growth stage, Lleida a perimeter class 0–4. The conclusion survives in its proper form: **the point cloud stays the binding input for LAI and crown geometry at every site**, because a size band cannot give either.

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

## 6. Recommendation — re-derived after the fact-check

**Changed: Badalona no longer leads. Mataró and Badalona are joint-first, with the portal check as an explicit gate, and Mataró is the better bet on the merits.**

The first draft put Badalona first on two pillars. The fact-check left one standing and knocked the other down:

| Criterion | Badalona, on verified evidence |
|---|---|
| 1 — leaf-on classified cloud | ✅ **Confirmed, and harder than before**: re-clipped at **six separate spots** across the municipality, 100% 2021-09-26, ASPRS-classified, 11.1–14.8 pts/m² |
| 2 — pluvial standing | ⚠️ **€658,154, the lowest of the ten**, just over ACA's threshold; the IRM AMC that made it look best is not a pluvial index (§2) |
| 3 — tree inventory | ❌ **Probably none.** Not "unknown": its GeoServer lists 161 layers with no tree layer, and it has no AOC CKAN organisation |
| 4 — dual hazard | ❌ **Weakest of the four.** A December midnight thermal flight with no published UHI value, and a 2025 event re-measured at **18.9 mm/h in a leaf-off month** — the Lisbon objection, applied to Badalona |
| 6 — policy driver | ❌ None of its own, and the DIBA fallback is mis-sourced (§5) |

**And the mission-day argument was overrated.** "Zero season, sensor or year difference" reads as decisive but is a *convenience*, not a validity condition: Mataró, Sabadell, Terrassa and Castelldefels are **also leaf-on, also classified, also 10–14 pts/m²**, just on other 2021 mission days. (The "same 10 km block 4358" detail is also wrong — northern Badalona sits above y = 4,590,000, in block 4359. Same date there, so the substance survives.)

**Mataró, on the same evidence:** in the 44 (€1,363,419, Pluvial-fluvial), leaf-on July 2021 classified tiles, a documented **calibrated level-III municipal drainage model**, a **leaf-on high-intensity September event** (120 mm, 90 mm/h — the right storm type for this thesis), and heat named in its own PAESC. Its inventory is untested **only because its portal is proxy-blocked**, which is a very different state from Badalona's near-negative.

**So:**
1. **Check Mataró's portal first** (`https://apex.mataro.org/dadesobertes`). If it has a species-level inventory, **Mataró is the transfer city.**
2. **Then Sabadell** (`https://dadesobertes.sabadell.cat/ca/dataset?q=arbrat`) — weakest on hazard, strongest on the decision problem, though now known to be a proposal rather than policy.
3. **Badalona stays on the shortlist** but leads on nothing except mission-day convenience, and its inventory is probably absent. Keep it as the fallback *if* a tree layer turns up behind its geoportal.
4. **Castelldefels re-enters the comparison**, having been wrongly excluded by the "marginal" leaf-on label: it is the **second-highest-damage municipality** (€6,826,265, typed plainly *Pluvial*) on leaf-on October tiles. Its real blocker is criterion 3 — **no tree dataset among its 25 AOC datasets** — and a 2022 rather than 2021 flight year.

**Do not pick Girona or L'Hospitalet** despite theirs being the only inventories downloadable today: L'Hospitalet is not in the 44 and ACA types it fluvial; Girona's clip came back unclassified, it is not in the 44 either, and its only heat map is 300 m per pixel.

## 7. Holes this screening did not close
- **Criterion 5 (design rainfall / IDF) was never checked for any Catalan city.** A silent hole, not a negative finding. Start from Meteocat XEMA series and any ACA IDF curves for the chosen municipality.
- **The licence of the ACA GIS layers is unknown.** `https://sig.gencat.cat/ows/AIGUA/wms` (layer `AIGUA_PLUVIAL_ARPSI`) rejects this container's user agent; open it locally.
- **The four unclassified clips** (Girona, Vic, Manresa, Figueres) may be an artefact of the clip service; re-check against the published `datacloud` tile before treating them as unclassified.
- **Correction to carry forward:** Sabadell's street-tree master plan is documented in a **2021** municipal presentation (APEVC, 18 Feb 2021), **not approved in 2019** — an earlier note in this repo said 2019 and that is withdrawn.
