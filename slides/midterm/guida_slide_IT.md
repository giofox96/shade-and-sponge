# Shade and Sponge, midterm: i concetti dietro ogni slide

Una guida di studio per il deck del midterm (24 slide, versione del 24 novembre 2026). Serve per spiegare ogni slide con parole tue e per rispondere alle domande. Per ogni slide trovi **cosa dice**, **i concetti che ci stanno dietro** e **le domande che potrebbero farti**. Il testo da dire a voce è in `speech_midterm.md`; questo file è lo sfondo.

I numeri vengono dal deck e dalle note del progetto. Dove qualcosa è una scelta di modello o un'approssimazione, è detto esplicitamente.

---

## Glossario (da leggere per primo)

- **Albero stradale / posizione / spot.** Una *posizione* è il punto in cui oggi c'è un albero stradale. Uno *spot libero* è un punto del marciapiede dove si potrebbe piantare un albero nuovo. Il metodo lavora su entrambi.
- **Chioma.** La parte con le foglie in alto. La sua dimensione (diametro, area) decide quanto suolo ombreggia e quanta pioggia trattiene.
- **LiDAR.** Una scansione laser da aereo che registra milioni di punti 3D. Da lì ricaviamo altezza, dimensione e densità della chioma di ogni albero, e la forma di edifici e terreno. Qui si usa il volo ICGC (l'istituto cartografico catalano) del 2021, fatto a fine settembre con le foglie.
- **LAI (leaf area index, indice di area fogliare).** Metri quadrati di foglie per metro quadrato di suolo sotto la chioma. Una chioma con LAI 2,3 ha 2,3 m² di foglie sovrapposti sopra ogni m² di suolo. LAI più alto significa chioma più densa, quindi più ombra e più pioggia trattenuta. Lo stimiamo dal LiDAR: più impulsi laser attraversano la chioma fino a terra, più la chioma è aperta (LAI più basso).
- **Ombra estiva (m²·h).** La nostra misura del calore. È l'area di suolo in ombra moltiplicata per le ore di ombra in un pomeriggio caldo di luglio (12–17): 10 m² in ombra per 5 ore fanno 50 m²·h. È un **proxy**: dice dove il sole viene bloccato, non quanto caldo sente una persona.
- **Ombra invernale / sole invernale.** La stessa misura in un giorno di gennaio (10–15). D'inverno l'ombra è un **costo**, perché le persone cercano il sole. Per questo gli alberi decidui (spogli d'inverno) ottengono buoni punteggi.
- **UTCI.** Universal Thermal Climate Index, una "temperatura percepita" in °C che combina temperatura dell'aria, radiazione del sole e delle superfici calde, vento e umidità. È il prossimo passo sul calore (Ladybug, Infrared City).
- **Runoff (deflusso).** L'acqua piovana che non si infiltra e non resta sulle foglie, e scorre in superficie. Troppa acqua nello stesso punto dà un **allagamento pluviale** (dovuto alla pioggia, non a un fiume).
- **Intercettazione.** La pioggia trattenuta da foglie e rami, che poi evapora invece di arrivare a terra.
- **Pioggia di progetto.** Una pioggia standard usata per progettare, definita dalla durata e dal **tempo di ritorno** T: una "pioggia a 2 anni" è così intensa che, in media, arriva una volta ogni due anni. Qui si usa quella del PDISBA (il piano di drenaggio di Barcellona) con T = 2 anni, 60 minuti, 31,9 mm.
- **Hotspot di allagamento.** Un punto dove l'acqua si accumula con pioggia forte, preso dal Barcelona Resilience Atlas del comune.
- **Pratica della città (S1b).** Le specie che la città ha davvero piantato quando ha sostituito alberi, 2018–2026, lette dal suo stesso inventario. È il riferimento principale. **S1a** è il mix annunciato dalla città (stampa), mostrato accanto.
- **Numero effettivo di specie.** Una misura di diversità: exp(indice di Shannon). Se pianti 10 specie in numero uguale vale 10; se una specie domina, scende anche se le specie presenti sono tante.
- **HiGHS.** Un solver open source di programmazione lineare. "Esatto" vuol dire che trova la risposta migliore e può dimostrare che non ce n'è una migliore.
- **Controllo do-no-harm ("non fare danni").** Una condizione, non un obiettivo: il metodo non deve peggiorare il runoff rispetto al riferimento, ma non cerca di ridurlo al massimo.

---

## Presentazione (slide 1–15, 20 secondi ciascuna)

### Slide 1. Titolo: "I am redesigning this street"
**Cosa dice.** Il talk si apre con il nome del progetto, Shade and Sponge, e con cosa è: un recommender di alberi stradali urbani. La tesi prende il punto di vista di un progettista che sta già ridisegnando una strada. Il layout è deciso; la domanda aperta sono gli alberi: tenerli, spostarli, sostituirli o aggiungerne, perché la strada sia più fresca d'estate e non peggiori con la pioggia, dentro le regole della città.

**Concetti.**
- Il tool non è uno strumento di pianificazione alla scala della città. Entra **alla scala del progetto**, dove gli alberi si decidono davvero.
- Due obiettivi, ma non alla pari: **il calore è l'obiettivo** (più ombra estiva), **il runoff è un vincolo** (non peggiorare).
- "Dentro le regole della città" vuol dire che la risposta deve essere accettabile per il comune: specie ammesse, limiti di dimensione, tetto del 15%.

**Domande possibili.** *Perché il progettista e non la città?* Perché la città sostituisce gli alberi uno alla volta nei progetti (il 46,8% delle sostituzioni sono alberi isolati, secondo l'analisi del 10 novembre), quindi la decisione avviene nel progetto.

### Slide 2. Contesto: sostituire alberi uno alla volta
**Cosa dice.** Barcellona ha sostituito 10.976 alberi stradali tra il 2018 e il 2026. Il piano degli alberi limita ogni specie al 15%, ma non dice quale specie mettere dove. La copertura arborea di Porta è il 20,1%, contro un obiettivo della città del 30%. E a parità di tronco, le chiome delle diverse specie vanno da un platano intero a circa un quarto di platano. Tutto è confrontato con il **platano**, perché è l'albero sostituito più spesso (13% delle sostituzioni osservate): i risultati sono dati come percentuale dell'ombra estiva di un platano.

**Concetti.**
- Il **Pla director de l'arbrat 2017–2037** (il piano degli alberi della città) stabilisce *quanto* di ogni specie (il tetto del 15%, per resistere a parassiti e malattie, per la resilienza climatica e per la biodiversità), non *quale specie in quale strada*.
- **Stesso tronco, chiome diverse.** La città classifica gli alberi per dimensione del tronco. Il grafico mostra che due alberi con lo stesso tronco possono ombreggiare aree molto diverse. Quindi la scelta della specie cambia l'ombra che riceve una strada, anche con lo stesso numero di alberi.
- Nel piano il tetto del 15% vale su tutta la città. Nel tool è applicato solo agli alberi stradali, una semplificazione dichiarata nella slide 22.

**Domande possibili.** *Da dove vengono le 10.976 sostituzioni?* Dall'inventario aperto degli alberi (Open Data BCN), confrontando le versioni nel tempo: una posizione in cui la specie è cambiata è una sostituzione.

### Slide 3. Porta in numeri
**Cosa dice.** Perché Porta: è il primo quartiere di Barcellona in cui calore, pericolo di allagamento e platani sono tutti alti (superficie in estate +1,4 °C rispetto alla città, pericolo di allagamento nel 20% più alto, 832 platani = 29% dei suoi alberi stradali). Porta copre 84 ha con 2.825 alberi stradali. Le chiome coprono 17 ha (20%). Per arrivare al 30% servirebbero circa 8 ha in più. Piantare ogni spot libero sui marciapiedi aggiunge solo circa 0,3 ha **di chioma** (copertura arborea vista dall'alto), contro gli 8 ha di chioma che mancano.

**Concetti.**
- **Il sito è stato scelto con i dati**, classificando i quartieri su entrambi i rischi; Porta è risultato primo. I platani contano perché il piano li vuole ridurre, quindi molti verranno sostituiti.
- **L'argomento chiave della slide:** gli spot nuovi sono pochi e piccoli, quindi aggiungere alberi non basta a colmare il divario. Al progettista resta la scelta di **quale specie** mettere in ogni spot, perché la dimensione della chioma dipende dalla specie.
- Piazze, parchi e cortili potrebbero aggiungere copertura, ma sono fuori dal perimetro (lavoro futuro).

**Domande possibili.** *1,4 °C è temperatura dell'aria?* No. È l'anomalia mediana della temperatura superficiale diurna estiva rispetto alla mediana della città (Landsat 8/9, 31 immagini serene, giugno–agosto 2022–2025), un indicatore di screening, non una temperatura percepita. *Perché "primo"?* Un quartiere era ammesso solo se quota allagabile, calore superficiale e densità di platani erano tutti sopra il 60° percentile della città; tra questi Porta è primo a ogni soglia provata.

### Slide 4. Stato dell'arte e gap
**Cosa dice.** La ricerca copre ogni parte del problema, ma separatamente; nessuno le unisce. Alcuni modelli valutano insieme calore e runoff senza scegliere le specie. Altri strumenti scelgono le specie, ma per un solo beneficio o senza posizioni. Dei 18 strumenti esaminati, nessuno sceglie le specie albero per albero, su calore e runoff, dentro le regole di una città.

**Concetti.**
- La rassegna funziona come un **imbuto**: 18 strumenti → 7 trattano insieme calore e runoff → 1 sceglie anche le specie (Dong et al. 2026) → 0 lo fanno albero per albero dentro regole reali di una città.
- **SylvCiT** (Nicol et al. 2026, Montréal) è il raccomandatore più vicino: sceglie le specie per diversità e carbonio, ma il suo modulo sul runoff è "in sviluppo" e non ha un modulo sul calore.
- Il contributo quindi è **un metodo**, non un nuovo modello fisico: unisce pezzi esistenti (chiome da LiDAR, ombra, intercettazione, percorsi dell'acqua, un ottimizzatore esatto) dentro i vincoli della città.

**Domande possibili.** *Il gap è reale o solo stretto?* È stretto di proposito: il tutor ha chiesto una tesi molto specifica. La parte specifica è "albero per albero, dentro le regole, contro la pratica reale".

### Slide 5. Domanda di ricerca rifinita
**Cosa dice.** A ottobre la tesi partiva dagli alberi contro gli allagamenti (Bologna). Il feedback è stato che il runoff dipende più dalla buca dell'albero che dalla specie, quindi il runoff è diventato un controllo do-no-harm. La domanda ora: quando un progetto stradale a Barcellona deve sostituire o aggiungere alberi, in che misura un metodo basato sui tratti, che sceglie specie e posizioni dentro le regole della città, può dare più raffrescamento estivo della pratica della città, senza perdere intercettazione della pioggia?

**Concetti.**
- **Perché il runoff è passato da obiettivo a controllo:** un albero trattiene pochi millimetri di pioggia, mentre un temporale forte ne porta decine. Il suolo e la buca contano più delle foglie. Quindi l'affermazione onesta è "non peggiora", non "migliora molto".
- **Basato sui tratti:** le specie si confrontano su proprietà misurabili (dimensione della chioma, densità delle foglie, mesi con le foglie), non per nome o per aspetto.
- **"In che misura"** rende la domanda misurabile: la risposta è un numero (quanta ombra in più), non un sì o un no.

### Slide 6. Cosa è fisso, cosa è libero
**Cosa dice.** Fissi: il layout della strada, il tetto del 15%, la larghezza del marciapiede (che decide la taglia dell'albero), semafori e passi carrabili. Liberi: quattro azioni per albero, tenere, spostare, sostituire o aggiungere; mai togliere senza sostituire. Il tool consiglia, il progettista decide.

**Concetti.**
- **Keep (tenere):** l'albero resta. **Move (spostare):** l'albero viene trapiantato e il suo posto si libera. **Replace (sostituire):** una specie nuova nella stessa buca. **Add (aggiungere):** un albero nuovo in uno spot libero.
- "Mai togliere senza sostituire" evita che il numero di alberi diminuisca.
- Il progettista sceglie l'azione (spesso per ragioni che i dati non vedono: salute dell'albero, lavori, vicini). L'ottimizzatore sceglie solo la **specie** per Replace e Add.

### Slide 7. Metodologia
**Cosa dice.** Tutto il metodo in un diagramma, da sinistra a destra: focus (stress da calore, allagamenti pluviali) → dati (inventario degli alberi, LiDAR 2021, giornata calda, terreno, hotspot di allagamento, pioggia di progetto, marciapiedi e oggetti, regole della città) → screening della città (indicatori per albero) → il progettista decide un'azione per albero → HiGHS sceglie le specie per Replace e Add, valutate su calore, runoff e copertura → valutazione rispetto a oggi e alla pratica della città → validazione a Porta, poi Sant Antoni, Mataró e Firenze.

**Concetti.**
- **I pallini accanto ai dati** indicano a quale rischio serve ogni dataset: marrone per il calore (LiDAR, giornata calda), blu per gli allagamenti (LiDAR, terreno, hotspot, pioggia).
- **Le regole della città entrano nell'ottimizzatore come vincoli** (la freccia dal riquadro City rules): 30 specie ammesse, tetto del 15%, taglia secondo il marciapiede.
- **Lo screening si fa una volta sola per tutta la città**; poi si ritaglia l'area di progetto. Per questo il tool è veloce.
- **Due confronti, alla fine:** una volta che l'ottimizzatore ha scelto, il risultato è confrontato con due riferimenti: gli alberi di oggi (la strada migliora?) e la pratica della città (il metodo fa meglio di quello che farebbe la città?).
- **Il terreno (DTM) a 0,5 m** serve per i percorsi dell'acqua: su un modello digitale del terreno ogni cella manda l'acqua alla cella vicina più in basso (metodo D8), e così si sa dove finisce la pioggia di ogni punto.

### Slide 8. Screening (la matrice degli indicatori)
**Cosa dice.** Gli stessi indicatori vengono calcolati una volta per ogni posizione di albero stradale e per ogni spot libero, una riga ciascuno. Tre gruppi di colonne: A, l'albero esistente (specie, tronco, chioma, LAI, priorità), che ordina i candidati alla sostituzione; B, il luogo (larghezza del marciapiede, taglia ammessa, se la pioggia va verso un hotspot), che decide quali specie ci stanno; C, un punteggio per ciascuna delle 30 specie in quella posizione. L'ottimizzatore sceglie una specie per riga dentro il tetto del 15%. I valori sulla slide sono illustrativi.

**Concetti.**
- **Perché una matrice:** quando ogni posizione ha un punteggio per ogni specie, la scelta diventa un problema di ottimizzazione pulito: una specie per riga, massimizzare il totale, rispettare il tetto.
- **Punteggio di una specie in una posizione:** una combinazione pesata dell'ombra estiva che darebbe lì, del sole invernale che toglierebbe (un costo) e della pioggia che tratterrebbe. I pesi li sceglie il progettista (slide 16).
- **La priorità** (gruppo A) segnala alberi deboli o problematici come candidati, ma decide il progettista.
- La stessa specie ha punteggi diversi in posizioni diverse, perché edifici, orientamento della strada e larghezza del marciapiede cambiano il suo effetto.

### Slide 9. Regole della città
**Cosa dice.** La larghezza del marciapiede decide taglia e distanza degli alberi, e nessuna specie può superare il 15%.

**Concetti.**
- Dalla guida degli alberi stradali della città (Parcs i Jardins, *Gestió de l'arbrat viari*, 2011): marciapiede sotto 2,5 m, nessun albero; 2,5–3,5 m, albero piccolo; 3,5–6 m, medio; oltre 6 m, grande; distanza di circa 7, 9 e 13 m.
- **Come si misura la larghezza:** dalla mappa comunale 1:1000, una linea dalla facciata più vicina, attraverso l'albero, fino al cordolo. Funziona per circa il 55% degli alberi di Porta; gli alberi sugli spartitraffico o senza facciata vicina non vengono filtrati per taglia (ipotesi dichiarata).
- L'ottimizzatore **non viola mai** queste regole: una specie troppo grande per un marciapiede semplicemente non è ammessa in quella posizione.

### Slide 10. Dove vanno gli alberi nuovi
**Cosa dice.** Porta ha 267 spot candidati: 153 liberi, 103 condizionati, 11 bloccati.

**Concetti.**
- **Libero:** niente in mezzo. **Condizionato:** c'è di mezzo un cartello, un attraversamento, un lampione, un dissuasore o una fermata del bus; di solito un progetto può spostarlo, ma serve un sopralluogo e costa. **Bloccato:** semafori e passi carrabili, che un progetto stradale di norma non può spostare.
- Questa classificazione è stata decisa con te il 18 novembre e ricalcolata il 23.
- Gli spot candidati rispettano le stesse regole di distanza e taglia della slide 9.
- I sottoservizi (tubi, cavi) **non** sono ancora in queste classi, quindi gli spot liberi sono un limite superiore (slide 22).

### Slide 11. Una chioma è un secchio
**Cosa dice.** 1 mm di pioggia su 1 m² è 1 litro. Nella pioggia di 1 ora a 2 anni (31,9 mm) cadono circa 1.000 litri su una chioma tipica di Porta. Circa 125 litri restano sulle foglie (1,75 mm × LAI ≈ 4 mm); circa 875 litri arrivano a terra. Lo stesso albero trattiene la stessa acqua ovunque si trovi.

**Concetti.**
- **Perché 1.000 litri:** una chioma tipica copre circa 31 m²; 31 m² × 31,9 mm ≈ 1.000 L.
- **Capacità della chioma = s × LAI.** s = 1,75 mm per unità di LAI, calibrato su dati di campo di Anys & Weiler (2024), 16 tigli e aceri urbani. Con LAI ≈ 2,3 la capacità è circa 4 mm, cioè circa 125 L su una chioma di 31 m².
- **"Un secchio":** quando le foglie sono piene, tutto il resto cade giù. In un temporale forte il secchio si riempie presto, quindi la maggior parte dell'acqua arriva comunque a terra. Per questo l'intercettazione da sola non risolve gli allagamenti.
- **La frase chiave della slide:** la quantità trattenuta dipende dall'albero, non da dove si trova. La posizione conta solo per dove *sarebbe andata* l'acqua trattenuta (slide successiva).
- s è incerto: un valore più basso (0,83–0,86 mm) è provato nella slide 24.
- **Ponte verso la slide 12 (perché il metodo conta anche per il runoff):** tutte le specie trattengono acqua, ma alcune molto di più (chioma più grande, foglie più fitte); il metodo mette le specie che trattengono **più acqua** nelle posizioni la cui pioggia sta andando verso un hotspot di allagamento, così lì se ne accumula meno. Succede ogni volta che il runoff ha un peso nel punteggio.

### Slide 12. L'albero sulla collina
**Cosa dice.** Un albero a monte di un hotspot impedisce ai suoi circa 125 litri di arrivarci. Ma il 74% delle posizioni degli alberi di Porta non drena verso nessun hotspot: seguendo la pendenza del modello del terreno, la pioggia che cade lì scorre via (verso altre strade, verso i tombini, fuori dal quartiere) senza mai passare da un hotspot, quindi l'acqua trattenuta da quegli alberi non cambia nessun allagamento. 100 alberi messi dal metodo tengono lontana dagli hotspot 5,6 volte più acqua di 100 alberi messi a caso. Ma è solo lo 0,5% dell'acqua che arriva all'hotspot, quindi il runoff è un controllo do-no-harm.

**Concetti.**
- **I percorsi dell'acqua** sul modello del terreno dicono, per ogni posizione, se la sua acqua finisce in un hotspot. Solo quelle posizioni possono aiutare l'hotspot.
- **×5,6 contro 0,5%:** il metodo è molto meglio del caso nello scegliere *dove*, ma l'effetto totale è minuscolo rispetto all'acqua che riceve un hotspot. Sono vere tutte e due le cose; la seconda spiega perché il runoff non può essere l'obiettivo principale.
- Il modello conta solo i volumi (niente fognature, niente ristagni nel tempo): un altro motivo per dire "non peggiora" e non "risolto".

### Slide 13. Pratica della città, non una regola
**Cosa dice.** Il riferimento è quello che la città ha davvero piantato (2018–2026). Un nuovo albero della città su cinque è più grande di quanto il suo marciapiede permetta. Le stesse regole valgono sia per la pratica della città sia per il metodo. Togliendo una regola e ri-ottimizzando si vede quanto costa quella regola.

**Concetti.**
- **Perché la pratica e non la regola scritta:** la tabella scritta delle sostituzioni (2004/2005) a Porta in gran parte non è seguita. Confrontarsi con quello che succede davvero è più corretto e più utile.
- **S1b** nasce da 1.444 sostituzioni di platani nell'inventario: il mix di specie osservato, collocato con la regola del marciapiede. **S1a** (il mix annunciato in stampa) resta accanto come secondo riferimento.
- **"1 su 5 troppo grande"** (21% delle nuove piantagioni della città): la città stessa non sempre rispetta la sua regola sulle taglie. Il metodo la rispetta, quindi il confronto lo svantaggia, non lo avvantaggia.
- **Costo di una regola:** si fa girare l'ottimizzatore con e senza, per esempio, il tetto del 15%; la differenza di ombra è quanto costa la regola. Utile per un comune che discute le sue regole.

### Slide 14. Prime evidenze: back-test e co-benefici
**Cosa dice.** 26 gruppi in cui la città ha davvero sostituito alberi, stesse posizioni, scelta della città contro metodo. Ombra estiva mediana per albero: 59 m²·h per la città, 139 per il metodo. Il metodo dà più ombra in 22 gruppi su 26, e in 26 su 26 non manda più acqua verso i punti allagabili. Co-benefici a Porta (riportati, non ottimizzati, oggi = 100): carbonio stoccato a maturità 56 contro 42; carico di polline sotto quello di oggi in ogni sostituzione; portare la diversità da 6,2 a 9,4 specie effettive costa solo 0,3 punti di ombra estiva (pratica della città: 15,6).

**Concetti.**
- **Back-test:** si rigioca il passato. Si prendono le posizioni che la città ha davvero sostituito, si tengono fisse, e ci si chiede cosa avrebbe piantato lì il metodo. È il test più equo, perché posizioni e vincoli sono identici.
- **Perché il carbonio è sotto 100:** gli alberi di oggi sono grandi platani maturi; gli alberi nuovi, anche cresciuti alla dimensione attuale della loro specie, stoccano meno. Il metodo stocca comunque più della pratica della città. Il carbonio usa l'allometria di Jucker et al. (2017).
- **Polline:** i platani sono molto allergenici (indice di Cariñanos et al. 2014), quindi ogni sostituzione lo abbassa.
- **La diversità** era il punto debole: senza un minimo il metodo si concentra su poche specie molto ombreggianti. Un minimo di diversità (un numero effettivo minimo di specie) risolve gran parte del problema quasi senza perdere ombra. La città pianta comunque più varietà (15,6).
- **Se ti chiedono il risultato sulla città:** con 30 specie il metodo mantiene in mediana il 91,2% dell'ombra estiva di un platano, +6,7 punti sul mix annunciato e +14,7 sulla pratica, e vince in 32 quartieri su 32.

### Slide 15. Prossimi passi
**Cosa dice.** Tre prossimi passi. (1) Temperatura percepita (UTCI) con Ladybug e Infrared City, per verificare che più ombra voglia dire una strada più fresca. (2) I test di trasferimento: Mataró dà già 83% contro 63% di ombra estiva (6 strade su 6) e ora viene rifatto con le chiome vere dal LiDAR ICGC; poi Firenze (test previsto 29 nov – 3 dic). (3) Le planimetrie dei sottoservizi, per vedere quali spot sono davvero liberi (oggi gli spot liberi sono un limite superiore). Il talk chiude con un semplice "Thank you".

**Concetti.**
- **Dall'ombra all'UTCI:** l'ombra è un proxy. Ladybug Tools (in Grasshopper) e Infrared City calcolano la temperatura percepita, che conta anche le superfici calde e il vento. Questo verifica se più ombra vuol dire davvero una strada più confortevole.
- **Trasferimento:** Mataró prova una città diversa con dati e pratica propri; Firenze (LiDAR comunale 2023) è il prossimo caso.
- La foto è di Porta.

---

## Slide di backup (solo se te le chiedono)

### Slide 16. Nel tool: priorità e compromessi
**Cosa dice.** Il progettista clicca un punto su un triangolo i cui vertici sono ombra estiva, sole invernale e runoff; l'ottimizzatore ricalcola nel browser. Ogni layout compare come un punto su un grafico ombra estiva contro ombra invernale, accanto agli alberi di oggi, alla pratica della città e a una palette casuale.

**Concetti.**
- **Il triangolo fissa i pesi** del punteggio (slide 8). Un vertice vuol dire "solo questo obiettivo"; il centro vuol dire equilibrato.
- **Compromesso:** più ombra estiva di solito vuol dire anche più ombra invernale (più chioma, più ombra tutto l'anno). Le specie decidue con chioma estiva densa rompono in parte questa regola. Il grafico fa vedere al progettista cosa guadagna e cosa paga.
- Sul grafico i layout ottimizzati stanno a destra della pratica della città e degli alberi di oggi (più ombra estiva), e diversi stanno anche sotto quelli di oggi (meno ombra invernale).
- **Idea di Pareto:** un layout è "efficiente" se non puoi guadagnare su un asse senza perdere sull'altro.

### Slide 17. Metodo (versione semplice)
Quattro passi: analizzare ogni albero e ogni spot libero; il progettista sceglie un'azione per albero, con un motivo; un ottimizzatore esatto sceglie la specie per ogni posizione sostituita o aggiunta; confronto con oggi e con la pratica della città. Usala se il diagramma completo (slide 7) è troppo denso per rispondere a una domanda.

### Slide 18. Screening (versione semplice)
Tre domande per ogni posizione: cosa c'è (specie, classe del tronco, dimensione della chioma, densità delle foglie, un indizio di chioma debole), dove si trova (larghezza del marciapiede → taglia; lampioni, cartelli, attraversamenti; la pioggia va verso un punto allagabile?), e cosa farebbe lì ciascuna delle 30 specie (ombra estiva +, ombra invernale −, pioggia trattenuta +). È il volto semplice della slide 8.

### Slide 19. HiGHS: il solver che sceglie ogni specie
**Cosa dice.** Un esempio con cinque posizioni e tre specie. Regole: una specie per posizione; solo specie che stanno nel marciapiede; nessuna specie oltre il suo tetto (qui 2 su 5). Ogni layout che rispetta le regole è un punto dentro una forma; il migliore è un vertice; HiGHS trova il vertice più alto e dimostra che nessuno è più alto. Totale 3,3. Il metodo greedy (la migliore per ogni posizione, A, A, A, B, C) viola il tetto; i metodi per tentativi (genetici, colonia di formiche) rispettano le regole ma non sanno mai se hanno trovato il migliore. Porta: 832 posizioni × 30 specie in circa 0,2 s; la risposta è sempre in alberi interi.

**Concetti.**
- **Programmazione lineare:** massimizzare una somma di punteggi con vincoli lineari. I layout ammissibili formano un poliedro; l'ottimo sta sempre su un vertice. I metodi di tipo simplesso camminano da un vertice all'altro salendo.
- **Perché l'esattezza conta:** dà una risposta difendibile ("la migliore con queste regole"), riproducibile ogni volta, e permette di misurare esattamente il costo di una regola.
- **Alberi interi:** questo problema di assegnazione ha una struttura (un problema di trasporto) i cui vertici sono numeri interi, quindi nessun albero viene diviso in frazioni.
- Deciso il 9 novembre: niente algoritmi genetici né surrogati ML nella tesi; solo HiGHS.

### Slide 20. Perché Mataró
**Cosa dice.** Mataró verifica se il metodo funziona con altri dati e un'altra pratica. Ha un inventario completo degli alberi (specie e posizione di ogni albero, ricevuto a novembre 2026), lo stesso LiDAR ICGC di Porta (volo estivo con le foglie, stesso sistema di coordinate), una sua pioggia di progetto (PDCLAM, l'unica città finalista che ce l'ha), rischio di allagamento pluviale (uno dei 44 comuni catalani dell'ACA) e lo stesso clima con scelte di piantagione diverse. È a 25 km da Porta.

**Concetti.**
- **Perché non Badalona:** non ha una pioggia di progetto propria, quindi dovrebbe prendere in prestito quella di Barcellona, e il test diventerebbe circolare.
- **Test di trasferimento:** si rifà girare il metodo con le stesse regole e la stessa palette sui dati di un'altra città; se batte ancora la pratica, non è tarato solo su Porta.
- L'inventario di Mataró non ha una licenza che permetta di condividerlo, quindi resta fuori dal repository pubblico.

### Slide 21. Mataró: sei strade di platani
**Cosa dice.** Nelle sei strade con più platani, un progetto sostituisce tutti i platani. Ombra estiva mediana degli alberi nuovi, in % dei platani della stessa taglia: 83% metodo contro 63% pratica della città; il metodo vince in 6 strade su 6; il runoff non è mai peggiore di nessuna pratica. Primo giro, approssimato: chiome = mediane di Barcellona per specie (il LiDAR di Mataró è il prossimo passo), edifici da Overture Maps, terreno piatto, nessuna mappa degli hotspot. València (stretta) è il caso debole: 42% contro 35%.

**Concetti.**
- **% dei platani della stessa taglia:** l'ombra di ogni albero nuovo divisa per l'ombra di un platano con lo stesso tronco, quindi 100% = buono quanto un platano.
- **È un "what-if" in avanti, non un back-test:** Mataró ha una sola fotografia dell'inventario, quindi non ci sono sostituzioni passate da rigiocare.
- **Qui la "pratica della città" è quella di Barcellona** (S1b), applicata a Mataró. Contro le piantagioni recenti di Mataró il metodo vince con un margine maggiore (circa +33 punti).
- **València:** in una strada stretta poche specie stanno tra le facciate, quindi ogni opzione è piccola e il divario si riduce.

### Slide 22. Ipotesi dichiarate
**Cosa dice.** Cosa il metodo dà per assunto, e perché oggi è accettabile:
1. Alberi nuovi alla taglia degli alberi di oggi: ogni specie prende la chioma mediana che ha oggi a Barcellona (LiDAR). Crescita e ciclo di vita non sono modellati; nel tool c'è una vista a circa 10 anni.
2. Calore = ombra estiva, non temperatura percepita; l'UTCI è il prossimo passo.
3. Un solo tasso di intercettazione per tutte le specie (1,75 mm per unità di LAI); tassi specifici per specie non cambiano la classifica.
4. Gli spot liberi sono un limite superiore: non ci sono dati aperti sui sottoservizi; le sostituzioni riusano la buca esistente; gli spot condizionati richiedono un sopralluogo.
5. Tetto del 15% solo sugli alberi stradali; il piano conta anche le piazze; da rivedere prima dei risultati finali.
6. Un albero spostato esce dal sito: la sua posizione si libera o viene ripiantata; dove finisce è fuori dal tool.

**Concetti.**
- **Dichiarare le ipotesi** è ciò che rende affidabile un metodo computazionale: chi legge sa dove il risultato potrebbe cambiare.
- Ogni ipotesi o è testata (l'intercettazione nella slide 24) o ha un passo già previsto (UTCI, sottoservizi, tetto).
- **Chioma mediana a Barcellona:** usare la mediana cittadina per specie evita di confrontare un albero nuovo giovane con uno vecchio, il che sarebbe ingiusto per la specie nuova.

### Slide 23. Caso studio: Av. Rio de Janeiro, Porta
**Cosa dice.** 22 pioppi tolti nel 2022–24 e ripiantati tutti insieme nel 2025. Prima: 16 *Populus nigra* + 6 *Populus alba*, 167 m²·h di ombra estiva per albero. La città ha piantato: 22 *Fraxinus angustifolia* (frassino meridionale), 74 m²·h. Metodo: 14 *Gleditsia triacanthos* (spino di Giuda) + 8 *Firmiana simplex* (albero parasole cinese), 240 m²·h. Per albero, tolti · città · metodo: pioggia trattenuta in una pioggia a 2 anni 123 · 54 · 219 litri; ombra invernale 92 · 29 · 85 m²·h; runoff verso i punti allagabili: uguale.

**Concetti.**
- **Un progetto vero dall'inizio alla fine**, mostrato come lo vedrebbe il progettista.
- Il metodo dà più ombra estiva e trattiene più pioggia della scelta della città, e anche più dei pioppi che c'erano.
- **Il costo è l'ombra invernale:** 85 contro 29 dei frassini della città, anche se resta sotto il 92 dei pioppi. È il compromesso della slide 16 in una strada reale.
- Due specie invece di una: anche un piccolo guadagno di diversità in quella strada.

### Slide 24. Costi e robustezza
**Cosa dice.** Costi: sostituire fino a 500 € per albero (abbattimento, rimozione della ceppaia, messa a dimora di un albero da 16–18 cm; tetto del contributo provinciale, IVA inclusa); spostare 502–2.867 € per albero (trapiantatrice, zolla da 90 a 300 cm; costo diretto); allargare una buca da 1 a 1,5 m² circa 100 € (costo diretto). Metodo e pratica della città sostituiscono gli stessi alberi, quindi il metodo cambia la specie, non il numero di interventi. Robustezza: dando a 11 delle 30 specie il loro tasso di intercettazione, l'ombra estiva di Porta è il 103,4% di oggi in entrambi i casi, e il runoff verso i punti allagabili è −0,2% contro −0,3% della pratica della città; con un tasso più basso per i temporali brevi (0,86 o 0,83 mm invece di 1,75) le differenze tra layout si dimezzano ma mantengono il segno, tutte sotto l'1%. La classifica regge.

**Concetti.**
- **I costi vengono** dal catalogo 2024–2027 della Diputació de Barcelona (tetto per la sostituzione) e dal generatore di prezzi CYPE (spostamento, buca).
- **"Stessi interventi":** il costo in più del metodo rispetto alla pratica della città è quasi zero, perché cambia solo la specie. Spostare è l'azione cara, quindi il progettista dovrebbe usarla con parsimonia.
- **Analisi di sensibilità:** si cambia un dato incerto e si controlla se la conclusione cambia. Qui cambia la dimensione della differenza sul runoff, ma non il segno né la classifica.
- **103,4% di oggi:** il layout ottimizzato di Porta dà un po' più ombra estiva degli alberi di oggi.

### Slide 25 (solo copia privata). Sottoservizi
**Cosa dice.** Tubi e cavi sotto il marciapiede possono rendere impossibile una buca anche dove la superficie sembra libera. Le planimetrie dei sottoservizi sono state richieste per il canale ufficiale; sono arrivate quasi tutte le reti, manca quella dell'acqua.

**Concetti.** Le planimetrie sono riservate: non vanno mai mostrate né pubblicate. Serviranno solo a trasformare alcuni spot liberi in bloccati o condizionati. Fino ad allora gli spot liberi sono un limite superiore (slide 22).
