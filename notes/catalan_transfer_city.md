# The Catalan fallback transfer city: screening of 18+ municipalities

*18 Oct 2026. Fallback to Florence (`notes/firenze_lidar_request.md`), whose point cloud must be requested. Criteria and their severity order from `notes/transferability.md` §2–3. Everything below was established by opening the document, the API or the point cloud itself; status marks as in the inventories.*

## Verification status (18 Oct 2026) — READ FIRST
A six-domain adversarial fact-check was run; **only two domains completed** before the account's weekly limit stopped the rest.

| Section | Status |
|---|---|
| §0, §2 — the ACA pluvial findings | ✅ **checked, 62 claims tested.** All 40 per-city numbers (ARPSI codes, typologies, euro damages, IRM values) reproduce **exactly** against Annex 8 Taula 1 and Annex 6 Apèndix. Nine problems found, all of framing or over-reading, and all corrected below |
| §1 — the LiDAR flight-date table | ❌ **not verified.** Rests on a single research pass |
| §3 — tree inventories | ❌ not verified |
| §4 — dual hazard | ❌ not verified |
| §5 — policy drivers (Sabadell's 23.95% / 30,238 / ~2,700 positions etc.) | ❌ not verified |

**Do not quote §1, §3, §4 or §5 to the tutor as established.** The recommendation in §6 rests on §1 (unverified) plus §2 (verified, but with its pluvial claim corrected downward below).

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
| Castelldefels | 2022-10-01 | 🟡 marginal | ✅ | 12.8 |
| El Prat de Llobregat | 2022-10-01 | 🟡 marginal | ✅ | 12.1 |
| Girona | 2021-08-26 | ✅ by date | ❌ **unclassified in the clip** | — |
| Vic | 2023-07-19 | ✅ by date | ❌ unclassified in the clip | — |
| Manresa | 2021-11-18 | ❌ **leaf-off** | ❌ unclassified | — |
| Figueres | 2021-04-24 | ❌ leaf-off/doubtful | ❌ unclassified | — |

**Caveat to resolve before relying on it:** these came from the clip service, not the published `datacloud` tiles. For the chosen city, download the actual 1×1 km LAZ over the study district and histogram the per-point date and class over the full extent. The four unclassified results in particular may be an artefact of the clip route rather than of the published product.

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

**Verified absent** via portal API or the national federation — eleven: Tarragona, **Terrassa** (126 datasets federated, zero tree hits), Santa Coloma, Vilanova, Granollers, Manresa, Rubí, Castelldefels, El Prat, Sant Cugat, Cornellà.

**Unreachable from the cloud container, and this is the blocker:** **Badalona, Mataró, Sabadell, Reus**.

**None of the six carries DBH or crown diameter**, and only Lleida has any height attribute. This confirms the general finding: **the LiDAR point cloud stays the binding input for LAI and crown geometry at every site** — the inventory supplies species and position, never geometry.

## 4. Dual hazard (criterion 4)
No Catalan municipality outside Barcelona has a single document mapping both hazards; the evidence comes from different institutions.
- **Granollers** — strongest pair: its own ICGC TASI-600 thermal flight (night 27–28 Sept 2021, **4 m pixel**, street-level UHI > 4.5 °C, LCZ layers, two greening simulations) plus documented flash floods (66 mm in ~45 min, June 2008; 108 mm with 50 mm in ~30 min, 5 Oct 2026). But no tree inventory and not in the 44.
- **Mataró** — second, and better balanced: its 2003 *Pla Director de Clavegueram* was written expressly to solve frequent flooding, its climate document names *"efectes illa de calor"*, and 16 Sept 2022 brought 120 mm (90 mm in one hour). **Uniquely among candidates, a real municipal pluvial model demonstrably exists.**
- **Badalona** — both documented, but the heat flight is **December** (ICGC TASI, 15 Dec 2017, 4 m, published in *Revista Catalana de Geografia* 60, 2020); pluvial event 20 Dec 2025, 76.4 mm, flooded ground floors, Plaça de la Vila, Gorg metro.
- **Sabadell** — weak: heat mapping only, from a nocturnal **December 2017** flight; no municipal pluvial evidence found.
- Heat only: L'Hospitalet, Cornellà, Manresa. Pluvial episodes only: Tarragona, Vilanova. Nothing found: Reus, Lleida.

## 5. Policy driver (criterion 6) — stronger than expected
**Barcelona's 15% cap is provincial guidance, not a local peculiarity.** The Diputació de Barcelona's *Guia per a la selecció d'espècies de verd urbà: arbrat viari* (2012) raises Santamour's 10% threshold to **15% for street trees**, and DIBA commissions tree master plans for its municipalities.

- **Sabadell — the best match to this thesis, by far.** The *Pla Director de l'Arbrat Viari* caps any species at 15%, records **Platanus at 23.95% of 30,238 street trees**, conserves 17 historic plane axes (10% of the stock) and commits to reducing the remaining plane alignments from 13.95% to **5%** — about **2,700 positions needing a species decision, roughly three times Porta's 832**. It already contains a municipal 16-parameter, 74-species *índex d'idoneïtat* that scores shade only as a qualitative class and contains **no interception, runoff or thermal-comfort metric at all** — precisely the gap this thesis fills.
- **L'Hospitalet** — the only formally approved one: *Pla Director del Verd Urbà 2018–2028* (532 pp, Junta de Govern Local, April 2019), states the 15% maximum, records *Platanus × hispanica* at 17.07% and *Ulmus* at 15.94% of 16,448 street trees (both over the cap). Four of the thesis's seven palette species are already in its top ten.
- **Girona** — newest and most demanding: *Pla Director de l'Arbrat Urbà*, definitive 9 May 2025, imposes 5-10-15 city-wide with 10-20-30 per neighbourhood, restricts *Celtis australis* (its commonest species) and classes 7,497 positions — 32% of street trees — as Low or Very Low suitability.

## 6. Recommendation, and the one check only the user can do
**Badalona**, because it is the only candidate top-ranked on the two most severe criteria at once: its LiDAR is the **identical ICGC mission to Porta's** (2021-09-26, classified, 12–16 pts/m², same 10 km block 4358), so the transfer carries **zero season, sensor or year difference**; and it is one of the 25 municipalities ACA types plainly *Pluvial*, with a documented 2025 event. **Corrected after fact-check:** an earlier draft called this "the strongest pluvial standing in Catalonia" on the strength of IRM AMC 100.00. That is wrong twice over — the IRM AMC is **not a pluvial index** (its hazard variables are precipitation, *cabal específic*, *llindar d'escolament*, climate change on flood flows and *densitat fluvial*, three of them fluvial-channel measures, none of them urban drainage), and 100.00 is merely the top of a 0–100 min-max normalisation across 635 municipalities. Badalona's recorded damages, €658,154, are the **lowest** of the ten candidates. Its pluvial standing is **adequate, not outstanding**; what still carries the recommendation is criterion 1. Its weakness is criterion 6 — no tree plan of its own, only DIBA's provincial 15% guidance.

**Its single blocking unknown is whether it publishes a tree inventory with species**, and that is a browser check, not a data request. **Four portals are blocked from this cloud container and must be opened from Windows**, in this order:

1. `https://www.badalona.cat/dades-obertes` and the layer list (and any WFS) behind `https://geoportal.badalona.cat/badalona42/visor/geoportal`
2. `https://apex.mataro.org/dadesobertes`
3. `https://dadesobertes.sabadell.cat/ca/dataset?q=arbrat`
4. `https://geoportal.reus.cat/inici/`

**If Badalona has no inventory → Mataró** (same leaf-on July 2021 classified tiles, in the 44, best-documented dual hazard, and a drainage master plan that demonstrably exists — worth one email to Aigües de Mataró for the PDCLAM model). **Then Sabadell**, whose policy driver is unmatched but which fails criterion 4.

**Do not pick Girona or L'Hospitalet** despite theirs being the only inventories downloadable today: L'Hospitalet is not in the 44 and ACA types it fluvial; Girona's clip came back unclassified, it is not in the 44 either, and its only heat map is 300 m per pixel.

## 7. Holes this screening did not close
- **Criterion 5 (design rainfall / IDF) was never checked for any Catalan city.** A silent hole, not a negative finding. Start from Meteocat XEMA series and any ACA IDF curves for the chosen municipality.
- **The licence of the ACA GIS layers is unknown.** `https://sig.gencat.cat/ows/AIGUA/wms` (layer `AIGUA_PLUVIAL_ARPSI`) rejects this container's user agent; open it locally.
- **The four unclassified clips** (Girona, Vic, Manresa, Figueres) may be an artefact of the clip service; re-check against the published `datacloud` tile before treating them as unclassified.
- **Correction to carry forward:** Sabadell's street-tree master plan is documented in a **2021** municipal presentation (APEVC, 18 Feb 2021), **not approved in 2019** — an earlier note in this repo said 2019 and that is withdrawn.
