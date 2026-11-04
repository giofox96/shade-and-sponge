# Co-benefits plan (draft, 3 Nov 2026): work to resume on 11 Nov

**Decision (Giovanni, 3 Nov):** before the 10 Nov tutor session, co-benefits are **not** objectives of the tool. The deck gets one backup slide (`slides/fig_v7/v7_17_cobenefits.png`, built by `scripts/make_slides_v7.py`, placed after "What comes next"; the 16 spoken slides and their timing are unchanged). From 11 Nov they become **reported indicators**: computed for every layout already produced (S0, the city mix baselines, the tool), shown next to heat and runoff, and not optimised unless a result justifies it.

**Why reported and not optimised.** The research question is heat + runoff. Adding objectives now widens the scope five weeks before delivery and each one opens data and method questions. Reporting them still answers the obvious tutor question ("what else changes when the planes go?") and is honest where the tool loses (carbon).

**Hook in the city's own plan.** The master plan lists "fewer disservices" (allergies, VOC emissions, invasiveness, pavement damage, litter) among the reasons to diversify (Pla director de l'arbrat 2017–2037 §1.3.4, p. 14; 2011 guide p. 16: avoid allergenic species), with no number per species (`notes/tree_master_plan.md` §2, row 5). Same pattern as heat and runoff: a qualitative aim, no quantities per position.

Status column: ✅ verified on the source on 3 Nov; 🟡 to verify before citing.

## Priority order

| # | Indicator | Value for the thesis | Effort | Risk |
|---|---|---|---|---|
| 1 | Diversity / resilience | Already computed; only needs reporting | ~0.5 day | Low |
| 2 | Pollen allergenicity | Likely a clear gain from replacing planes | ~1–2 days | Species scores from Granada, not Barcelona |
| 3 | Carbon storage + sequestration | Expected question; honest even if it loses | ~2–3 days | Allometry for Mediterranean species is thin; planes may win |
| 4 | Ozone / VOC | Interesting, but chemistry is local and non-linear | — | Kept as a declared limit |

## 1. Diversity and resilience (report only)

- **Already in the code:** `eff_species` = exp(Shannon H) in every replacement-layout row of the summary (`shade_sponge/README.md`, `--diversity=N`; `layout.py`), the measure SylvCiT uses (Nicol et al. 2026) ✅.
- **To do:** a table per barri and city-wide: effective species, largest species share, and the genus and family shares (the 10-20-30 rule of Santamour 1990, already cited in the deck) for S0, the city mix baselines and the tool. Show that the 15% cap and the local ceiling are what drive it.
- **Data:** street-tree inventory (have it); genus and family from the species name (needs a small lookup table, e.g. from the species palette files).

## 2. Pollen allergenicity

- **Method:** IUGZA, Cariñanos, Casares-Porcel & Quesada-Rubio 2014, *Landscape and Urban Planning* 123:134-144, doi:10.1016/j.landurbplan.2013.12.009 ✅. Per species: allergenic potential ap (0–3, 4 for main local allergens), pollen emission pe (0 female dioecious, 1 insect, 2 amphiphilous, 3 wind), pollination period ppp (1–3 by weeks); per tree: crown area S and height class H. Normalised by area. *Platanus hispanica*: ap = 4, pe = 3, ppp = 2 (Table 2, 77 taxa, Granada) ✅.
- **For streets:** compute the sum per barri (or per street buffer) instead of per park; crown area and height come from LiDAR (have them). Report the change vs S0, not the absolute index (the normalisation was built for parks).
- **Data gaps:** check which palette species are in the 77 Granada taxa; for the rest, use the later update by the same group (Cariñanos et al. 2016 or 2019, 🟡 to find and verify) or mark as missing. Do not invent scores.
- **Barcelona context:** plane pollen seasons in Catalonia (Xarxa Aerobiològica de Catalunya; "Aerobiological behaviour of *Platanus* L. pollen in Catalonia", doi:10.1023/A:1021370724043, 🟡 not read yet).
- **OPALS** (Ogren Plant Allergy Scale) is the other common scale, but it is a commercial, US-based scale and is not openly documented per species 🟡. Prefer IUGZA (published, Spanish, formula open).

## 3. Carbon storage and sequestration

- **Method:** biomass from DBH with urban allometry → × carbon fraction; sequestration = difference over one year of growth. Storage at maturity and at planting, so the young-tree deficit is visible (the planes win early, the question is when the replacement catches up).
- **Sources:** McPherson, van Doorn & Peper 2016, *Urban tree database and allometric equations*, USDA PSW-GTR-253 (171 species, 17 US cities; data RDS-2016-0005) ✅ for the citation; **species coverage for the Porta palette not checked** 🟡 (Platanus × acerifolia is likely, Tipuana, Brachychiton, Melia less so). Fallback: genus- or wood-density-based general equation, marked `ASSUMPTION`. i-Tree Eco uses the same family of equations.
- **Barcelona reference:** Baró et al. 2014, *Ambio*, i-Tree Eco for Barcelona's urban forest (carbon and air quality) 🟡 open PDF blocked by a captcha from the cloud; read it locally. Useful to sanity-check orders of magnitude, not as per-species input.
- **Data:** DBH is in the inventory as a class; LiDAR gives height and crown. Growth rates per species are the weak point (needed for sequestration and for "years to catch up").
- **Expected result, to test not assume:** the tool's mix may store less carbon than S0 for years, because mature planes are large. Report it either way.

## 4. Ozone and VOC (declared limit)

- Some species emit isoprene or monoterpenes; ozone formation also depends on local NOx and sunlight. A per-species ozone-forming potential exists (Benjamin & Winer 1998, 308 species, Southern California, 🟡 citation to verify; emission factors per species: Lancaster/Hewitt database, 🟡).
- **Decision:** not modelled. One sentence in the limits chapter, plus a column with the emitter class per palette species if the data is easy to find.

## Not in the plan (and why)

- **Air pollution removal (PM, NO₂):** depends on leaf area like shade does, so it would mostly repeat the heat result; i-Tree-style deposition rates are US-calibrated.
- **Pavement damage, litter, maintenance cost:** the plan names them, but there is no open per-species data for Barcelona.

## Outputs to produce from 11 Nov

1. `scripts/cobenefits.py` → `databases/barcelona/cobenefits_species.csv` (one row per palette species: ap, pe, ppp, allometry source, emitter class, source column) and `cobenefits_layouts.csv` (per layout and barri).
2. One figure for the results chapter (indicators side by side, change vs S0).
3. A methodology section (§ co-benefits) and a limits paragraph.
