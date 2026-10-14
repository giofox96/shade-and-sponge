# Heat module: tree representation, tau, validation rule (issue #8, 14 Oct 2026)

Builds on `methodology.md` §3/§5 and matrix rows 51 and 53 (not re-derived). Matrix ids are those of the branch on 14 Oct (main ends at id 56; this branch already has rows up to #128); new rows are #129-133 and may need renumbering if other PRs add rows. Marks: (abs) = abstract only; 🟡 = unverified or seen in a search summary only. Code lines refer to `master` on 14 Oct 2026 and can shift; all fetched through `raw.githubusercontent.com`.

## 1. Tier 1 crown treatment in ladybug-tools

**Crowns are context geometry that blocks rays, nothing else.** There is no transmittance, LAI or tree object in this path.

| Step | File (repo) and lines | What it does |
|---|---|---|
| Direct-sun exposure | `LB Human to Sky Relation.py` (ladybug-grasshopper `ladybug_grasshopper/src/`) l.201 `join_geometry_to_mesh(_context)`, l.214 `intersect_mesh_rays` (sun vectors), l.132-153 `fract_exposed_from_mtx` | Fraction of human points whose ray to each sun position is unobstructed. Output `fract_body_exp`, an hourly collection in 0-1 (binary per ray, averaged over the body points). |
| Sky exposure | same file, l.226 `intersect_mesh_rays` (Tregenza dome vectors), l.169-173 `sky_exposure_from_mtx` | Patch-weighted unobstructed sky fraction (145 patches). Output `sky_exposure`. |
| Wiring | `LB Outdoor Solar MRT.py` l.34 `fract_body_exp_`, l.41 `sky_exposure_`, l.86 `OutdoorSolarCal(...)` | The two collections are plain inputs. |
| Collection class | `ladybug_comfort/collection/solarcal.py` l.130 `OutdoorSolarCal`, l.185-213 (inputs, `_fraction_input_check`), l.221 `_calculate_solarcal` | Passes them to the function level. |
| Body flux | `ladybug_comfort/solarcal.py` l.440-476 `body_solar_flux_from_parts` | `dir + diff + ref`. |
| Direct term | same, l.636-661 `body_dir_from_dir_normal` | `proj_fac * fract_exposed * dir_normal_solar` (l.661). Linear in `fract_exposed`. |
| Diffuse and reflected | same, l.555-568 and l.571-588 | `0.5 * sky_exposure * fract_efficiency * diff_horiz` (l.568); reflected has the same factor (l.588). Longwave sky term also takes `sky_exposure` (l.404). |

Surfaces blocking the sky are assumed to be at the `_surface_temp_` input (docstring l.~20 of the MRT component: "typically outdoor dry bulb"), so an opaque crown emits longwave at air temperature. That part of the longwave is already a reasonable approximation.

**Where Peng's tau enters (no source change needed).** Because the direct term is linear in `fract_body_exp`, tau can be folded into that input before `LB Outdoor Solar MRT`:

1. Run `LB Human to Sky Relation` twice per point: context = buildings only, giving `f_b`; context = buildings + crowns, giving `f_bc`.
2. Set `fract_body_exp_ = f_bc + tau(t) * (f_b - f_bc)`, with `tau(t) = exp(-0.5 * LAI(t))` per hour (leaf-on/off calendar from `season.py`). A point under several crowns takes the mean tau of the crowns it sees (🟡 simplification).

This is my construction from the code above, not text from Peng 2026. Methodology §5 says "in the SolarCal step"; this is the input that does it. 🟡 Whether Peng modified source code or the inputs is not recorded in the matrix; check the PDF in `papers/`.

**Does sky view / diffuse need it?** Not recorded for Peng (🟡 check PDF). Physically yes: an opaque crown sets `sky_exposure` too low, which lowers the diffuse (l.568), reflected (l.588) and sky-longwave terms, so it adds to the low shade-MRT bias. The same trick applies, `sky_exposure_ = s_bc + tau_d * (s_b - s_bc)`, but `tau_d` (hemispherical) is not `exp(-0.5 LAI)`: the Beer-Lambert path length depends on zenith angle. STMRT handles direct and diffuse separately with leaf-angle projection G (Li et al. 2023, #95, full text). Recommendation: correct direct only in Tier 1 (the part with evidence), report diffuse as an untested residual, and use the Tier 2 comparison (section 6) to size it.

**Tier 2 (honeybee-radiance).**
- Tree crowns as `Shade` objects with a Radiance modifier; the comfort map traces sun rays to each sensor (`HB UTCI Comfort Map.py`, docstring l.25-34: Radiance enhanced 2-phase for shortwave, direct sun by ray to the sun position; outdoor context shades at air temperature).
- Modifier for tau: `honeybee_radiance/modifier/material/glass.py`, `Glass.from_single_transmittance(identifier, rgb_transmittance)` (l.257) or `from_transmittance` (l.183). It converts transmittance to Radiance transmissivity in `_transmissivity_from_transmittance` (l.416-420: `(sqrt(0.8402528435 + 0.0072522239*T^2) - 0.9166530661) / 0.0036261119 / T`), with `transmissivity_from_transmittance` (l.383) and the inverse (l.397). Glass is specular (no scatter), so it suits the direct beam and ignores foliage scattering; `Trans` (`trans.py` l.12, `from_average_properties` l.351, `average_transmittance` l.200) is the scattering alternative (🟡 not tested which one the 2-phase direct-sun trace honours better).
- Energy side: `honeybee_energy/properties/shade.py` l.25 `transmittance_schedule` (a schedule, default None = opaque) is the hook for the leaf-on/off cycle.
- Reference for the tau-to-Radiance mapping: the conversion above is the Radiance glass-primitive relation as implemented in honeybee (the Radiance reference manual itself was not read, 🟡). Tan & Liu 2026 (#80, full text) is the only precedent in the matrix that drives Honeybee radiation with species-specific Beer-Lambert canopy transmittance; the matrix does not record their mapping.

## 2. Tau correction and the LiDAR LAI proxy

- **Formula and source:** tau = exp(-k LAI), k = 0.5 (Peng et al. 2026, #53, DOI 10.1007/s10980-026-02324-z, full text). One camphor tree, LAI 3.2: measured MRT 46.5-48.6 °C; stock LBT 42.1-44.0 °C (>6 °C low); LAI-revised 45.2-46.5 °C (2-4 °C low). Tau at LAI 3.2 is exp(-1.6) = 0.20 (my arithmetic).
- **Limits of constant k:** k = 0.5 is the spherical-leaf value and ignores sun zenith, clumping and leaf angle. STMRT (Li et al. 2023, #95, 10.1016/j.buildenv.2022.109846, full text 12 Oct): MRT within about 2.3 °C of measurement; species leaf-angle differences change MRT by up to 9.5 °C, a uniform leaf-angle assumption (as in ENVI-met) by up to 5.7 °C.
- **Can the LiDAR LAI proxy feed tau? Technically yes, but it is circular, and the values are high.**
  - `scripts/bcn_lidar_porta.py` l.127: `lai_proxy = -ln(gap_fraction.clip(0.02, 1)) / K`, K = 0.5. So `exp(-0.5 * lai_proxy)` returns the LiDAR gap fraction itself: tau = share of pulses reaching the ground inside the crown disk. It carries no information beyond the gap fraction.
  - Medians of the species checked, not all palette species (`databases/barcelona/porta_species_lidar_summary.csv`): gap 0.23 (Jacaranda) to 0.39 (Gleditsia), i.e. tau 0.23-0.39; Platanus 0.32 (LAI proxy 2.31).
  - Sourced comparison values: Barcelona Platanus rows, best-fitting SOLWEIG canopy transmissivity 10% (SOLWEIG default 3%; Colaninno et al. 2025, #129, full text); Peng camphor 0.20 (computed above). The proxy tau for Platanus (0.32) is about three times Colaninno's best fit and 1.6 times Peng's, so Tier 1 would still under-shade (shade MRT too high, the opposite sign of the original error). Definitions differ (SOLWEIG scheme vs Beer-Lambert), so this is a direction check, not a correction.
  - Field LAI (Kaluarachchi et al. 2020, #45, canopy imager, Sydney): Platanus 2.8 (tau 0.25), Pyrus calleryana 2.6 (0.27), Jacaranda 2.0 (0.37). Proxy tau: 0.32, 0.35, 0.23. The ranking of Jacaranda flips. Different city and method (as in methodology §4b).
  - Leaf-on only: the LiDAR was flown 26 Sept 2021. Leaf-off tau needs a separate source (woody area; Sanusi & Livesley 2020, #66, PAI 4.0-5.0 before to 2.8-2.9 after a heatwave, a reminder that PAI varies in time).
- **Calibration needed before use (proposal):**
  1. Treat tau as a bracketed parameter: run {0.03, 0.10, 0.20, proxy gap} and report whether the species order of the heat result is stable (Kendall between settings). Brackets are all sourced above.
  2. Per-species scale factor from an independent gap fraction: sky-behind-crown photographs of Platanus, Jacaranda, Tipuana and others. The photo routine in `notes/todo_manual.md` l.6 (leaf state, Nov-Mar) already produces such frames; whether it can double as a gap-fraction measurement is the user's call.
  3. If a Platanus shade/sun globe pair is obtained (section 5, 6), fit one global tau on it, as Colaninno did, but on separate points from the ones used to judge it.

## 3. Validation table (heat, trees)

| # | Source, DOI | Method | How trees / LAI enter | Exact errors | Read level |
|---|---|---|---|---|---|
| 1 | Peng et al. 2026, 10.1007/s10980-026-02324-z (#53) | Field MRT under one camphor vs LBT, Shanghai | tau = exp(-0.5 LAI), LAI 3.2, in Outdoor Solar MRT | Measured 46.5-48.6 °C; stock LBT 42.1-44.0; LAI-revised 45.2-46.5 (2-4 °C low). No RMSE reported | full text |
| 2 | Mannucci et al. 2025, 10.1016/j.cacint.2025.100215 (#51) | LBT vs ENVI-met, 4 points, Ostia (Rome), hottest day | Trees as shade only | UTCI MBE 0.8-2.3 °C, CVRMSE 7-13%; MRT MBE 2.4-5.9 °C, CVRMSE 22-38%; up to +8.65 °C UTCI at 7-8 h; vegetation cooling underestimated by ~2-3 °C | full text; model vs model |
| 3 | Colaninno et al. 2025, 10.1016/j.scs.2025.106498 (#129) | SOLWEIG vs globe-derived Tmrt, 3 plazas in Gràcia, Barcelona, 26 Jul and 28 Aug 2022 | Tree DSM, canopy transmissivity 3/10/20% | Sun points: +6.6 to +8.7 °C (sim above measurement, 26 Jul). Shaded Rovira (Platanus rows): 29.5 °C (aniso., 10%) vs 30.4 °C measured; tau 3->10% raises Tmrt ~2.5 °C, ->20% up to ~6 °C. 28 Aug: aniso. model 3.3-4.0 °C below measurement | full text |
| 4 | Li et al. 2023 (STMRT), 10.1016/j.buildenv.2022.109846 (#95) | Canopy radiative-transfer model vs measurements and 4SAIL | Beer-Lambert with leaf-angle G, direct and diffuse | MRT within about 2.3 °C of measurement; vs 4SAIL < 2.0 °C except LAI 1-2 at zenith 70-80° | full text (12 Oct) |
| 5 | Ibrahim et al. 2020 (BSO), no DOI (#130) | Modified vs original LBT vs ENVI-met, Cairo and London, no trees | none | MRT RMSE new/original: 3.9/7.9, 6.9/9.1, 6.1/10.1, 7.1/8.2 °C; UTCI (Cairo 7 Jun) RMSE 4.44 -> 3.45 °C | full text; model vs model |
| 6 | López-Cabeza et al. 2025, 10.1016/j.ecmx.2025.101257 (#133) | LBT longwave MRT vs aerial thermography, Huelva | not stated | no numbers seen | (abs) search summary 🟡 |
| 7 | Lindberg & Grimmond 2011, 10.1007/s00704-010-0382-8 | SOLWEIG vegetation scheme, Göteborg | transmissivity scheme | RMSE 3.1 K, small overestimation in vegetation shade (search summary only) | not read 🟡 |
| 8 | Silva et al. 2025 (#47) | ENVI-met UTCI vs climate walks, Lisbon | LAD | UTCI RMSE ~2 °C | full text |

Gap: no source gives a Ladybug Tools (stock or tau-corrected) RMSE against measured MRT under Mediterranean trees. Rows 1 and 3 are the nearest (one reports ranges, the other is SOLWEIG). Nothing was found for Honeybee UTCI Comfort Map vs measurement with trees; a 2024 shade-textile study (Sci. Direct S2212095524002372, title only, page returned 403) is the closest and is not a canopy (🟡 not read).

## 4. The "Bath study"

Methodology §5 replaced "Bath study (to add)" with Mannucci 2025 on 8 Oct (commit 81042ff); the swap was not recorded. One search found the likely candidates: Ibrahim, Kershaw & Shepherd (University of Bath), a PLEA 2020 paper (Ladybug-tools vs ENVI-met, MRT/UTCI, three hypothetical layouts, no numbers on the portal page; #131, abs) and a BSO 2020 paper (#130, row 5 above, full text). Both are model-to-model, without trees or field data. That these are the study the issue meant is 🟡 (by name only). No DOI was found for either. Verdict: not a usable validation source; no reason to restore it.

## 5. Open measured MRT / globe / UTCI data for Barcelona

Result: no open dataset of measured MRT, globe temperature or UTCI for Barcelona was found.

| Dataset | What | Status | Licence |
|---|---|---|---|
| Colaninno et al. 2025 campaign (#129) | Globe, air T, RH, wind at 1.5 m at Joanic, Revolució, Rovira (Gràcia), 1-min, 30 and 20 min sessions | Not published; paper states "Data will be made available on request"; supplementary Annex has 1-min plots | none stated; request needed |
| Segura Barrero et al. 2022 (#132, abs) | Vehicle transects of up/down radiation, air T, humidity on two Barcelona streets with different tree density | Data location unknown; paper links a DDD UAB record (https://ddd.uab.cat/record/265716), contents not checked 🟡 | Paper CC BY-NC-ND 4.0; data unknown |
| Meteocat XEMA via Dades obertes de Catalunya (`analisi.transparenciacatalunya.cat`, dataset nzvn-apee; variable metadata 4fb2-n3yi) | Hourly station data. Metadata (68 variables, API read 14 Oct) lists global irradiance W/m² (code 36) and net irradiance (59) and no globe temperature | Reachable by API; nearest station to Porta not identified | Licence field says "See Terms of Use" (not read); Barcelona City Council copies labelled CC BY 4.0 (search summary 🟡) |
| Barcelona City Council weather-station files (`opendata-ajuntament.barcelona.cat`, station metadata and yearly statistics 2020-2025) | XEMA stations in the city | Variables not confirmed; portal blocked by a captcha from this environment | CC BY 4.0 (search summary 🟡) |

Use: XEMA irradiance can check the EPW forcing (issue #7), not MRT. Simulated-only Tmrt exists for Gràcia (Colaninno 2025) and is not an observation.

## 6. Tier 1 / Tier 2 agreement, acceptance rule, proxy check

All thresholds are sourced errors adopted as limits (a choice, stated as such), not independent standards.

**Metrics** (same layouts, same design hours, same sensor grid; Tier 2 is the reference):
- M1 per-point UTCI MBE and CVRMSE (Mannucci's metrics), and MRT MBE.
- M2 layout level: Kendall rank correlation of the site metric f1 across at least N layouts, and the paired difference between two layouts as computed by Tier 1 vs Tier 2.

**Acceptance rule (Tier 1 usable inside the optimiser):**
- A1: UTCI MBE <= 2.3 °C and CVRMSE <= 13% (upper ends of Mannucci's LBT vs ENVI-met range).
- A2: Tier 1 shade MRT within 4 °C (upper end of Peng's LAI-revised residual, 2-4 °C). Applies against Tier 2 now and against measurement if section 5 data are obtained.
- A3: Kendall >= 0.84, the rank agreement reported for the surrogate in Tan & Liu 2026 (#80) and used here as a precedent benchmark.
- Resolution floor: published layout effects are small (best vs worst layout 0.3 °C, Hao et al. 2023, #62; 0.55-1.32 °C between configurations, Tan & Liu 2026). These are below the 2.3 °C tolerance in A1, so A1 alone does not show that Tier 1 ranks layouts correctly; A3 and the paired difference carry the test. Proposed paired criterion: Tier 1 and Tier 2 differences between layouts agree within 0.3 °C (taken from the smallest published effect; 🟡 my choice).
- If A1-A3 fail: use Tier 1 only to pre-screen, and Tier 2 for ranking the final layouts. State the failure as a finding.

**Calibration check for the shade x tau proxy (§6 of methodology):**
1. Sample 30 plane positions (stratified by orientation and species; 30 is a placeholder 🟡) and compute per position the Tier 1 benefit (tree vs no tree, UTCI and MRT at the design hours, with tau applied through `fract_body_exp_`) and the proxy value.
2. Report Kendall and the OLS slope proxy vs Tier 1; after the linear rescale, CVRMSE <= 13% (A1) and Kendall >= 0.84 (A3).
3. Repeat across the tau bracket (section 2 step 1); if the species order changes with tau, the species result is not robust and is reported with the range.

**Field measurement: user decision** (`notes/todo_manual.md` l.53, "Field check of crown temperature / MRT in Porta ... Decide whether to drop it"; the backlog cites l.41, which is now the Ladybug test run).
- Drop it: validation rests on Tier 1 vs Tier 2 and on the published errors above (Peng, Colaninno); claims limited to relative ranking of layouts.
- Minimal campaign: one shaded (Platanus) and one sunny point, black globe at 1.5 m plus air T and wind, 1-min logging, 20-30 min, first 10 min discarded, ASHRAE globe equation (Colaninno's protocol). The todo note says no hot days before December, against delivery on about 18 Dec; a winter session would test leaf-off only.
- Ask Colaninno et al. for the Gràcia data (Platanus rows, same city): no field work, but 3 points and 2 sessions.

## Remaining gaps
Peng diffuse/code path (read PDF); Lindberg & Grimmond 2011 numbers; López-Cabeza error table; stock-Ladybug MRT bias in the current release (Ibrahim's 2020 comparison may be out of date); nearest XEMA station and licence text; whether Glass or Trans is better for the Tier 2 direct beam.
