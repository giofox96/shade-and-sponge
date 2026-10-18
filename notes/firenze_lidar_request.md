# Data request: Comune di Firenze LiDAR point cloud (27 June 2023 flight)

*Drafted 18 Oct 2026, for the user to send or deliver in person. Never sent by an agent (see `.claude/agents/data-scout.md`). The letter below is in **Italian** at the user's explicit request; the surrounding notes stay in English per CLAUDE.md.*

## Why this request exists
`databases/data_inventory.md` §6.1 established that **no classified, leaf-on LiDAR point cloud over the built-up area of Florence is publicly downloadable**. The only public cloud (Geoscopio lot 002 "Bacino dell'Arno") is unclassified, ~2 pts/m², flown across a leaf-off-to-leaf-on window, and misses the city centre. The Comune, however, **publishes DTM and DSM rasters derived from a LiDAR flight of 27 June 2023** — whole municipality, 485 tiles, CC BY 4.0 — which is unambiguously **leaf-on**. The point cloud behind those rasters is the missing input.

**The one thing that matters most:** a leaf-on, classified cloud is still useless to this method if it was thinned to ground + first pulse. The LAI proxy is a *gap fraction of points inside each crown*, so it needs multiple returns per pulse with vegetation returns retained. **Ask that before asking about licence** — if the answer is "first pulse only", the request stops there and nothing is lost.

## Who to address

| | |
|---|---|
| **Office** | SIT — Sistema Informativo Territoriale, Comune di Firenze. **Note the Direzione:** the Comune's *Funzionigramma* (Rev. 10.0, in force 25/11/2024) assigns the *Sistema Informativo Territoriale* macrofunzione (cod. 4.8) to the **Direzione Urbanistica**; the **Direzione Sistemi Informativi** holds its *development* (cod. 4.9) and open data (cod. 36.8), and is the `author` on the CKAN records. If the first contact cannot help, ask for Urbanistica. |
| **Address** | Via Reginaldo Giuliani 250, 50141 Firenze — **secondo piano** |
| **Telephone** | 055 3283858 |
| **Email** | `sit@comune.fi.it` |
| **Second email** | `opendata@comune.fi.it` — the author/maintainer address on the Comune's own dataset records; put it in cc |
| **Formal route, if the informal one stalls** | An *accesso civico generalizzato* request: D.Lgs. 33/2013 **art. 5 c. 2** establishes the right, **c. 3** says the request needs no justification, **c. 4** makes release free *salvo il rimborso del costo effettivamente sostenuto* for reproduction on physical media (the clause a multi-GB delivery would trigger), **c. 6** sets a 30-day deadline, and **art. 7** makes the data reusable citing the source. For the PEC address, look it up on the Comune's *Amministrazione trasparente* pages — this note does not record one, because none was verified. Use this route only as a fallback: a technical office answers a technical question faster than a legal one. |

Sources: the Direzione attribution comes from the Comune's *Funzionigramma* (Rev. 10.0) and the CKAN `author` field, **not** from the two sources below, neither of which names a Direzione. The address, telephone and `sit@comune.fi.it` come from the Comune's own WMS service metadata (`https://tms.comune.fi.it/tiles/service/wms?request=GetCapabilities`, `<ContactInformation>` block); the "secondo piano" from the official SIT page (`comune.firenze.it/pagina/territorio/sistema-informativo-territoriale`); `opendata@comune.fi.it` from the CKAN record of the Comune's datasets.

**Going in person:** the official page gives no counter hours and the SIT is a technical office, not a public-facing desk. **Phone 055 3283858 first** and ask for an appointment with whoever manages the *rilievi LiDAR / cartografia*; turning up unannounced risks finding nobody who can answer. Bring the letter printed, plus the three technical questions on a single sheet.

---

## The letter (Italian — send as email to `sit@comune.fi.it`, cc `opendata@comune.fi.it`)

**Oggetto:** Richiesta di accesso alla nuvola di punti LiDAR del rilievo aereo del 27 giugno 2023 — tesi di ricerca universitaria

Gentili responsabili del Sistema Informativo Territoriale,

mi chiamo [NOME COGNOME] e sono studente del Master in Advanced Computation for Architecture & Design (MaCAD) presso l'Institute for Advanced Architecture of Catalonia (IAAC) di Barcellona. Sto sviluppando una tesi su un **metodo computazionale per la selezione e la collocazione delle alberature stradali**, valutate simultaneamente rispetto allo stress termico dei pedoni (indice UTCI) e alla riduzione del deflusso superficiale durante le piogge intense.

Il metodo è stato messo a punto su un quartiere di Barcellona e vorrei verificarne la trasferibilità su Firenze. Utilizzo già il dataset **"Alberi"** e il censimento **"Life Escapos — Alberature pubbliche"**, e ho individuato e consultato i metadati del **DTM e del DSM LiDAR 2023** (licenza CC BY 4.0).

**Oggetto della richiesta.** Vorrei chiedere se sia possibile accedere alla **nuvola di punti LiDAR** (formato LAS/LAZ, o il formato in cui è conservata) del **volo del 27 giugno 2023**, quello da cui derivano il DSM e il DTM pubblicati. La richiesta può limitarsi a **un'area circoscritta** — sarebbe sufficiente un settore di 1–2 km² nella zona **Rifredi / Novoli (Firenze Nova)** — e non all'intero territorio comunale.

**Perché serve la nuvola di punti e non il raster.** Il metodo stima l'indice di area fogliare (LAI) di ogni albero a partire dalla **frazione di vuoto dei punti laser all'interno della chioma**, cioè dalla quota di impulsi che attraversano la chioma e raggiungono il suolo. Questa informazione esiste solo nella nuvola di punti: un modello digitale di superficie, per quanto accurato, restituisce l'altezza e l'ampiezza della chioma ma non la sua densità fogliare. Il volo del 27 giugno 2023 è particolarmente prezioso proprio perché effettuato **in piena stagione vegetativa**, condizione necessaria per questo tipo di stima.

**Tre domande tecniche preliminari.** Prima ancora della questione dell'accesso, mi sarebbe molto utile conoscere tre caratteristiche del rilievo, perché da esse dipende se il dato sia effettivamente utilizzabile per questo scopo:

1. Qual è la **densità media e minima di punti per metro quadrato** del volo del 27 giugno 2023?
2. Il sensore ha registrato **più ritorni per impulso** e, soprattutto, **i ritorni sulla vegetazione sono stati conservati** nel dato consegnato, oppure la nuvola è stata filtrata mantenendo solo il terreno e/o il primo ritorno?
3. La nuvola è **classificata** (ad esempio secondo lo schema ASPRS: suolo, vegetazione bassa/media/alta, edifici) e, in caso affermativo, quali classi sono state utilizzate?

Se la nuvola fosse stata filtrata al solo primo ritorno, il dato non sarebbe utilizzabile per questa analisi e non avrei motivo di procedere oltre con la richiesta: mi basterebbe saperlo.

**Licenza e utilizzo.** Qualora l'accesso fosse possibile, vorrei chiedere esplicitamente sotto quale licenza il dato verrebbe fornito e se sia consentito **pubblicare i prodotti derivati** — modello di altezza delle chiome, stime di LAI per singolo albero, figure e mappe — all'interno di una **tesi di laurea magistrale** e in un **repository pubblico di codice** (GitHub), con la citazione della fonte nella forma che il Comune riterrà corretta. Segnalo che IAAC è un istituto privato, quindi, se esistessero condizioni riservate ai soli enti pubblici, preferirei saperlo in anticipo.

**Disponibilità.** Sarò ben lieto di citare il Comune di Firenze come fonte in ogni elaborato, di condividere i risultati e i prodotti derivati con il Vostro ufficio, e di inviare copia della tesi una volta conclusa. Sono inoltre disponibile a passare di persona presso i Vostri uffici di via Reginaldo Giuliani 250, previo appuntamento, se ciò rendesse più semplice la valutazione della richiesta.

Ringrazio per l'attenzione e resto a disposizione per qualsiasi chiarimento.

Cordiali saluti,
[NOME COGNOME]
Master in Advanced Computation for Architecture & Design (MaCAD)
Institute for Advanced Architecture of Catalonia (IAAC), Barcellona
[email] — [telefono]

---

## Using your professional standing (user is a licensed architect in Italy)

**What it changes.** A request signed by an *architetto iscritto all'Ordine*, with an albo number, reads to a technical office as a professional undertaking rather than a student enquiry, and it makes one specific lever credible: **offering to sign a *dichiarazione di utilizzo dei dati*** — a written declaration of the scope of use, of non-redistribution of the raw cloud, and of the attribution formula. In Italian municipalities that declaration is very often what unlocks a dataset sitting in an *accesso riservato* tier, because it gives the office something to file. Offer it explicitly rather than waiting to be asked.

**What it does NOT change — do not waste a request on this.** Being registered with an Ordine does **not** make you an *ente pubblico*. The Regione Toscana 2019–2021 LiDAR is restricted *"solo per enti pubblici"* (owner: Italian Remote Sensing S.r.l.), and professional registration does not satisfy that condition. That dataset stays out of reach either way; the Comune's own 27 June 2023 survey is the target.

**One honest-framing warning.** The purpose of this request is a **master's thesis**, i.e. research. Present the qualification as what it is — professional standing that supports a commitment to handle the data properly — and keep the stated purpose research. Do not let the letter imply a commissioned professional job that does not exist: a technical officer who later discovers the work was academic will remember it, and the Comune's SIT is a small office you may need again.

**Worth one phone call, unverified:** whether the **Ordine degli Architetti PPC di Firenze** has any standing arrangement with the Comune for access to municipal cartography. This note has *not* checked that; if such a convention exists it would be a faster route than an individual request.

### Paragraph to insert in the letter (after the "Perché serve la nuvola di punti" paragraph)

> **Qualifica e impegni d'uso.** Sono architetto abilitato e iscritto all'Ordine degli Architetti P.P.C. di [PROVINCIA] al n. [NUMERO]; la presente richiesta è tuttavia formulata a **fini di ricerca**, nell'ambito della tesi di master sopra descritta. Sono pienamente disponibile a sottoscrivere una **dichiarazione di utilizzo dei dati** che specifichi l'ambito della ricerca, l'impegno a **non ridistribuire la nuvola di punti grezza** e la formula di citazione della fonte che il Comune riterrà corretta, nonché a concordare qualsiasi ulteriore condizione il Vostro ufficio ritenga opportuna.

### Signature block, revised

> Cordiali saluti,
> **[NOME COGNOME]**
> Architetto — Ordine degli Architetti P.P.C. di [PROVINCIA], n. [NUMERO]
> Studente, Master in Advanced Computation for Architecture & Design (MaCAD)
> Institute for Advanced Architecture of Catalonia (IAAC), Barcellona
> [email] — [telefono] — [PEC, se la usi]

Add your **PEC** if you have one as a professional: a PEC-to-PEC exchange with the Comune is formally tracked and tends to be answered more reliably than ordinary email. If you send from PEC, address it to the Comune's protocol PEC and name the SIT in the subject line.

## If you go in person: what to say in 30 seconds

> "Buongiorno, sono architetto e sto facendo un master in architettura computazionale allo IAAC di Barcellona. Sto facendo una tesi sugli alberi stradali e uso già i vostri dati aperti sugli alberi; ho visto che pubblicate anche il DTM e il DSM LiDAR del 2023. Avrei bisogno di sapere tre cose tecniche sul volo del 27 giugno 2023: la densità di punti al metro quadrato, se sono stati registrati più ritorni per impulso e se i ritorni sulla vegetazione sono stati conservati, e se la nuvola di punti è classificata. Se la risposta alle prime due è sì, vorrei chiedere se è possibile avere la nuvola di punti di una zona limitata, Rifredi–Novoli, e sapere con quale licenza."

Then hand over the printed letter.

## What the answers mean for the thesis
| Answer | Consequence |
|---|---|
| Multiple returns retained + ≥ 5 pts/m² + classified | **Florence transfer is on.** Proceed exactly as in Porta |
| Multiple returns retained, but unclassified | Workable: classify with PDAL/lasground ourselves; add it as a methodology step and a limitation |
| First pulse / ground-filtered only | **Florence cannot support the LAI proxy.** Fall back to the Catalan city, and say so in the thesis as a data-availability finding |
| Access refused or reserved to public bodies | Same as above; record it as the licence barrier it is |
| No reply before ~10 Nov | Treat as a no for planning purposes — the transfer window is 2–10 Dec |


---

## Fact-check, 18 Oct 2026 (27 claims tested against primary sources)
**The letter's load-bearing facts hold.** Verified independently: the flight date **27 June 2023** and licence **CC BY 4.0** are verbatim in the CKAN records of `dtm-lidar-2023` (c_d612:D.7683) and `dsm-lidar-2023` (D.7684) — *"realizzato mediante elaborazione del rilievo Lidar effettuato in data 27 giugno 2023"*; the published archive has exactly **485** tiles on a 500 m step covering X 673000–688500 / Y 4843500–4856500, with the Duomo, Novoli and Gavinana tiles all present. The point-cloud premise was re-confirmed through Geoscopio WMS GetFeatureInfo: every sheet over the built-up city reads *"Su questo foglio nuvola di punti non disponibile"*, while the Osmannoro sheet carries lot 002 "BACINO DELL'ARNO", *"Data volo: DAL 2/3/2008 AL 10/5/2008"*. Address, telephone, email and "secondo piano" are verbatim in the cited sources, and Pacetti et al. (2022) do name **district D5 Rifredi–Novoli** as their pilot.

**Three things were corrected above:** the Direzione attribution (the SIT sits under Urbanistica, not Sistemi Informativi); the letter's claim to *already use* the 2023 rasters, which the repository has never downloaded; and the accesso-civico citation, which conflated four separate commi and dropped the reimbursement clause.
