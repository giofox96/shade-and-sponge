# Data and information requests to institutions: status board

*Started 3 Nov 2026. One place for every request to an outside body. Update the row when anything moves.
Replies to the city forms go to giovanni.carlo.volpe@students.iaac.net (IAAC inbox), which Claude cannot read:
forward replies or paste them in the thread. Nothing here is sent by Claude.*

## Giovanni's to-do (updated 3 Nov, 13:10)
- [x] TRY: data release started (3 Nov). Wait for the pickup email, then forward it.
- [x] LinkedIn: connection request to Cati Montserrat Martí sent without a note (3 Nov). When she accepts, send the follow-up message.
- [ ] **BCASA**: send the follow-up (form text in the thread, 3 Nov) through the Atenció en línia form, same category, subject "Seguimiento BDM9240"; send me the new code.
- [ ] **AMB contact form** (amb.cat → Contacte): message for Cati Montserrat (text in the thread, 3 Nov).
- [x] Slack: María asked (3 Nov); Pinyol lead dropped, go for Joan Guitart.
- [ ] **LinkedIn**: look up Joan Guitart (Ajuntament de Barcelona, arbrat) and connect without a note.
- [ ] **Víctor Ténez (UPC)**: send the email (text in the thread, 3 Nov) to victor.tenez@upc.edu.
- [ ] **AiEM (UPC)**: pick a researcher on https://aie.upc.edu/equip/ and send the email (text in the thread, 3 Nov).
- [ ] **Wed 4 Nov, Parcs i Jardins**: one follow-up via the form quoting RGF7342 (§2).
- [ ] **10 Nov, tutor**: ask Angelos for an Àrea d'Arbrat contact; mention the BCASA letter if BCASA says it can be done remotely.
- [x] PDISBA PDFs downloaded (3 Nov); Diagnosi read.
- [ ] Optional, another day: re-download Plànols Vol. II only, in the browser (BCNROC rate-limited us on 3 Nov).
- [ ] Barcelona Regional: phone +34 932 237 400 around 13 Nov if still silent.

## Board (3 Nov 2026)

| # | Body | What we ask | Channel | Status | Next step (who, when) |
|---|---|---|---|---|---|
| 1 | **BCASA** (Barcelona Cicle de l'Aigua) | 5-min rain-gauge series near Nou Barris; 1D/2D drainage results (depths, velocities, T = 1–2 yr) | City "Atenció en línia" form, code **BDM9240** (30 Oct) | **Answered 30 Oct:** unpublished data only via a formal *instància* + tutor letter + a separate rain-gauge form; academic use, no sharing | **The complicated one, see §1.** Ask BCASA for the rain-gauge form, get the tutor letter, register the instància |
| 2 | **Parcs i Jardins** | Replacement list, streets keeping planes (Meridiana), 15% cap scope, official 2026 mix, sidewalk widths | City form, code **RGF7342** (sent 21–24 Oct). Old address parcsijardins@mail.bcn.es does not work (user, 3 Nov) | No reply after ~2 weeks. **No longer blocking:** S1b (observed replacements), the plan text (cap) and sidewalk work cover most questions; still open: Meridiana, the "adapted species" list | One follow-up via the form on 4 Nov (draft §2); ask the tutor for an Àrea d'Arbrat contact on 10 Nov; otherwise a stated limitation |
| 3 | **Barcelona Regional** | Licence for RESCCUE depth layers (`rcc_iu1_*`), units of `depth2d`/`speed2d`, any T = 1 yr run | Web form bcnregional.com/contacte-2 (30 Oct, no code). The 13 Oct email to br@bcnregional.com **bounced** | No reply recorded | Phone +34 932 237 400 ~13 Nov if silent. Point 3 of the BCASA instància asks the same licence, so either answer settles it |
| 4 | **TRY database** (MPI Jena) | Traits for the 21 Porta species (request **53077**, 13 Oct) | try-db.org | **Data release started 3 Nov** by Giovanni (datasets with permission "yes", incl. BROT 2.0; AusTraits, Bauerle, BIEN excluded: no permission) | Wait for the TRY pickup email; forward it; save in `databases/TRY_DATABASE/` |
| 5 | **Infrared City** (Angelos Chronis, Serjoscha Duering, Oana Taut) | Research access; trees as geometry or LAI; API limits; validation | Email | Angelos replied ~1 Nov (free tier, results must be open); **Giovanni replied 2 Nov** | Wait. Ask about crown transmittance/LAI if not answered. Reminder ~9 Nov, or ask in person on 10 Nov |
| 6 | **PEMB** (Giulio) | Access/contacts for tree and flood data | Email (with Fiona) | **Closed 30 Oct:** no data, pointed to providers (rows 1–3) | None |
| 7 | **Comune di Firenze, SIT** | LiDAR point cloud, 27 Jun 2023 flight, 1–2 km² Rifredi/Novoli | Email sit@comune.fi.it (cc opendata@) | **Drafted 18 Oct, not sent** (`notes/firenze_lidar_request.md`) | Decide whether Florence is still the transfer test; if yes, send after 10 Nov |
| 8 | **Ajuntament de Mataró** | Per-tree species table (Safetree / ORDS `T_C_ARBRAT`) | Browser check first, then request | Not started (browser check pending, `notes/todo_manual.md`) | Only if Mataró stays the Catalan fallback |
| 9 | **BCASA, gauge series (optional)** / **Meteocat XEMA** | Real storms to replay | Covered by row 1 / free API key | Optional | No action |

## 0. PDISBA: what the published volumes already hold (read 3 Nov)
PDISBA on BCNROC (https://bcnroc.ajuntament.barcelona.cat/items/3cc3df7e-be95-4111-a995-98715dbe172e, hdl 11703/119275,
licence **CC BY-NC-ND**): all 11 TXT layers downloaded by Giovanni to `databases/barcelona/raw/pdisba/` (gitignored),
renamed `01_memoria.txt` … `11_planols_vol5.txt`.
- **A T = 1 yr run exists for the current network.** Diagnosi §4.4.2 (Doc. 3, p.152): the 1D/2D model was run for
  T = 1, 10, 50, 100, 500 yr, present climate and RESCCUE 2100 climate. Results are in the map series, Diagnosi
  Taula 38 (p.179): **T = 1 → plànols 6.2** (present climate), 7.1 (climate change), 12.1/13.1 (with SUDS).
- Each series has 10 plates: 6.2.1 flows, 6.2.2 velocities, 6.2.3 network functioning, **6.2.4 surface drainage**,
  **6.2.5 pedestrian hazard**, 6.2.6 vehicle hazard, 6.2.7–6.2.8 risk, 6.2.9 damages, **6.2.10 detail plans**.
- Diagnosi Fig. 127 (p.271) charts the high-risk area for pedestrians per district (Nou Barris included) for T1–T500.
- The plates are raster maps inside the 1.7 GB Plànols PDFs (the TXT layer holds only the index); which volume holds
  series 6.2 is not yet known. **They are PDF maps, not GIS**, and ND forbids publishing modified versions.
- **Diagnosi PDF read (3 Nov, OMEN copy).** Fig. 59 (doc p.179 = PDF p.198), current network, present climate, metres
  of sewer by state: **T = 1: 1,628,413 m free-surface, 201,260 m pressurised, 10,004 m within 0.5 m of ground,
  45,982 m surcharging above ground**; T = 10: 757,601 / 618,324 / 63,931 / 445,803 m. So at T = 1 about 2.4% of the
  network surcharges to the surface, at T = 10 about 24% (shares computed here from the figure's table).
  §6.2.3 lists T = 10 critical points with maps; two are in or near Nou Barris: **6.2.3.11 Plaça Llucmajor** (old Riera
  de Sant Andreu, surface flow down c/ Garrofers; Fig. 71) and **6.2.3.12 Tajo – Cartellà** (c/ Cartellà drains the
  strip between Ronda de Dalt and Turó de la Peira; Fig. 72). Whether either lies inside Porta is not yet checked.
- **Plànols PDFs: downloads incomplete** (Vol I 1.23 GB and Vol II 1.15 GB truncated, III/IV partial, V empty; pdfinfo
  cannot open any). Vol IV is complete (394 pp.) but holds series 12 (future + SUDS; p.100 = plate 12.2.10, sheet B04, 1:5000 grid). Series 6.2 is probably in Vol II. On 3 Nov BCNROC answered curl with a rate-limit page (`error_400_rateExceeded`): retry Vol II only, in the browser, another day.
- **Consequence for the BCASA request:** no need to ask *whether* a T = 1 run exists; ask for the **GIS layers of
  plànols series 6.2 (and 6.3, T = 10) for Nou Barris**, plus the gauge series.

## 1. BCASA instància: why it is complicated, and the package

BCASA's reply to BDM9240 (full text in `notes/data_sources_pemb_30oct.md` §5 on branch `claude/project-thread-synuk4`)
asks for four things, and three of them depend on someone else:

1. **The instància itself**: city form 00106
   (https://seuelectronica.ajuntament.barcelona.cat/sites/default/files/00106_instancia_formulari_0.pdf), with the
   "Exposo / Sol·licito" text below. Registered either online (needs a digital certificate: idCAT, Cl@ve, or DNIe/NIE
   certificate) or **on paper at an Oficina d'Atenció Ciutadana** (OAC; book a cita prèvia, bring ID).
2. **The separate rain-gauge form**: BCASA mentioned it but did not attach it. Ask for it by replying to BDM9240.
3. **A tutor letter** on IAAC letterhead, signed (text below). Angelos is the natural signer.
4. **Exact thesis title** (both the instància and the letter quote it).

**Conflict to settle first.** BCASA forbids sharing with third parties; Angelos (for Infrared) asked that all thesis
results and methods be open. Compatible if BCASA data stays out of the public repo and web app (raw files gitignored,
only the thesis document and academic presentations), but say so to the tutor when asking for the letter.

**Is it worth it before 18 Dec?** The tool already runs on PDISBA's published IDF and the RESCCUE depths. BCASA data
would add (a) real storms to replay and (b) a T = 1–2 yr flood run, the one storm PDISBA lacks for frequent events.
Useful for validation, not blocking. A formal instància can take weeks.

### 1a. Reply to BDM9240 asking for the rain-gauge form (Spanish, reply from the IAAC inbox)
> Asunto: Re: BDM9240 – formulario de datos pluviométricos
>
> Buenos días:
> Muchas gracias por la respuesta a la consulta BDM9240. Para preparar la instancia que me indican, ¿podrían
> enviarme el formulario específico para la solicitud de datos pluviométricos, que no venía adjunto?
> Atentamente,
> Giovanni Carlo Volpe – MaCAD, IAAC – giovanni.carlo.volpe@students.iaac.net

### 1b. Instància, "Exposo / Sol·licito" (Spanish)
**Expongo:** Soy estudiante del Master in Advanced Computation for Architecture & Design (MaCAD) del Institute for
Advanced Architecture of Catalonia (IAAC), curso 2025–2026. Mi trabajo final de máster, «[TÍTULO EXACTO]», desarrolla
un método computacional que propone especies y posiciones de arbolado viario para reducir el estrés térmico estival y la
escorrentía pluvial, aplicado al barrio de la Porta (Nou Barris). Siguiendo la respuesta de BCASA a la consulta BDM9240,
adjunto la carta de mi tutor y el formulario de datos pluviométricos.

**Solicito**, para uso exclusivamente académico, sin cesión a terceros y citando «Barcelona Cicle de l'Aigua, SA,
Ajuntament de Barcelona»:
1. Series de precipitación a 5 minutos de los pluviómetros de BCASA más cercanos a Nou Barris (periodo disponible).
2. En formato SIG, los resultados del modelo 1D/2D del PDISBA para Nou Barris representados en los planos 6.2 (T = 1 año)
   y 6.3 (T = 10 años) sin cambio climático: calados, velocidades y drenaje superficial.
3. Si existe, la autorización para usar en la tesis las capas RESCCUE publicadas en el Atles de Resiliència (tablas
   `rcc_iu1_*`), con la cita que indiquen.

### 1c. Email to the tutor asking for the letter (English)
> Subject: Signed letter for a BCASA data request (thesis)
>
> Hi Angelos,
> BCASA (Barcelona's water utility) can share its rain-gauge series and drainage-model results for Nou Barris, but
> only through a formal request with a letter from my tutor confirming enrolment, programme, thesis title and content.
> I attach a draft; could you sign it on IAAC letterhead, or tell me who at IAAC should?
> One condition to flag: the data is for academic use only, with no sharing to third parties. It would stay out of the
> public repo and web app and appear only in the thesis document and presentations; the methods and code stay open.
> Thanks,
> Giovanni

### 1d. Tutor letter (to sign on IAAC letterhead)
To: Barcelona Cicle de l'Aigua, SA (BCASA), Ajuntament de Barcelona

I confirm that Giovanni Carlo Volpe is enrolled in the Master in Advanced Computation for Architecture & Design (MaCAD)
at the Institute for Advanced Architecture of Catalonia (IAAC), academic year 2025–2026, and that I supervise his
master's thesis "[title]". The thesis develops a computational method that suggests street-tree species and positions
to reduce summer heat stress and pluvial runoff, tested in the Porta neighbourhood (Nou Barris). The data requested
(rain-gauge series and drainage-model results) will be used only for this academic work, will not be shared with third
parties and will be credited to Barcelona Cicle de l'Aigua, SA, Ajuntament de Barcelona.

[Name, role, IAAC, date, signature]

### 1e. Steps, in order
1. Giovanni sends 1a (IAAC inbox) and 1c (to Angelos), and gives Claude the exact thesis title.
2. When the rain-gauge form arrives, Claude fills what it can; Giovanni signs.
3. Giovanni fills form 00106 with 1b, attaches letter + gauge form, and registers it (online with certificate, or OAC).
4. Log the registry number in row 1.

## 3. Leads from the IAAC Slack (3 Nov, via María; colleagues' hearsay) and what a web search found
- **Update 3 Nov 13:49:** María's colleague is unsure of the name and has no email; Pinyol lead dropped. Target **Joan Guitart** instead (RGF7342 follow-up addressed to him + LinkedIn).
- **Víctor Ténez** (UPC, architecture; trees and environment, per María, a former student). Email given by María: victor.tenez@upc.edu ("assuming he is still teaching there"; not verified).
- **Joan Pinyol**, said to work on trees in urban projects for the city. **Not found** in any public source (3 Nov
  searches). The person the press and the city's own presentations name for the tree plan is **Joan Guitart**
  (Pla director de l'arbrat presentations, e.g. DIBA deck "Presentació Joan Guitart"; head of the Àrea d'Arbrat per
  press 2022). Possibly a mix-up; ask María.
- **Cati Montserrat Martí**, AMB (Àrea Metropolitana de Barcelona), garden/green-space projects: LinkedIn profile found
  (https://www.linkedin.com/in/cati-montserrat-mart%C3%AD-8295787b/). Contact route: LinkedIn message. AMB is
  metropolitan, so useful for practice and a design-side view, not for city street-tree data.
- **AiEM / AIEM**: UPC research group *Arquitectura, Energia i Medi Ambient* (Dept. Tecnologia de l'Arquitectura;
  site aie.upc.edu; ta.upc.edu news "Research visiting, grup de recerca AIEM"). Fits the heat/UTCI side (urban
  microclimate, vegetation). Contact route: the group site; pick a named researcher before writing.

### 3b. Non-Barcelona leads (James, IAAC Slack, 3 Nov): literature first, contact later
- **Ronita Bardhan** (University of Cambridge; profile https://www.cst.cam.ac.uk/people/rb867). James recalls a paper on
  urban tree species and thermal comfort; press reports a Cambridge study on the cooling role of trees in overheating
  cities. Exact paper not yet identified: find it, add it to the literature matrix if relevant, then decide on contact.
- **Rob Adams** (former City Architect / Director City Design, City of Melbourne): lecture on Melbourne's trees.
  Melbourne's urban forest strategy and open tree data are a precedent for the state of the art, not a data source for
  Porta. Melbourne already appears in the matrix through Livesley's group (Baptista 2018, Grey 2018, Thom 2020).

## 2. Parcs i Jardins follow-up (Catalan, same city form, Wed 4 Nov)
> Assumpte: Seguiment de la consulta RGF7342 – a l'atenció del Sr. Joan Guitart (Àrea d'Arbrat)
>
> Bon dia,
> A l'octubre vaig enviar la consulta RGF7342 sobre la substitució d'arbrat viari a la Porta (Nou Barris), per a
> la meva tesi de màster a l'IAAC. Voldria saber si ha arribat a l'equip d'Arbrat i si hi ha previsió de resposta.
> Hi afegeixo una pregunta breu: quines espècies compten com a "adaptades" per a l'objectiu del Pla Clima de passar del
> 30% al 40%? Hi ha una llista publicada?
> Moltes gràcies,
> Giovanni Carlo Volpe – MaCAD, IAAC – giovanni.carlo.volpe@students.iaac.net
