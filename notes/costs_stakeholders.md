# Costs and stakeholders of the method (note for slides and chapter 8, 26 Nov 2026)

Answers the midterm feedback of 24 Nov (`notes/tutor_feedback_24nov.md`, points C1, S1–S3, W3, W4; §3c, §3d, §3h). Italian copy for Giovanni: project files `notes/costi_attori_it.{md,docx}`.
All prices are **direct costs** (no overhead, profit or VAT) copied from the cited source unless stated. Anything without a source is marked **GAP** or **ASSUMPTION**. No eWise or other confidential data. Numbers rounded to 2–3 significant figures. Fact-checked 26 Nov 2026.

## 1. Cost per action (keep, move, replace, add)

| Action | Items | Direct cost per tree | Sources |
|---|---|---|---|
| **Keep** | protection during works (movable fence 3.5×2 m, set-up and removal) | **~44 €** (43.55) | CYPE 0CB010 [Protección de árbol](https://generadordeprecios.info/espacios_urbanos/Actuaciones_previas/Protecciones_provisionales/Arbolado/Proteccion_de_arbol.html) |
| **Replace** | small tree: felling incl. stump and roots 27.23 + nursery tree 16–18 cm 66.70 + planting 51.33 + staking 42.63. Large tree (e.g. mature plane): plus large stump 884.67 | **~190 €** (small) – **~1,070 €** (large) | CYPE ADL015 (felling; page marked obsolete); Arenys de Mar 2024 (stump, planting, staking; BEDEC 2024 among others); CYPE deciduous tree. Detail: `/mnt/project-files/notes/budget_replacement_transplant.md` §2. Caveat: ADL015 covers 15–30 cm trunks and already includes the stump, so for a mature plane felling is underpriced and the large stump partly overlaps: the high value is an order of magnitude |
| | check: subsidy ceiling for a full small street-tree replacement, **incl. VAT** | **500 €** | Diputació de Barcelona, Catàleg 2024–2027, aid 305108 |
| **Add** (new pit on a free spot) | demolish 1 m² of sidewalk 4.73 + pit border 120×120 98.03 + tree 66.70 + planting 51.33 + staking 42.63 | **~260 €** | CYPE DMX050, MLA010 + Replace sources |
| **Move** (transplant) | tree spade (root ball 90 / 200 / 300 cm) + receiving pit (~200 €, Add items without the tree) | **~700 / ~1,650 / ~3,060 €** | CYPE JSP020 (502.41 / 1,450.93 / 2,867.03) |
| | mature planes (ball > 300 cm, crane and boxed ball) | **GAP** | no price found |
| **Conditional** spot (move an object) | dismantle sign 2.94 + new sign 75.67 (post excluded); dismantle street lamp ≤ 4 m 36.96 (foundation, cables and re-installation excluded) | sign **~80 € + post (GAP)**; lamp **GAP** | CYPE DTM030, TSV050, DUI030 |

For every action with a new tree:
- **Watering for 4 years** (160–180 L a week, Parcs i Jardins 2020 rule): **GAP**, likely the largest item after the tree.
- **Value of the lost tree** (Norma Granada, used by Barcelona for the works deposit): makes Keep and Move cheaper than the works sum alone suggests. Formula not read (**GAP**).

Plain reading: **keep ~44 €, add ~260 €, replace ~190–1,070 €, transplant a young tree ~700 €; a mature plane has no public transplant price and is risky** (survival: Struve et al. 2000; Watson 1985; see budget note §3).

## 2. Cost of the method vs city practice (Porta, S1c)

Case: the **513 planes that change** in Parcs i Jardins' real plan for Porta (S1c: 512 replacements, 110 of them plane for plane 'Vallis Clausa', plus 1 position removed) vs the method at the **same diversity** (9.7 effective species). Source: `databases/barcelona/tool_v0_summary_barcelona_div9.7_sizeexact_trunkTERCERA_replporta_plan_planes.csv` (method = S4 s0.50 w0.25 r0.25). Shade = effective shade (weighted by crown opacity) on sunlit open ground, sidewalk and street, 15 July, 12–17 h (6 hours); m²·h / 6 = mean shaded m² over the afternoon.

| | Today (S0) | City plan (S1c) | Method |
|---|---|---|---|
| Summer shade | 100% | 98.2% | **101.4%** |
| Winter shade (less = better) | 100% | 104.4% | **98.1%** |
| Runoff | 17,649 m³ | 17,651 m³ | 17,644 m³ (equal: below what the model resolves) |
| Trees planted on the 513 positions | — | 512 (+1 removed) | 513 |
| Direct cost | — | **~100,000–550,000 €** | **same** (one tree more) |

- **Gain over the city plan:** +11,700 m²·h, i.e. **~1,950 m² more shaded ground** (sidewalk and street) on average over the summer afternoon (~3.8 m² per replaced tree).
- **Cost of the gain:** same positions, same action (replace; the method also plants the position the plan removes), so the only difference is the nursery price between species (**GAP**). **Extra € per m² of shade gained over the city plan ≈ 0.**
- **€ per m² of shade vs today:** the method gains +5,080 m²·h (~850 m²) for ~100,000–550,000 € → **~110–650 €/m²**; the city plan loses shade (−6,640 m²·h) for the same spend.
- **€ per tree:** ~190–1,070 € direct (no watering); 500 € incl. VAT as the Diputació reference.

Real scale: one street project in Porta costs more than all these replacements. Santapau executive project, final approval 9 Oct 2025: **1,101,205.00 € incl. VAT**; Desfar, initial approval 16 Sep 2025: **557,352.07 €** (BOPB [3833557](https://bop.diba.cat/anuncio/ver-pdf/3833557), [3819788](https://bop.diba.cat/anuncio/ver-pdf/3819788)). The joint Santapau, Emili Roca and Desfar project is announced at **2.3 M€** (Nou Barris district news, 19 Jan 2026).

## 3. Impact statement: "with 10 M€"

**Slide sentence (Porta only, measured):** *If the 513 planes the city already plans to change in Porta followed the method instead of the plan: ~1,950 m² more shaded ground on summer afternoons, less winter shade, runoff no worse, same diversity, at the same cost (~100,000–550,000 € direct).*

**Order of magnitude on 10 M€ (extrapolation, ASSUMPTION):**
- 10 M€ / 1,070 € ≈ **9,300 replacements** (full cost with large stump, no watering). Same order as the **10,976 street-tree replacements the city made in 2018–2026** (observed inventory, thesis ch. 5).
- If each replacement gave Porta's mean gain (+22.9 m²·h per tree), 9,300 replacements would give **~35,000 m² (~3.5 ha) more shaded ground** on summer afternoons, **at no extra cost**: the method does not ask for more money, it chooses species and position better for trees the city replaces anyway.
- Limits to state: the per-tree gain is measured in Porta only (and the back-test, 23 wins of 26); it is **shade, not °C** (UTCI only where Ladybug/Infrared ran); runoff is a do-no-harm constraint, not a gain; watering and the lost tree's value are not priced.

## 4. Stakeholder map

| Role | Who | What they do | Source |
|---|---|---|---|
| **Pays and approves** | Ajuntament de Barcelona (Comissió de Govern) | approves the executive project and its budget | BOPB Santapau, 9 Oct 2025 |
| **Promotes** | District (Nou Barris) | announces and follows the works | district news, 19 Jan 2026 |
| **Manages the investment** | BIMSA (Barcelona d'Infraestructures Municipals SA) | "executa actuacions d'inversió per encàrrec de les diferents Àrees i Districtes"; **contracts the drafting of projects** | [BIMSA budget 2018](https://bcnroc.ajuntament.barcelona.cat/jspui/bitstream/11703/110703/4/Pressupost%20Barcelona%20Infraestructures%20Municipals%2c%20S.A._2018.pdf.txt), memòria (a 2017 forecast) |
| **Designs** (tool user) | commissioned firms (via BIMSA) or municipal technicians | draws the street section, pits, trees | same document; **which one for each project: to verify case by case** |
| **Decides the species and maintains** | Parcs i Jardins de Barcelona, Institut Municipal | administers the green infrastructure, conserves and maintains street trees, "vetllar per la qualitat de tots els projectes urbans que fan referència a zones verdes i/o arbrat"; species per pit (plan received 24 Nov); 15% cap; Norma Granada report and deposit during works | [Institut page](https://ajuntament.barcelona.cat/espaisverds/ca/institut/institut-municipal-de-parcs-i-jardins); *Protecció d'elements vegetals* (2017) |
| **Agronomists and botanists** | inside Parcs i Jardins | 21 "tècnic superior del verd o gestió" and 72 "tècnic/a mitjà/na del verd o gestió" of 919 staff (30 Nov 2022); call for **9 agricultural technicians** (2017 public employment offer) | [PiJ_Plantilla.pdf](https://ajuntament.barcelona.cat/espaisverds/sites/default/files/2024-08/PiJ_Plantilla.pdf); [call application form](https://apidocs.barcelona.cat/convocatoria_pro/doc/58878964/ParcsiJardins_Sol·licitudOposAgrícoles.pdf). How many hold agronomy or botany degrees: not verified |
| **Utilities** | water, sewer, electricity, gas, telecom companies | provide the affected-services plans (ACEFAT/eWise) | procedure used in the thesis; data confidential, not shown |
| **Citizens** | residents | comment during the public display (30 working days) | BOPB |

**Where the tool enters:** in **drafting the project** (the designer picks species and position per tree inside the city's rules) and as a **check for Parcs i Jardins** (same rules, numbers comparable with their practice). It does not replace the agronomists' judgement; it gives them the quantitative comparison that is missing today.

## 5. Contribution (slide sentence)

*No published tool picks the species and position of each tree, for heat and runoff together, inside a real city's planting rules* (prior-art funnel 18 → 7 → 1 → 0, `notes/lit/prior_art_matrix.csv`). *The method does, tests itself against what the city really planted, and measures what each city rule costs, at the same cost as the replacements the city already makes.*

## 6. Gaps (for the limits slide)
1. Price of 4 years of watering (Parcs i Jardins maintenance contract).
2. Barcelona BEDEC prices (ITeC licence) instead of CYPE and Arenys.
3. Transplanting mature planes (crane, boxed ball) and their survival.
4. Full relocation of a street lamp (foundation, cables, re-installation) and the sign post.
5. Nursery prices for all 30 palette species.
6. Who drafts each project (external firm or municipal technicians): verify project by project.
