# Reply to Serjoscha Duering (Infrared City), 11 Nov 2026 (draft, to send from Giovanni's inbox)

Answers Serjoscha's reply of 11 Nov to `notes/email_infrared_city_reply.md` (sent 2 Nov). Numbers from:
Ladybug/Honeybee checks (memory note, slide 16 of the 10 Nov deck; `scripts/porous_utci.py`), Infrared run on Pg
Andreu Nin S0 (`databases/barcelona/infrared_utci_andreu_nin*.csv`, `scripts/infrared_utci_andreu_nin.py`, PR #111),
surrogate position as stated in the 10 Nov deck Q&A (`slides/outline_10nov.md`). Attachment:
`notes/figures/infrared_vs_honeybee_andreu_nin.png`.

---

**Subject:** Re: Request for Infrared City research access

Hi Serjoscha,

Thank you, this is very helpful. Answers and an update below.

**1. Account.** I will create the account with giofox96@gmail.com today and write to you as soon as it is active.

**2. Transmissivity, height, crown.** Good news for the method: I will set a transmissivity per tree from its leaf area index (τ = exp(−0.5·LAI), the same porous-crown formula I use in Ladybug), plus height and crown diameter for every tree. For existing trees these come from the 2021 ICGC LiDAR; for new species from the trait table of the tool.

**3. Ladybug result on Passeig d'Andreu Nin (as promised).** 80 plane trees, 1,974 test points, mean UTCI 12–17 h on 15 July (El Prat TMYx 2011–2025):
- A Python re-implementation of the Ladybug chain matches Grasshopper (bias −0.02 °C, r = 0.998), so I can run it on all of Porta.
- Replacing the planes with the tool's layout changes mean UTCI by −0.19 °C with porous crowns (−0.15 °C in Honeybee). So, for heat, the tool's layout is no worse than today's planes within model uncertainty; the gains are elsewhere (runoff, diversity, winter sun).
- My shade proxy ranks points like Ladybug: r = −0.73 across points, −0.82 on the layout difference.
- First Infrared run on the same street, today's trees: mean 30.00 °C vs 30.81 °C in Honeybee with opaque crowns, point-by-point r = 0.88. Infrared is cooler mainly under the crowns and along the west façade (see the attached map), which fits a lower default transmissivity. I will repeat it with the per-tree values from point 2.

One question: I assumed that an Infrared hour h covers the interval starting at h, so that my window 12–17 h corresponds to EPW records 13–17. Is that right?

**4. The surrogate: what I decided.** I will not train my own surrogate as a main step. Infrared City is already an ML surrogate of UTCI, and my shade proxy is fast and ranks positions like Ladybug. So the plan is:
1. per-tree runs (with tree minus without tree, as you suggest) on sample streets, to calibrate the proxy in °C;
2. full Infrared runs to re-score the final layouts (today's trees, the city's own replacement mix, the tool's layout);
3. my own surrogate only if the calibration fails (Kendall τ below 0.84, as in Tan & Liu 2026).
Thanks for the note on wind: I will state that the per-tree effect is shade and radiation, not wind.

**5. Cost.** I will check every job with `preview_area` first and keep the runs to the sample streets and the final layouts.

I'll send you the per-tree results when I have them.

Best,
Giovanni
