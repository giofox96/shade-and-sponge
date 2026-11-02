# Ladybug su Pg Andreu Nin: guida passo passo

**Obiettivo:** ottenere l'UTCI medio dalle 12 alle 17 del 15 luglio su 1.974 punti lungo Pg Andreu Nin. Fai due calcoli:
- **S0:** i platani di oggi.
- **S4:** gli alberi scelti dal tool.

Alla fine mi mandi 2 file CSV.
Tempo: circa 1 ora la prima volta.

---

## PARTE A. Preparare la cartella (5 minuti)

1. Scompatta lo zip in una cartella semplice, per esempio `C:\ladybug_test\`.
2. Copia **tutti i file** dentro un'unica cartella, per esempio `C:\ladybug_test\dati\`, cioè:
   - i 5 file `street_andreu-nin_...`;
   - il file meteo `.epw`.
3. Controlla che in `C:\ladybug_test\dati\` ci siano questi 6 file:
   - `street_andreu-nin_buildings_20261031.geojson`
   - `street_andreu-nin_context_trees_20261031.csv`
   - `street_andreu-nin_testpoints_20261031.csv`
   - `street_andreu-nin_trees_S0_current_20261031.csv`
   - `street_andreu-nin_trees_S4_s1.00_w0.00_r0.00_20261031.csv`
   - un file che finisce in `.epw` (El Prat)

---

## PARTE B. Aprire Rhino e Grasshopper (2 minuti)

1. Apri **Rhino 8** e scegli il template **Large Objects - Meters**. Le unità devono essere **metri**.
2. Nella riga di comando di Rhino scrivi `Grasshopper` e premi Invio. Si apre la finestra di Grasshopper.
3. Controlla che Ladybug sia installato: in alto, tra le schede di Grasshopper, deve esserci la scheda **Ladybug**. Se non c'è, installa Ladybug Tools (food4rhino o il Package Manager di Rhino 8) e riavvia Rhino.

**Trucco per tutta la guida:** per aggiungere un componente, fai **doppio clic su uno spazio vuoto** del canvas di Grasshopper, scrivi il nome del componente (per esempio `LB Import EPW`) e premi Invio.

---

## PARTE C. Caricare la geometria con UN solo script (15 minuti)

### C1. Crea il componente script
1. Doppio clic sul canvas e scrivi `Python 3 Script`. Invio.
2. Si crea un componente con due ingressi a sinistra (`x`, `y`) e un'uscita a destra (`a`).

### C2. Imposta gli ingressi (a sinistra)
Gli ingressi devono essere 3: `folder`, `scenario`, `every`.
1. Fai **zoom** sul componente finché vedi i segni **+** e **−** vicino agli ingressi.
2. Clicca **+** finché gli ingressi sono 3.
3. Rinomina ogni ingresso: **tasto destro sul nome**, poi clicca sul nome nel menu, scrivi il nuovo nome e premi Invio.
   - primo ingresso: `folder`
   - secondo ingresso: `scenario`
   - terzo ingresso: `every`

### C3. Imposta le uscite (a destra)
Le uscite devono essere 3: `context`, `pts`, `info`.
- Con lo stesso metodo (zoom, +, tasto destro, rinomina) crea 3 uscite e rinominale `context`, `pts`, `info`.
- Se c'è un'uscita `out` o `stdout`, lasciala com'è: mostra gli errori.

### C4. Incolla il codice
1. **Doppio clic sul componente.** Si apre l'editor.
2. Cancella tutto quello che c'è dentro e incolla questo:

```python
import csv, json, os
import Rhino.Geometry as rg

def crown(r):
    h, hb = float(r["height_m"]), float(r["crown_base_m"])
    d, z0 = float(r["crown_diam_m"]), float(r["ground_z"])
    c = rg.Point3d(float(r["x"]), float(r["y"]), z0 + (h + hb) / 2.0)
    s = rg.Sphere(rg.Point3d.Origin, 1.0).ToBrep()
    s.Transform(rg.Transform.Scale(rg.Plane.WorldXY, d / 2.0, d / 2.0, max(h - hb, 1.0) / 2.0))
    s.Transform(rg.Transform.Translation(rg.Vector3d(c)))
    return s

f = lambda name: os.path.join(folder, name)
every = int(every) if every else 1

# buildings
buildings = []
gj = json.load(open(f("street_andreu-nin_buildings_20261031.geojson"), encoding="utf-8"))
for ft in gj["features"]:
    g, p = ft["geometry"], ft["properties"]
    polys = [g["coordinates"]] if g["type"] == "Polygon" else g["coordinates"]
    for poly in polys:
        z0 = p["ground_z"]
        crv = rg.PolylineCurve([rg.Point3d(q[0], q[1], z0) for q in poly[0]])
        if crv.ClosedCurveOrientation(rg.Vector3d.ZAxis) == rg.CurveOrientation.Clockwise:
            crv.Reverse()                      # so the extrusion goes up
        ext = rg.Extrusion.Create(crv, p["height_m"], True)
        if ext:
            buildings.append(ext.ToBrep())

# trees around the street (the same in both runs)
others = [crown(r) for r in csv.DictReader(open(f("street_andreu-nin_context_trees_20261031.csv"), encoding="utf-8"))
          if r["flag"] == "ok" and r["crown_base_m"]]

# street trees: S0 = today, S4 = tool layout
name = "street_andreu-nin_trees_S0_current_20261031.csv" if scenario == "S0" else \
       "street_andreu-nin_trees_S4_s1.00_w0.00_r0.00_20261031.csv"
street = [crown(r) for r in csv.DictReader(open(f(name), encoding="utf-8"))]

# test points (every = 1 all points; 20 = one in twenty, for a quick test)
rows = list(csv.DictReader(open(f("street_andreu-nin_testpoints_20261031.csv"), encoding="utf-8")))
pts = [rg.Point3d(float(r["x"]), float(r["y"]), float(r["z"])) for r in rows[::every]]

context = buildings + others + street
info = "scenario {}: {} buildings, {} context crowns, {} street crowns, {} points".format(
    scenario, len(buildings), len(others), len(street), len(pts))
```
3. Chiudi l'editor e conferma il salvataggio, se te lo chiede.

### C5. Collega i valori agli ingressi
Usa un **Panel** per ogni valore: doppio clic sul canvas, scrivi `Panel`, Invio. Per scrivere dentro un Panel fai doppio clic sul Panel.
1. **Panel 1:** scrivi `C:\ladybug_test\dati`, cioè la tua cartella, senza `\` finale. Collega l'uscita del Panel all'ingresso `folder`: trascina dal pallino destro del Panel al pallino di `folder`.
2. **Panel 2:** scrivi `S0` e collegalo a `scenario`.
3. **Panel 3:** scrivi `20` e collegalo a `every`. Per ora usiamo un punto su venti, così il primo giro è veloce.

### C6. Controlla che funzioni
1. Crea un altro **Panel** e collegalo all'uscita `info`. Deve mostrare:
   `scenario S0: 30 buildings, 87 context crowns, 80 street crowns, 99 points` (99 punti perché `every` = 20).
2. Se il componente diventa **rosso**, passa il mouse sopra il pallino rosso oppure collega un Panel all'uscita `out`: lì c'è l'errore. Mandamene uno screenshot.
3. Nella vista di Rhino devi vedere edifici e chiome in anteprima. Se non vedi niente, scrivi `Zoom` → `Extents` (comando `ZE`).

---

## PARTE D. Il meteo (10 minuti)

1. **`LB Import EPW`** (doppio clic, scrivi, Invio).
   - Crea un **Panel** con il percorso completo del file .epw, per esempio `C:\ladybug_test\dati\ESP_CT_Barcelona-El.Prat...epw`. Il nome esatto lo copi da Esplora file: tasto destro sul file, "Copia come percorso", poi togli le virgolette.
   - Collega il Panel all'ingresso `_epw_file`.
2. **`LB Analysis Period`**. Dagli questi 6 numeri: crea uno **Panel** (o un **Number Slider**) per ciascuno e collegalo all'ingresso con lo stesso nome.

   | Ingresso | Valore |
   |---|---|
   | `_start_month_` | 7 |
   | `_start_day_` | 15 |
   | `_start_hour_` | 11 |
   | `_end_month_` | 7 |
   | `_end_day_` | 15 |
   | `_end_hour_` | 16 |

   Le ore 11–16 del file EPW sono le **12–17 ora locale** (il file è in ora solare).
3. **`LB Apply Analysis Period`**: ne servono **6**. Ne crei uno e poi lo copi con Ctrl+C / Ctrl+V. In ognuno:
   - `_data` = una delle uscite di LB Import EPW: `dry_bulb_temperature`, `relative_humidity`, `wind_speed`, `direct_normal_rad`, `diffuse_horizontal_rad`, `horizontal_infrared_rad`;
   - `_period` = l'uscita `period` di LB Analysis Period (la stessa per tutti e 6).

   Mettili in colonna e annota accanto a ciascuno (con un Panel) quale dato filtra, così non ti confondi.

---

## PARTE E. Il calcolo (15 minuti più l'attesa)

1. **`LB Human to Sky Relation`**:
   - `_location` ← uscita `location` di LB Import EPW
   - `_position` ← uscita `pts` dello script
   - `_context` ← uscita `context` dello script
   - `_run` ← un **Boolean Toggle** (doppio clic, scrivi `Boolean Toggle`), messo su **True**

   È il passo più lento. Con `every` = 20 dovrebbe metterci poco.
2. **`LB Outdoor Solar MRT`**:
   - `_location` ← `location`
   - `_surface_temp` ← temperatura filtrata (dry bulb)
   - `_dir_norm_rad` ← direct normal filtrata
   - `_diff_horiz_rad` ← diffuse horizontal filtrata
   - `_horiz_infrared` ← horizontal infrared filtrata
   - `_fract_body_exp_` ← uscita `fract_body_exp` di Human to Sky
   - `_sky_exposure_` ← uscita `sky_exposure` di Human to Sky
   - `_ground_ref_` ← un Panel con `0.25`
   - `_run`, se c'è ← Boolean Toggle True
3. **`LB UTCI Comfort`**:
   - `_air_temp` ← temperatura filtrata
   - `_mrt_` ← uscita `mrt` di Outdoor Solar MRT
   - `_rel_humid` ← umidità filtrata
   - `_wind_vel_` ← vento filtrato

   L'uscita che ci serve è `utci`.

I nomi degli ingressi possono cambiare un po' tra versioni di Ladybug, per esempio con un trattino basso in più o in meno. Collega per significato e, se qualcosa non torna, mandami uno screenshot.

---

## PARTE F. Salvare il risultato e vedere la media (10 minuti)

### F1. Secondo script
1. Crea un nuovo **`Python 3 Script`**.
2. Imposta 5 ingressi: `folder`, `scenario`, `pts`, `utci`, `run`.
3. **Molto importante:** per `pts` e `utci` fai tasto destro sull'ingresso e scegli **List Access**. Gli altri restano **Item Access**.
4. Imposta un'uscita: `mean`.
5. Incolla questo codice:

```python
import csv, os
vals = []
rows = []
for i, (p, dc) in enumerate(zip(pts, utci)):
    for dt, v in zip(dc.datetimes, dc.values):
        vals.append(float(v))
        rows.append([scenario, str(dt), i, round(p.X, 2), round(p.Y, 2), round(p.Z, 2), round(float(v), 3)])
mean = "mean UTCI {:.2f} C over {} values ({} points)".format(sum(vals) / len(vals), len(vals), len(pts)) if vals else "no values"
if run:
    out = os.path.join(folder, "from_gh")
    if not os.path.isdir(out):
        os.makedirs(out)
    with open(os.path.join(out, "utci_{}.csv".format(scenario)), "w") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(["scenario", "hour", "point_id", "x", "y", "z", "utci_C"])
        w.writerows(rows)
```

### F2. Collega il secondo script
- `folder` ← lo stesso Panel della cartella (Panel 1)
- `scenario` ← lo stesso Panel `S0` (Panel 2)
- `pts` ← uscita `pts` del primo script
- `utci` ← uscita `utci` di LB UTCI Comfort
- `run` ← un **Boolean Toggle** nuovo, per ora su **False**
- l'uscita `mean` ← un Panel. Deve mostrare qualcosa come `mean UTCI 3x.xx C over ... values`. Ogni punto ha **6 valori**, uno per ora.

---

## PARTE G. Il calcolo vero (S0, poi S4)

1. Nel Panel 3 (`every`) scrivi **`1`**: tutti i 1.974 punti. Aspetta che Ladybug finisca: può volerci parecchio, e Grasshopper sembra bloccato ma sta lavorando.
2. Metti il Toggle `run` del secondo script su **True**, poi di nuovo su **False**. Si crea `C:\ladybug_test\dati\from_gh\utci_S0.csv`.
3. Nel Panel 2 cambia `S0` in **`S4`**. Grasshopper ricalcola tutto con gli alberi del tool.
4. Quando ha finito, Toggle `run` su **True** e poi **False**. Si crea `utci_S4.csv`.
5. Annota i due valori `mean` (S0 e S4).

---

## PARTE H. Mandami

- i due file `from_gh\utci_S0.csv` e `from_gh\utci_S4.csv`;
- i due valori `mean`;
- la versione di Ladybug, che trovi in `LB Versioner` (doppio clic, scrivi, l'uscita mostra la versione), e quanto è durato il calcolo.

Io calcolo la differenza S4 − S0 punto per punto e la confronto con il proxy d'ombra del tool.

**Limite di questo primo giro:** le chiome sono solide, cioè non lasciano passare il sole. Va bene così: è scritto come limite noto.
