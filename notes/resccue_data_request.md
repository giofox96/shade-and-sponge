# RESCCUE flood-depth data: licence request (13 Oct 2026)

**Why:** the thesis uses the RESCCUE 1D/2D flood-depth tables (`rcc_iu1_*`) read from the Resilience Atlas public CARTO account
(`scripts/bcn_resccue_depth.py`, `databases/data_inventory_barcelona.md` B1). They are readable without a login, but no licence
is stated. Before the final thesis (and any public slide) we need written permission and the correct citation.

## Step by step
1. **Send the email below** to Barcelona Regional: `br@bcnregional.com` (general address, printed in the credits of the
   Resilience Atlas reports, e.g. *Territorialització de riscos – Diagnosi del Pla de Resiliència*, EP4 Espais Verds,
   © 2020 Ajuntament de Barcelona and Barcelona Regional, co-produced with the Departament de Resiliència Urbana). Phone: +34 932 237 400 (from a city directory listing, not checked on Barcelona Regional's own site).
2. **Optional second channel:** the city's general online contact form ("Formulari de contacte", linked from the
   Ajuntament's citizen-channels page https://ajuntament.barcelona.cat/canals-comunicacio-ciutadana/):
   https://atencioenlinia.ajuntament.barcelona.cat/ca/fitxa/resultat-busqueda?origen=WEB_BARCELONA_CAT&tema=7&element=1121
   Paste the same text and ask them to forward it to the Departament de Resiliència Urbana. Or phone 010 (city
   information line). The area's own contact page (urbanisme-accio-climatica-...) has no form, only links.
3. **CC your tutor** (or mention the tutor by name). An institutional request (IAAC) is answered faster.
4. **Attach nothing heavy.** If you want, attach `notes/figures/resccue_porta_depth.png` to show exactly what you use.
5. **Log it:** tick the item in `notes/todo_manual.md`; save the reply as `databases/barcelona/resccue_licence_reply.pdf`
   (or .eml) and tell Claude to update the inventory row B1 and the figure credit.
6. **If no answer in ~10 days:** phone Barcelona Regional, or ask the tutor/IAAC to forward the email to a contact.
7. **Until a reply:** keep using the data internally (raw files stay in `databases/barcelona/raw/`, gitignored), always
   credit "PDISBA'19-RESCCUE (Barcelona Regional / Ajuntament de Barcelona)", and do not redistribute the raw layers.

## Email

**To:** br@bcnregional.com
**CC:** [tutor's email]
**Subject:** Request for permission to use RESCCUE pluvial flood-depth layers (Resilience Atlas) in a master's thesis (IAAC)

Dear Barcelona Regional team,

I am a student of the Master in Advanced Computation for Architecture & Design (MaCAD) at the Institute for Advanced
Architecture of Catalonia (IAAC), supervised by [tutor's name]. My master's thesis develops a computational method that
suggests street-tree species and positions to reduce both summer heat stress and pluvial runoff, tested in the Porta
neighbourhood (Nou Barris), which my screening of Landsat surface-temperature data and the Resilience Atlas flood-hazard
index placed above the city's 60th percentile for both heat and pluvial-flood hazard.

The RESCCUE urban-flooding results published in the Barcelona Resilience Atlas would be very valuable for this work. I found
the flood-depth layers from the PDISBA'19-RESCCUE 1D/2D model (tables `rcc_iu1_t10_actual`, `rcc_iu1_t100_actual`,
`rcc_iu1_t10_futur`, `rcc_iu1_t100_futur`) in the atlas's public map service. I would like to use them only for:

- characterising where water accumulates in Porta during the 10- and 100-year design storms;
- checking the plausibility of my own simplified runoff model against your results;
- maps and summary figures in the thesis document and in academic presentations, always credited to
  PDISBA'19-RESCCUE / Barcelona Regional / Ajuntament de Barcelona.

I will not redistribute the raw data, and no commercial use is planned. Could you please tell me:

1. whether I may use these layers for this purpose, under which licence or conditions, and how you would like them cited;
2. the units of `depth2d` and `speed2d` (I assume metres and metres per second), and the design-storm and climate
   scenario behind the "actual" and "futur" runs;
3. whether a 1-year return-period run also exists, and whether the results are available as rasters.

If there is a formal procedure for data requests, I am happy to follow it. Thank you very much for your time and for
making these results public.

Kind regards,
[Your full name]
MaCAD student, Institute for Advanced Architecture of Catalonia (IAAC)
[your email] · [phone, optional]
