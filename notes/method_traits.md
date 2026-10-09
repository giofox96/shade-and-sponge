# Canopy trait parameters for the palette: citations, gap-filling rules, coverage (issue #4)

Draft, 9 Oct 2026. Data: `notes/lit/species_canopy_params.csv` (101 rows: 8 palette species, 6 optional taxa, 3 class rows). LiDAR and BROT values are in `databases/traits/porta_trait_table.csv` and are referenced, not copied. Leaf-on calendar: `databases/traits/phenology_palette.csv`. Marks: (abs) = abstract only; 🟡 = from a web-search summary, not the paper.

## 1. Monsi & Saeki citation (for methodology §3, "to add")

- Original: Monsi, M. & Saeki, T. (1953). Über den Lichtfaktor in den Pflanzengesellschaften und seine Bedeutung für die Stoffproduktion. *Japanese Journal of Botany* 14: 22-52. **No DOI exists for the original**; the page numbers come from a reference list that cites it, not from the journal record 🟡.
- English translation (cite this for readers): Monsi, M. & Saeki, T. (2005). On the factor light in plant communities and its importance for matter production. *Annals of Botany* 95(3): 549-567. DOI **10.1093/aob/mci052** 🟡 (title, volume, pages and DOI read from the Oxford Academic issue listing via search; the article page itself was not opened).
- Review that explains the theory: Hirose, T. (2005). Development of the Monsi-Saeki theory on canopy structure and function. *Annals of Botany* 95(3): 483-494. DOI 10.1093/aob/mci047 (verified on PMC4246794).
- What the source gives: light attenuates through leaf layers following a Beer-Lambert form; the extinction coefficient is 1 for ideally distributed horizontal leaves and falls with leaf angle down to 0.44 (leaf angle 90 deg) 🟡.
- Proposed wording for `methodology.md` §3 line 31 (not edited): "τ = exp(−k·LAI) (Beer-Lambert; Monsi & Saeki 1953, English translation 2005, doi:10.1093/aob/mci052)".

## 2. Decision on k

`methodology.md` §3 already fixes k = 0.5 "as in Peng et al. (2026)" (matrix #53: canopy transmittance exp(−0.5·LAI) in Ladybug Outdoor Solar MRT; the same value is in `scripts/bcn_lidar_porta.py` and `shade_sponge/heat.py`). I did not reopen it. Species-specific k is treated only as a sensitivity question: the theory range 0.44 to 1 (🟡) is the band to test, and no species-specific k was found for any of the 14 taxa. Peng's own check is a warning, not a fix: under one camphor tree (LAI 3.2) the LAI-revised MRT was 45.2-46.5 C against 46.5-48.6 C measured (#53), so a constant k still leaves an error of about 1-2 C (own subtraction of the quoted ranges; #53 reports 2-4 C).

## 3. Gap-filling rules (measured species per class)

| Rule | Applies to | Class values (measured species n) | Flag |
|---|---|---|---|
| A. Summer LAI bracket | species with no literature LAI (Celtis, Pyrus, Jacaranda, Tipuana, Brachychiton; all optional taxa) | Deciduous broadleaf: 1.98-4.71, n = 9 (Platanus 3.02, Ulmus procera 4.71, Betula pendula 2.6, Ginkgo 1.98, Zelkova 3.28, Aesculus turbinata 3.37, Styphnolobium 2.61 from full text; Tilia cordata max 4.7 and Gleditsia max 2.4 from abstracts). Melia azedarach 1.3-3.0 (🟡, plantation) is kept outside the range. | Deciduous n = 9 is fine. **Evergreen / semi-deciduous broadleaf n = 1** (camphor, LAI 3.2, Peng 2026): below 2, so Brachychiton, Tipuana, Jacaranda, Citrus, Grevillea, Casuarina take the deciduous bracket as an ASSUMPTION. The values are single trees or juveniles with different instruments (TLS, handheld TLS, hemispherical photos), not harmonised. The LiDAR proxy already exists for 7 of 8 palette species, so this rule is a sensitivity bracket, not a replacement. |
| B. Leaf-off LAI | all deciduous taxa in the leaf-off months | Betula pendula leafless 0.8 (full text); Moser-Reischl 2025 (abs) reports a branch area index of 0.5 in autumn / winter (0.3 in spring), a different quantity, not a second leaf-off band. Species-level n = 1. | **n = 1: below 2.** Platanus leaf-off is only known as storage −90% (Baptista, #6), not as LAI. Semi-deciduous Tipuana / Jacaranda: n = 0, no rule; use a bracket between the deciduous leaf-off band and leaf-on, ASSUMPTION. Evergreen: leaf-off = leaf-on. |
| C. Transmissivity | all taxa | k = 0.5 default, sensitivity band 0.44-1.0. Species-level k measured: n = 0. | **n = 0.** Leaf-on / leaf-off transmissivity is derived from LAI, never measured per species. |
| D. Wood porosity (transpiration class) | all taxa | Genus-level class from InsideWood or TRY once available. Measured / classified species found: n = 0. | **n = 0**; waits for the TRY request in `notes/todo_manual.md`. Why it matters: diffuse-porous species transpire 2-3x ring-porous ones (Bachofen 2025, #43). |

Habit and leaf calendar need no rule: they are sourced for 7 of 8 palette species (Styphnolobium missing), with Jacaranda and Tipuana flagged uncertain (conflicting sources in the CSV).

## 4. Coverage of the six parameters (species-level values only; class defaults and the k default do not count)

| Parameter | Palette species covered (of 8) | % | Notes |
|---|---|---|---|
| Summer LAI (literature) | 3 (Platanus, Melia 🟡, Styphnolobium) | 38 | Pyrus measured by Armson 2013 but values unread |
| Leaf-off LAI | 0 | 0 | class value only |
| Transmissivity / k | 0 | 0 | method default only |
| Leaf habit | 7 (Jacaranda, Tipuana uncertain; Styphnolobium missing) | 88 | 5 firm = 63% |
| Leaf-out / fall months | 5 (Platanus and Celtis leaf-out + Celtis fall 🟡, Jacaranda, Tipuana, Brachychiton) | 63 | Melia, Pyrus = class default; Platanus fall = default |
| Wood porosity | 0 | 0 | |
| **All 48 palette cells** | **15** | **31** | optional taxa: 0 of 36 (0%); all 84 cells: 15 (18%) |

| Species | Parameters covered (of 6) | % |
|---|---|---|
| Platanus x acerifolia | 3 (LAI, habit, months) | 50 |
| Celtis australis | 2 (habit, months) | 33 |
| Melia azedarach | 2 (LAI 🟡, habit) | 33 |
| Pyrus calleryana | 1 (habit) | 17 |
| Jacaranda mimosifolia | 2 (habit uncertain, months) | 33 |
| Tipuana tipu | 2 (habit uncertain, months) | 33 |
| Brachychiton populneus | 2 (habit, months) | 33 |
| Styphnolobium japonicum | 1 (LAI) | 17 |
| Six optional taxa | 0 each | 0 |

LAI literature vs the LiDAR proxy: only Platanus (3.02 literature, juvenile potted; the proxy is lower), Melia (proxy inside 1.3-3.0) and Styphnolobium (2.61, no proxy because only 5 trees) can be compared. The Jacaranda proxy is the highest of the palette although its crown is fine-leaved and possibly semi-deciduous, so it is worth a check.

## 5. PDFs the user must fetch

All listed in `notes/lit/to_get_manually.md` (added today). In order of use:
1. Moser-Reischl et al. 2025, doi 10.1016/j.ufug.2025.128795: species LAI and leaf-off values; check for Platanus, Robinia, Populus, Catalpa.
2. Armson et al. 2013, doi 10.48044/jauf.2013.021: per-species LAI and shade temperature (the user's local PDF exists; only the abstract was read here).
3. Santos Nouri et al. 2018, doi 10.3390/atmos9010012 (already in `notes/todo_manual.md`): confirm simulated vs measured and the winter values.
4. Abreu-Harbich et al. 2015, doi 10.1016/j.landurbplan.2015.02.008: Tipuana and Jacaranda species values (unverified that they are included).
5. Sanusi & Livesley 2020 (already listed): Platanus leaf-off LAI after heat.
6. Gandia-Ventura et al. 2025, Biology 14(11):1569 (Jacaranda phenology; cited in `phenology_palette.csv`, DOI not verified here).
7. Not duplicated here: the TRY request (leaf phenology, vessel anatomy) in `notes/todo_manual.md`, which would fill Rules B and D and the phenology gaps.
