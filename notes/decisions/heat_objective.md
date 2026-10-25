# Heat objective f1: options memo (issue #7)

**DECIDED (user, 19 Oct): mean UTCI over 12–17 h on a hot design day**, with the hottest real day as a check. The peak-hour metric is dropped because it saturates (§5). The RQ wording follows in `notes/topic_decision.md` §8. The sections below are the memo that led to it.

**Clock basis, DECIDED (user, 25 Oct): 12–17 h local clock (CEST in summer)**, the window the tool's proxy already uses. The user sets the matching hours in Ladybug. The EPW is in standard time (UTC+1), so 12–17 h CEST is EPW hours 11–16. The bounding run in §1 used EPW hours 12–17 (13–18 h CEST), one hour later than the decided window.

Status: **exploratory bounding, pending user decision.** No geometry, trees or grid were used. Numbers come from `scripts/heat_bounds.py` -> `databases/barcelona/heat_design_hours.csv` (51 rows). Methodology status is PROTOTYPING; `methodology.md` and `topic_decision.md` are not edited.

## 1. What the bounding run shows (TMYx El Prat 2011-2025, EPW wind, hours 12-17)
Time convention: EPW standard time UTC+1 (no DST in the file); hour label 12-17 = 12:00-17:59 standard time = 13:00-18:59 CEST. Solar noon in Barcelona is about 12:50 standard time (ASSUMPTION from longitude 2.07 E, not computed). MRT: Ladybug `OutdoorSolarCal`, sun = body fully exposed, shade = no direct beam but full sky diffuse (shade MRT is an upper bound for a tree crown, so the sun-shade gap is a lower bound). Surface temperature = air temperature, floor reflectance 0.25, sky exposure 1 (ASSUMPTION, ladybug defaults).

| Candidate day (El Prat 2011-2025) | Ta range | UTCI shade | UTCI sun | Sun minus shade | Hours (of 6) >= 32 C: shade / sun |
|---|---|---|---|---|---|
| Hottest TMYx day (doy 217) | 31.2-32.7 | 30.8-35.9 | 33.6-38.3 | 2.4-3.1 | 5 / 6 |
| Middle of hottest TMYx week (doy 218, 6 Aug) | 28.7-30.5 | 28.0-33.4 | 31.0-36.2 | 2.3-3.0 | 2 / 5 |
| DDY cooling 0.4% day | 30.2-31.3 | 29.6-32.9 | 34.2-37.1 | 4.1-4.7 | 3 / 6 |
| DDY heating 99.6%, hour 12 | 1.8 | -12.4 | -12.4 | 0 | 0 / 0 |

All UTCI values use the EPW 10 m wind as is. Exact rows: `databases/barcelona/heat_design_hours.csv`.

Findings:
1. **The class limit saturates on the hottest day.** On the hottest TMYx day even full shade is at or above 32 C in 5 of the 6 hours, so a "share of points > 32 C" metric counts shade and sun alike and cannot show a benefit. On the hot-week day (6 Aug) sun is above 32 C in 5 hours and shade in 2, and on the DDY cooling day sun in 6 and shade in 3: a share-above-32 metric discriminates only on days like these, and only in the middle of the window.
2. **The sun-shade gap is 2.3-4.7 C** with full shade (a lower bound for a tree). A tree layout shades only part of the points, so a domain-mean difference between two layouts is a fraction of this gap.
3. **Model error is of the same size.** Ladybug vs ENVI-met: UTCI MBE 0.8-2.3 C, CVRMSE 7-13% (Mannucci et al. 2025, `literature_matrix.csv` #51, full text). Absolute f1 values are therefore not reliable to better than about 1-2 C; rankings of layouts share the systematic error and are more robust.
4. **Wind is the largest single input.** Using the city-terrain 10 m profile instead of the raw EPW speed raises UTCI by about 1.5-3.1 C in summer (columns `UTCI_*_citywind`; see `weather_forcing.md`).
5. **The 12-17 h window matters.** On the hottest day the full-sun MRT falls from 63.1 C (hour 12) to 50.7 C (hour 17), so the heat load, and the shadow positions that matter for tree placement, change across the afternoon; a single "design hour" is fragile.

## 2. f1 options
| Option | Definition | Works on | Problem |
|---|---|---|---|
| A | Mean UTCI over fixed points, hours 12-17 | any day | Differences small relative to model error; rewards the few points that stay sunlit |
| B | Share of points with UTCI > 32 C (strong heat stress), hours 12-17 | only days where shade < 32 < sun, e.g. DDY cooling day | Saturates on the hottest TMYx day (finding 1) |
| C | Degree-hours above 32 C over the hot week | Tier 2 only | Needs 7 days x hours per layout; too slow for Tier 1 |

Class limits used: 26-32 moderate, 32-38 strong, 38-46 very strong, > 46 extreme heat stress. Verified source for the paper: Bröde et al. 2012, Int J Biometeorol 56:481-494, DOI **10.1007/s00484-011-0454-1** (Crossref lookup: title, journal, volume, pages and authors match). The numeric class limits were read from the thermofeel documentation (secondary, 🟡); a search listing for Bröde et al. 2012 did not show the table, so check Table 1 of the paper locally.

## 3. Domain rule (scenario-independent)
Points on the 2 m sidewalk grid inside the design sub-area that are **sunlit by buildings only (no trees) at the chosen hours**, computed once on the no-tree scenario and then held fixed for every layout. This keeps the point set identical across S0-S4 and removes the objective's dependence on which layout is evaluated. ASSUMPTION: the no-tree baseline is a valid reference (S0 has existing plane trees, which is a separate decision).

## 4. Minimum meaningful difference
Tie it to the sourced error: an f1 difference counts only if it exceeds the Ladybug-vs-ENVI-met UTCI MBE, **0.8 C (low end) to 2.3 C (high end)** (Mannucci 2025, #51). For layouts that share the same systematic bias, the low end is defensible; the high end is conservative. The Peng 2026 (#53) canopy-transmittance correction was validated on MRT, not UTCI (MRT within 2-4 C of measurement), so it gives no UTCI error to use. No number here is a new estimate. The choice is pending user decision.

## 5. Recommended default (pending user decision)
- **Metric A**, mean UTCI over the fixed domain, **hours 12-17 on the DDY cooling day** (or the hottest TMYx day), reported alongside **metric B** only on the DDY cooling day. Reason: it is defined on both stations' files, sun and shade stay 4-5 C apart on that day, and it needs one day, not a week.
- The RQ wording "UTCI at the peak summer hour" (`topic_decision.md` §7) needs more than one hour: change it to "UTCI over the 12-17 h afternoon window on a hot design day". `methodology.md` §1/§5 and `slides/outline_20oct.md` (heat metric) would change with it; **not edited here**.
- The DDY day is synthetic; the hottest TMYx day is real but one realisation. Run both as a robustness check.

## 6. Question for the user
Do you accept an afternoon-window mean UTCI (hours 12-17, standard time) on the DDY cooling day as f1, instead of a single peak hour, and a minimum difference equal to the 0.8 C Ladybug-vs-ENVI-met MBE?
