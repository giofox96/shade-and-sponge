# Data and information requests to institutions: status board

*Started 3 Nov 2026. One place for every request to an outside body. Update the row when anything moves.
Replies to the city forms go to giovanni.carlo.volpe@students.iaac.net (IAAC inbox), which Claude cannot read:
forward replies or paste them in the thread. Nothing here is sent by Claude.*

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
| 8 | **Ajuntament de Mataró** | Per-tree species table (Safetree / ORDS `T_C_ARBRAT`) | **SENT 10 Nov** by Giovanni to `bustia@ajmataro.cat` (asked to forward to the Servei d'Infraestructura Verda; text `/mnt/project-files/notes/mataro_tree_request_draft.md`). Same day: LinkedIn message to the Ajuntament de Mataró page asking which service to contact; Slack request to classmates in Spain to open the ORDS URL and save the JSON | 10 Nov: no tree dataset on the city's open-data portal (seu-e.cat), AOC, DIBA or datos.gob.es. `apex.mataro.org` times out on ports 80/443 from an Italian home connection too (www.mataro.cat answers), so its firewall drops outside traffic: the ORDS check cannot be done from Italy. Licence for city data = Llicència oberta d'ús d'informació – Catalunya (mataro.cat/transparencia/llicencia-de-reutilitzacio-de-la-informacio-publica) | Only if Mataró stays the Catalan fallback |
| 9 | **BCASA, gauge series (optional)** / **Meteocat XEMA** | Real storms to replay | Covered by row 1 / free API key | Optional | No action |
| 10 | **ENVI-met** (student licence) | Student licence: 1 year, 50 simulations, grids up to 100x100x50, proof of enrolment required. Use stated: UTCI check (hot design day, 12–17 h) on a few street segments, current trees vs city replacement vs tool replacement, ~20–40 runs, single user, non-commercial | "Get in touch" web form, sent 9 Nov by Giovanni from the IAAC email | Form accepted ("Thanks for submitting the form"), no reply yet | Send the IAAC enrolment certificate (PDF) when they ask. A 100x100 grid at 2 m covers ~200 × 200 m: one street segment, not all of Porta |

## 0. Before the instància: unread PDISBA volumes (3 Nov)
PDISBA on BCNROC (https://bcnroc.ajuntament.barcelona.cat/items/3cc3df7e-be95-4111-a995-98715dbe172e, hdl 11703/119275, licence **CC BY-NC-ND**) has 11 files: Memòria, Pluges (read: IDF §2.6), Diagnosi Xarxa (338 p), Prognosi, Pla rehabilitació, Pla inversió, Plànols Vol. 1–5 (~1.7 GB each). Diagnosi and Plànols are unread and may hold current-network flood maps per return period for Nou Barris (check for T = 1–2). To do from the OMEN (cloud is blocked). The 5-min gauge series and GIS files are not in the PDFs, so the BCASA follow-up still goes out.

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
2. Resultados del modelo 1D/2D de drenaje (PDISBA) para Nou Barris: calados y velocidades máximas para los periodos de
   retorno disponibles, en especial T = 1 o 2 años, en formato SIG.
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

## 2. Parcs i Jardins follow-up (Catalan, same city form, Wed 4 Nov)
> Assumpte: Seguiment de la consulta RGF7342
>
> Bon dia,
> A l'octubre vaig enviar la consulta RGF7342 sobre la substitució d'arbrat viari a la Porta (Nou Barris), per a
> la meva tesi de màster a l'IAAC. Voldria saber si ha arribat a l'equip d'Arbrat i si hi ha previsió de resposta.
> Hi afegeixo una pregunta breu: quines espècies compten com a "adaptades" per a l'objectiu del Pla Clima de passar del
> 30% al 40%? Hi ha una llista publicada?
> Moltes gràcies,
> Giovanni Carlo Volpe – MaCAD, IAAC – giovanni.carlo.volpe@students.iaac.net
