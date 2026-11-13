# Barris rerun with 1:1000 map footprints (12–13 Nov 2026)

What changed: building footprints in all 32 barris now come from the city's 1:1000 topographic map (WMS layer `Polígons_construccions`, CC BY 4.0) instead of OSM or LiDAR-traced polygons, heights still from LiDAR (same rule as Porta, PR #117). Run: `python scripts/run_barris.py <32 barris> --buildings` (buildings step, site cache rebuilt, tool rerun with `--size=exact --trunk=TERCERA`). No barri fell back to LiDAR footprints. "Before" = the committed results of 28–31 Oct.

Margins are the summer-shade share of today (S0) of the optimised layout with the most summer shade minus the city mix (S1a, 10 seeds) or the observed mix (S1b), in percentage points (`databases/barcelona/barris_summary.csv`).

| Barri | Buildings | Roofs % | S0 runoff m³ | Margin vs city mix S1a (pts) | Margin vs S1b (pts) |
|---|---|---|---|---|---|
| Sant Pere, Santa Caterina i la Ribera | 1,263 → 17,238 | 21.7 → 21.8 | 23,281 → 23,300 | 9.9 → 11.5 | 14.8 → 15.2 |
| Sant Antoni | 2,415 → 30,352 | 52.5 → 52.2 | 19,674 → 19,670 | 6.9 → 8.7 | 7.0 → 12.5 |
| el Fort Pienc | 767 → 10,184 | 28.6 → 28.4 | 20,855 → 20,854 | 9.8 → 10.0 | 5.4 → 4.6 |
| l'Antiga Esquerra de l'Eixample | 2,586 → 36,165 | 58.8 → 54.0 | 30,929 → 30,141 | 7.9 → 7.1 | 7.1 → 6.5 |
| la Dreta de l'Eixample | 3,385 → 45,969 | 48.1 → 46.6 | 53,028 → 52,202 | 11.0 → 12.5 | 12.3 → 17.2 |
| la Nova Esquerra de l'Eixample | 2,089 → 30,755 | 49.5 → 48.1 | 33,526 → 31,613 | 8.4 → 8.1 | 11.4 → 10.2 |
| la Sagrada Família | 735 → 24,541 | 48.3 → 49.1 | 25,942 → 24,796 | 3.1 → 3.2 | 5.3 → 7.5 |
| Horta | 2,465 → 17,992 | 12.3 → 13.3 | 58,770 → 58,804 | 7.1 → 6.5 | 7.2 → 6.4 |
| Pedralbes | 1,051 → 14,820 | 13.2 → 13.7 | 50,742 → 50,864 | 3.4 → 3.4 | 7.9 → 7.9 |
| la Maternitat i Sant Ramon | 1,388 → 12,408 | 22.9 → 23.4 | 41,560 → 41,533 | 4.8 → 4.2 | 12.6 → 12.2 |
| les Corts | 1,985 → 23,054 | 40.9 → 38.1 | 32,199 → 32,130 | 2.1 → 2.1 | 3.6 → 3.5 |
| Baró de Viver | 127 → 1,417 | 19.1 → 20.0 | 5,388 → 5,389 | 0.8 → 1.2 | 0.9 → 1.8 |
| Navas | 1,425 → 12,564 | 45.2 → 43.3 | 10,570 → 10,101 | 3.1 → 6.0 | 4.3 → 8.3 |
| Sant Andreu | 3,651 → 23,044 | 36.1 → 36.1 | 44,873 → 44,864 | 10.0 → 9.6 | 12.6 → 12.3 |
| el Bon Pastor | 1,225 → 8,585 | 38.2 → 40.9 | 46,367 → 46,433 | 5.4 → 5.2 | 6.9 → 11.0 |
| el Congrés i els Indians | 1,051 → 11,749 | 46.7 → 42.0 | 9,739 → 9,715 | 0.9 → 1.1 | 1.3 → 1.4 |
| la Sagrera | 1,517 → 14,379 | 26.0 → 30.3 | 23,056 → 23,069 | 3.2 → 3.1 | 9.0 → 5.8 |
| la Trinitat Vella | 752 → 3,820 | 16.4 → 16.8 | 16,875 → 16,876 | 7.4 → 5.4 | 8.2 → 7.0 |
| Diagonal Mar i el Front Marítim del Poblenou | 504 → 5,024 | 13.6 → 13.2 | 29,633 → 23,362 | 5.7 → 6.0 | 3.4 → 3.6 |
| Provençals del Poblenou | 779 → 7,868 | 14.4 → 13.0 | 26,121 → 24,392 | 3.6 → 4.7 | 8.9 → 13.4 |
| Sant Martí de Provençals | 533 → 4,717 | 26.5 → 24.0 | 17,660 → 15,425 | 6.8 → 7.9 | 12.0 → 10.8 |
| el Besòs i el Maresme | 1,091 → 4,095 | 23.7 → 21.0 | 29,736 → 27,779 | 5.3 → 4.9 | 12.5 → 12.5 |
| el Camp de l'Arpa del Clot | 548 → 21,601 | 52.2 → 51.8 | 18,704 → 18,468 | 2.2 → 2.7 | 2.5 → 3.4 |
| el Clot | 1,350 → 14,576 | 34.2 → 35.3 | 17,357 → 15,168 | 5.9 → 6.3 | 12.0 → 12.7 |
| el Parc i la Llacuna del Poblenou | 812 → 12,101 | 32.7 → 32.0 | 27,854 → 25,578 | 6.2 → 6.4 | 11.0 → 14.2 |
| el Poblenou | 775 → 11,169 | 32.4 → 31.4 | 38,731 → 35,153 | 10.1 → 10.1 | 18.1 → 16.2 |
| la Verneda i la Pau | 887 → 5,893 | 31.5 → 29.4 | 27,536 → 27,505 | 10.2 → 8.6 | 7.9 → 6.1 |
| la Vila Olímpica del Poblenou | 708 → 5,645 | 22.5 → 20.9 | 22,366 → 19,483 | 5.5 → 4.9 | 4.4 → 4.1 |
| el Poble-sec | 2,826 → 23,287 | 13.9 → 14.4 | 43,574 → 43,625 | 3.6 → 2.4 | 5.4 → 4.3 |
| Sant Gervasi - Galvany | 3,069 → 36,259 | 47.6 → 46.0 | 39,494 → 39,460 | 6.9 → 7.1 | 6.0 → 7.4 |
| Sant Gervasi - la Bonanova | 1,953 → 25,411 | 23.4 → 22.6 | 49,411 → 46,722 | 2.8 → 2.8 | 3.2 → 2.9 |
| les Tres Torres | 1,312 → 16,781 | 33.7 → 33.4 | 18,375 → 18,349 | 4.7 → 5.3 | 6.9 → 6.6 |
| **Median (32)** | 1,244 → 14,478 | 31.9 → 30.9 | 27,695 → 25,187 | 5.6 → 5.7 | 7.2 → 7.5 |

**Reading.**
- No sign changes: the tool beats S1a and S1b in all 32 barris, before and after. Median margin vs S1a 5.6 → 5.7 pts, vs S1b 7.2 → 7.5 pts.
- Ranking of barris by the S1a margin: Spearman 0.93; 28 of 32 barris move, by at most 11 places (many margins are within a few tenths).
- Building counts grow about tenfold (the map splits blocks into volumes); median roof share 31.9% → 30.9%.
- S0 runoff falls by more than 5% in Diagonal Mar (−21%), Sant Martí de Provençals (−13%), el Clot (−13%), la Vila Olímpica (−13%), el Poblenou (−9%), el Parc i la Llacuna (−8%), el Besòs (−7%), Provençals (−7%), Sant Gervasi - la Bonanova (−5%) and la Nova Esquerra (−6%). The roof share alone does not explain all of it (not checked further).
- **Open:** la Verneda i la Pau and Sant Gervasi - la Bonanova were built while Overpass was down, so their pervious ground comes from NDVI only (no OSM parks/gardens/grass); to rerun.
- **Open:** the city-wide LP with the local ceiling (`scripts/city_lp.py --local-ceiling`, Porta + 27) is now infeasible: in el Camp de l'Arpa del Clot (496 planes) the ceiling leaves Celtis 0 trees, and some positions fit no other species under the new façade distances. `citylp_*` tables and the city slide figures are therefore still the 31 Oct ones. The Barcelona-palette (30 species) per-barri runs were not redone either.
