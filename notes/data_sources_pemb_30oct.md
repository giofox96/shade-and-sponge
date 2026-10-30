# Data sources suggested by PEMB (30 Oct 2026)

PEMB (Pla Estratègic Metropolità de Barcelona) replied to Giovanni and Fiona that it has no direct access or contact for
the data, and pointed to two public sources, suggesting to contact the "providers" if the data is not there.
The Barcelona hosts are blocked from cloud containers; the tree checks were run from the OMEN PC on 30 Oct.

## 1. Street trees: "Arbres de Barcelona" (https://arbres.barcelona/)
Checked from the OMEN PC on 30 Oct (static files under `https://arbres.barcelona/data/`).
- **Not an official source**: a static React/MapLibre app by Manuel Cerezo. Its JSON-LD names Open Data BCN
  (Ajuntament de Barcelona, CC BY 4.0) as the data provider. No API; the data are static JSON files
  (`meta.json`, `trees-{viari,parcs,zona}.json.gz`, stats). 222,617 trees: viari 145,305, parcs 33,336, zona 43,976.
- **Same fields as the open inventory** (A1–A2): code, position, species, size category, district, barri, address,
  irrigation. Street trees: height filled on 0 of 145,305, planting date on 32,006, sidewalk width and tree-pit
  fields empty, no DBH, no trunk perimeter, no crown. **It does not solve DBH or height**; the LiDAR proxy stays.
- **What it adds: inventory history.** 23 quarterly snapshots, 2021 Q1 to 2026 Q3, rebuilt from the Open Data BCN
  quarterly files (each keeps its CKAN download URL), plus weekly copies of the app data since 1 Jul 2026. Across the
  series: 45,830 trees missing, 26,488 added, 11,635 reappeared, 9,086 category changes. Downloadable as plain JSON:
  `/data/history/official/manifest.json`, `observations-*.json`, `records/*.json.gz`.
  The site itself warns that a missing tree is not proof of a felling, nor an added one of a planting.
- **Use for the thesis:** an observed S1. Matching removals and additions at the same position or street (2021–2026)
  would show which species the city actually plants when it replaces a tree, instead of the 2004/2005 table
  (`notes/tree_master_plan.md` §5b). Better to rebuild it from the **official quarterly files on Open Data BCN** (the
  primary source the site uses) than to cite the site.

### Related: Biodiversity Atlas tree layers (official, CC BY 4.0, last modified 23 Sep 2025)
- `atles-biodiversitat-arbrat-geometries` (`ab_vw_arbrat_geometries.csv`, 14.66 MB, 243,999 rows): **points only**
  (WGS84 WKT); columns `geom_fid, nom_cat, nom_cas, nom_eng, geom_wgs84`; names only on 662 rows (named groups).
  `atles-biodiversitat-arbrat-especies`: 525 species with descriptive text, no traits.
- Same tables on the atlas CARTO account (`urbisadmin`, no key): `ab_vw_arbrat_geometries` (243,999),
  `ab_arbrat_geometries` (133,375), `ab_vw_arbrat_especies` (525), `ab_arbrat_especies` (465). The CARTO geometry
  tables carry `codi` (the inventory tree code, unique), so they join to the inventory, plus `tipus_elem_invent_id`
  (codes 1, 2, 4, 5, 6, 8; meaning not found). **No height, DBH or crown anywhere: nothing new for the tool.**

## 2. Flood data: "Inundabilitat – Atles de resiliència"
(https://coneixement-eu.bcn.cat/widget/atles-resiliencia/index_inundabilitat.html)
- **Already in use.** The flood-hazard index (`ar_in_perill_inun`) and the RESCCUE depth tables (`rcc_iu1_*`) behind
  this atlas were read on 8 and 13 Oct (`databases/data_inventory_barcelona.md` B1, `scripts/bcn_resccue_depth.py`).
- The page itself shows maps and charts only, with no download and no licence for the maps; the only contact is the
  Àrea d'Ecologia, Urbanisme i Mobilitat form (https://ajuntament.barcelona.cat/ecologiaurbana/ca/contacte).
- Sources named on the page: **Barcelona Regional** (hazard maps, network functioning) and **BCASA** (Barcelona Cicle
  de l'Aigua: rainfall series, retention tanks, the sewer model the maps derive from).
- Still missing: written licence, units of `depth2d`/`speed2d`, any T = 1 yr run, the BCASA rain-gauge series.

## 3. The providers, and where each request stands
| Data | Provider | Status |
|---|---|---|
| Tree replacement rules, sidewalk widths, 15% cap scope | Parcs i Jardins (via Atenció en línia form) | Sent 21 Oct, code **RGF7342**; follow up ~4 Nov |
| RESCCUE depth licence, units, T = 1 yr | Barcelona Regional, br@bcnregional.com | Sent 13 Oct; **reminder overdue** (was due 23 Oct) |
| Rain-gauge series 1994–2019, sewer model results | BCASA | Not contacted. No verified email: use the contact page on BCASA's own site or the Ecologia Urbana form |
| Inventory history | Open Data BCN quarterly files (also mirrored by arbres.barcelona) | Public, no request needed |

So PEMB's advice points to providers already contacted, except BCASA. Drafts below; **nothing has been sent.**

## 4. Drafts (not sent)

### 4a. Reminder to Barcelona Regional
**To:** br@bcnregional.com
**Subject:** Follow-up: permission to use RESCCUE flood-depth layers in a master's thesis (IAAC)

Dear Barcelona Regional team,

On 13 October I wrote to ask for permission to use the RESCCUE flood-depth results published in the Barcelona
Resilience Atlas (tables `rcc_iu1_t10_actual`, `rcc_iu1_t100_actual`, `rcc_iu1_t10_futur`, `rcc_iu1_t100_futur`) in my
MaCAD master's thesis at IAAC. PEMB has since confirmed that the Atlas is the right source and suggested I contact the
data provider directly, so I am writing again.

In short, I would be grateful to know:
1. whether I may use these layers for academic, non-commercial work, credited to PDISBA'19-RESCCUE / Barcelona
   Regional / Ajuntament de Barcelona, and how you would like them cited;
2. the units of `depth2d` and `speed2d` (I assume m and m/s);
3. whether a 1-year return-period run exists.

If another office (for example BCASA) is the right contact, a name or address would already help a lot.

Kind regards,
Giovanni Carlo Volpe
MaCAD student, Institute for Advanced Architecture of Catalonia (IAAC)
giovanni.carlo.volpe@students.iaac.net

### 4b. New request to BCASA (short enough for a ~1,000-character web form)
**Subject:** Data request for a master's thesis (IAAC): rain-gauge series and pluvial flood model results

Dear BCASA team,

I am a MaCAD master's student at IAAC. My thesis builds a computational method that suggests street-tree species and
positions to reduce summer heat and pluvial runoff, tested in Porta (Nou Barris). The Barcelona Resilience Atlas
credits BCASA for the rainfall series and the sewer model behind its flood maps. For academic, non-commercial use, could
you share, or tell me how to request:
1. 5-minute rainfall series from the BCASA gauges nearest to Nou Barris;
2. the flood-depth results of the 1D/2D model for Nou Barris, especially any frequent-event run (T = 1 or 2 years).
All data would be credited to BCASA and not redistributed.

Kind regards,
Giovanni Carlo Volpe, MaCAD student, IAAC · giovanni.carlo.volpe@students.iaac.net
