# Email to Angelos Chronis: Infrared City access (draft, 26 Oct 2026)

Sources for the numbers below, all vendor-stated and read on 26 Oct 2026 (not independently verified): pricing page https://infrared.city/pricing; SDK 1.0 docs https://infrared.city/docs/sdk/1.0/; drift report https://github.com/Infrared-city/infrared-skills/issues/148 (it says the SDK docs and the SDK differ in places, so every limit is to be confirmed with the company).

**Subject:** Infrared City API access for my thesis (Porta, Barcelona): what I need and expected usage

Dear Angelos,

Thank you for offering to forward my request to Infrared City. Below is what I would use it for and how much I expect to consume, so they can judge it quickly.

**Thesis in one line.** A computational method that proposes which tree species replace the plane trees due for replacement, and where, in Porta (Nou Barris, Barcelona, 0.84 km²), scored on two outcomes: mean UTCI over 12–17 h on a hot design day, and pluvial runoff. The tool is written in Python; the heat part is currently a fast shade proxy, and Ladybug is my cross-check.

**What I would use Infrared City for**
1. **Validate my heat proxy.** Compare UTCI from Infrared City, Ladybug (my Tier 1) and my proxy on the same street, for the baseline and for one replacement. This is the first real UTCI number I need for the 10 Nov session.
2. **Score the final layouts** at district scale: baseline, the city's own replacement rule, and the optimised layouts (about 5 scenarios).
3. **Training data for a surrogate** (optional, only if the budget allows): a few hundred runs on one tile, so the optimiser can search species and positions without calling the API thousands of times.
4. **Transfer test** in a second city (Florence), and Sant Antoni (Barcelona) as a contrast site, with 2 scenarios each.

**Why Infrared City rather than only Ladybug.** In the literature I use, Ladybug costs 20–25 min per layout for 42 trees (Shaamala et al. 2025), and 10–20 s up to 2–3 h per 200 evaluations on a small site (Peng et al. 2026). A UTCI run in seconds is what makes layout comparison at district scale feasible within my deadline (final delivery 18 Dec).

**Expected consumption (my estimate, UTCI only, no wind analysis)**
I read in the SDK docs that a run is billed per 512 m tile, while the pricing page lists a standard analysis at 10 tokens, so I give both counts in jobs and let you or the company convert them. Porta needs about 6 tiles; a window of 12–17 h on one hot day is one run.

| Phase | Runs | Jobs (approx.) |
|---|---|---|
| Validation on one street, 3 scenarios × 3 weather files × a few canopy-transmissivity values | ~20 | 20 |
| Porta, 5 scenarios × 6 tiles × 3 weather sensitivities | 90 | 90 |
| Sant Antoni + Florence transfer (2 scenarios each) | ~18 | 18 |
| Margin for repeats (the docs say repeated runs are billed again) | | ~30 |
| **Core total** | | **~160** |
| Surrogate training set, one tile, ~300 layouts (optional) | 300 | 300 |
| Final check of the best ~10 layouts over 6 tiles | 60 | 60 |
| **Total with surrogate** | | **~520** |

At 10 tokens per job that is **about 1,600 tokens for the core and about 5,200 with the surrogate**. I will use `preview_area` before every run so nothing is billed unexpectedly. If the budget is smaller, I do the core only and train the surrogate on Ladybug instead.

**What I am asking**
- Free or academic access for the thesis period (until 18 Dec), sized as above; or, if that is not possible, the Free tier plus a top-up of about 4,000 tokens.
- API key for the Python SDK; I would also use the Grasshopper/Rhino plugin if it covers the same analysis.

**Three technical questions** (they decide how I model species)
1. **Trees.** The docs say a tree is a point with genus, height, crown diameter and a `canopy_transmissivity` (request-wide, with a per-tree override and a leaf-off value). Is that the right way to carry species-level differences? I plan to set transmissivity per species from LAI (τ = exp(−k·LAI)) and from the leaf-on calendar. Is evapotranspiration cooling modelled, or is the tree only a shade/radiation object?
2. **Limits.** Is there a rate limit or a cost reason not to submit a few hundred small runs on the same tile? Does a run with identical geometry and a different tree set re-bill in full?
3. **Validation.** Is there a published or internal validation of the UTCI/MRT output against ENVI-met or Ladybug, and which version of the model does the API currently run? I would cite it in the thesis.

I would be glad to share my results with the company afterwards (a Barcelona case with validation against Ladybug). I would ideally like an answer before the 10 Nov session, so I can show a first Infrared City number there.

Thank you very much,
[your name]
