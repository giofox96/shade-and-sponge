# Datasets not in this repository (licence reasons)

These datasets are used by the thesis but are **not committed**, because their licence forbids redistribution, restricts it (non-commercial, no-derivatives, no sublicensing), or has not been confirmed. All of them can be obtained again from the source. Put each one in the folder given, which `.gitignore` already excludes, and the scripts find it there.

Large open datasets (CC BY or CC0, e.g. the Barcelona street-tree inventory, ICGC LiDAR, OSM) are also kept out of the repo, but only for size. They are re-downloaded by the scripts and are not listed here.

## Available now

| Dataset | Used for | Licence / reason | How to get it | Local folder |
|---|---|---|---|---|
| **Mataró tree inventory** (`T_C_ARBRAT`, Ajuntament de Mataró, SafeTree via the GeoMat viewer): 25,062 trees, species per tree, trunk-girth class, condition, WGS84 points | Transfer test (Mataró) | Ajuntament de Mataró, *Llicència oberta d'ús d'informació – Catalunya* (cite source and update date; no sublicensing) | ORDS REST endpoint `https://apex.mataro.org/ords/sig/geodades/T_C_ARBRAT?limit=10000`, then `&offset=10000`, `&offset=20000` until `"hasMore": false`. On 10 Nov 2026 the host did not answer from Italy (connection timed out); it loaded from a connection in Spain (12 Nov 2026). Text fields are double-encoded UTF-8: decode with `s.encode('latin-1').decode('utf-8')` | `databases/mataro/raw/` |
| **PDISBA** text layers and map plates (Pla Director Integral de Sanejament de Barcelona) | Design storms, flood-risk context | CC BY-NC-ND | BCNROC, hdl 11703/119275: https://bcnroc.ajuntament.barcelona.cat/items/3cc3df7e-be95-4111-a995-98715dbe172e | `databases/barcelona/raw/pdisba/` |
| **RESCCUE flood depth** tables `rcc_iu1_*` (PDISBA'19-RESCCUE, Barcelona Regional / BCASA / Ajuntament) | Runoff hotspot comparison | Licence not stated; request to Barcelona Regional pending (`notes/data_requests.md`) | `scripts/bcn_resccue_depth.py` (public CARTO account `urbisadmin`) | `databases/barcelona/raw/` |
| **TRY Plant Trait Database**, request 53077, and the other third-party trait files in that folder | Species trait table | TRY data-use terms (released to the requester; no redistribution). Check each other file's own terms | Request at https://www.try-db.org | `databases/TRY_DATABASE/` |
| **Anys & Weiler (2024)** throughfall dataset | Interception calibration (s = 1.75 mm/LAI) | CC BY-NC 4.0 | FreiDok plus, record 242951 | `databases/traits/raw/anys_weiler_2024/` |
| **Florence "Life Escapos – Alberature pubbliche"** (Comune di Firenze, c_d612:D.7840) | LAI ground-truth check (`scripts/escapos_lai_check.py`) | CC BY-NC 4.0 | https://datigis.comune.fi.it/shp/escapos_tree_census.zip (downloaded by the script) | `databases/florence/raw/` |
| **EPW weather files** (TMYx, Barcelona El Prat and others) | Ladybug / UTCI runs | Licence not confirmed | climate.onebuilding.org, Spain / Catalonia; exact names in the `scripts/bcn_epw_summary.py` docstring | `databases/*/weather/` |
| **City policy documents** (tree master plan, Pla Clima, etc.) and their extracted text | Policy chain, species rules | Copyright of the issuing body | Links in `notes/tree_master_plan.md` §8 | `databases/policy/` |
| **Papers** (PDFs and text derived from them) | Literature review | Publisher copyright | Zotero library; references in `notes/lit/literature_matrix.csv` | `papers/`, `notes/lit/text/`, `notes/lit/digest/` |

## Requested, not received yet (will stay out of the repo)

| Dataset | Condition | Status |
|---|---|---|
| BCASA rain-gauge series and sewer-model results | Academic use only, no sharing with third parties | `notes/data_requests.md` |
| Comune di Firenze LiDAR point cloud (Firenze Nova) | Research only, no redistribution, delete after the thesis | `notes/data_requests.md` |
