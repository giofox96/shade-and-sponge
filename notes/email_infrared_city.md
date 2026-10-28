# Email to Angelos Chronis: Infrared City access request (v3, updated 28 Oct 2026)

Sources for the numbers below, all vendor-stated and read on 26 Oct 2026 (not independently verified): pricing page https://infrared.city/pricing; SDK 1.0 docs https://infrared.city/docs/sdk/1.0/; drift report https://github.com/Infrared-city/infrared-skills/issues/148 (it says the SDK docs and the SDK differ in places, so every limit is to be confirmed with the company). Problem paragraph (when and why planes are replaced): `notes/tree_master_plan.md` §3–§5 (plan text; the 2026 targets and several reasons are press only, Nació Digital 4 May 2026 and Betevé 7 May 2026; 2004/2005 table check in §5b); Porta numbers: `notes/topic_decision.md`. Added 28 Oct: the web-app status, and the fit with the INFRARED papers and the 2025 Riyadh app (sources: `notes/precedent_duering_tech.md`, a portfolio, so the author's own claims; `notes/lit/literature_matrix.csv` #144–#146, read in full). The pricing page says 10 tokens per standard analysis; the SDK docs say one billed job per 512 m tile. The estimates below are the author's: ~6 tiles for Porta, and the scenario and sensitivity counts are assumptions to check with `preview_area`.

**Subject:** Request for Infrared City research access: tree-species selection for urban heat (MaCAD thesis, Barcelona)

Dear Angelos,

As you suggested, here is what I would do with Infrared City, so you can forward it to the team. I am asking for free access for my thesis, until the final delivery on 18 Dec 2026.

**The problem.** Barcelona's tree master plan (2017–2037) targets no species above 15% of the city's trees by 2037. Plane trees are the only one above it, at about 27% of street trees. According to the press (May 2026), the city will cut them by 56%, to 12%, within ten years, gradually: as they die and during street works. The reasons are monoculture risk, the plane's pests and diseases, and its poor fit with a warmer climate. The plan does not say which species replaces which tree, or what that does to heat or runoff. In Porta (Nou Barris, 0.84 km²) there are 832 planes, about 29% of the neighbourhood's canopy.

**What I am building.** A Python tool that proposes which species replace which tree, and where, within the city's own rules (such as the 15% cap). Proposals are scored on summer thermal comfort (mean UTCI, 12–17 h, hot design day) and on stormwater runoff. A public web app already runs for Porta (https://giofox96.github.io/shade-and-sponge/). Runoff uses my own model. Heat rests on a fast shade proxy of mine, which is why I need an independent engine.

**What I would use Infrared City for**
1. **Reference UTCI** for the current trees and the final layouts.
2. **Validation of my proxy**, against Infrared City and Ladybug on the same street.
3. **A transfer test** in Florence and in a contrast site in Barcelona.

I would use the Python SDK (and the Grasshopper plugin, if it covers the same analysis). Trees would go in as points with genus, height, crown diameter and canopy transmissivity (set per species from leaf area index, with a leaf-off value).

**Expected usage.** About 160 runs for the core work (roughly 1,600 tokens by my estimate), and up to about 500 runs (roughly 5,000 tokens) if I can train a surrogate for the optimiser. I will check the cost with `preview_area` before every run.

**Three questions**, because they change how I model species:
1. Is a tree only a shade/radiation object, or is evapotranspiration modelled? Is genus plus transmissivity the right way to carry species differences?
2. Is there any limit, or any reason not to submit a few hundred runs on the same tile?
3. Is there a published or internal validation against ENVI-met or Ladybug that I can cite?

I would be grateful for an answer before my tutor session on 10 Nov, where I would like to show a first Infrared City result. I will credit Infrared City in the thesis and can share the Barcelona results and the validation with the team.

Thank you,
[your name]
