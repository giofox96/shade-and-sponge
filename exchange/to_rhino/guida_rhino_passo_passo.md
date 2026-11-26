# Kit Rhino per le slide finali: guida passo passo

**Obiettivo:** fare in Rhino le 3 visual segnate "RHINO" nel deck finale:
1. **Mappa di Porta**: le 832 posizioni dei platani, colorate per strada secondo quanta ombra estiva in più dà il metodo rispetto alla pratica della città.
2. **Aree del back-test**: uno o due gruppi di sostituzioni reali, chioma per chioma in 3D: prima, scelta della città, scelta del metodo.
3. **Strade prima e dopo**: la stessa strada con i platani di oggi (S0) e con gli alberi del metodo.

Non devi mandarmi niente indietro: le immagini vanno direttamente nelle slide.
Tempo: circa 1 ora la prima volta, poi 10 minuti per ogni immagine nuova.

**Numeri da usare nelle slide (PR #184, dopo la correzione degli "alberi ago"):**
- Porta, 832 platani sostituiti, ombra estiva rispetto a oggi: **città annunciata (S1a) 100,3%, pratica della città (S1b) 98,9%, metodo 106,7%**. Inverno: metodo 99% dell'ombra di oggi, pratica della città 109%. Deflusso: uguale.
- Back-test su 26 gruppi reali: il metodo dà più ombra estiva della città in **23 su 26**; ombra estiva aggiunta per albero (mediana): **città 76 m²h, metodo 130 m²h (1,7 volte)**; deflusso nei punti critici mai peggiore (26 su 26).

**Attenzione (importante):** i valori per albero e per strada nel kit sono il "potenziale" di ogni albero **da solo**, senza le sovrapposizioni tra chiome. Servono per **colorare e ordinare** le strade, non per scrivere percentuali. Per esempio, la somma per strada dà circa +30%, mentre il modello completo dà +7% (106,7 contro 98,9). Sulla mappa scrivi solo la legenda "meno → più ombra estiva rispetto alla pratica della città", senza numeri.

---

## PARTE A. Preparare la cartella (5 minuti)

1. Scompatta `rhino_kit_final.zip` in una cartella semplice, per esempio `C:\rhino_kit\`.
2. Controlla che dentro ci siano:
   - `porta\` con 6 file: `porta_crowns_planes.csv`, `porta_context_trees.csv`, `porta_streets_gain.csv`, `porta_buildings.geojson`, `porta_sidewalks.geojson`, `porta_boundary.csv`
   - `backtest\` con `backtest_groups.csv`, `backtest_crowns.csv` e la cartella `context\` (52 file, due per gruppo)
   - `gh\` con 3 script: `crowns.py`, `buildings.py`, `lines.py`
3. Tutte le coordinate sono in **metri locali**. Porta: EPSG:25831 meno l'origine (430800, 4586800), la stessa del kit Ladybug. Back-test: ogni gruppo ha la sua origine (colonne `origin_x`, `origin_y` in `backtest_groups.csv`), quindi ogni gruppo sta vicino a (0, 0). La quota Z è la quota assoluta del terreno (m s.l.m.).

---

## PARTE B. Aprire Rhino e Grasshopper (2 minuti)

1. Apri **Rhino 8**, template **Large Objects - Meters**.
2. Riga di comando: `Grasshopper`, Invio.

**Trucco per tutta la guida:** per aggiungere un componente, **doppio clic su uno spazio vuoto** del canvas, scrivi il nome (per esempio `Panel`) e premi Invio.

---

## PARTE C. I tre script (15 minuti, si fa una volta sola)

Ogni script si crea così:
1. Doppio clic sul canvas, scrivi `Python 3 Script`, Invio.
2. Zoom sul componente finché vedi **+** e **−** vicino a ingressi e uscite. Aggiungi o togli finché il numero è giusto.
3. Rinomina ingressi e uscite: **tasto destro sul nome**, clic sul nome, scrivi, Invio.
4. **Doppio clic sul componente**, cancella tutto, incolla il contenuto del file `.py` (aprilo con Blocco note), chiudi l'editor.
5. A ogni ingresso di testo collega un **Panel** con il testo scritto dentro (doppio clic sul canvas, `Panel`, poi doppio clic sul panel per scrivere).

### C1. Script `crowns` (chiome in 3D)
- File: `gh\crowns.py`
- Ingressi (5): `path`, `scenario`, `street`, `group`, `value`
- Uscite (5): `crowns`, `trunks`, `colors`, `values`, `species`
- Un ingresso lasciato **vuoto** vuol dire "tutti". Per lasciarlo vuoto, non collegare niente.

### C2. Script `buildings` (edifici estrusi)
- File: `gh\buildings.py`
- Ingressi (1): `path` · Uscite (2): `breps`, `heights`

### C3. Script `lines` (marciapiedi e confine)
- File: `gh\lines.py`
- Ingressi (2): `path`, `kind` · Uscite (2): `curves`, `kinds`
- `kind` può essere `facade` (linea delle facciate), `kerb` (cordolo) oppure vuoto (tutti e due).

**Se un componente diventa rosso:** passa il mouse sopra il pallino, leggi l'errore. Quasi sempre è un percorso sbagliato nel Panel. Usa il percorso completo, per esempio `C:\rhino_kit\porta\porta_crowns_planes.csv`.

---

## PARTE D. Visual 1: mappa di Porta (20 minuti)

### D1. Base della mappa
1. `lines` con `path` = `C:\rhino_kit\porta\porta_boundary.csv` → il confine di Porta.
2. Un secondo `lines` con `path` = `C:\rhino_kit\porta\porta_sidewalks.geojson` e `kind` = `facade` → il disegno delle strade.
3. (Facoltativo) `buildings` con `porta_buildings.geojson`: per la mappa in pianta basta il contorno; per una vista assonometrica usa gli edifici estrusi.

### D2. Le chiome colorate per strada
1. `crowns` con:
   - `path` = `C:\rhino_kit\porta\porta_crowns_planes.csv`
   - `scenario` = `method`
   - `value` = `street_gain_pct`
2. Aggiungi un componente **Gradient**. Collega `values` all'ingresso `t` del Gradient. Collega un **Number** o un Panel con `0` a `L0` e uno con `60` a `L1`. Scegli i colori del gradiente con il tasto destro (preset), oppure modifica i punti: chiaro = poco, verde scuro = molto.
3. Aggiungi **Custom Preview**: `crowns` in `Geometry`, l'uscita del Gradient in `Material`.
4. Spegni l'anteprima del componente `crowns` (tasto destro → Preview off), così vedi solo il Custom Preview.
5. (Facoltativo) Le altre chiome della zona, in grigio: secondo `crowns` con `path` = `porta_context_trees.csv` (nessun scenario) e Custom Preview con un colore grigio chiaro.

**Quale variabile colorare:**
- `street_gain_pct`: un solo colore per strada (consigliato per la slide).
- `tree_gain_m2h`: un colore per albero (più dettagliato, più "rumoroso").
- `scenario` = `S1b_city_practice` con `value` vuoto e i colori delle specie (uscita `colors` nel Material): le specie della città, da affiancare al metodo.

### D3. Etichette (facoltativo)
`porta_streets_gain.csv` ha una riga per strada: numero di platani, centro della strada (`x`, `y`), specie più frequente per città (`top_city`) e metodo (`top_method`). Se vuoi le etichette, scrivile a mano in Rhino o in PowerPoint: sono poche strade.

### D4. Esportare l'immagine
1. Vista **Top**, modalità di visualizzazione **Arctic** o **Rendered**, sfondo bianco.
2. Riga di comando: `ViewCaptureToFile`, larghezza 4000 px, spunta "Transparent background" se vuoi, salva PNG.

---

## PARTE E. Visual 2: aree del back-test (20 minuti)

### E1. Scegli il gruppo
Apri `backtest\backtest_groups.csv` in Excel. Consigliati (sono in Porta, quindi coerenti con il resto della presentazione):
- **6128**: 22 alberi, fine 2025. Prima *Populus nigra*; la città ha messo *Fraxinus angustifolia* (61% dell'ombra estiva dei pioppi tolti); il metodo avrebbe messo soprattutto *Celtis australis* (136%).
- **6503**: 13 alberi, 2026. Prima *Populus alba*; città *Casuarina* (58%); metodo *Celtis* (114%).
- **5762**: 11 alberi, 2025. Prima *Catalpa*; città *Handroanthus* (70%); metodo *Gleditsia* (127%).

### E2. Costruisci le tre versioni
1. `buildings` con `path` = `C:\rhino_kit\backtest\context\backtest_6128_buildings.geojson`.
2. `crowns` con `path` = `C:\rhino_kit\backtest\context\backtest_6128_context_trees.csv` → alberi intorno, grigi.
3. Tre componenti `crowns` con `path` = `C:\rhino_kit\backtest\backtest_crowns.csv`, `group` = `6128` e `scenario` rispettivamente `before`, `city`, `method`.
4. Per vederli affiancati: dopo ciascuno metti un **Move** con un vettore diverso (per esempio X = 0, 150, 300 con `Unit X` e un Number). Sposta allo stesso modo anche edifici e contesto (copiali tre volte), oppure fai tre immagini dalla stessa vista e accostale in PowerPoint (più semplice).
5. Colori delle chiome: uscita `colors` nel Material di un Custom Preview (colori delle specie, gli stessi della web app; le specie fuori palette sono grigie). In alternativa un colore fisso per scenario: grigio = prima, blu = città, verde = metodo.

### E3. Esportare
Vista **Perspective** a volo d'uccello, stessa camera per le tre immagini (salvala con `NamedView`), poi `ViewCaptureToFile`.

**Da sapere:** nel back-test tutti gli alberi (prima, città, metodo) sono confrontati **alla stessa taglia di tronco** (TERCERA), non come erano o come sono stati piantati. I diametri di chioma sono quelli del back-test; altezze e base della chioma seguono la stessa regola (colonna `height_source`).

---

## PARTE F. Visual 3: strade prima e dopo (10 minuti)

1. `buildings` con `porta_buildings.geojson` (tutta Porta; se è lento, va bene lo stesso: si fa una volta).
2. Due `crowns` con `path` = `porta_crowns_planes.csv` e lo stesso `street`, per esempio `Pg Andreu Nin`:
   - uno con `scenario` = `S0_today` (i platani di oggi, chiome misurate dal LiDAR 2021)
   - uno con `scenario` = `method`
   - (facoltativo) un terzo con `S1b_city_practice`
3. Accendi uno alla volta (tasto destro → Preview) e cattura la stessa vista per ciascuno.
4. Contesto: un `crowns` con `porta_context_trees.csv` e `street` uguale, oppure vuoto per tutta Porta.

**Strade consigliate** (in `porta_streets_gain.csv`): **Pg Andreu Nin** (80 platani, la stessa del test Ladybug), **Av Meridiana** (194, la più lunga), **Pg Valldaura** (39, guadagno alto). Scrivi il nome della strada **esattamente** come nel CSV, compreso `C\ ` per i carrer (per esempio `C\ Doctor Pi i Molist`).

---

## Colonne dei file

| File | Colonne principali |
|---|---|
| `porta_crowns_planes.csv` | `scenario` (S0_today, S1b_city_practice, method), `tree_id`, `street`, `x`, `y`, `ground_z`, `species`, `short`, `color`, `crown_diam_m`, `height_m`, `crown_base_m`, `shade_summer_m2h` (potenziale dell'albero da solo; vuoto per S0), `street_gain_pct`, `tree_gain_m2h` (metodo meno città, stesso punto) |
| `porta_streets_gain.csv` | `street`, `n_planes`, `shade_city_m2h`, `shade_method_m2h`, `gain_pct`, `x`, `y`, `top_city`, `top_method` |
| `porta_context_trees.csv` | tutti gli altri alberi di strada di Porta con chioma misurata (LiDAR 2021) |
| `backtest_groups.csv` | `group`, `barri`, `quarter`, `n`, `origin_x/y`, specie principali prima / città / metodo, `summer_pct_*` (% dell'ombra estiva degli alberi tolti), ombra aggiunta per albero, deflusso nei punti critici, `method_wins_summer` |
| `backtest_crowns.csv` | `group`, `scenario` (before, city, method), `x`, `y` (locali al gruppo), `ground_z`, `species`, `color`, `crown_diam_m`, `height_m`, `crown_base_m`, `height_source` |

**Fonti da citare sulla slide** (non i nostri file): ICGC, LiDAR 2021; Open Data BCN, arbrat viari 2018–2026; Ajuntament de Barcelona, cartografia 1:1000.

**Dati in "S1b":** è una delle 10 estrazioni della pratica della città (S1b_obs_0, 99,4% d'estate). Il numero da citare resta la mediana delle 10, 98,9%.

Lo script che rigenera il kit è `scripts/make_rhino_kit.py` nel repo.
