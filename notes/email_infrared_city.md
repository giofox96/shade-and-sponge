# Email to Angelos Chronis: Infrared City access request (v2, 26 Oct 2026)

Sources for the numbers below, all vendor-stated and read on 26 Oct 2026 (not independently verified): pricing page https://infrared.city/pricing; SDK 1.0 docs https://infrared.city/docs/sdk/1.0/; drift report https://github.com/Infrared-city/infrared-skills/issues/148 (it says the SDK docs and the SDK differ in places, so every limit is to be confirmed with the company). The pricing page says 10 tokens per standard analysis; the SDK docs say one billed job per 512 m tile. The estimates below are the author's: ~6 tiles for Porta, and the scenario and sensitivity counts are assumptions to check with `preview_area`.

**Subject:** Request for Infrared City research access: tree-species selection for urban heat (MaCAD thesis, Barcelona)

Dear Angelos,

As you suggested, here is what I would do with Infrared City, so you can forward it to the team. I am asking for free access for my thesis, until the final delivery on 18 Dec 2026.

**The problem.** Barcelona's tree master plan decides how many trees of each species the city plants, but not which species goes where, and it quantifies neither heat nor runoff. In Porta (Nou Barris, 0.84 km²), planes are due for replacement, so the choice of species is real and imminent.

**What I am building.** A Python tool that, for a site, proposes which species replace which tree, and where. It respects the city's own rules as hard constraints (such as the cap of 15% per species). The proposals are scored on two outcomes: outdoor thermal comfort in summer (mean UTCI, 12–17 h, hot design day) and stormwater runoff. The heat part inside the optimiser is a fast shade proxy that I wrote myself.

**What I would use Infrared City for**
1. **Reference for the heat results.** The proxy is fast but simplified, so I need an independent, accepted engine to score the baseline and the final layouts. Without it, my UTCI numbers are only as good as my own model.
2. **Validation of the proxy.** I compare Infrared City, my proxy and Ladybug on the same street and report the differences in the thesis.
3. **A transfer test.** The same workflow in a second city (Florence) and in a contrast site in Barcelona, to show that the method is not tied to one site.

**Why it matters for the thesis.** The thesis is judged on a computational workflow and its validation. A UTCI run that takes seconds, instead of the 20–25 minutes per layout reported for Ladybug in the literature (Shaamala et al. 2025), makes it possible to compare layouts at district scale in the time I have. Without it I can only compare a handful of layouts, on one street.

**How I would use it.** Through the Python SDK (and the Grasshopper plugin, if it covers the same analysis). Trees would go in as points with genus, height, crown diameter and canopy transmissivity (set per species from leaf area index, with a leaf-off value).

**Expected usage.** About 160 runs for the core work (roughly 1,600 tokens by my estimate, 10 tokens per run). If the budget allows, up to about 500 runs in total (roughly 5,000 tokens), to train a surrogate for the optimiser. I will check the cost with `preview_area` before every run, and I will not run anything larger than I need.

**Three questions**, because they change how I model species:
1. Is a tree only a shade/radiation object, or is evapotranspiration modelled? Is genus plus transmissivity the right way to carry species differences?
2. Is there any limit, or any reason not to submit a few hundred runs on the same tile?
3. Is there a published or internal validation against ENVI-met or Ladybug that I can cite?

**Timing.** I would be very grateful for an answer before my tutor session on 10 Nov, where I would like to show a first Infrared City result.

In return, I will credit Infrared City in the thesis, and I can share the Barcelona results and the validation against Ladybug with the team.

Thank you,
[your name]
