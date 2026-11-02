# Ladybug test on Pg Andreu Nin: click-by-click guide

**Goal.** Compute UTCI (felt temperature) at 1,974 points along Pg Andreu Nin, 15 July, 12–17 h local time.
Run it twice: **S0** = today's 80 planes; **S4** = the tool's species on the same 80 spots. Then send me the two CSV files.

You need: Rhino 7 or 8, Grasshopper, Ladybug Tools 1.x (the "LB ..." components), and the kit folder.

The canvas you build has **7 boxes**. Your Grasshopper (GH) work is only the two Python boxes, which you copy and paste, plus five Ladybug boxes:

```
[folder panel] ─┐
[scenario panel]┼─> (1) LOAD ──context──┐
[step slider] ──┘          └──pts───────┼─> (3) LB Human to Sky Relation ─┐
(2) LB Import EPW ──location────────────┘                                 │
        │ ──dry bulb, radiation──> (4) LB Outdoor Solar MRT <─────────────┘
        │                                │ mrt
        └──dry bulb, RH, wind──> (5) LB UTCI Comfort
                                         │ utci
                       (6) LB Apply Analysis Period (15 Jul, 11–16)
                                         │
                                  (7) SAVE ──> CSV in exchange/from_gh
```

---

## Step 0: Prepare (5 min)

1. **Unzip** `ladybug_andreu_nin.zip` somewhere short, e.g. `C:\ladybug_andreu_nin\`. Inside you see `exchange\` and `weather\`.
2. **Open Rhino** and start a new model. The template doesn't matter.
3. **Set the units to metres.** Type `Units` in the command line, press Enter, and set *Model units = Meters*. Press OK.
4. **Open Grasshopper.** Type `Grasshopper` in the command line and press Enter.
5. **How to place a component** (you will do this 7 times): **double-click on an empty part of the canvas**, type the component name (e.g. `LB Import EPW`), and press Enter.
6. **How to connect:** drag from an output (the small half-circle on the **right** of a box) to an input (on the **left** of another box).
7. **How to read a value:** hover the mouse over any input or output and wait one second. A tooltip shows its name and data.

---

## Step 1: The LOAD component (reads all the geometry)

1. Double-click the canvas and type:
   - **Rhino 8:** `Python 3 Script`
   - **Rhino 7:** `GhPython Script`

   Then press Enter.
2. **Inputs.** The box has inputs `x` and `y`; you need three: `folder`, `scenario`, `step`.
   - Zoom in on the box (mouse wheel) until small **+** and **−** signs appear next to the inputs. Click **+** once to get a third input.
   - **Rename** each input: right-click its name > click the name field at the top of the menu > type the new name > Enter.
   - Use these names exactly, in this order: `folder`, `scenario`, `step`.
3. **Input settings.** Right-click each input:
   - `folder`: *Item Access* (the default). Then *Type hint* > `str`.
   - `scenario`: *Item Access*. Then *Type hint* > `str`.
   - `step`: *Item Access*. Then *Type hint* > `int`.
4. **Outputs.** Make three outputs, the same way (zoom in, **+**, rename): `context`, `pts`, `info`.
   - In Rhino 8 the default output is called `a`; rename it to `context`, then add two more.
   - In Rhino 7 the defaults are `out` and `a`. Leave `out`; rename `a` to `context`, then add `pts` and `info`.
5. **The code.** Double-click the box to open the editor.
   - Delete everything in it.
   - Open `exchange\gh_scripts\load_andreu_nin.py` in Notepad, select all (Ctrl+A), copy, and paste it into the editor.
   - Rhino 8: press the **Run/Play** button, then close the editor. Rhino 7: click **OK**.
6. **Feed the inputs:**
   - **folder:** double-click the canvas, type `Panel`, Enter. Double-click inside the panel and write the full path of the `to_gh` folder, e.g. `C:\ladybug_andreu_nin\exchange\to_gh`. Click outside the panel, then connect the panel to `folder`.
   - **scenario:** another Panel with the text `S0`, connected to `scenario`.
   - **step:** double-click the canvas, type `Number Slider`, Enter. Right-click the slider > *Edit*: Type = Integer, Min = 1, Max = 20, Value = **10**. Connect it to `step`.

     10 means "use every 10th point": about 200 points instead of 1,974. **First do a quick test with 10, then the real run with 1.**
7. **Check:** connect a Panel to the output `info`. It should say:

   `scenario S0: 30 buildings, 87 context crowns, 80 street crowns, 198 test points`

   (with step = 1: 1,974 test points).

   In the Rhino viewport (zoom extents: type `Zoom`, Enter, then `Extents`) you should see boxes (the buildings), ellipsoids (the trees) and points.
   - If the box turns **red**: hover over it and read the message. A wrong path is the usual cause: copy it from the Windows Explorer address bar.

---

## Step 2: Weather (LB Import EPW)

1. Place `LB Import EPW`.
2. Panel with the full path of the EPW file, e.g. `C:\ladybug_andreu_nin\weather\ESP_CT_Barcelona-El.Prat.AP.081810_TMYx.2011-2025.epw`. Connect it to `_epw_file`.
3. Nothing else to set. The outputs you use are `location`, `dry_bulb_temperature`, `relative_humidity`, `wind_speed`, `direct_normal_rad`, `diffuse_horizontal_rad`, `horizontal_infrared_rad`.

---

## Step 3: Which part of the body sees the sun (LB Human to Sky Relation)

1. Place `LB Human to Sky Relation`.
2. Connect:
   - `_location` ← `location` from LB Import EPW
   - `_position` ← `pts` from LOAD
   - `_context` ← `context` from LOAD
   - Leave the other inputs empty. If there is a `_run` input, connect a `Boolean Toggle` (double-click the canvas, type `Boolean Toggle`) and set it to **True**.
3. **This is the slow step.** With step = 10 it should take a few minutes; with step = 1 it can take much longer. Grasshopper freezes while it works: that's normal.
4. Outputs: `fract_body_exp` and `sky_exposure`.

---

## Step 4: Radiant temperature (LB Outdoor Solar MRT)

1. Place `LB Outdoor Solar MRT`.
2. Connect:
   - `_location` ← `location` (LB Import EPW)
   - `_surface_temp` ← `dry_bulb_temperature` (LB Import EPW)
   - `_dir_norm_rad` ← `direct_normal_rad`
   - `_diff_horiz_rad` ← `diffuse_horizontal_rad`
   - `_horiz_infrared` ← `horizontal_infrared_rad`
   - `fract_body_exp_` ← `fract_body_exp` (Human to Sky Relation)
   - `sky_exposure_` ← `sky_exposure` (Human to Sky Relation)
   - `_ground_ref_` ← a Panel with `0.25`
   - If there is a `_run` input: a Boolean Toggle set to **True**.
3. Output: `mrt`.

---

## Step 5: UTCI (LB UTCI Comfort)

1. Place `LB UTCI Comfort`.
2. Connect:
   - `_air_temp` ← `dry_bulb_temperature` (LB Import EPW)
   - `_mrt_` ← `mrt` (Outdoor Solar MRT)
   - `_rel_humid` ← `relative_humidity` (LB Import EPW)
   - `_wind_vel_` ← `wind_speed` (LB Import EPW)
   - If there is a `_run` input: a Boolean Toggle set to **True**.
3. Output: `utci`.

---

## Step 6: Keep only 15 July, 12–17 h (LB Analysis Period + LB Apply Analysis Period)

1. Place `LB Analysis Period`. Give it Panels (one per input):
   - `_start_month_` = `7`, `_start_day_` = `15`, `_start_hour_` = `11`
   - `_end_month_` = `7`, `_end_day_` = `15`, `_end_hour_` = `16`

   **Why 11–16:** the EPW is in winter time (UTC+1). 11–16 in the file = **12–17 h on the July clock**. This window was decided on 25 Oct.
2. Place `LB Apply Analysis Period`:
   - `_data` ← `utci` (UTCI Comfort)
   - `_analysis_period` ← `period` (Analysis Period)
3. Output: `data`. It holds 6 hourly values per point.
4. **Check:** connect a Panel to `data`. You should see numbers around 30–40 °C. In the sun they are higher; under the trees, lower.

---

## Step 7: The SAVE component (writes the CSV)

1. Make a second Python box, exactly as in Step 1, points 1–5, but:
   - **Inputs, in this order:** `folder`, `scenario`, `pts`, `utci`, `run`.
     - `folder` and `scenario`: *Item Access*, *Type hint* `str`.
     - `pts` and `utci`: right-click > **List Access**.
     - `run`: *Item Access*, *Type hint* `bool`.
   - **Output:** `info` (in Rhino 7 leave `out` and rename `a` to `info`).
   - **Code:** paste `exchange\gh_scripts\write_utci.py`.
2. Connect:
   - `folder` ← a Panel with the `from_gh` path, e.g. `C:\ladybug_andreu_nin\exchange\from_gh`
   - `scenario` ← the **same** scenario Panel as LOAD (the one with `S0`)
   - `pts` ← `pts` from LOAD
   - `utci` ← `data` from LB Apply Analysis Period. Then **right-click the `utci` input > Flatten**. A small arrow icon appears on it.
   - `run` ← a **Button** (double-click the canvas, type `Button`)
3. Panel on `info`. Click the Button once. The panel says `saved 198 points x 6 hours to ...\utci_S0_<date>.csv`.

   If it says `NOT SAVED ... Flatten`, step 2's Flatten is missing.

---

## Step 8: The real runs

1. **Quick test done (step = 10)?** You should now have a `utci_S0_...csv`.
2. Set the slider `step` to **1** and wait for everything to recompute. It's slow, so leave the PC alone. Click **SAVE**. This overwrites the S0 file of the same day with all 1,974 points.
3. Change the scenario Panel from `S0` to **`S4`**. Everything recomputes with the new trees. Click **SAVE** again: you get `utci_S4_<date>.csv`.
4. **Save the GH file** (File > Save As) into the `exchange\from_gh` folder. That way we know exactly what was run.
5. **Send me back the `from_gh` folder:** the two CSVs, plus the .gh if possible. Also send:
   - the Ladybug version (Grasshopper menu > Ladybug > About, or the LB Versioner component);
   - how long step 3 took.

I then compute the mean UTCI 12–17 h for S0 and S4, and the difference point by point.

---

## If something goes wrong
- **Red box:** hover it and read the message. Send me a screenshot of the canvas and of the message.
- **Orange box:** a warning, usually not blocking. Read it anyway.
- **An LB input has a different name** from this guide (Ladybug versions change): hover over the inputs, match them by meaning, or send me a screenshot.
- **Too slow:** keep step = 10 for both S0 and S4 and send me those. A first result with 200 points is already useful.

## Known limits of this first run (just note them)
- Crowns are **opaque**: species differ only by crown size and shape, not by leaf density.
- No cooling from transpiration: Ladybug probably underestimates the trees' effect.
- The weather is from El Prat airport, not from Porta.
- 15 July is an ASSUMPTION, the same as in the tool.
