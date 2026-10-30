# Data sources suggested by PEMB (30 Oct 2026)

PEMB (Pla Estratègic Metropolità de Barcelona) replied to Giovanni and Fiona that it has no direct access or contact for
the data, and pointed to two public sources, suggesting to contact the "providers" if the data is not there.
Status checked from a cloud container on 30 Oct: the Barcelona hosts (`arbres.barcelona`, the open data portal API,
the atlas CARTO account) refused the connection from the container, so the checks below were made through a web
reader and need one browser look where marked.

## 1. Street trees: "Arbres de Barcelona" (https://arbres.barcelona/)
- **Not an official source.** The page metadata names one author, Manuel Cerezo; no city logo, licence or data
  source is stated. Its description: map with filters by species, district, neighbourhood and space type, statistics,
  and "historial de l'inventari municipal".
- It almost certainly re-publishes the city's open inventory (`arbrat-viari`, `arbrat-parcs`, `arbrat-zona`), which the
  tool already uses (`databases/data_inventory_barcelona.md` A1–A2). That is an inference, not checked: the page body
  is rendered by JavaScript and could not be read.
- **What it could add:** the "inventory history". If the author kept weekly snapshots of `arbrat-viari`, they show
  which trees were removed and what was planted in their place, street by street. That would give an observed S1
  (the city's real replacement practice) instead of the 2004/2005 table (`notes/tree_master_plan.md` §5b).
- **What it does not solve:** DBH and height. The open inventory has neither, and nothing suggests this site does.
  Per-tree size stays with the LiDAR proxy.
- **Browser check (2 min):** open a tree in Porta and note the fields shown; look for a "Sobre"/About page, the data
  source, and whether the history can be downloaded.

### Related find: Biodiversity Atlas tree layer (official)
`atles-biodiversitat-arbrat-geometries` on Open Data BCN (CC BY 4.0, published 25 Feb 2025, weekly update, file
`ab_vw_arbrat_geometries.csv`, 14.3 MB; Direcció d'Espais Verds i Biodiversitat). The portal page does not list its
fields or geometry type. **Browser check:** download it and look at the header: crown polygons or a size field would
matter; points with species only would duplicate A1–A2.

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
| Inventory history | Manuel Cerezo (arbres.barcelona) | Optional; contact only if the browser check shows a history |

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

### 4c. Optional, to the author of arbres.barcelona (only after the browser check)
Hi Manuel, I am a master's student at IAAC working on street-tree selection in Barcelona. Your site mentions the history
of the municipal inventory: do you keep past snapshots of the street-tree dataset, and would you share them (or the
dates covered) for academic use? It would let me see which species the city actually plants when it replaces a tree.
Thanks, Giovanni Carlo Volpe (giovanni.carlo.volpe@students.iaac.net)
