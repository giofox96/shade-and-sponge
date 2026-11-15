# Reply to Serjoscha Duering (Infrared City), 11 Nov 2026 (draft, to send from Giovanni's inbox)

Answers Serjoscha's reply of 11 Nov and Angelos's note of 11 Nov (training a surrogate on Infrared City results is not allowed by their T&Cs) to `notes/email_infrared_city_reply.md` (sent 2 Nov). Numbers from:
Ladybug/Honeybee checks (memory note, slide 16 of the 10 Nov deck; `scripts/porous_utci.py`), Infrared run on Pg
Andreu Nin S0 (`databases/barcelona/infrared_utci_andreu_nin*.csv`, `scripts/infrared_utci_andreu_nin.py`, PR #111),
surrogate position as stated in the 10 Nov deck Q&A (`slides/outline_10nov.md`). Attachment:
`notes/figures/infrared_vs_honeybee_andreu_nin.png`.

---

**Subject:** Re: Request for Infrared City research access

Hi Serjoscha, hi Angelos,

Thank you, this is very helpful. Answers and an update below.

**1. Account.** I will create the account with giofox96@gmail.com today and write to you as soon as it is active.

**2. Transmissivity, height, crown.** Good news for the method: I will set a transmissivity per tree from its leaf area index (τ = exp(−0.5·LAI), the same porous-crown formula I use in Ladybug), plus height and crown diameter for every tree. For existing trees these come from the 2021 ICGC LiDAR; for new species from the trait table of the tool.

**3. Ladybug result on Passeig d'Andreu Nin (as promised).** 80 plane trees, 1,974 test points, mean UTCI 12–17 h on 15 July (El Prat TMYx 2011–2025):
- A Python re-implementation of the Ladybug chain matches Grasshopper (bias −0.02 °C, r = 0.998), so I can run it on all of Porta.
- Replacing the planes with the tool's layout changes mean UTCI by −0.19 °C with porous crowns (−0.15 °C in Honeybee). So, for heat, the tool's layout is no worse than today's planes within model uncertainty; the gains are elsewhere (runoff, diversity, winter sun).
- My shade proxy ranks points like Ladybug: r = −0.73 across points, −0.82 on the layout difference.
- First Infrared run on the same street, today's trees: mean 30.00 °C vs 30.81 °C in Honeybee with opaque crowns, point-by-point r = 0.88. Caveat: this run may sit one hour later than the Ladybug window (see the question below); I will rerun it. Infrared is cooler mainly under the crowns and along the west façade (see the attached map), which fits a lower default transmissivity. I will repeat it with the per-tree values from point 2.

One question on hours: is hour h in the API the interval that starts at h, i.e. EPW record h+1? In that case `start_hour=10, end_hour=15` reads the same EPW records as my Ladybug window 11–16 (12–17 local summer time).

**4. The surrogate.** Thank you, Angelos, understood: I will not train any model on Infrared City results. That fits the plan anyway, since a surrogate is not the focus of the thesis. Infrared City will only evaluate layouts:
1. per-tree runs (with tree minus without tree, as Serjoscha suggests) on a few sample streets, to check whether my shade proxy ranks the trees in the same order;
2. full runs to score the final layouts (today's trees, the city's own replacement mix, the tool's layout).
Any calibration of the proxy will be done against Ladybug, which is open. Thanks also for the note on wind: I will state that the per-tree effect is shade and radiation, not wind.

**5. Cost.** I will check every job with `preview_area` first and keep the runs to the sample streets and the final layouts.

I'll send you the per-tree results when I have them, and we can discuss the rest on Tuesday.

Best,
Giovanni
