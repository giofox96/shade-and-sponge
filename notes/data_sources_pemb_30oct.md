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
| RESCCUE depth licence, units, T = 1 yr | Barcelona Regional, **contact form** https://www.bcnregional.com/contacte-2/ (type "Research / Study"); phone +34 932 237 400 | **br@bcnregional.com bounced on 30 Oct** (address not found), so the 13 Oct email most likely never arrived. **Full request (4a) sent through the form on 30 Oct** (no request code) |
| Rain-gauge series 1994–2019, sewer model results | BCASA (site https://www.barcelona.cat/bcasa/ca: no email, no own form) | **Sent 30 Oct, code BDM9240** (category "Información sobre la red de alcantarillado"). Channel: the city online-service form https://atencioenlinia.ajuntament.barcelona.cat/ca (general contact form, ask to forward to BCASA), or 010 |
| Inventory history | Open Data BCN quarterly files (also mirrored by arbres.barcelona) | Public, no request needed |

So PEMB's advice points to providers already contacted, except BCASA. Drafts below; **nothing has been sent.**

## 4. Drafts (not sent)

### 4a. Request to Barcelona Regional (web form, "Research / Study")
**Subject:** Permission to use RESCCUE flood-depth layers in a master's thesis (IAAC)

Dear Barcelona Regional team,

I would like to ask for permission to use the RESCCUE flood-depth results published in the Barcelona Resilience Atlas (tables `rcc_iu1_t10_actual`, `rcc_iu1_t100_actual`, `rcc_iu1_t10_futur`, `rcc_iu1_t100_futur`) in my
MaCAD master's thesis at IAAC. PEMB (Pla Estratègic Metropolità de Barcelona) confirmed that the Atlas is the right source and suggested I contact the
data provider directly.

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

## 5. BCASA reply to BDM9240 (30 Oct) and the formal request
BCASA (Sanejament, AM27188) answered the same day: published material is the PDISBA
(http://hdl.handle.net/11703/119275, already used for the city IDF, `databases/barcelona/pdisba_idf_city.csv`).
Unpublished data needs a formal **instància** registered with the Ajuntament, with: project title, data requested,
**a separate form for rain-gauge data** (not attached to the reply; to ask for), and **a letter from the tutor**
(confirming enrolment, programme, title and content of the work). Online registration needs a digital certificate
(https://seuelectronica.ajuntament.barcelona.cat/ca/registre-electronic); otherwise fill the PDF
(https://seuelectronica.ajuntament.barcelona.cat/sites/default/files/00106_instancia_formulari_0.pdf) and register it at
an Oficina d'Atenció Ciutadana.

**Conditions** (they bind the thesis): academic and teaching use only; no disclosure or transfer to third parties; no
commercial use; do not alter the content or its meaning; cite "Barcelona Cicle de l'Aigua, SA, Ajuntament de Barcelona"
and the date of last update (Ley 37/2007, art. 8). **Consequence:** BCASA data may appear in the thesis document and in
academic presentations, but **not in the public repo or the public web app** (GitHub Pages); keep it in `raw/`
(gitignored) and publish only derived figures, if at all.

### 5a. Instància text (Spanish; paste in "Exposo / Sol·licito")
**Expongo:** Soy estudiante del Master in Advanced Computation for Architecture & Design (MaCAD) del Institute for
Advanced Architecture of Catalonia (IAAC), curso 2025–2026. Mi trabajo final de máster, «[título exacto de la tesis]»,
desarrolla un método computacional que propone especies y posiciones de arbolado viario para reducir el estrés térmico
estival y la escorrentía pluvial, aplicado al barrio de la Porta (Nou Barris). Siguiendo la respuesta de BCASA a la
consulta BDM9240, adjunto la carta de mi tutor/a [y el formulario de datos pluviométricos].
**Solicito**, para uso exclusivamente académico, sin cesión a terceros y citando «Barcelona Cicle de l'Aigua, SA,
Ajuntament de Barcelona»:
1. Series de precipitación a 5 minutos de los pluviómetros de BCASA más cercanos a Nou Barris (periodo disponible).
2. Resultados del modelo 1D/2D de drenaje (PDISBA) para Nou Barris: calados y velocidades máximas para los periodos de
   retorno disponibles, en especial T = 1 o 2 años, en formato SIG.
3. Si existe, la autorización para usar en la tesis las capas RESCCUE publicadas en el Atles de Resiliència
   (tablas `rcc_iu1_*`), con la cita que indiquen.

### 5b. Tutor letter (to be signed by the tutor on IAAC letterhead)
To: Barcelona Cicle de l'Aigua, SA (BCASA), Ajuntament de Barcelona
I confirm that Giovanni Carlo Volpe is enrolled in the Master in Advanced Computation for Architecture & Design (MaCAD)
at the Institute for Advanced Architecture of Catalonia (IAAC), academic year 2025–2026, and that I supervise his
master's thesis "[title]". The thesis develops a computational method that suggests street-tree species and positions
to reduce summer heat stress and pluvial runoff, tested in the Porta neighbourhood (Nou Barris). The data requested
(rain-gauge series and drainage-model results) will be used only for this academic work, will not be shared with third
parties and will be credited to Barcelona Cicle de l'Aigua, SA, Ajuntament de Barcelona.
[Name, role, IAAC, date, signature]

## 6. Observed replacements from the quarterly inventory (31 Oct, `scripts/inventory_history.py`)
Run on the OMEN PC. Open Data BCN `arbrat-viari` holds **35 quarterly files, 2018 Q1 – 2026 Q3** (zipped CSVs).
Street trees: 156,253 (2018 Q1), peak 157,674 (2020 Q3), 145,034 (2026 Q3).
- **The city keeps a tree-pit code when it replants it**, so most replacements show up as a species change on the same
  code, not as a removal + new code (only 225 position-matched pairs). Raw species changes are dominated by re-coding
  (e.g. 42,106 *Platanus × hispanica* → *× acerifolia* in 2023 Q1; spelling fixes; re-identifications). After filters
  (genus+species names, same-genus changes dropped, >50 identical changes per quarter = re-coding, reversed changes =
  corrections, 9 listed renames; all ASSUMPTION): **10,758 same-code replacements** + 218 position-matched ones.
- **Planes replaced 1,444 times** city-wide; species planted instead: *Celtis australis* 296, *Melia azedarach* 219,
  *Gleditsia triacanthos* 105, *Koelreuteria paniculata* 89, *Styphnolobium japonicum* 86, *Grevillea robusta* 70,
  *Pyrus calleryana* 65, *Jacaranda mimosifolia* 54.
- **Porta: 227 replacements**, mostly not planes (10): *Catalpa* → *Handroanthus heptaphyllus* 47, *Populus nigra* →
  *Fraxinus angustifolia* 28 / *Casuarina* 21 / *Grevillea* 15, *Populus alba* → *Fraxinus angustifolia* 11 /
  *Pyrus calleryana* 10.
- Same-species replanting is invisible on a kept code, so its share cannot be measured (22% only on the 218 new-code pairs).
- Not yet checked: the synonym list against a taxonomic authority; whether the 50-per-quarter threshold drops real
  whole-street replantings.
Outputs: `databases/barcelona/inventory_snapshots.csv`, `inventory_replacements.csv` (column `kind`),
`inventory_replacement_matrix.csv`.
