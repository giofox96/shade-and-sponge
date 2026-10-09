# TRY data request: Porta street-tree palette (prepared 9 Oct 2026, not yet submitted)

Claude cannot submit the request. TRY makes the registered user the PI of the request, and the PI signs the
TRY Intellectual Property Guidelines, so the user must submit it from their own account
(https://www.try-db.org/TryWeb/Prop0.php). Everything to paste is below.
Save the reply (zip / `.txt` export) in `databases/TRY_DATABASE/` (git-ignored), then run `scripts/try_clean.py` on it.

## Files
- `species_ids.csv`: the 21 species of `databases/traits/porta_trait_table.csv` with their TRY `AccSpeciesID`
  (from `https://www.try-db.org/dnld/TryAccSpecies.txt`). *Platanus × acerifolia* is listed in TRY as *Platanus x hispanica* (252869).
- `trait_ids.csv`: the 18 TraitIDs to tick, grouped by the four requested traits (from the public TRY Data Explorer trait table).
- `coverage_preview.csv`: number of TRY records per species and trait group, split into public / restricted / not yet curated
  (TRY Data Explorer, "Measurement table sorted by trait", per species, 9 Oct 2026). Counts only, no trait values.

## TraitIDs to tick
| Requested trait | TraitIDs |
| --- | --- |
| Leaf phenology type | 37 (Leaf phenology type), 1251 (Plant vegetative phenology), 12 (Leaf lifespan) |
| Leaf area | 3108, 3109, 3110, 3111, 3112, 3113, 3114 (all petiole / leaflet variants) |
| Wood vessel anatomy (ring- vs diffuse-porous) | 1239 (Wood vessel distribution), 273 (Wood growth ring distinction), 275 (Wood vessel arrangement), 276 (Wood vessel grouping) |
| Leaf wettability / water storage | 930 (Leaf contact angle of water droplets), 713 (Leaf water storage time constant), 714 (Leaf water storage transfer resistance), 436 (Crown rainfall interception) |

Which vessel TraitID carries "ring-porous / diffuse-porous" is not stated in the trait table (no definitions).
1239 "Wood vessel distribution" is the most likely one; check its values in the reply.

## Coverage preview (what the reply can contain)
- **Leaf wettability / water storage: 0 records for all 21 species.** TRY has these traits for only 4–6 species worldwide.
  The gap must be filled from the literature (contact-angle and storage-capacity studies) or stay a stated limitation.
- **Leaf phenology:** public records for 20 of 21 species; none at all for *Handroanthus heptaphyllus*.
- **Leaf area:** public records for 14 species. Only restricted records for *Platanus*, *Catalpa*, *Handroanthus*
  and *Styphnolobium*; none for *Pyrus calleryana*, *Jacaranda* or *Tipuana*.
- **Wood vessel anatomy:** public records for 14 species; none for *Pyrus*, *Tipuana*, *Brachychiton*, *Grevillea*,
  *Casuarina*, *Celtis sinensis* or *Handroanthus*.
- Restricted records need the data owners' permission (TRY says they answer within two weeks). Public data are released as soon as processed.

## Steps (user)
1. Log in at try-db.org (register first if needed), then Data Portal → Request Data → "Get data from the TRY database" (traits and species).
2. Accept the Intellectual Property Guidelines.
3. Tick the 18 TraitIDs above.
4. Select the 21 species by `AccSpeciesID` / name from `species_ids.csv`.
5. Paste the project description below. Request restricted data too: the description is what convinces the data owners.
6. Submit. When the email arrives, save the export in `databases/TRY_DATABASE/` and record the request ID, date and release version here.

## Project description to paste
Title: Trait-based street-tree selection for pluvial runoff and heat mitigation in Barcelona

MaCAD thesis, Institute for Advanced Architecture of Catalonia (IAAC), 2026. We build a computational method that selects and
places street-tree species in one Barcelona neighbourhood (Porta, Nou Barris) to reduce surface runoff during design storms and
improve outdoor thermal comfort (UTCI). Species-level traits feed a canopy interception model and a shading model: leaf phenology
(winter interception and shade), leaf area and leaf water storage or wettability (canopy storage capacity), and wood vessel anatomy
(drought vulnerability under future heat). The request covers the 21 species of the current street-tree palette. Trait values are
used only as species means or medians, with the source datasets cited individually and TRY cited as Kattge et al. (2020).

## Status
- [ ] Request submitted (date, request ID)
- [ ] Public data received
- [ ] Restricted data answered
