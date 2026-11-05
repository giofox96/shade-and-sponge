# Follow-ups from reading SylvCiT (user notes, 5 Nov 2026)

Source read: Nicol et al. 2026, SylvCiT (`papers/SylvCiT_-_An_AI-based_support_to_urban_forest_resi.pdf`).
Status of each item: TO CHECK = needs a verification before any work; PLANNED = agreed, after the 10 Nov session.
Order of work after 10 Nov (proposed 5 Nov, awaiting the user's ok): 1 → 2 → 3 → 4; 5–7 only as noted.

| # | Item (user's note) | Assessment | Status | First check |
|---|---|---|---|---|
| 1 | Use case on a real Barcelona project: take its area and show how the tool helps design the greening | Strongest item for the narrative; the tool already runs on any polygon | TO CHECK | Find an ongoing street/square project (ideally Nou Barris) with a published perimeter and planting brief |
| 2 | Documentation and use cases | Cheap, and the thesis is judged on the tool | PLANNED | Short user guide with 2–3 cases: one street rebuild, single plane replacements, a barri plan |
| 3 | Diversity indicators: Shannon, effective number of species (ENS), SylvCiT's x = n1/n0 − 1 | Already computed: `eff_species` = exp(Shannon) = ENS; x is the relative change of ENS. Report per barri, before/after, as a result, not an objective (diversity stays a constraint, decided 7 Oct) | PLANNED | Confirm the definition in `shade_sponge/layout.py` and SylvCiT's methods section |
| 4 | How does SylvCiT choose its top 10 species? | It ranks species by score gain after filtering (10-20-30 rule, invasive and pest-affected species out). The tool picks quantities by LP, but per-species gains exist: a per-site ranking is a cheap extra output (also for the web app) | TO CHECK | Re-read SylvCiT's ranking step; check which per-species potentials the tool already writes |
| 5 | Haase et al. (gap) and Lin et al. (field is moving) | For the gap chapter, not the tool | TO CHECK | Confirm both are in `papers/`/Zotero and what exactly they say before citing |
| 6 | Tree nurseries in Barcelona (point raised by Mathilde Marengo ~late Oct) | Only worth it as a filter if a public catalogue of available species exists; otherwise a declared limitation | TO CHECK | Ask the user what Mathilde said; search for a municipal/regional nursery catalogue |
| 7 | SylvCiT's future work: planting and maintenance costs, site preference (street/park), abiotic and biotic risks (flood, drought, disease, pests), method of Esperon-Rodriguez et al. (their ref. [71]) | Out of scope before December: a "future work" section that sits next to SylvCiT's own list | PLANNED (text only) | Read ref. [71] in SylvCiT's reference list to cite it correctly |
