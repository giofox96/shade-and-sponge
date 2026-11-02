# Reply to Angelos Chronis (cc Serjoscha Duering, Oana Taut): Infrared City account, surrogate, open source (draft, 1 Nov 2026)

Answers Angelos's three points from his reply to `notes/email_infrared_city.md` (sent 30 Oct). Sent by Giovanni on 2 Nov 2026 (with Tan & Liu 2026 attached); awaiting reply. Grounded in `shade_sponge/heat.py` (shade proxy), `shade_sponge/layout.py` (LP over positions × species, HiGHS), `notes/methodology.md` §6 (Tan & Liu 2026 as template), `notes/method_heat_validation.md` §6 (acceptance thresholds). The run counts repeat the first email's estimates (author's, not vendor-checked).

---

**Subject:** Re: Request for Infrared City research access

Dear Angelos, dear Serjoscha, dear Oana,

Thank you for the quick reply and for looping in the team.

**1. Account.** Yes, I already have an account, registered with my IAAC institutional email (giovanni.carlo.volpe@students.iaac.net). If it is better to have it under my personal email (giofox96@gmail.com), for example so that it stays active after the master ends, I can open a second one; just let me know which you prefer for the credits. I will check each job's cost with `preview_area` before running it.

**2. How the tool works now, and where a surrogate would come in.**

*Today.* For each district, the tool takes the plane trees due for replacement (832 in Porta, 31,580 across 28 districts in the city-wide run) and decides which species goes in each position. It does this as a linear program: every position and species pair gets a heat score and a runoff score, and the solver picks the best mix while respecting the city's rules (such as the 15% cap per species). The heat score is my own shade proxy: the shadow each crown casts on sunlit pavement between 12 and 17 h on a hot day, weighted by how much light the crown lets through (from its leaf area index). It runs in seconds for the whole city, and in 27 of the 28 districts it gives more summer shade than the city's own replacement mix.

*Its limit.* The proxy measures shade in m²·h, not thermal comfort. It does not see longwave radiation from hot walls and pavement, wind, or the sky view factor, so I cannot yet say how many °C of UTCI a layout gains, and I cannot be sure it ranks species correctly on every street.

*What Infrared City adds, in order of need:*
1. **Scoring the final layouts in UTCI** (today's trees, the city's mix, the tool's layout) on a sample of streets. This turns the result into °C and is the core use, about 160 runs.
2. **Calibrating the proxy.** On the same runs, I fit the proxy against the Infrared City UTCI change. If the two agree well (rank agreement Kendall τ ≥ 0.84, the value reported by Tan & Liu, 2026), a simple rescale of the proxy is enough, and no surrogate is needed.
3. **A surrogate, only if the calibration fails.** Then I would train a small regressor (random forest or gradient boosting, as in Tan & Liu, 2026) on up to about 500 runs. It would predict, for a tree of a given species at a given position, the UTCI change on the sidewalk around it, from the species traits (height, crown, leaf area index), the street geometry (orientation, height-to-width ratio, sky view factor) and the proxy value itself. Its output would replace the proxy score in the linear program, so the optimiser would work in °C directly across the whole city, which Infrared City alone cannot do at 31,580 positions × several species.

Either way, the linear program adds tree effects one by one, so overlapping crowns are not captured inside it. That is why the final layouts are always re-scored with full Infrared City runs and cross-checked with Ladybug on one street.

**Order of work.** Before spending any Infrared City credits, I will first run a Ladybug UTCI test this week on one street in Porta (Passeig d'Andreu Nin, 80 plane trees), to check my shade proxy against an accepted engine. I will share the result with you, and it will tell me which positions and layouts are worth sending to Infrared City first.

I attach the Tan & Liu (2026) paper, which is the closest precedent for step 3.

Joscha and Oana, I would be glad to have your view on this, in particular whether a tree in Infrared City carries a species-specific transmissivity, and whether a per-tree target like the one in step 3 makes sense with how the models work.

**3. Open access / open source.** Understood, and I am happy with it. The code (Python core, web app) is already public on GitHub: https://github.com/giofox96/shade-and-sponge (web app: https://giofox96.github.io/shade-and-sponge/). The code is under the MIT licence and the text and figures under CC BY 4.0, and the thesis will be released open access. One question so I plan it right: may I publish the Infrared City outputs used for training, and the trained surrogate itself, together with the code? If not, I would release the training scripts and the sampling design, so that anyone with an account can regenerate the data.

Thank you again, and I look forward to your thoughts.

Best regards,
Giovanni
