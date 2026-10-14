# Canopy storage S: definition, units and reference areas (issue #5, 10 Oct 2026)

Records what runoff v1 already implements, reconciles the reference areas used in the notes, and defines the parameters of the two published models mentioned as refinements. Values are in `notes/lit/interception_params.csv`; references are verified in `notes/lit/method_references.md`. Marks: (abs) abstract only, 🟡 not checked against the primary text.

## 1. Implemented definition (runoff v1)

- **S [mm of water depth over the crown projected area] = s [mm per unit one-sided LAI] x LAI [m2 leaf per m2 crown projection].**
- Event interception **I = min(P, S)** [mm], applied as a depth over every cell inside the crown disk (`storage_raster`, `scripts/runoff_model.py` lines 87-95). Where crowns overlap, the cell takes the **maximum** S, not the sum. Over **roofs S = 0** (roof runoff goes to downpipes). Background (park/private) canopy gets s x 2.3 (`runoff_params.json`, ASSUMPTION for the 2.3).
- Effective rain P_eff = P - I goes into SCS-CN (TR-55 curve numbers; CN 74 for pervious is an ASSUMPTION).
- **s = 1.75 mm per unit LAI** is **calibrated**, not measured storage: pooled median over 16 *Tilia cordata* / *Acer platanoides* in Freiburg (Anys & Weiler 2024, 10.1002/hyp.15146; `scripts/calibrate_interception.py`; table `databases/traits/interception_calibration.csv`). Range across trees 1.22-3.85 (lime median 1.85, maple 1.60). It is an **effective** value: the fit absorbs wet-canopy evaporation during events, drip lag and wood storage into one number, which is why the model can ignore event evaporation (docstring of `runoff_model.py`). Consequences: (a) it is not a physical storage and must not be compared 1:1 with simulator values; (b) it was fitted on 6.7 mm mean events in a Cfb climate; for Barcelona's short intense storms it may be lower (methodology 4b already says so; sensitivity s = 0.86 / 1.75 / 2.2 in `runoff_sensitivity_storage.csv`); (c) transfer to Mediterranean species and to evergreens is an ASSUMPTION.
- Stemflow is ignored (<1% of rain, Anys & Weiler 2024).

## 2. Reconciling the reference areas

| Quantity | Value | Reference area | Where used |
|---|---|---|---|
| s (calibrated) | 1.75 mm per LAI | crown projected area, per unit one-sided leaf area index | runoff_model.py, methodology 4b |
| s per PAI (calibrated) | median 1.39 (1.06-2.85) | crown projected area, per unit plant area index (leaf + wood) | interception_calibration.csv |
| Xiao & McPherson 2016 storage | 0.86 mean; Platanus 0.87, Pyrus 0.51, Celtis sinensis 0.71 | **per unit leaf + stem surface area** (rainfall simulator, water held after drip) | methodology 4b lower bound; 3 species factor s_sp = s C_sp / 0.86 |
| Baptista 2018 Cmax | Platanus 0.49 (LAI 3.02), Ulmus 0.69 (LAI 4.71) | **canopy projected area**, juvenile potted trees, rain-limited | not used as capacity |
| i-Tree Hydro S_L | 0.2 mm per LAI (S_vmax = S_L LAI) | per unit LAI, leaf only | Huang 2017, Wang 2008 (via i-Tree docs) |

Problems on main:
1. **0.86 is a per-surface-area film depth, not a per-LAI canopy depth.** Using it as the lower bound of s (methodology 4b) is only valid if leaf+stem surface area per unit crown projection is about 1 x LAI. Whether Xiao & McPherson's leaf area is one-sided or both-sided was not checked in this task 🟡; if both-sided, per one-sided LAI the film depth is up to 2 x 0.86.
2. **The bridge** from surface-area values to crown depth is: S_crown = c_surf x A_surf / A_crown, with A_surf / A_crown = PAI x f (f = 1 one-sided, 2 both-sided). With c_surf = 0.86 and the calibration-set mean PAI 4.24 (mean LAI 3.5) the static film storage is 3.6 mm (f = 1) up to 7.3 mm (f = 2), i.e. 0.86 to 1.7 mm per unit PAI. The calibrated s per PAI (median 1.39) falls inside that range, which supports 1.75 per LAI as a film-storage-order value rather than needing event evaporation to explain it. That is a plausibility check, not a validation.
3. **s_sp = s x C_sp / 0.86 is a relative scaling**: valid only if species differ in film depth per surface area but not in surface area per LAI. It stays an option for v2; the species factor should be applied to s per LAI, and PAI/LAI ratio (leafless wood share) is a separate trait.
4. **Baptista 0.49 mm is about 11 x smaller than s x LAI** (1.75 x 3.02 = 5.3 mm) and about 5 x smaller than 0.87 x LAI. The authors' event delivered only 0.64 mm, so the value is rain-limited; do not use it as a capacity. i-Tree's 0.2 mm per LAI (0.6 mm at LAI 3) is the low end; Coville 2022's 2.0 mm leaf storage depth (as quoted in methodology 4b, not re-read) the high end.

## 3. Parameters of the revised Gash model (for a possible v2)

Definitions and units follow the table in Zhang et al. 2006 (10.5194/hess-10-65-2006, Table 2, opened); the formulas themselves are from Gash 1979 and Gash et al. 1995 and were not checked against those papers 🟡. Rain events are discrete; each has a wetting-up, a saturated and a drying phase.

| Symbol | Meaning | Unit |
|---|---|---|
| P_G | gross rainfall of a storm | mm |
| P_G' | rain needed to saturate the canopy = -(R/E) S ln[1 - E/R] (simplified form; Zhang 2006 Table 2 has E/((1-p-p_t) R) inside the log; sparse form uses S_c and E_c per unit cover) | mm |
| S | canopy storage capacity, per unit **ground area** of the stand | mm |
| S_c = S / c | capacity per unit **canopy-covered** area (sparse-forest version, Gash et al. 1995) | mm |
| c | canopy cover fraction (p is often set to 1 - c) | - |
| p | free throughfall coefficient | - |
| p_t | fraction of rain diverted to stemflow | - |
| S_t | trunk storage capacity | mm |
| E (E_c = E/c) | mean evaporation rate from the wet canopy during rain | mm h-1 |
| R | mean rainfall rate over the hours when it rains, canopy saturated | mm h-1 |
| E/R | the ratio Huang et al. 2017 (abs for the number) found most sensitive | - |
| epsilon | ratio of trunk to canopy evaporation (Valente et al. 1997) | - |

Reference-area warning: the Gash S is per ground area of the stand (S_c per covered area), our s x LAI is per crown projection, so a street tree's S_c is the comparable quantity. Gash is built for forest stands; Huang et al. 2017 applied it to trees but validated on two conifers only (matrix row 33). Values of E/R were not extracted (see interception_params.csv, empty cells).

## 4. i-Tree Hydro / UFORE parameters (read in the i-Tree documents)

- Leaf storage: **S_vmax = S_L x LAI, S_L = 0.0002 m = 0.2 mm per unit LAI** (Wang et al. 2008 as implemented in i-Tree Eco v5). Leaf only; bark, branches and trunk are omitted in this form (i-Tree Streets/Design/Eco comparison, section 2.2).
- Cover: c = 1 - exp(-k LAI), k = 0.7 trees, 0.3 shrubs; free throughfall = P (1 - c).
- Evaporation from storage: E_v = (S_v / S_vmax)^(2/3) PE.
- **Bark/trunk storage: no numeric value found in these documents**; the older Xiao et al. 1998 model includes leaf and trunk storage but its details are "not revealed" (comparison document). Cell left empty.
- Compare: 0.2 mm per LAI (i-Tree) vs 1.75 (ours, effective) vs 0.86 (Xiao per surface area): three different quantities, factor 9 apart.

## 5. Proposed rewording of methodology section 4, step 2 (proposal only)

Current text: "storage-bucket I = min(P, S) with S from species storage capacity x LAI."

Proposed: "**Canopy interception** over each crown's projection: storage bucket I = min(P, S), S = s x LAI [mm over the crown projected area], with s = 1.75 mm per unit one-sided LAI, an effective value calibrated on Anys & Weiler (2024) that includes evaporation during events (sensitivity 0.86-2.2). Where crowns overlap the larger S applies; over roofs S = 0. Species enter only through LAI (and, in v2, a relative factor C_sp / 0.86 on s from Xiao & McPherson 2016, whose values are per unit leaf + stem surface area and are not directly depths over the crown). An analytical Gash-type model (Hassan et al. 2017; Huang et al. 2017) is the refinement, with the limits stated in section 3 above."

Also for §3/§4b: say that 0.86 mm is a surface-area film depth and a lower bound only after conversion by PAI x f (section 2).

## 6. Open

- Whether Xiao & McPherson's leaf area is one- or two-sided (read their Methods) fixes f.
- No numeric interception or storage source for *Melia azedarach*, *Tipuana tipu*, *Brachychiton populneus*, *Catalpa bignonioides*, *Grevillea robusta*, *Populus nigra*; *Citrus*, *Robinia*, *Casuarina*, *Jacaranda* only as genus/class or low-confidence values. Fallback: leaf-habit class (deciduous / evergreen) with the calibrated s and the sensitivity range.
- Transfer of s from Freiburg Tilia / Acer to Barcelona storms and species is an ASSUMPTION.
