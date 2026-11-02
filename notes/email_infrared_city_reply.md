# Reply to Angelos Chronis (cc Serjoscha Duering, Oana Taut): Infrared City account, surrogate, open source (draft, 1 Nov 2026)

Answers Angelos's three points from his reply to `notes/email_infrared_city.md` (sent 30 Oct). Not sent. Grounded in `shade_sponge/heat.py` (shade proxy), `shade_sponge/layout.py` (LP over positions × species, HiGHS), `notes/methodology.md` §6 (Tan & Liu 2026 as template), `notes/method_heat_validation.md` §6 (acceptance thresholds). The run counts repeat the first email's estimates (author's, not vendor-checked). Fill the [IAAC address] bracket before sending.

---

**Subject:** Re: Request for Infrared City research access

Dear Angelos, dear Serjoscha, dear Oana,

Thank you for the quick reply and for looping in the team.

**1. Account.** Yes, I already have an account, registered with my IAAC institutional email ([IAAC address]). If it is better to have it under my personal email (giofox96@gmail.com), for example so that it stays active after the master ends, I can open a second one; just let me know which you prefer for the credits. I will check each job's cost with `preview_area` before running it.

**2. The surrogate.** The aim is narrow: a model that predicts how much one tree of a given species, planted at a given street position, lowers pedestrian UTCI. My optimiser assigns replacement species to the existing plane-tree positions (832 in Porta, 31,580 across 28 districts in the city-wide run) as a linear program. It needs one number for every position and species pair, and today that number comes from my own shade proxy (crown shadow × canopy transmissivity from LAI). The surrogate would replace that number with one learned from Infrared City.

- **Target:** the change in mean UTCI over 12–17 h on a hot design day, at 1.1 m on the sidewalk cells around the tree, with the tree minus without it.
- **Inputs:** species traits (height, crown diameter, LAI, so transmissivity), street geometry (orientation, canyon height-to-width ratio, sky view factor) and the sun hours the position already gets from the buildings. My proxy value goes in too, so the surrogate learns a correction to it, not everything from scratch.
- **Model:** a gradient-boosted trees or random-forest regressor, following Tan & Liu (2026), who used a random-forest surrogate on 1,500 radiation and CFD runs to optimise the species and positions of 30 trees. Small, tabular and quick to retrain, so no deep network.
- **Training data:** Infrared City runs on street tiles sampled across Barcelona by orientation and width, each with planted layouts that vary species and spacing. About 160 runs for the core work, and up to about 500 if the credits allow, as in my first email.
- **Acceptance:** tested on held-out runs. Rank agreement with Infrared City of Kendall τ ≥ 0.84 (the value Tan & Liu report), and layout-to-layout differences within 0.3 °C, the smallest layout effect published (Hao et al., 2023). If it fails, I keep my proxy inside the optimiser and use Infrared City only to score the final layouts. Either way, the final layouts are scored with Infrared City and cross-checked with Ladybug on one street.

One limit I will state: the linear program adds tree effects one by one, so neighbouring crowns that overlap are not captured in the surrogate. That is why every final layout is re-scored with the full Infrared City run.

Joscha and Oana, I would be glad to have your view on this, in particular whether a tree in Infrared City carries a species-specific transmissivity, and whether a per-tree target like this one makes sense with how the models work.

**3. Open access / open source.** Understood, and I am happy with it. The code (Python core, web app) is in a GitHub repository that I will make public under an open licence at submission, and the thesis will be released open access. One question so I plan it right: may I publish the Infrared City outputs used for training, and the trained surrogate itself, together with the code? If not, I would release the training scripts and the sampling design, so that anyone with an account can regenerate the data.

Thank you again, and I look forward to your thoughts.

Best regards,
Giovanni
