# Underground utilities and free planting spots: Santapau / Emili Roca / Desfar demo (22 Nov 2026)

Data credit: **Ayuntamiento de Barcelona - Información de base y cartografía (IBC)**, via ACEFAT eWise request 872551; the plans
are valid until about 18 Feb 2027. Raw utility geometry stays on the OMEN (`databases/barcelona/raw/ewise/`, gitignored) and must
not go into the repo, the web app, slides or project files (AGBAR: exclusive use; Nedgia: confidential). Only derived per-spot
distances and a flag are committed.

## Rule
Source: IMPJB, *Plec de prescripcions tècniques per al disseny, l'execució i la recepció d'espais verds* (PTEV), last revised
May 2024 (ajuntament.barcelona.cat/ecologiaurbana, `PPT_DissenyExecucioRecepcio_EspaisVerds.pdf`), read 22 Nov 2026.
- **p. 31 (§2.2.6.2):** pits must not be placed over existing buried infrastructure unless the project provides waterproofing and
  drainage ("no es podran situar parterres ni escocells a tocar de façanes ni sobre infraestructures soterrades existents sense
  preveure'n la impermeabilització i drenatge en el projecte"). So a pit over a service is **conditional**, not forbidden.
- **p. 82 (§3.2, Protecció dels serveis existents):** the promoter must ask the gas, electricity, telephone, water and sewer
  operators for their plans and permits, and must protect or divert affected services. **No distance is given.**
- **p. 116 (§5.3.9, Escocells):** minimum pit 1 × 1 m (optimum 1.5 × 1.5 m; at least 1 m² open, 80 cm in any direction).
  **No distance to services is given.**
- **p. 87 (tree-protection list, item 3):** avoid opening trenches within 1 m of tree pits. This is a rule for works near
  existing trees, not a planting distance from services. It is used below only as context.

**The PTEV gives no numeric minimum distance between a pit or trunk and gas, telecom or electricity lines.** So the only flag is
"the pit footprint intersects a line". The footprint is the 1 × 1 m minimum pit taken as a disc of radius 0.5 m around the spot.
This is an ASSUMPTION: the pit's orientation is unknown, so the inscribed circle is used.

## Method
`scripts/utilities_conditional.py`. It reads the LWPOLYLINE layers of the two vector plans: gas `BP` (mains, 231 lines) and
`ACOMETIDA` (service lines, 256), and Telefónica `Canalizacion_Barna_shape` (ducts, 54), all in EPSG:25831. It then measures the
distance from each free planting spot inside the demo rectangle (X 431150–431450, Y 4586830–4587110) to the nearest line of each
network. Free spots are the non-excluded spots of `porta_planting_spots.csv`, the ones the web app shows.

Output: `databases/barcelona/porta_spots_utilities.csv`, with spot id, three distances (0.1 m) and `utility_conditional`. The flag
also goes into `web/public/data/porta*/trees.json`: the web app draws a conditional spot with an orange centre dot and adds a line
to its tooltip. `shade_sponge/web_export.py` carries the flag forward when it re-exports.

## Counts
- **Free spots in the rectangle: 11. Conditional (pit over a line): 0.** Two spots (ADD0132, ADD0133) are 0.9 m from a gas main,
  and ADD0054 is 1.1 m away.
- **Existing street trees in the rectangle** (web export positions and kept trees, for context): **232. 20 would fail the same
  rule**, and 37 are within 1.0 m of a line. So today's trees already stand on or next to these services more often than any free
  spot would. Per-tree values are not written to disk.

## Limits
- The utility plans are indicative, with no depths, and their positional accuracy is not stated in the files used. A 0.5 m test may
  be finer than that accuracy. Read the flag as "check on site", not as a measured conflict.
- Networks delivered only as PDF (no vectors) are **not used**: AGBAR water (AJBCN-SNJ), electricity (FE), ONO and the city's
  own layers (FIB, LLU, SMF). The gas and Telefónica *Compact* PDFs were not compared with the DXFs. Electricity in particular is missing, and the PTEV
  names it among the services to check.
- The radius 0.5 m pit footprint is an ASSUMPTION. With the 1.5 × 1.5 m optimum pit (radius 0.75 m), the count would still be 0.
  At 1.0 m it would be 2 spots.
- Valid only for this demo rectangle; elsewhere the flag is 0, meaning not checked.
