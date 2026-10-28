# Precedent scan: duering.tech (Serjoscha Duering, CTO of Infrared City), 28 Oct 2026

**Source:** https://duering.tech/, read from its project data (`/data/projects.json`, `/data/publications.json`) on 28 Oct 2026.

**Read level:** portfolio descriptions written by the author. They are not peer-reviewed, and the numbers in them are the author's claims.

**Relevance:**
- Duering is also IAAC faculty ("AI in Urbanism", since Feb 2020).
- Infrared City is the heat engine planned for this thesis (CLAUDE.md, "Heat engine").

## Projects relevant to this thesis

| Project (year) | What it does (author's description) | Relevance |
|---|---|---|
| **Custom Climate Design Webapp** (2025; with A. Chronis, J. Bunge, A. Markopoulou, E. Naboni) | Project-specific planning app for a Riyadh corridor, built in 10 days for the ISOCARP AI Masterclass. It combines infrared.city (microclimate) and GUS ("trees-as-infrastructure"). Features: Year 1 vs Year 10 twin timelines, parallel climate simulations, "Chat with trees", RAG answers, and design tools for planting, shading and surfaces with live cost tracking. Stack: React, deck.gl, Mapbox, n8n, Infrared API, GUS API | Closest practice precedent (ch. 4.4). No runoff and no species/position optimisation are described |
| **infrared.city** (2020–) | ML surrogates trained on CFD results, for real-time wind and solar simulation ("8 hours per CFD run → under a second") | The surrogate idea behind our fast proxy |
| **Performance Driven Design** (portfolio says SimAUD 2020; probably the same work as #145, *Optimizing Urban Systems*; the collaborators listed differ) | Multi-objective design optimisation on real-time simulation (microclimate, wind, solar, accessibility, retail), with trade-offs explored interactively | Precedent for the trade-off front (ch. 4.3) |
| **Environmental Performance Assessment** (CAADRIA 2022, #146) | 5,000 tower massing variants scored on 7 KPIs as counted in the paper body (facade sun counted once per tower; the published abstract says six); dashboard of trade-offs | Design-space exploration with fast simulation |
| **Urban Design Comparison Dashboard** (2025) | One column per scenario (maps, charts, KPIs) side by side; a 4th column for consolidated views or AI summaries; AI personas score the scenarios | UI pattern for S0 / S1a / Opt / R / A / R+A |
| **Urban Renewal Uzbekistan** (2019, World Bank) | 10 interventions simulated, combined into packages under a budget, then ranked with KPI scoring and transparent reasoning | "Ranked packages" framing for R / A / R+A |
| **Frankfurt High-Rise Plan** (2021) | Workshop tool with instant CFD and shading feedback for architects | Workshop use of fast feedback (the computational-designer persona) |
| **rhino-mcp**, **Grasshopper + n8n**, **Grasshopper live bridge** (2025) | Claude and agents read and drive Grasshopper canvases | Could replace the CSV exchange. Conflicts with the project rule "Claude never opens Rhino" (CLAUDE.md), so not adopted |

**The three papers were read in full on 28 Oct** (`papers/`; matrix #144–#146). The portfolio's venues were wrong for two of them:

| Paper | Venue (from the PDF) | The portfolio said |
|---|---|---|
| Chronis, Aichinger, Duering, Galanos, Fink, Vesely & Koenig, *INFRARED: An Intelligent Framework for Resilient Design* (#144) | **CAADRIA 2020**, Paper 179, preprint | SimAUD 2022 |
| Duering, Chronis & Koenig, *Optimizing Urban Systems* (#145) | **SimAUD 2020**, Vienna, pp. 503–509; confirmed by #146's reference list | eCAADe 2020 |
| Duering, Fink, Chronis & Koenig, *Environmental Performance Assessment: The Optimisation of High-Rises in Vienna* (#146) | POST-CARBON, Proc. 27th CAADRIA 2022, pp. 545–554, doi:10.52842/conf.caadria.2022.1.545 (AIT record; the PDF read is a pre-camera-ready draft) | CAADRIA 2022, as stated. The portfolio adds Khean and Galanos as authors; the AIT record has the 4 authors of the PDF |

**What they show:**
- ML surrogates (Ladybug/OpenFOAM training data, predictions in under 100 ms) make multi-objective optimisation and 5,000-variant exploration feasible in Grasshopper.
- **None of the three models trees or vegetation in its microclimate predictions.** #144 has green space only as an area parameter and ratio. The decision variables are buildings and streets.
- **None has runoff;** the InFraReD paper names rainfall and rainwater as future metrics (pp. 7, 9).
- The InFraReD paper does not validate its models ("not in the scope of this paper"). The 80–95% accuracy against CFD is cited in #146 from Kabosová et al. 2021 and Galanos et al. 2019. #146's §2.2 attributes 5,000–15,000× to #144 and #145, which do not contain that number.

They are now used in chapter 4 (heat models, Table 4.1, and a fourth group of optimisers for building form).

## What to take, in order of value for the thesis

1. **Time horizon: Year 1 vs Year 10.** This is our open "young/mature horizon" (`shade_sponge/README.md`, "Next"). Chapter 5 already says that equal trunk size is not a forecast. A "planting → 10 years → mature" switch, scoring each layout with crowns by size class, would answer the transition question: today, a young replacement loses about 37% of the street-tree runoff benefit (methodology §4b). It needs crown growth per species, which we don't have yet (`ASSUMPTION`, or the inventory's trunk classes as stages).
2. **Side-by-side scenario columns** in the web app: S0 | city rule | optimised, then R / A / R+A. This is a better fit for the municipal-planner persona than one layout at a time, and the data are already exported.
3. **Present R / A / R+A as ranked packages** with explicit reasoning, as in the Uzbekistan project. This is a framing change only, in ch. 7 and the slides.
4. **The INFRARED / SimAUD / CAADRIA papers are cited** in ch. 4 (done 28 Oct). Use them, not the portfolio, for any technical claim.
5. **Infrared API access:** these projects show that the API is used in custom web apps. Mention that in the email to the tutor (to-do item 5).

## What not to take

- **AI personas and "chat with trees":** they score or answer from an LLM, not from a model, so they would weaken the validation argument. Out of scope.
- **Live cost tracking:** there are no Barcelona per-tree cost data in the repo. Add it only if a sourced cost table turns up.
