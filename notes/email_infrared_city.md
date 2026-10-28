# Email to Angelos Chronis: Infrared City access request (v3, updated 28 Oct 2026)

Sources for the numbers below, all vendor-stated and read on 26 Oct 2026 (not independently verified): pricing page https://infrared.city/pricing; SDK 1.0 docs https://infrared.city/docs/sdk/1.0/; drift report https://github.com/Infrared-city/infrared-skills/issues/148 (it says the SDK docs and the SDK differ in places, so every limit is to be confirmed with the company). Problem paragraph (when and why planes are replaced): `notes/tree_master_plan.md` §3–§5 (plan text; the 2026 targets and several reasons are press only, Nació Digital 4 May 2026 and Betevé 7 May 2026; 2004/2005 table check in §5b); Porta numbers: `notes/topic_decision.md`. Added 28 Oct: the web-app status, and the fit with the INFRARED papers and the 2025 Riyadh app (sources: `notes/precedent_duering_tech.md`, a portfolio, so the author's own claims; `notes/lit/literature_matrix.csv` #144–#146, read in full). The pricing page says 10 tokens per standard analysis; the SDK docs say one billed job per 512 m tile. The estimates below are the author's: ~6 tiles for Porta, and the scenario and sensitivity counts are assumptions to check with `preview_area`.

**Subject:** Request for Infrared City research access: tree-species selection for urban heat (MaCAD thesis, Barcelona)

Dear Angelos,

As you suggested, here is what I would do with Infrared City, so you can forward it to the team. I am asking for free access for my thesis, until the final delivery on 18 Dec 2026.

**The problem.** Barcelona's tree master plan (*Arbres per viure*, 2017–2037) sets a target for 2037: no species above 15% of the city's trees. Plane trees (*Platanus*) are the only species above it, at about 27% of street trees (43,722 trees, May 2026). In May 2026 the city announced, according to the press, that it will cut the planes by 56%, to 12%, within ten years, i.e. by about 2036–2037. The replacement is gradual: planes are replaced as they die and during street works.

The city's reasons: the risk of a monoculture (one pest or disease can take a large share of the stock), the plane's known pests and diseases (plane lace bug, powdery mildew, bark canker), sudden leaf loss in summer under water stress, and, in the press, allergies, fruit nuisance and root damage to paving. The city also says planes suit today's climate less well (warmer, rain less frequent but harder, water that does not infiltrate the street). Planes stay on the large avenues and in emblematic places.

What the plan does not do is say which species replaces which tree, and where, or what that does to heat or runoff. The only per-street rule I found is a qualitative 2004/2005 table by district and sidewalk width, and Porta's recent plantings mostly do not follow it (up to about 90%, an upper bound). In Porta (Nou Barris, 0.84 km²) there are 832 planes (194 of them on Av. Meridiana, which the city may keep as a large avenue), which give about 29% of the neighbourhood's canopy cover (20.1%, against the city's 30% target). So the choice of species for each replaced plane is real and imminent, and today nothing quantifies its effect on heat or runoff.

**What I am building.** A Python tool that, for a site, proposes which species replace which tree, and where. It respects the city's own rules as hard constraints (such as the cap of 15% per species). The proposals are scored on two outcomes: outdoor thermal comfort in summer (mean UTCI, 12–17 h, hot design day) and stormwater runoff. The heat part inside the optimiser is a fast shade proxy that I wrote myself.

**Where the tool is today.** The core (Python) and a public web app already run for Porta: https://giofox96.github.io/shade-and-sponge/. It compares three layouts side by side (today's trees, the city's own replacement rule, and the optimised layout), for a project area drawn on the map, with replacement trees at planting size or at about 10 years. Runoff is computed with my own model. Heat is the part that still rests on my shade proxy, with Ladybug as the planned check, which is why the independent engine matters.

**What I would use Infrared City for**
1. **Reference for the heat results.** The proxy is fast but simplified, so I need an independent, accepted engine to score the baseline and the final layouts. Without it, my UTCI numbers are only as good as my own model.
2. **Validation of the proxy.** I compare Infrared City, my proxy and Ladybug on the same street and report the differences in the thesis.
3. **A transfer test.** The same workflow in a second city (Florence) and in a contrast site in Barcelona, to show that the method is not tied to one site.

**How it fits your own work.** The INFRARED papers (CAADRIA 2020, SimAUD 2020, CAADRIA 2022) optimise buildings and streets, and none of them models trees or runoff. My thesis adds the tree dimension (species, position, runoff) on top of that approach, and it follows the pattern of the 2025 Riyadh climate web app that combines the Infrared API with a trees layer. I cite the three papers in the literature chapter, and Infrared City would appear as the reference engine.

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
