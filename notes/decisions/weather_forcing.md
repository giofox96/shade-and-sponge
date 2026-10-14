# Weather forcing for UTCI: EPW period, wind, urban offset (issue #7)

Status: **exploratory, pending user decision.** Scripts: `scripts/bcn_epw_summary.py` -> `databases/barcelona/epw_summary.csv`; `scripts/heat_bounds.py` -> `databases/barcelona/heat_design_hours.csv`. Files were downloaded on 13 Oct 2026 from climate.onebuilding.org (reachable from the cloud session this time; the 7 Oct test had failed). The EPW/DDY files are **not committed**: the licence was not confirmed (see §5). Download URLs are in the script docstring.

## 1. EPW period and station options
| File | Period of record (file header) | Hours missing (Ta, RH, wind speed, wind dir) | Summer mean Ta (Jun-Aug) | Summer max Ta | Mean wind 10 m |
|---|---|---|---|---|---|
| El Prat AP 081810, TMYx 2009-2023 | 2009-2023 | 0, 0, 0, 0 | 24.8 | 33.0 | 4.15 m/s |
| El Prat AP 081810, TMYx 2011-2025 | 2011-2025 | 0, 0, 0, 0 | 25.2 | 33.0 | 4.16 m/s |
| Barcelona 081800, TMYx 2011-2025 (city station, 41.417 N, 2.133 E, 176 m) | 2017-2025 per the file's comment line | 0, 0, 0, 0 | 24.5 | 29.7 | 2.98 m/s |

- **Wind direction is complete** in all three files (no 999 values), so the forum report of missing direction (inventory C4) does not apply to these files. The file header only says "no special attempts at re-creating missing data"; I did not check the original observations behind the values.
- 2011-2025 is the newer period and includes recent hot summers (the "hottest day" is in August, doy 217); the two El Prat files differ by 0.4 C in summer mean Ta.
- **The city file is closer to Porta** than the airport (Porta is in Nou Barris; I did not compute the distance) and has stronger sheltering (mean wind 3.0 vs 4.2 m/s). Its record is 9 years, not 15, and its summer maximum is 3.3 C below El Prat. Whether this reflects altitude and sea distance or the shorter record is not tested.
- DDY cooling 0.4% (dry bulb) design day: Tmax 31.3 C, wind 4.8 m/s at 10 m (El Prat files).

## 2. Wind at pedestrian height
UTCI expects the **10 m meteorological wind speed**; the Fiala model's ground speed is taken as 10 m speed / 1.5 (ladybug_comfort docstring, `universal_thermal_climate_index`; LB UTCI Comfort docs say the same and takes `_wind_vel_` as a 10 m value). LB UTCI Comfort passes the EPW value straight to the UTCI function (no height conversion in the component source checked on 13 Oct, `LB UTCI Comfort.py`). Therefore:
| Option | UTCI input | Effect (summer, hours 12-17, El Prat) |
|---|---|---|
| 1. EPW 10 m as is (Ladybug default) | the El Prat days' EPW speeds (airport, open terrain) | baseline |
| 2. `WindProfile('city','country')` power law to 10 m | 2.1-3.5 m/s | UTCI +1.5 to +3.1 C (CSV columns `*_citywind`) |
| 3. Pedestrian height 1.5 m | not valid for UTCI (double correction) | information only (`wind_ped`) |
Option 2 is a sheltering assumption for a dense street, not a measurement. Winter is more sensitive: DDY heating hour 12: UTCI -12.4 C (option 1) vs -3.0 C (option 2). **Recommended default: option 1 for the main run (matches the Ladybug workflow the user runs), option 2 as a sensitivity.** Pending user decision.

## 3. Urban offset
- The existing +1/+2 C offsets in `methodology.md` §5 have no source. Bounds from the repo's matrix: Iungman et al. 2023 (#35, full text digest): mean summer UHI 1.5 C across 93 cities (range 0.5-3.0); the Barcelona-specific value is not recorded in the matrix, so look it up in the paper. Lauwaet et al. 2024 (#37, abstract only, (abs)): UHI indicator 0.57-2.54 C (mean 1.43) over 100 cities.
- The two TMYx files do **not** show a positive city-minus-airport difference: summer mean Ta is 0.7 C lower at the city file (24.5 vs 25.2), which reflects site, altitude and record length, not a heat island. An urban offset cannot be taken from this pair.
- **Recommended range for a sensitivity: 0 to +1.5 C air temperature** (upper value = Iungman mean; ASSUMPTION that it applies to Porta). Pending user decision.
- UrbClim 100 m hourly data (2008-2017, 100 cities): the CDS entry is listed as "Deprecated 10-05-2024" (search listing of cds.climate.copernicus.eu/datasets/sis-urban-climate-cities). A Copernicus hub page (hds.hub.copernicus.eu/datasets/hh-dataset-sis-urban-climate-cities) appears in search results, but it returned HTTP 503 when fetched, so availability, licence and Barcelona coverage are **to check locally**. No key-gated station data (Meteocat, AEMET) was requested, so `notes/data_requests.md` was not needed.

## 4. Recommended default (pending user decision)
Main run: TMYx El Prat 2011-2025 EPW and DDY, wind as in the file, no offset. Sensitivities: city file 081800; city-terrain wind; +1.5 C offset. Reason: it is the file named in the inventory, covers the hottest recent summers and has the DDY file needed for a design day.

## 5. Open items
- Licence of the TMYx files not found on the site home page or in the files' headers: **to check** before committing them.
- Whether the user has already run a Ladybug test (`exchange/from_gh/` does not exist in this checkout), so no cross-check of `heat_bounds.py` against a Ladybug run was possible.
