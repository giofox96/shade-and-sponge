# Cosa fa HiGHS in Shade and Sponge, spiegato con calma

Una spiegazione a sé stante del solver che sceglie le specie nel tool. Parte da esempi di tutti i giorni e arriva esattamente a quello che il nostro codice chiede a HiGHS. Leggila in ordine: ogni sezione usa la precedente.

---

## 1. La versione in una frase

HiGHS riceve una tabella di punteggi (quanto sarebbe buona ogni specie in ogni posizione) e una lista di regole (una specie per posizione, solo specie che ci stanno, nessuna specie oltre il suo tetto), e restituisce **l'assegnazione di specie alle posizioni con il punteggio totale più alto che non viola nessuna regola**, insieme alla garanzia che nessun'altra assegnazione fa di meglio.

HiGHS non sa niente di alberi, ombra o pioggia. Vede solo numeri e regole. Tutto ciò che riguarda gli alberi succede prima (lo screening che riempie la tabella dei punteggi) e dopo (la valutazione del layout che restituisce).

---

## 2. Un esempio banale: tre amici e tre pizze

Tre amici, Anna, Bruno e Carla, ordinano tre pizze diverse: margherita, diavola e quattro formaggi. Ognuno dà a ogni pizza un voto da 0 a 10:

| | Margherita | Diavola | Quattro formaggi |
|---|---|---|---|
| Anna | 9 | 6 | 3 |
| Bruno | 8 | 7 | 3 |
| Carla | 7 | 4 | 2 |

Regola: ognuno riceve esattamente una pizza, e ogni pizza va a una sola persona. Obiettivo: rendere il gruppo il più contento possibile, cioè massimizzare la somma dei voti.

**Prima idea, quella "golosa" (greedy):** ognuno prende la sua preferita. Anna prende la margherita (9), Bruno prende la margherita (8)… ma la margherita è una sola. L'idea golosa viola la regola.

**Seconda idea, golosa ma educata:** si va in ordine e ciascuno prende la pizza migliore ancora disponibile. Anna prende la margherita (9), Bruno la diavola (7), a Carla resta la quattro formaggi (2). Totale **18**.

**18 è il massimo?** Proviamo le altre. Ci sono solo 3 × 2 × 1 = 6 modi di dividere tre pizze tra tre persone:

| Anna | Bruno | Carla | Totale |
|---|---|---|---|
| Margherita 9 | Diavola 7 | Quattro formaggi 2 | 18 |
| Margherita 9 | Quattro formaggi 3 | Diavola 4 | 16 |
| Diavola 6 | Margherita 8 | Quattro formaggi 2 | 16 |
| Diavola 6 | Quattro formaggi 3 | Margherita 7 | 16 |
| Quattro formaggi 3 | Margherita 8 | Diavola 4 | 15 |
| Quattro formaggi 3 | Diavola 7 | Margherita 7 | 17 |

Qui il goloso educato vince: 18 è il massimo. Ma è stata fortuna, come mostra il prossimo esempio. E con tre persone potevamo controllare a mano tutte e sei le opzioni. Con tante persone diventa impossibile (sezione 4).

---

## 3. L'esempio della slide 19: cinque posizioni, tre specie

La stessa idea con gli alberi. Cinque posizioni lungo una strada, tre specie A, B e C. Ogni casella è il punteggio di quella specie in quella posizione (numeri inventati, come sulla slide). Una × vuol dire che la specie lì non ci sta: il marciapiede è troppo stretto per la sua taglia.

| Posizione | Marciapiede | A | B | C |
|---|---|---|---|---|
| 1 | largo | 0,9 | 0,6 | 0,3 |
| 2 | largo | 0,8 | 0,7 | 0,3 |
| 3 | largo | 0,7 | 0,4 | 0,2 |
| 4 | medio | × | 0,6 | 0,5 |
| 5 | stretto | × | × | 0,4 |

Regole:
1. Ogni posizione riceve **esattamente una** specie.
2. Solo specie che **ci stanno** (niente ×).
3. **Tetto**: nessuna specie su più di 2 delle 5 posizioni (a Porta il tetto è il 15%; qui 2 su 5 tiene piccolo l'esempio).

**Goloso maleducato** (la specie migliore ovunque): A, A, A, B, C = 0,9 + 0,8 + 0,7 + 0,6 + 0,4 = **3,4**. Sembra ottimo, ma A compare tre volte: **viola il tetto**. Non è ammesso.

**Goloso educato** (si va in ordine da 1 a 5 e si prende la specie migliore che ha ancora posto):
- posizione 1: A (0,9). A usata una volta.
- posizione 2: A (0,8). A usata due volte: A è piena.
- posizione 3: A è piena, quindi B (0,4).
- posizione 4: B (0,6). B è piena.
- posizione 5: C (0,4).
- Totale: 0,9 + 0,8 + 0,4 + 0,6 + 0,4 = **3,1**.

**La risposta di HiGHS:** A in 1 e 3, B in 2 e 4, C in 5 = 0,9 + 0,7 + 0,7 + 0,6 + 0,4 = **3,3**.

Perché 3,3 è meglio del 3,1 del goloso educato? Confronta la posizione 2 con la posizione 3:
- In posizione 2, A dà 0,8 e B dà 0,7: B **perde solo 0,1** rispetto ad A.
- In posizione 3, A dà 0,7 e B dà 0,4: B **perde 0,3** rispetto ad A.

Visto che A può andare solo in due posti, conviene metterla dove il suo **vantaggio** sull'alternativa è più grande, non semplicemente dove il suo punteggio è più alto. Il goloso guarda una posizione alla volta e non può accorgersene. HiGHS guarda tutto insieme. Questo è il senso di un ottimizzatore: **una risorsa limitata (il tetto) va spesa dove fa più differenza.**

Nei progetti veri queste differenze si sommano su centinaia di posizioni e 30 specie, ed è per questo che il metodo batte le scelte fatte un albero alla volta.

---

## 4. Perché non provare semplicemente tutte le combinazioni?

Con 5 posizioni e 3 specie le combinazioni sono 3⁵ = 243: un computer le controlla in un istante.

A Porta ci sono circa 832 posizioni e 30 specie. Le combinazioni sono 30⁸³². È un numero con **circa 1.229 cifre**. Per confronto, il numero di atomi nell'universo osservabile ha circa 80 cifre. Anche un computer che controllasse un miliardo di miliardi di combinazioni al secondo non finirebbe mai, né nell'età dell'universo né in un miliardo di età dell'universo.

Quindi "provare tutto" è impossibile. Esistono altre due famiglie di metodi:

- **Per tentativi (euristiche)**: algoritmi genetici, colonia di formiche, simulated annealing. Provano tante combinazioni promettenti, tengono le migliori, le mescolano, riprovano. Spesso trovano buone risposte, ma **non sanno mai se la risposta è la migliore**, e due esecuzioni possono dare due risposte diverse.
- **Ottimizzazione esatta**: metodi che sfruttano la struttura del problema per arrivare alla risposta migliore **senza** provare tutto, e **dimostrano** che è la migliore. HiGHS appartiene a questa famiglia.

Il nostro problema ha una struttura che rende facile l'ottimizzazione esatta: tutto è una somma di punteggi, e ogni regola è del tipo "il conteggio deve essere uguale a / al massimo". Si chiama problema **lineare**.

---

## 5. Cosa vuol dire "programmazione lineare", con un disegno

Dimentica gli alberi per un momento. Un problema minuscolo con solo due numeri da scegliere:
- x = quanti alberi di specie A piantiamo,
- y = quanti alberi di specie B.

Regole:
- al massimo 4 posizioni in tutto: x + y ≤ 4,
- tetto su A: x ≤ 2,
- tetto su B: y ≤ 3,
- niente alberi negativi: x ≥ 0, y ≥ 0.

Obiettivo: massimizzare 3x + 2y (ogni A vale 3 punti, ogni B 2).

Disegnalo su un foglio a quadretti, x in orizzontale e y in verticale. Ogni regola è una retta, e il lato ammesso è un semipiano. Insieme ritagliano una figura, un **poligono**, con questi vertici:

| Vertice | x | y | Punteggio 3x + 2y |
|---|---|---|---|
| (0, 0) | 0 | 0 | 0 |
| (2, 0) | 2 | 0 | 6 |
| (2, 2) | 2 | 2 | **10** |
| (1, 3) | 1 | 3 | 9 |
| (0, 3) | 0 | 3 | 6 |

Ogni punto dentro il poligono è una scelta ammessa. Ora immagina l'obiettivo come un righello appoggiato sul foglio: tutti i punti sulla retta 3x + 2y = 6 hanno punteggio 6, quelli su 3x + 2y = 9 hanno punteggio 9, e così via. Queste rette sono tutte parallele. Fai scorrere il righello nella direzione in cui il punteggio cresce. L'**ultimo** punto del poligono che tocca prima di uscirne è il migliore, e quel punto è sempre **un vertice** (qui (2, 2), punteggio 10).

Questo è il fatto chiave della programmazione lineare: **quando obiettivo e regole sono tutte rette, la risposta migliore sta sempre su un vertice della figura delle scelte ammesse.** Non è mai nascosta nel mezzo.

La slide 19 mostra proprio questo disegno: una figura grigia (tutti i layout che rispettano le regole), un vertice di "start", frecce che vanno da un vertice all'altro, e il vertice "best" in alto.

A Porta i numeri non sono 2 ma 832 × 30 ≈ 25.000. La "figura" vive in 25.000 dimensioni e non si può disegnare, ma la regola è la stessa: la risposta migliore è su un vertice.

---

## 6. Come HiGHS cammina fino al vertice migliore (l'idea del simplesso)

Sapere che la risposta sta su un vertice aiuta, ma una figura a 25.000 dimensioni ha un numero astronomico di vertici. HiGHS non li visita tutti. Il suo metodo principale, il **metodo del simplesso** (nella forma "duale rivista", la versione per cui HiGHS è noto), funziona come un escursionista nella nebbia che vuole arrivare in cima a una montagna:

1. Parte da un vertice qualsiasi (per esempio un layout banale ma ammesso).
2. Guarda gli spigoli che escono da quel vertice. Ce n'è uno lungo il quale il punteggio sale?
3. Se sì, lo percorre fino al vertice successivo.
4. Ripete.
5. Quando nessuno spigolo sale più, si ferma: è in cima.

In una catena montuosa potresti restare bloccato su una collinetta. **In un problema lineare no**: la figura è convessa (non ha rientranze), quindi un vertice da cui nessuno spigolo sale è il punto più alto in assoluto. Per questo la risposta è esatta, non solo buona.

Nell'esempio delle pizze un passo della camminata sarebbe: "scambiamo le pizze di Bruno e Carla: il totale sale?" Il simplesso è un modo molto furbo e molto veloce di scegliere quali scambi provare, così arriva in cima in pochi passi invece di provare tutto.

HiGHS ha anche un secondo metodo, il **metodo dei punti interni**, che invece di camminare lungo gli spigoli taglia dentro la figura verso il vertice migliore. Per un problema come il nostro non importa quale dei due gira: la risposta è lo stesso vertice. HiGHS sceglie da solo.

---

## 7. Come HiGHS dimostra che la risposta è la migliore

"Esatto" ha un significato preciso. Quando HiGHS si ferma, ha non solo un layout ma anche un **certificato**: un secondo insieme di numeri, uno per ogni regola, chiamati **valori duali** o **prezzi ombra**.

Un modo intuitivo per vederlo. Ogni regola riceve un "prezzo" che dice di quanto salirebbe il punteggio totale se quella regola fosse allentata di un'unità. Nell'esempio della slide 19:
- il tetto su A è attivo (A è usata due volte, il massimo). Se il tetto su A fosse 3 invece di 2, potremmo mettere A in posizione 2 al posto di B e guadagnare 0,8 − 0,7 = 0,1. Quindi il tetto su A "costa" 0,1 in quel punto.
- Il tetto su C non è attivo (C è usata una volta su 2). Permettere una C in più non farebbe guadagnare niente. Il suo prezzo è 0.

Con questi prezzi si può controllare, regola per regola, che nessun cambiamento del layout può aumentare il totale. È come uno scontrino che chiunque può ricontrollare senza rifare tutto il calcolo.

Questo si collega a un'idea della tesi: **"quanto costa ogni regola"** (slide 13). Nella tesi lo misuriamo direttamente, rifacendo girare l'ottimizzatore con e senza una regola (per esempio con e senza il tetto del 15%) e confrontando i totali. I prezzi ombra sono la stessa idea per un cambiamento di un'unità.

---

## 8. Perché la risposta è sempre in alberi interi

Un dubbio: nel disegno della sezione 5 il poligono contiene anche punti come (1,5; 2,3). HiGHS potrebbe rispondere "mezzo Celtis e mezza Tipuana in posizione 47"? Per gli alberi non avrebbe senso.

Nel nostro codice il numero che HiGHS sceglie per ogni posizione e specie, chiamiamolo x(i, j), in principio può stare ovunque tra 0 e 1. Ma il nostro problema ha una struttura speciale, chiamata **problema di trasporto**: posizioni da una parte, specie dall'altra, "ogni posizione riceve esattamente una" e "ogni specie viene mandata al massimo cap volte". I matematici hanno dimostrato da tempo che per questa struttura **ogni vertice della figura è fatto di numeri interi** (0 o 1). Siccome la risposta migliore sta su un vertice, è automaticamente in alberi interi, senza lavoro in più. Il commento nel nostro codice lo dice: "transportation LP, integral at a vertex".

Lo stesso vale quando aggiungiamo i tetti per quartiere (nelle simulazioni sull'intera città): i gruppi sono annidati dentro i totali per specie, quindi la struttura resta un flusso su rete e i vertici restano interi.

C'è un caso in cui questo non è più gratis: il **minimo di diversità** (sezione 11).

---

## 9. Cosa dà esattamente il nostro codice a HiGHS

La funzione è `assign` in `shade_sponge/layout.py`, che chiama HiGHS tramite SciPy (`scipy.optimize.linprog(method="highs")`). Nella web app lo stesso problema viene risolto nel browser con HiGHS compilato in WebAssembly.

**Le incognite.** Per ogni posizione i e ogni specie j, un numero x(i, j) tra 0 e 1: 1 vuol dire "la specie j va nella posizione i".

**L'obiettivo.** Massimizzare la somma di punteggio(i, j) × x(i, j) su tutte le posizioni e le specie.

**Le regole.**
1. *Una specie per posizione*: per ogni posizione i, la somma degli x(i, j) su tutte le specie è uguale a 1.
2. *Solo specie che ci stanno*: se la specie j non ci sta nella posizione i (troppo grande per il marciapiede, o urterebbe la facciata), x(i, j) è forzato a 0 dal suo limite superiore.
3. *Tetto per specie*: per ogni specie j, la somma degli x(i, j) su tutte le posizioni è al massimo cap(j). A Porta cap(j) viene dalla regola del 15%.
4. *(Solo nelle simulazioni sulla città)* anche i tetti per quartiere.

**Da dove vengono i punteggi.** Per ogni posizione e specie lo screening calcola tre "potenziali":
- ombra estiva (m²·h di ombra sul suolo aperto soleggiato nel giorno di progetto di luglio), da massimizzare;
- ombra invernale (lo stesso nel giorno di gennaio), da minimizzare perché d'inverno il sole è desiderato;
- pioggia trattenuta sopra il suolo che drena verso un hotspot di allagamento (m³ nella pioggia di progetto), da massimizzare.

Ogni potenziale viene diviso per il suo valore massimo, così tutti e tre vanno da 0 a 1 e si possono sommare. Poi:

punteggio = w₁ × ombra estiva − w₂ × ombra invernale + w₃ × pioggia trattenuta, più un minuscolo spareggio,

dove w₁, w₂ e w₃ sono i pesi che il progettista sceglie con il triangolo nel tool (slide 16), e la loro somma è 1. Lo spareggio (un millesimo della somma senza pesi) decide solo tra opzioni che altrimenti avrebbero esattamente lo stesso punteggio, per esempio nelle posizioni che non drenano verso nessun hotspot.

**La risposta.** Per ogni posizione, la specie con x = 1.

---

## 10. Lo sweep: tanti pesi, tante risposte

Il progettista non sempre sa quali sono i pesi giusti. Per questo il tool fa anche uno **sweep**: risolve il problema per ogni combinazione di pesi su una griglia con passo 0,25. Con tre obiettivi sono 15 combinazioni, da "solo ombra estiva" (1, 0, 0) passando per "equilibrato" fino a "solo pioggia" (0, 0, 1). Ognuna è una soluzione HiGHS separata, ognuna esatta per i suoi pesi.

Questi 15 layout sono i punti del grafico dei compromessi nella slide 16. Siccome ogni soluzione richiede una frazione di secondo, lo sweep intero è veloce, e nella web app un clic in qualsiasi punto del triangolo viene risolto al volo.

---

## 11. Il minimo di diversità: quando HiGHS deve lavorare di più

Senza nessuna regola sulla diversità, l'ottimizzatore tende a riempire ogni specie fino al suo tetto, partendo dalle migliori. Il risultato può avere poche specie. La tesi misura la diversità come **numero effettivo di specie**, exp(Shannon H). Il minimo di diversità dice: "il layout piantato deve avere almeno N specie effettive" (per esempio 9,4).

Due problemi:

1. **La formula di Shannon non è una retta.** Contiene un logaritmo, una curva. La programmazione lineare accetta solo rette. La soluzione nel nostro codice: la curva viene sostituita da tanti segmenti dritti corti che restano appena **sotto** di essa (un'approssimazione "lineare a tratti"). Siccome stanno sotto, se il layout supera il minimo con i segmenti, supera anche il minimo vero: l'approssimazione è prudente (`_entropy_chords` nel codice).

2. **I conteggi devono essere numeri interi.** La regola sulla diversità è scritta sul numero di alberi di ogni specie, n(j). Con la curva in gioco, i vertici della figura non sono più garantiti interi. Quindi i conteggi n(j) vengono dichiarati **interi**. Il problema diventa un problema **misto-intero** (MILP): alcune incognite devono essere intere, altre no.

HiGHS risolve i problemi interi con il **branch and bound** (ramifica e limita). L'idea, con un esempio banale: supponiamo che la risposta migliore del problema rilassato dica "pianta 4,6 Celtis". HiGHS divide il problema in due rami, uno con "Celtis ≤ 4" e uno con "Celtis ≥ 5", e risolve ognuno come un normale problema lineare. Se un ramo dà una risposta intera, quella è una candidata. Se il miglior punteggio possibile di un ramo è già peggiore di una candidata trovata prima, l'intero ramo viene scartato senza esplorarlo (questo è il "bound"). Continua finché nessun ramo può battere la candidata migliore. La risposta resta esatta, solo più lenta. Nel nostro codice sono interi solo i 30 conteggi per specie; i 25.000 valori x restano un problema di trasporto, quindi resta veloce.

Il risultato nella slide 14: il minimo porta la diversità da 6,2 a 9,4 specie effettive al costo di soli 0,3 punti di ombra estiva.

---

## 12. Cosa HiGHS NON fa (i limiti da dire ad alta voce)

- **Non calcola l'ombra né la pioggia.** Si fida completamente della tabella dei punteggi. Se un punteggio è sbagliato, il layout "migliore" è il migliore per numeri sbagliati. Per questo contano lo screening e le sue ipotesi (slide 22).
- **Tratta ogni posizione come indipendente.** L'ombra di un albero è calcolata come se fosse da solo (`no overlaps` nel codice). In realtà due chiome vicine possono ombreggiare lo stesso pezzo di suolo, quindi l'ombra totale è un po' più bassa della somma. Questo tiene il problema lineare ed esatto; la valutazione dopo la soluzione conta l'ombra reale, con le sovrapposizioni.
- **Non sceglie le azioni.** Keep, move, replace o add li decide il progettista. HiGHS riempie solo le posizioni segnate Replace o Add.
- **Non decide i pesi.** "Migliore" vuol dire sempre "migliore per questi pesi". Per questo il tool mostra lo sweep e il grafico dei compromessi invece di una sola risposta.
- **Non modella il tempo.** Gli alberi hanno la taglia che ogni specie ha oggi a Barcellona (mediana dal LiDAR), non crescono.

---

## 13. Perché HiGHS e non altro

- **Esatto e riproducibile**: lo stesso input dà sempre la stessa risposta, con una dimostrazione. Un revisore può rifarlo girare e ottenere lo stesso layout.
- **Veloce**: Porta, 832 posizioni × 30 specie, in circa 0,2 secondi.
- **Open source** (licenza MIT), sviluppato all'Università di Edimburgo, incluso in SciPy e disponibile in WebAssembly per il browser. Niente licenze da pagare, niente da installare per chi usa la web app.
- **Deciso il 9 novembre**: niente algoritmi genetici, niente colonia di formiche e niente surrogati di machine learning nella tesi. Il problema è lineare, quindi un'euristica aggiungerebbe solo incertezza sul fatto che la risposta sia la migliore.
- **Riferimento**: Huangfu, Q. e Hall, J. A. J. (2018) "Parallelizing the dual revised simplex method", *Mathematical Programming Computation*, 10, pp. 119–142. Il nome HiGHS non ha un'espansione ufficiale (highs.dev).

---

## 14. Spiegarlo in 30 secondi (se Angelos lo chiede)

In inglese, da dire così:

"For every position and every species, the screening gives a score: how much summer shade, winter sun and rain held that species would give there. HiGHS then picks one species per position so that the total score is the highest possible, without breaking the city's rules: only species that fit the sidewalk, and none above 15%. It does not try every combination, which would be impossible; it uses linear programming, which guarantees that the answer is the best one and proves it. Porta takes a fifth of a second."

In italiano, per capirlo tu: per ogni posizione e ogni specie lo screening dà un punteggio; HiGHS sceglie una specie per posizione in modo che il totale sia il più alto possibile senza violare le regole della città; non prova tutte le combinazioni, cosa impossibile, ma usa la programmazione lineare, che garantisce e dimostra che la risposta è la migliore; per Porta ci mette un quinto di secondo.
