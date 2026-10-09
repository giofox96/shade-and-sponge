# Replacement-species evidence check (issue #4)

Draft, 9 Oct 2026. Matrix ids refer to `notes/lit/literature_matrix.csv` (new rows 62-68 added today; the issue said "from id 57", but ids 57-61 were already taken). Read levels: full text = digest or full text in the matrix; (abs) = abstract only; 🟡 = web-search summary, not the paper. Parameter values: `notes/lit/species_canopy_params.csv`; rules and coverage: `notes/method_traits.md`.

## 1. Evidence class per species

Classes: measured runoff / measured heat / simulated only / LAI or structure only / nothing found. A species can hold more than one.

| Species | Runoff evidence | Heat evidence | Class | Matrix ids, read level |
|---|---|---|---|---|
| Platanus x acerifolia (current tree, comparator) | Storage 0.87 mm per unit leaf + stem area (Xiao & McPherson 2016); Cmax / Cmin 0.49 / 0.29 mm, LAI 3.02, rain-limited (Baptista 2018) | Transpiration cooling 33.3% of incoming solar at 39.1 C air (Bachofen 2025); in-situ shade and transpiration cooling (Helletsgruber 2020); heatwave leaf loss (Sanusi & Livesley 2020) | measured runoff + measured heat + LAI | #3 full text, #6 full text, #43 full text, #40 full text, #68 🟡 |
| Celtis australis | Nothing for the species. Congener C. sinensis 0.71 mm (measured) | Nothing found | nothing found (species); congener measured runoff | #3 full text |
| Melia azedarach | Nothing measured | Nothing measured. Included in an i-Tree Eco multi-criteria clustering (modelled monetary values) | LAI or structure only (plantation LAI 1.3-3.0 🟡) + simulated only | #59 full text |
| Pyrus calleryana | Storage 0.51 mm (Xiao & McPherson 2016, full text); winter interception 15% (second-hand) | **Measured**: surface temperature under shade, species effect significant, Pyrus among the two most cooling of five species; MRT reduction ~4 C pooled (Armson 2013, Manchester, abstract). **Simulated**: UTCI −3.53 to −6.27 C, default ENVI-met tree, geometry not species (Silva 2025) | measured runoff + measured heat (abs) + simulated | #3 full text, #62 (abs), #47 full text |
| Jacaranda mimosifolia | Modelled 15.3% interception, small tree, city-scale model, second-hand (Xiao & McPherson 2003 via Huang 2017) | Nothing confirmed. Abreu-Harbich 2015 may include it (🟡, not verified) | simulated only (runoff); heat unverified | #33 full text (secondary), #65 🟡 |
| Tipuana tipu | Nothing found | **Field-measured** MRT / PET under a Tipuana cluster in Campinas, tropical, value not in abstract (Abreu-Harbich 2012, abs). **Simulated** PET −15.6 C summer, −2.7 C winter, Lisbon canyons (Santos Nouri 2018 🟡) | measured heat (tropical, cluster, value unread) + simulated | #63 (abs), #64 🟡, #47 secondary |
| Brachychiton populneus | Nothing found | Transpiration only, <5000 kg/yr per tree, lowest of the Los Angeles species, second-hand (McCarthy 2011 via Berland 2017) | LAI or structure only / second-hand transpiration | #58 full text (secondary) |
| Styphnolobium japonicum (Sophora) | Event interception 35.79% mean of 6 events, one tree, Seoul (Yang 2019); infiltration +118% vs unplanted tank, young tree (Zhang 2019); interception 4.0-4.3 mm pooled with two other species (Ji 2025, abs) | Nothing found | measured runoff (3 sources, all single or young trees) | #5 full text, #17 full text, #67 (abs) |

Optional taxa (Citrus, Robinia, Catalpa, Grevillea, Casuarina, Populus nigra): nothing found at species level. Robinia has relative values only (transpiration ~0.25x Tilia, lower LAI; Rahman 2020, #44 abs).

### Santos Nouri et al. 2018: measured or simulated?
Simulated 🟡. Search summaries of the abstract describe a reference-point system with SkyHelios, RayMan and the modified PET (mPET), locally obtained global radiation values, and the most common canyon cases of the historic quarter with Tipuana tipu. The PET reduction of 15.6 C (mPET 11.6 C) on a very hot day (Tmax above 35 C) is therefore a modelled value, and it mixes canyon geometry with the species. In winter, because the species keeps its foliage, the reduction is up to 2.7 C (mPET 2.6 C). MDPI blocked the page here (HTTP 403), so confirm against the paper (listed in `to_get_manually.md`).

### Styphnolobium: does it belong in the palette?
Yes as a named candidate, with two flags. (1) Evidence: it has the most measured runoff evidence of any replacement candidate (Yang 2019 #5; Zhang 2019 #17; Ji 2025 #67 abs), but only for single or young trees, and no heat value. (2) Naming: inventory D1 lists "Sophora" among the replacement species named in the press, but the problem statement lists six (Celtis, Melia, Pyrus, Jacaranda, Tipuana, Brachychiton) and omits it; the master plan text was not read (D1 is 🟡). Only 5 trees stand in Porta, so there is no LiDAR crown or LAI; it needs size-class defaults. Recommendation: add it to the named list only after the master plan text confirms it; until then mark it "named in press (D1), 5 trees in Porta, no LiDAR crown".

## 2. Replacement for "none has a measured cooling value"

The clause is wrong as written. Armson et al. 2013 (abstract) measured Pyrus calleryana and found it, with Crataegus laevigata, provided significantly more surface cooling than three other street trees; Abreu-Harbich et al. 2012 (abstract) measured shade under a Tipuana tipu cluster in the tropics.

Proposed sentence (replaces "and none has a measured cooling value" in the problem statement):

> "Yet in the literature we reviewed, only *Pyrus calleryana* has a measured canopy-storage value (Xiao & McPherson 2016) and a measured shade-cooling value (surface temperature under street trees in Manchester, where Pyrus and Crataegus cooled most; the radiant-temperature reduction was not species-specific; Armson et al. 2013), while *Tipuana tipu* has only field shade data from a tropical city (Abreu-Harbich et al. 2012) and a modelled thermal-comfort value (Santos Nouri et al. 2018); we found no species-level cooling value for *Celtis*, *Melia*, *Jacaranda* or *Brachychiton*."

Caveats to keep in the text: Armson reports temperature under the shade of small trees in a temperate city, not UTCI; per-species values come from the paper, the abstract gives only pooled means (surface −12 C, MRT −4 C); Armson and Abreu-Harbich are read as abstracts. A shorter slide version: "Only Pyrus has a measured cooling value, and in a temperate city; for the other five we found none that is species-level and measured in a Mediterranean climate" (this "Mediterranean" qualifier is true for the evidence found, but no Mediterranean search beyond the queries below was done).

## 3. Files that repeat the claim (wording proposed, nothing edited)

1. `notes/topic_decision.md` §7 line 121 (problem statement): "and **none has a measured cooling value**". Replace with the sentence in section 2.
2. `slides/outline_20oct.md` slide 6 script, line 39: "rain storage is measured for only one of them, and none has a measured cooling value." Proposed: "Rain storage is measured for only one of them, Pyrus, and so is cooling, in a temperate city; the others have none, or only modelled values."
3. `scripts/make_infographics.py` lines 279-280 (closing sentence of `fig_palette`: "cooling values are only modelled or second-hand") and the "Cooling (measured)" column. Pyrus should be marked measured (Armson 2013) with the Silva note kept as the modelled value; Tipuana footnote c should say "PET −15.6 C modelled (Santos Nouri 2018), field shade data tropical (Abreu-Harbich 2012)". The scoring function `lit()` reads `lit_heat` in `porta_trait_table.csv`, which does not yet hold Armson's values, so the table needs the new species_measurements rows first. Regenerate `slides/fig/05_palette_data_gap.svg` and `.png` after that.
4. `databases/data_inventory_barcelona.md` D2 (line 43): "The named replacements (Celtis, Melia, Tipuana, Jacaranda, Brachychiton) have no values". Proposed: "...have no measured runoff value; Tipuana has modelled and tropical field heat values, Pyrus (named, not in this list) has measured runoff and heat". §E item 2 (line 49): "no interception or cooling measurements for Celtis, Melia, Tipuana, Jacaranda, Brachychiton" -> "no interception measurements for these five; cooling: modelled / tropical field only for Tipuana, none for the other four".
5. `notes/methodology.md` §3 gap-filling bullet (line 29, "covers Celtis, Melia, Tipuana, Jacaranda and Brachychiton"): still correct for runoff; add "Pyrus has measured storage and shade temperature; Tipuana has modelled PET".
6. Also check `notes/todo_manual.md` line 30 ("would give a second candidate species a cooling value"): consistent after the change, since Pyrus is the first.

## 4. Query log (WebSearch unless noted)

Found:
1. Santos Nouri 2018 Tipuana tipu Lisbon: found (simulation, SkyHelios / RayMan; summary only).
2. Monsi & Saeki 1953 title / DOI: no DOI for the original.
3. Monsi & Saeki 2005 Annals of Botany translation: found, doi 10.1093/aob/mci052 🟡. WebFetch PMC4246794: Hirose 2005, doi 10.1093/aob/mci047 (verified).
4. Armson 2013 species LAI values: abstract only; PDF URL returned HTML / 404 (WebFetch 404; curl returned an HTML page).
5. Melia azedarach LAI: plantation LAI 1.3-3.0 (Bot. Stud. 2017 table; Springer redirected to a login, so values are 🟡).
6. Moser-Reischl 2025 (via TUM portal WebFetch and a search): LAI database for 15 species; max LAI Tilia 4.7, Gleditsia 2.4; BAI 0.3 spring, 0.5 autumn / winter.
7. Barcelona leaf-fall / leaf-out (Catalan query): Celtis loses all leaves early to mid December (Betevé 2023); Tipuana "deciduous" in a UPC guide.
8. Abreu-Harbich 2015: found, doi 10.1016/j.landurbplan.2015.02.008; species values not shown.
9. Sanusi & Livesley 2020: found, no LAI numbers in the retrievable text.

Nothing found:
10. Platanus x acerifolia summer / winter LAI (street trees): none (closest: Peper & McPherson 2004 method paper; P. orientalis foliation LAI 0.80-2.76 not used).
11. Celtis australis LAI / transmissivity: none (only C. occidentalis in a thesis, numbers not read).
12. Tipuana tipu LAI / transmissivity: none.
13. Jacaranda mimosifolia LAI / transmittance: none; leaf habit conflicts across guides.
14. Pyrus calleryana LAI: none retrievable.
15. Robinia pseudoacacia LAI (street, hemispherical): none.
16. InsideWood / wood porosity for Celtis, Melia, Platanus, Styphnolobium: none retrievable.
17. Brachychiton populneus LAI / habit: no LAI; habit evergreen (some semi-deciduous in Canberra).
18. Dong 2025 global urban tree LAI dataset (doi 10.1038/s41597-025-04729-y): checked, aggregate 500 m product, no species values; not added to the matrix.

Failed fetches: MDPI atmos 9(1):12 (HTTP 403), Springer table (login redirect), auf.isa-arbor.com PDF (HTML or 404), reading.ac.uk eprints (proxy 502). The 18 logged queries plus 6 fetches stay inside the modest budget.
