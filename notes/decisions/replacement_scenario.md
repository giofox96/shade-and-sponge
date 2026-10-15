# Replacement scope and S1 baseline (issue #9, 15 Oct 2026)

Status: **options plus a recommended default, pending one user answer.** Methodology status in CLAUDE.md is PROTOTYPING; `methodology.md` and `topic_decision.md` are not edited here. No optimiser code was written.
Marks: 🟡 press only or search summary; (abs) abstract only; ✅ opened and read. Scripts: `scripts/palette_headroom.py`, `scripts/porta_recent_plantings.py`. Files: `databases/barcelona/palette_headroom.csv`, `porta_recent_plantings.csv`, `candidate_palette.csv`.

## 0. Findings that change the framing

1. **The 15% rule is a city rule on the urban fabric, not a Porta rule.** Plan (✅, `Pla-director-arbrat-barcelona-CA_0.pdf`, Repte 3 for 2037 (a challenge, not an objective), printed pp.24-25): "què dins la trama urbana cap espècie d'arbrat representi més del 15% del total". The 2012 origin is "en 50 anys cap espècie superi el 15% del total de la població" (p.20, street trees and palms). So methodology §6's Porta-local 15% cap is the thesis's own stricter proxy, not the plan.
2. **The plan text has no plane-specific target.** "15% by 2027" and "12% by 2037" are press only 🟡 (Vilaweb 28.05.2022; 3Cat 29.05.2022; Betevé, undated page). I found neither figure in the plan PDF. The sources also disagree on what the 12% covers: Betevé (fetch summary) groups plane and *lledoner* in one 12% share.
3. **Only three of the six topic_decision §7 species have a source as "named for replacement".** Press names *lledoner* (Celtis), *sòfora*, *mèlia*, *tipuana* (Vilaweb 2022, 3Cat 2022) and, in the Betevé summary, ~5% for *Pyrus calleryana*, sophora and tipuana, 7.25% *Melia* 🟡. **Jacaranda and Brachychiton are named in no source I could open.** *Styphnolobium* is named (press), which matches inventory D1. So "the six replacement species the city names" (runoff_model.py CANDIDATES, make_infographics.py line 283, slides 3 and 6, topic_decision §7) is not supported for two of six.
4. **The 40% target is about species, not trees, and its list is not in the plan.** Repte 2 for 2037 (p.25): "un 40% de les espècies d'arbres siguin adaptades al canvi global, en lloc del 30 % actual". The "inventari d'espècies adaptades" is only referenced (p.14: tipuana and xicranda "s'han inclòs a l'inventari d'espècies adaptades existent"); the list itself is not reproduced. Needs the plan annex or Parcs i Jardins: to check locally.
5. **Denominators differ.** `species_coverage.csv`: 140,404 trees (planes 28.6%). methodology §6 note 6: 145,176 (27.6%). Press: 42,709 of 154,235 (27.7%). Plan p.20 (public trees incl. parks): planes ~49,300 = 20.8%. The cap in trees moves by ±1,000 with the denominator; the conclusions below do not flip.

## 1. Headroom table (`palette_headroom.csv`)

Headroom = cap minus current trees of the species; replacement keeps the totals constant. Caps: (a) Porta 15% of 2,825 = 423; (b) city 15% of 140,404 = 21,060; (c) city 12% = 16,848. City counts exist only for the top-30 species.

| Species | Porta | City | (a) | (b) | (c) |
|---|---:|---:|---:|---:|---:|
| Platanus × acerifolia (incl. 3 PLATANOR) | 832 | 40,092 | -409 | -19,032 | -23,244 |
| Celtis australis | 296 | 19,384 | 127 | 1,676 | **-2,536** |
| Melia azedarach | 167 | 6,263 | 256 | 14,797 | 10,585 |
| Pyrus calleryana | 147 | 3,481 | 276 | 17,579 | 13,367 |
| Jacaranda mimosifolia | 145 | 3,235 | 278 | 17,825 | 13,613 |
| Tipuana tipu | 139 | 6,636 | 284 | 14,424 | 10,212 |
| Brachychiton populneus | 103 | 5,251 | 320 | 15,809 | 11,597 |
| Styphnolobium japonicum | 5 | 8,427 | 418 | 12,633 | 8,421 |
| Grevillea robusta | 67 | 1,543 | 356 | 19,517 | 15,305 |
| Fraxinus angustifolia | 44 | 901 | 379 | 20,159 | 15,947 |
| Casuarina cunninghamiana | 62 | 696 | 361 | 20,364 | 16,152 |
| Handroanthus heptaphyllus | 45 | outside top-30 (<588) | 378 | not computed | not computed |

Reading: *Celtis* is the only candidate where the cap bites. It has 127 trees of Porta headroom, 1,676 city-wide at 15%, and is **already over the 12% scenario** (13.8%). Under (c) no more *Celtis* may be added anywhere.

**The 3 PLATANOR 'Vallis Clausa' trees count as planes.** `is_plane = species.startswith('Platanus')` (`scripts/bcn_lidar_porta.py` line 121), so 832 = 829 *Platanus × acerifolia* + 3 PLATANOR in `exchange/to_gh/porta_street_trees.csv` (checked: 832 `is_plane` rows). `porta_species.csv` lists the 3 on their own row (829 + 3). `palette_headroom.csv` merges them (cultivar stripped).

## 2. Minimum plane replacements per scope

| Scope | Planes allowed | Minimum replaced in Porta |
|---|---|---|
| (a) Porta-local 15% | 423 | **409** (832 - 423) |
| (b) city 15% | 21,060 city-wide | City excess is 19,032 (40,092 - 21,060). Porta (832 planes) cannot meet it alone. No Porta minimum follows from the rule; pro-rata share 395 (ASSUMPTION: Porta contributes in proportion to its 832/40,092) |
| (c) city 12% (ASSUMPTION: 12% per species; Betevé gives 12% for plane + lledoner combined) | 16,848 city-wide | City excess 23,244. Pro-rata share 483 (same ASSUMPTION). Replacing all 832 still leaves 39,260 planes citywide |

## 3. Recent plantings (`porta_recent_plantings.csv`)

379 of 2,825 trees are dated 2017 or later (29 species); **2,266 of 2,825 (80.2%) have no planting date** and 180 are dated before 2017. Bias caveat: the dated subset is the trees that entered the inventory with a date, so it is not a random sample of Porta. It is also clustered in street batches (2025: 35 *Handroanthus*, 31 *Fraxinus angustifolia*). Leaders: Handroanthus 45 (11.9%), Grevillea 44 (11.6%), Fraxinus angustifolia 44 (11.6%), Casuarina 41 (10.8%), Celtis australis 33 (8.7%), Pyrus calleryana 28 (7.4%), Robinia 19, Catalpa 18, Melia 15, Prunus cerasifera 14, Jacaranda 9, Tipuana 4, Platanus 4. The recent mix is not the six-species palette: *Tipuana* is 1.1%, *Brachychiton* 1.3%.
City-wide version: **to check locally.** `arbrat_viari.csv` is not in the repo and the open-data download returns a bot-detection page from this sandbox (the CKAN metadata API answers; the file does not).

## 4. S1 options (all-832 replacement, plane excluded) and Shannon values

Shannon H (natural log) and exp(H) over species with cultivars stripped; replaced planes enter as fractional counts. Cap check = any species over (a) 423 trees; genus share = largest genus.

| Mix | H | exp(H) | Species | Largest genus | Breaks (a) cap |
|---|---:|---:|---:|---:|---|
| **S0 (today)** | 2.823 | **16.82** | 51 | Platanus 29.5% | planes 832 |
| S1-R: recent-planting mix (non-plane, 2017+) | 3.174 | 23.91 | 50 | 15.4% | none |
| S1-A=: equal shares, topic_decision six | 2.913 | 18.42 | 50 | 17.4% | Celtis 435 |
| S1-B=: equal shares, press four (Celtis, Styphnolobium, Melia, Tipuana) | 2.928 | 18.68 | 50 | 19.8% | Celtis 504 |
| S1-A~: Porta proportions of the six | 2.886 | 17.93 | 50 | 21.2% | Celtis 543 |
| S1-B~: Porta proportions of the press four | 2.794 | 16.35 | 50 | 26.8% | Celtis 702 |

Reading: the "named palette in its proportions" S1 (§7 wording, S1-A~) **breaks the Porta 15% cap by itself** (Celtis 543 > 423) and raises exp(H) only from 16.8 to 17.9. Any equal-share or proportional palette needs capping or redistribution to be a valid like-for-like baseline. The recent mix is the only one that is cap-feasible as is, and the only one with a documented source in the repo's data. Under (c), every option that adds *Celtis* adds to a species already above 12%.

## 5. Diversity-floor options

| Option | Value | Status |
|---|---|---|
| Not below S0 | exp(H) >= 16.82 (H >= 2.823) | computed here |
| Plan species cap | no species > 15% (Porta-local: 423) | plan p.24-25 ✅; Porta scope is our adaptation |
| 10-20-30 rule | species <= 10%, genus <= 20%, family <= 30% (Santamour 1990, as stated in the Avolio 2023 abstract (abs), `notes/lit/candidates.csv`; used by SylvCiT per CLAUDE.md summary of Nicol 2026, matrix #28; I could not re-open the SylvCiT PDF here 🟡) | S0 already fails it: planes 29.5% of species and genus; *Celtis* 10.5%. Family level not computed (no family table in the repo) |
| Plan climate-adapted share | 40% of species adapted (p.25) | list unavailable: to check locally |

Recommended floor: the **plan's 15% species cap (Porta-local, 423) plus exp(H) not below S0 (16.8)**; report the 10-20-30 genus and species shares as outputs, not constraints (S0 fails them, so they would make S0 infeasible).

## 6. Replacement-location options and decision variables

| Option | Decision variables | Notes |
|---|---|---|
| O1 all 832 replaced, plane excluded from the palette | 832 species choices | Matches slide 8 and methodology §6 wording. Plane share falls from 29.5% to 0 in Porta. Stronger than the cap needs |
| O2 plane allowed but cap-limited (>= 409 must change) | 832 positions, alphabet = palette + "keep plane", plane count <= 423 | Same 832 variables; the optimiser decides which 409 or more go. Fits the cap as written; S1 then needs the same rule |
| O3 sub-area only | e.g. Av Meridiana 194; top five streets 536 (Meridiana 194, Rio de Janeiro 111, Andreu Nin 80, Fabra i Puig 77, Pi i Molist 74); 23 streets hold planes | Cannot reach 409 unless five or more streets are chosen. Needs a user rule for the area |

Planes by size class: TERCERA 347, SEGONA 336, EXEMPLAR 132, PRIMERA 17. Size class matters for the "same number and size class" wording of H1.

## 7. Candidate checks (`candidate_palette.csv`; sources in the CSV)

- **Invasive (RD 630/2013, BOE-A-2013-8565, consolidated, last update 12/05/2025, ✅ full text searched):** *Ailanthus altissima* is listed. None of the candidates (Celtis, Melia, Pyrus, Jacaranda, Tipuana, Brachychiton, Styphnolobium, Handroanthus, Grevillea, Fraxinus, Casuarina) nor *Robinia*, *Ligustrum*, *Platanus* appears in the text. This closes the D4 doubt for the national catalogue. Catalan list: **to check locally** (a Catalan fact-sheet search and a gencat repository page returned nothing usable; the repository page is behind an anti-bot challenge).
- **Pests (EPPO Global Database, pages read):** *Ceratocystis platani*: Spain "Absent, pest eradicated" (distribution page, updated 2026-01-30); EPPO A2 (1978), EU quarantine pest Reg. (EU) 2019/2072 Annex II B; hosts are *Platanus* only. *Xylella fastidiosa* in Spain: "Transient" (2024), under eradication/containment in Baleares, Alicante, Madrid, Extremadura; **no Catalonia entry**. EPPO Xylella hosts include *Pyrus calleryana*, *Jacaranda mimosifolia*, *Fraxinus angustifolia*, *Celtis occidentalis* / *Celtis* sp., *Robinia*, *Ligustrum lucidum*, *Platanus × hispanica*. Not on the list: *Celtis australis*, *Melia*, *Tipuana*, *Brachychiton*, *Styphnolobium japonicum*, *Handroanthus*, *Casuarina*, *Grevillea robusta*. Absence means no record, not immunity. This weakens the pest argument for *Pyrus*, *Jacaranda* and *Fraxinus* as replacements.

## 8. Recommended default (to adopt unless you object)

- **Constraint:** Porta-local 15% cap (423 per species), as in methodology §6; check (b) and (c) as post-hoc flags (*Celtis* fails (c)).
- **Replacement set:** O2 (832 variables, "keep plane" allowed, plane <= 423, so at least 409 replaced). If you prefer a clean story, O1 gives the same variable count.
- **S1:** the recent-planting mix of non-plane species (S1-R), applied to all 832 positions at its shares, cap-feasible, exp(H) 23.9. Keep the equal-share palette as a sensitivity case only after capping *Celtis* at 423.
- **Floor:** exp(H) >= 16.8 plus species <= 15%.
- **Palette for the optimiser:** the species in `candidate_palette.csv` with a LiDAR/trait row; add or drop *Jacaranda* and *Brachychiton* as "observed in Porta, not named by the city".

## 9. What must change downstream

- **Runoff v1 `R_*` scenarios are single-species sensitivity runs, not S1.** They replace all planes with one species (`runoff_model.py` CANDIDATES; methodology §4b; `runoff_scenarios.csv`: R_Celtis, R_Melia, R_Pyrus, R_Jacaranda, R_Tipuana, R_Brachychiton, R_Styphnolobium, each mature and young). All 832 as *Celtis* would put 1,128 *Celtis* in Porta (296 + 832) against a cap of 423, so every R_* layout breaks the 15% rule in all three scopes. S1 is still undefined in methodology §7.
- **S1 drives H1 and the PS species list** (topic_decision §7; `slides/outline_20oct.md` slides 3, 6 and 8; `slides/fig/05_palette_data_gap`, `make_infographics.py` line 283). The phrase "the six replacement species the city names" and "the city's named palette in its proportions" are not supported as written (section 0, point 3; section 4).

## 10. Remaining gaps (to check locally)

1. Plane target text (15% by 2027, 12% by 2037) in an official document: not in the plan PDF read; press only.
2. The climate-adapted species list behind the 40% target.
3. Any rule linking species size to sidewalk, street width or façade distance: **not in plan.** The plan only lists street width and orientation, soil, paving and building height as general factors (p.7) and "Acció 4.4 Revisar els criteris de planificació i disseny de la plantació" and "Acció 2.9 Seleccionar les espècies arbòries amb visió de futur (resistència al medi urbà, port, floració)" as titles without content. The façade-clearance constraint in methodology §6 has no municipal rule behind it yet.
4. City-wide recent plantings and top-30 cut-off counts (needs `arbrat_viari.csv` locally; rerun `species_coverage.py` with a larger `top_n`).
5. Catalan invasive-species list.
6. bcnroc (`bcnroc.ajuntament.barcelona.cat`) still answers from this sandbox with a 301 to a rate-limit page; the plan was read from the Ajuntament copy instead.

## One question for you

**Do you accept S1 = the species mix the city has actually planted in Porta since 2017 (S1-R, cap-feasible), instead of "the named palette in its proportions", which breaks the cap and has no source for two of its six species?**
