"""Infographics for the 20 Oct talk (literature review + method): 1600x900 SVG (editable) + PNG (Google Slides).

Numbers come from notes/lit/literature_matrix.csv, notes/lit/species_measurements.csv,
databases/traits/porta_trait_table.csv and notes/methodology.md; every figure prints its sources.
"*" = assessed from the abstract only. PNG export uses headless Edge/Chrome (no extra Python packages).
Output: slides/fig/*.svg, slides/fig/*.png. File numbers are the SLIDE numbers of slides/outline_20oct.md
(so 01, 04, 14 and 15 have no figure here: they use a photo or a notes/figures plot).
"""
import csv, os, re, shutil, subprocess, tempfile, pathlib, textwrap
from xml.sax.saxutils import escape
import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "slides/fig"
W, H = 1600, 900
INK, MUTED, GRID, BG = "#1F2933", "#6B7280", "#E5E7EB", "#FFFFFF"
HEAT, RAIN, TREE, WARN = "#D9622B", "#2F6DB5", "#3B7F4A", "#B7791F"
FONT = "Arial, Helvetica, sans-serif"


# ---- SVG helpers
def t(x, y, s, size=20, fill=INK, weight="normal", anchor="start", italic=False, halo=False):
    it = ' font-style="italic"' if italic else ""
    it += f' stroke="{BG}" stroke-width="5" paint-order="stroke"' if halo else ""
    return f'<text x="{x:.0f}" y="{y:.0f}" font-size="{size}" fill="{fill}" font-weight="{weight}" text-anchor="{anchor}"{it}>{escape(s)}</text>'


def para(x, y, s, width, size=18, lh=1.3, **k):
    """Wrapped text (Arial ~0.5 em per character); returns (svg, height)."""
    lines = textwrap.wrap(s, max(8, int(width / (0.5 * size))))
    return "".join(t(x, y + i * size * lh, ln, size, **k) for i, ln in enumerate(lines)), len(lines) * size * lh


def rect(x, y, w, h, fill, rx=8, op=1.0, stroke="none"):
    return f'<rect x="{x:.0f}" y="{y:.0f}" width="{w:.0f}" height="{h:.0f}" rx="{rx}" fill="{fill}" fill-opacity="{op}" stroke="{stroke}" stroke-width="2"/>'


def line(x1, y1, x2, y2, stroke=GRID, sw=2, dash="", arrow=False):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    a = ' marker-end="url(#arr)"' if arrow else ""
    return f'<line x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}" stroke="{stroke}" stroke-width="{sw}"{d}{a}/>'


def ball(cx, cy, v, color, r=15):
    """Harvey ball: 1 = addressed / measured, 0.5 = partly, 0 = not."""
    s = f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{r}" fill="{BG}" stroke="{color}" stroke-width="2.5"/>'
    if v >= 1:
        s += f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{r}" fill="{color}"/>'
    elif v > 0:
        s += f'<path d="M{cx:.0f},{cy - r:.0f} A{r},{r} 0 0,0 {cx:.0f},{cy + r:.0f} Z" fill="{color}"/>'
    return s


def chip(x, y, label, color):
    w = 0.6 * 14 * len(label) + 20
    return rect(x, y, w, 26, color, rx=13, op=0.15) + t(x + w / 2, y + 18, label, 14, color, "bold", "middle")


def legend_balls(x, y, color=INK):
    s = ""
    for i, (v, lab) in enumerate(((1, "yes / measured"), (0.5, "partly"), (0, "no"))):
        s += ball(x + i * 190, y, v, color, 10) + t(x + i * 190 + 18, y + 6, lab, 16, MUTED)
    return s


def save(name, title, subtitle, body, source):
    head = t(60, 78, title, 38, weight="bold") + t(60, 116, subtitle, 21, MUTED)
    foot, _ = para(60, 852, "Sources: " + source, W - 120, 13, fill=MUTED)
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="{FONT}">'
           '<defs><marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">'
           f'<path d="M0,0 L10,5 L0,10 z" fill="{MUTED}"/></marker></defs>'
           f'<rect width="{W}" height="{H}" fill="{BG}"/>{head}{body}{foot}</svg>')
    p = OUT / f"{name}.svg"
    p.write_text(svg, encoding="utf-8")
    to_png(p)
    print("wrote", p.relative_to(ROOT))


def to_png(svg, scale=2):
    """Headless Edge/Chrome/Chromium screenshot. Windows first (the user's machine), then the Chromium a cloud session has.

    scale=1 for the photo title slide: the source photo is 1240 px wide, so a 2x render would only upscale it."""
    cand = [r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            shutil.which("msedge"), shutil.which("chrome"), shutil.which("chromium")]
    cand += sorted(str(p) for p in pathlib.Path("/opt/pw-browsers").glob("chromium*/chrome-linux/chrome"))
    exe = next((e for e in cand if e and pathlib.Path(e).exists()), None)
    if not exe:
        print("  no Edge/Chrome found: PNG skipped")
        return
    flags = [] if os.name == "nt" else ["--no-sandbox"]          # headless Chromium refuses to start as root otherwise
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as prof:   # Edge may still hold profile files
        subprocess.run([exe, "--headless", "--disable-gpu", "--hide-scrollbars", f"--user-data-dir={prof}", *flags,
                        f"--screenshot={svg.with_suffix('.png')}", f"--window-size={W},{H}",
                        f"--force-device-scale-factor={scale}", svg.as_uri()], capture_output=True, timeout=60)


# ---- 1. What the review covers
def fig_lit_map():
    rows = [r for r in csv.DictReader(open(ROOT / "notes/lit/literature_matrix.csv", encoding="utf-8"))
            if not r["relevance_to_topic"].startswith("Not used")]   # screened out as off-topic
    c = {}
    for r in rows:
        for b in r["bucket"].split("/"):
            c.setdefault(b.strip(), [0, 0])["full text" in r["read_level"]] += 1   # [abstract, full text]
    n_full = sum("full text" in r["read_level"] for r in rows)
    groups = [("Runoff side", RAIN, [("B1", "Interception & runoff traits"), ("B2", "Runoff modelling"),
                                     ("B4", "Flood context & policy")]),
              ("Bridge", TREE, [("B3", "Species selection & decision tools"), ("B5", "Design & optimisation precedents"),
                                ("B8", "Heat-flood trade-offs"), ("B6", "Co-benefits")]),
              ("Heat side", HEAT, [("B7", "Heat, shade & cooling"), ("B9", "City screening (heat + flood)")])]
    b, y, x0 = "", 170, 480
    k = min(22, 600 / max(sum(v) for v in c.values()))   # longest bar + label must stay left of the stats column (x=1150)
    for g, col, items in groups:
        b += t(60, y, g.upper(), 15, col, "bold")
        y += 12
        for code, lab in items:
            ab, fu = c.get(code, [0, 0])
            b += t(60, y + 26, lab, 20)
            b += rect(x0, y + 6, fu * k, 30, col, rx=3) + rect(x0 + fu * k, y + 6, ab * k, 30, col, rx=3, op=0.3)
            b += t(x0 + (fu + ab) * k + 10, y + 28, str(fu + ab), 18, INK, "bold")
            y += 44
        y += 20
    b += rect(60, y + 4, 22, 16, INK, rx=2) + t(90, y + 18, "read in full text", 16, MUTED)
    b += rect(260, y + 4, 22, 16, INK, rx=2, op=0.3) + t(290, y + 18, "abstract only", 16, MUTED)
    b += t(440, y + 18, "a paper can sit in two themes", 16, MUTED, italic=True)
    x = 1150
    b += t(x, 250, str(len(rows)), 110, INK, "bold") + t(x, 290, "sources in the review matrix", 21, MUTED)
    b += t(x, 400, str(n_full), 72, TREE, "bold") + t(x, 432, "read in full text", 21, MUTED)
    b += t(x, 540, str(len(rows) - n_full), 72, MUTED, "bold") + t(x, 572, "not yet read in full", 21, MUTED)
    tk, _ = para(1150, 650, "Two large literatures, runoff and heat. The bridge between them, species traits judged on "
                            "both goals at once, is thin: that is where this thesis sits.", 390, 21, weight="bold")
    save("05_lit_map", "What the literature review covers", f"{len(rows)} sources screened in 9 themes (7-12 Oct 2026)",
         b + tk, "notes/lit/literature_matrix.csv (OpenAlex / Semantic Scholar search, own screening).")


# ---- 2. Runoff evidence: species differ, effect fades with storm size
def fig_runoff_evidence():
    m = pd.read_csv(ROOT / "notes/lit/species_measurements.csv")
    m = m[(m.objective == "runoff") & m.measure.str.contains("interception") & (m.read_level != "secondary")
          & m.value.astype(str).str.match(r"^[\d.]+(-[\d.]+)?$")]
    m[["lo", "hi"]] = m.value.astype(str).str.split("-", expand=True).reindex(columns=[0, 1]).astype(float).values
    m["hi"] = m.hi.fillna(m.lo)
    m = m.sort_values("hi", ascending=False)
    ctx = {"Anys & Weiler 2024": "event mean, street trees, Freiburg", "Hassan et al. 2017": "annual, isolated trees, Spain",
           "Zabret & Sraj 2019": "share of rainfall over 2 years, Ljubljana", "Bean et al. 2021": "range by rain depth, Alabama",
           "Yang et al. 2019": "event mean, one tree, Seoul"}
    b = t(60, 175, "Rain intercepted by the crown (% of rainfall)", 22, RAIN, "bold")
    x0, x1, y = 400, 860, 205
    step = 46
    H = len(m) * step
    sx = lambda v: x0 + (x1 - x0) * v / 80
    for v in range(0, 81, 20):
        b += line(sx(v), 195, sx(v), 205 + H, GRID, 1) + t(sx(v), 205 + H + 22, f"{v}%", 15, MUTED, anchor="middle")
    b += line(sx(23.9), 195, sx(23.9), 205 + H, MUTED, 2, "6 5")
    b += t(sx(23.9), 205 + H + 44, "global median 23.9%, forests (de Mello 2024)", 13, MUTED, anchor="middle")
    for r in m.itertuples():
        star = "*" if r.read_level == "abstract" else ""
        b += t(60, y + 20, r.species, 18, italic=True)
        b += t(60, y + 38, f"{ctx.get(r.source, '')} ({r.source}{star})", 12, MUTED)
        b += rect(sx(r.lo), y + 8, max(sx(r.hi) - sx(r.lo), 8), 22, RAIN, rx=4)
        lab = f"{r.lo:.3g}" if r.lo == r.hi else f"{r.lo:.3g}-{r.hi:.3g}"
        b += t(sx(r.hi) + 10, y + 26, lab + "%", 17, INK, "bold", halo=True)
        y += step
    n1, _ = para(60, y + 58, "Surface storage varies threefold across 20 urban species, 0.51-1.81 mm per unit leaf + stem area; "
                             "Platanus 0.87, Pyrus calleryana 0.51 (Xiao & McPherson 2016). Metrics differ (event vs annual): "
                             "read as ranges, not as a ranking.", 1040, 14, fill=MUTED)
    b += n1
    x = 960
    b += t(x, 175, "...but the benefit fades as storms grow", 22, RAIN, "bold")
    cards = [("31-49% \u2192 26-46%", "runoff cut by green infrastructure, 0.25-yr \u2192 1-yr storm", "Liu et al. 2026, dense catchment, no trees"),
             ("28% \u2192 14%", "runoff cut by combined NbS, 2-yr \u2192 50-yr storm", "Esraz-Ul-Zannat et al. 2024, review"),
             ("3.5-4% of runoff", "avoided by 31 street trees (shown by removal); peak flow unchanged", "Selbig et al. 2021; Coville et al. 2022, paired catchment"),
             ("85% → 62%", "rain held by a 40-yr Zelkova crown, 2-yr → 25-yr 5-min storm", "Xiao & McPherson 2016, model; leaf-off only 16-26%")]
    y = 200
    for big, sub, src in cards:
        b += rect(x, y, 580, 130, RAIN, op=0.08) + rect(x, y, 6, 130, RAIN, rx=0)
        b += t(x + 28, y + 48, big, 32, RAIN, "bold") + t(x + 28, y + 82, sub, 17) + t(x + 28, y + 110, src, 14, MUTED)
        y += 148
    save("06_runoff_evidence", "Trees intercept rain: species differ, and the effect fades with storm size",
         "Runoff side of the review (bucket B1-B2)", b,
         "notes/lit/species_measurements.csv (first-hand values only); literature_matrix.csv rows 1-3, 5, 7-11, 24, 32, 34. * abstract only.")


# ---- 3. Shared drivers and trade-offs between heat and runoff
def fig_traits():
    xh, xr, cw = 370, 975, 565
    b = rect(xh, 150, cw, 44, HEAT, op=0.12) + t(xh + 18, 179, "HEAT: shade + transpiration", 20, HEAT, "bold")
    b += rect(xr, 150, cw, 44, RAIN, op=0.12) + t(xr + 18, 179, "RUNOFF: canopy interception", 20, RAIN, "bold")
    bands = [("HELP BOTH", TREE, [
        ("Leaf area (LAI, crown density)",
         "Canopy density is the strongest driver of cooling (Rahman et al. 2019); LAI ranks among the top shade predictors and wide crowns help (Speak et al. 2020)",
         "Interception rises with LAI / PAI (Anys & Weiler 2024); leaf-area density drives storage capacity (Baptista et al. 2018)"),
        ("Crown size",
         "Big, dense crowns with a low base give the best shade and comfort (Helletsgruber et al. 2020)",
         "About 66 L of runoff avoided per m\u00b2 of canopy per leaf-on season (Selbig et al. 2021; Coville et al. 2022)")]),
        ("PULL APART", WARN, [
        ("Leaf habit and season",
         "Dense LAI is best in summer, sparse LAI in winter (Peng et al. 2026); evergreen street trees were the weakest summer option for both heat and runoff (Wu et al. 2024)",
         "Bare crowns hold far less rain: a Zelkova holds 85% of a 2-yr storm in leaf, 16% leaf-off (Xiao & McPherson 2016); Barcelona's intense storms come mainly in autumn (Resilience Atlas)"),
        ("Water use",
         "Transpiration cools the air more than shade: 1.15 vs 0.43 \u00b0C (Park et al. 2026); diffuse-porous Platanus transpires 2-3x ring-porous species (Bachofen et al. 2025)",
         "Dry soils before a storm give ~10% more runoff reduction; wet soils give more cooling (Pace et al. 2025)")]),
        ("LIMITS", MUTED, [
        ("Context",
         "Surface material can outweigh tree traits for surface cooling (Kaluarachchi et al. 2020)",
         "Leafy crowns hold only the first 2-4 mm of a storm, so canopies work best in short, light storms (Kuehler et al. 2017)")])]
    y = 208
    for band, col, rows in bands:
        b += t(60, y + 16, band, 15, col, "bold") + line(160, y + 11, 1540, y + 11, col, 1.5)
        y += 30
        for lab, heat, rain in rows:
            hs, hh = para(xh + 12, y + 22, heat, cw - 24, 17)
            rs, rh = para(xr + 12, y + 22, rain, cw - 24, 17)
            rh_ = max(hh, rh) + 14
            l1, _ = para(60, y + 24, lab, 280, 20, weight="bold", fill=col if col != MUTED else INK)
            b += rect(xh, y, cw, rh_, col, rx=6, op=0.07) + rect(xr, y, cw, rh_, col, rx=6, op=0.07) + l1 + hs + rs
            y += rh_ + 8
        y += 4
    tk, _ = para(60, y + 34, "Leaf area and crown size push both goals the same way; leaf habit and water use pull them apart. "
                             "Species choice therefore needs a multi-objective search, not a single score.", 1480, 21, weight="bold")
    save("08_heat_runoff_traits", "Same tree, two jobs: which traits help both, and where they conflict",
         "Heat and runoff evidence side by side (buckets B1, B7, B8)", b + tk,
         "literature_matrix.csv rows 1, 3, 6, 9-11, 13, 38-40, 42, 43, 45, 53, 56; Barcelona Resilience Atlas.")


# ---- 4. Gap: state of the art vs this thesis
def fig_gap():
    cols = ["Heat stress (UTCI / MRT)", "Pluvial runoff", "Species traits drive results", "Optimises species and positions"]
    cx = [880, 1060, 1240, 1420]
    b = "".join(para(x, 190, c, 160, 17, weight="bold", anchor="middle")[0] for x, c in zip(cx, cols))
    rows = [("Nicol et al. 2026: SylvCiT", "Trait-based species recommender, Montreal; runoff module disabled; diversity traits only", [0, 0, .5, .5]),
            ("Pacetti et al. 2022", "Pluvial-flood hotspot index for siting NBS, Florence; no runoff simulation", [0, .5, 0, .5]),
            ("Cortinovis et al. 2022", "Barcelona-wide NBS scenarios: InVEST heat index + curve-number runoff; trees as land cover", [.5, 1, 0, 0]),
            ("Hao et al. 2023", "Genetic algorithm places identical trees in a Hong Kong park for UTCI; no species", [1, 0, 0, .5]),
            ("Wu et al. 2024", "Canopy energy balance + SWMM, Sendai; LAI and greening scenarios, surface temperature", [.5, 1, .5, 0]),
            ("Mannucci et al. 2025", "Grasshopper + Ladybug + curve number, one square in Rome; scenarios, trees as shade only", [1, 1, 0, 0]),
            ("Shaamala et al. 2025", "Ant-colony optimisation of 42 trees and 4 species (chosen by crown shape) against UTCI", [1, 0, .5, 1]),
            ("Peng et al. 2026", "Ladybug + NSGA-II with LAI-based canopy transmittance; generic tree types, UTCI and cost", [1, 0, .5, 1]),
            ("Tan & Liu 2026", "Surrogate + NSGA-II places 4 species (allometric crowns) in a Chicago block: UTCI, CO2, diversity", [1, 0, 1, 1]),
            ("This thesis", "Plane-tree replacement in Porta, Barcelona: species and positions for UTCI and runoff", [1, 1, 1, 1])]
    y = 236
    for name, sub, v in rows:
        me = name == "This thesis"
        if me:
            b += rect(45, y - 6, 1510, 52, TREE, op=0.1)
        b += t(60, y + 18, name, 20, TREE if me else INK, "bold")
        s, _ = para(60, y + 39, sub, 760, 15, fill=MUTED)
        b += s
        for x, val, col in zip(cx, v, (HEAT, RAIN, TREE, INK)):
            b += ball(x, y + 24, val, col, 15)
        y += 54
    b += legend_balls(60, y + 20)
    save("09_gap_matrix", "No method yet chooses species and positions for heat and runoff together",
         "Closest precedents from the review vs this thesis", b,
         "literature_matrix.csv rows 18, 28, 51-53, 56, 62, 69, 80 (all read in full). Half ball: Wu = surface temperature, not UTCI; "
         "Cortinovis = heat index, not UTCI; Hao = positions only; Shaamala = crown shape only; Peng = generic LAI classes. Tan: full ball, but crowns are allometric estimates for 5-year-old trees.")


# ---- 5. Data gap for the replacement palette
def fig_palette():
    tr = pd.read_csv(ROOT / "databases/traits/porta_trait_table.csv").set_index("species")
    palette = ["Platanus \u00d7 acerifolia", "Celtis australis", "Melia azedarach", "Pyrus calleryana",
               "Jacaranda mimosifolia", "Tipuana tipu", "Brachychiton populneus", "Styphnolobium japonicum"]

    def lit(s):          # 1 = numeric measured value, 0.5 = qualitative / value not yet extracted, 0 = none
        if pd.isna(s):
            return 0
        return 1 if re.search(r"= ~?\d", s) else 0.5

    cols = [("Crown size + LAI (LiDAR, this study)", TREE, lambda r: float(pd.notna(r.lidar_crown_diam_med) and pd.notna(r.lidar_lai_proxy_med))),
            ("Leaf + wood traits (SLA, wood density)", TREE, lambda r: float(pd.notna(r["3tf_SLA"]) or pd.notna(r["3tf_WD"]))),
            ("Drought vulnerability (P50)", TREE, lambda r: float(pd.notna(r.brot_P50_MPa))),
            ("Rain storage (measured)", RAIN, lambda r: lit(r.lit_runoff)),
            ("Cooling (measured)", HEAT, lambda r: lit(r.lit_heat))]
    notes = {("Celtis australis", 3): ("a", "Celtis: only the congener C. sinensis is measured (0.71 mm; Xiao & McPherson 2016)"),
             ("Pyrus calleryana", 4): ("b", "Pyrus: UTCI -3.5 to -6.3 °C, but modelled as a default ENVI-met tree, so it reflects size, not species (Silva et al. 2025)"),
             ("Tipuana tipu", 4): ("c", "Tipuana: PET up to -15.6 °C in summer, but up to -2.7 °C in winter (leafed, as cited); modelled with measured under-crown radiation (Santos Nouri et al. 2018)"),
             ("Jacaranda mimosifolia", 3): ("d", "Jacaranda: 15.3% interception for a small tree, city-scale model, second-hand (Xiao & McPherson 2003, cited in Huang et al. 2017)"),
             ("Brachychiton populneus", 4): ("e", "Brachychiton, Jacaranda: water use only, second-hand (McCarthy et al. 2011 via Berland et al. 2017; Pataki et al. 2011 via Thom et al. 2022)"),
             ("Jacaranda mimosifolia", 4): ("e", "Brachychiton, Jacaranda: water use only, second-hand (McCarthy et al. 2011 via Berland et al. 2017; Pataki et al. 2011 via Thom et al. 2022)"),
             ("Styphnolobium japonicum", 0): ("f", "Styphnolobium: only 5 trees in Porta; crown and LAI from 367 LiDAR trees on 25 streets in one 1 km tile elsewhere in the city"),
             ("Styphnolobium japonicum", 3): ("g", "Styphnolobium: event interception 35.8% on one tree in Seoul, not a storage value (Yang et al. 2019)")}
    cx = [700, 880, 1060, 1240, 1420]
    b = "".join(para(x, 175, c, 170, 16, weight="bold", anchor="middle", fill=col)[0] for x, (c, col, _) in zip(cx, cols))
    y = 225
    for sp in palette:
        r = tr.loc[sp]
        cur = sp.startswith("Platanus")
        b += t(60, y + 22, sp, 21, italic=True) + t(60, y + 44, ("current tree, " if cur else "candidate, ") + f"{int(r.n_porta)} in Porta", 14, MUTED)
        for i, (x, (_, col, f)) in enumerate(zip(cx, cols)):
            b += ball(x, y + 22, 0.5 if (sp, i) in notes else f(r), col, 15)
            if (sp, i) in notes:
                b += t(x + 22, y + 12, notes[(sp, i)][0], 16, MUTED, "bold")
        if cur:
            b += line(60, y + 62, 1540, y + 62, GRID, 2)
        y += 46 if not cur else 70
    b += legend_balls(60, y + 16)
    b += "".join(t(60, y + 44 + 18 * j, f"({k}) {v}", 14, MUTED) for j, (k, v) in enumerate(dict.fromkeys(notes.values())))
    tk, _ = para(60, y + 68 + 18 * len(set(notes.values())), "Crowns are measured by LiDAR for every candidate (Styphnolobium: city sample). Rain storage is measured for Pyrus only, "
                              "Celtis via a congener; cooling only modelled or second-hand. Gaps get trait proxies and sensitivity ranges.", 1480, 19, weight="bold")
    save("10_palette_data_gap", "The replacement palette: crowns we can measure, rain and cooling mostly not",
         "Plane tree vs the six replacement species the city names, plus Styphnolobium (named in the press); all grow in Porta", b + tk,
         "databases/traits/porta_trait_table.csv (ICGC LiDAR 2021; 3TF v1.3; BROT 2.0; notes/lit/species_measurements.csv); "
         "Styphnolobium crown from styphnolobium_lidar_summary.csv (city-wide sample, no_merge_flag, n = 367). "
         "TRY and i-Tree requests pending.")


# ---- 6. Method pipeline
def fig_method():
    def box(x, y, w, h, col, head, lines, status, scol):
        s = rect(x, y, w, h, col, rx=10, op=0.08) + rect(x, y, w, 6, col, rx=0)
        s += t(x + 16, y + 38, head, 20, col, "bold")
        yy = y + 70
        for ln in lines:
            p, hh = para(x + 16, yy, ln, w - 32, 18)
            s += p
            yy += hh + 10
        return s + chip(x + 16, y + h - 40, status, scol)

    b = box(60, 160, 290, 600, INK, "1  DATA", [
        "Street trees: species, position, size (Ajuntament)", "LiDAR 2021, leaf-on (ICGC)",
        "Buildings: OSM footprints + LiDAR height", "Pervious ground: NDVI 2017 + parks",
        "Design storms: PDISBA rainfall curves", "Weather: EPW Barcelona (Ladybug)",
        "Traits: BROT 2, 3TF, literature; TRY, i-Tree requested"], "collected", TREE)
    b += box(400, 160, 260, 600, INK, "2  TREE MODEL", [
        "Per tree: height, crown diameter, crown base, LAI proxy (2,600 LiDAR crowns)",
        "Per species: traits from databases; gaps filled by genus or leaf habit, with ranges",
        "Young vs mature crowns for replacements"], "traits in progress", WARN)
    b += box(710, 160, 360, 285, RAIN, "3a  RUNOFF (Python)", [
        "1 m grid, design storms T = 1, 2, 10 yr", "Canopy storage S = 1.75 mm x LAI, calibrated on Freiburg field data",
        "SCS curve number \u2192 event runoff (m\u00b3)"], "v1 done", TREE)
    b += box(710, 475, 360, 285, HEAT, "3b  HEAT (Grasshopper)", [
        "Ladybug: sky view + solar MRT \u2192 UTCI at 1.1 m on sidewalks", "Honeybee check of final layouts",
        "Infrared City API if access is granted"], "next", WARN)
    b += box(1120, 160, 200, 600, INK, "4  SEARCH", [
        "NSGA-II", "Decision: species at each of the 832 plane positions",
        "Constraints: \u2264 15% per species, diversity floor, no invasive or pest hosts"], "planned", MUTED)
    b += box(1370, 160, 170, 600, TREE, "5  RESULT", [
        "Pareto front: heat vs runoff", "Scenarios S0-S4", "Tests H1 and H2", "Transfer: Sant Antoni, Florence"], "planned", MUTED)
    for x1, y1, x2, y2 in ((350, 460, 398, 460), (660, 380, 708, 300), (660, 540, 708, 620),
                           (1070, 300, 1118, 400), (1070, 620, 1118, 520), (1320, 460, 1368, 460)):
        b += line(x1, y1, x2, y2, MUTED, 2.5, arrow=True)
    v, _ = para(60, 800, "Validation: interception vs Freiburg field data (done); runoff vs the Selbig 2021 field benchmark "
                         "(same order, done); Ladybug fast vs detailed runs; sensitivity on every assumed parameter.", 1480, 17, fill=MUTED)
    save("13_method_pipeline", "Method: from LiDAR trees to a heat-runoff trade-off",
         "Python modules + Grasshopper; status on 8 Oct 2026", b + v,
         "notes/methodology.md; scripts/bcn_lidar_porta.py, runoff_model.py, calibrate_interception.py.")


# ---- 7. Backup: the tree as a system (crown + pit + soil), scope extension
def fig_tree_system():
    SOIL, PAVE = "#A47148", "#9CA3AF"
    b = rect(70, 600, 680, 18, PAVE, rx=0) + t(80, 640, "sealed pavement", 14, MUTED)
    b += rect(70, 618, 680, 150, SOIL, rx=0, op=0.12) + t(520, 660, "compacted fill: no survey data", 14, MUTED)
    b += rect(330, 600, 170, 160, SOIL, rx=4, op=0.45) + t(415, 750, "pit soil", 15, BG, "bold", "middle")
    b += rect(405, 390, 20, 210, "#6B4F3A", rx=3)
    b += f'<ellipse cx="415" cy="300" rx="210" ry="115" fill="{TREE}" fill-opacity="0.55"/>'
    b += "".join(line(x, 165, x - 8, 188, RAIN, 3) for x in range(300, 580, 40))
    b += "".join(line(x, 470, x - 8, 495, RAIN, 3) for x in (110, 150, 190, 230))
    b += f'<circle cx="700" cy="190" r="34" fill="{HEAT}" fill-opacity="0.85"/>'
    b += line(665, 215, 600, 255, HEAT, 3, arrow=True)
    # water path: pavement runoff -> pit -> roots -> crown
    b += line(110, 590, 320, 590, RAIN, 4, arrow=True) + t(110, 572, "① runoff into the pit", 16, RAIN, "bold")
    b += line(450, 640, 450, 735, RAIN, 4, "8 6", arrow=True) + t(510, 715, "② infiltration", 16, RAIN, "bold")
    b += line(432, 580, 432, 420, TREE, 4, "8 6", arrow=True) + t(395, 535, "③ water for transpiration", 16, TREE, "bold", "end")
    b += t(290, 180, "④ interception", 16, RAIN, "bold", "end")
    b += line(560, 380, 660, 520, HEAT, 3, arrow=True) + t(622, 448, "⑤ shade + cooling", 16, HEAT, "bold")
    b += f'<circle cx="690" cy="555" r="9" fill="{INK}"/>' + line(690, 564, 690, 598, INK, 4) + t(705, 582, "UTCI", 14, INK, "bold")
    cards = [("CROWN", TREE, "core", "Species × position, as in the method today. Data: LiDAR crowns, trait tables."),
             ("PIT", RAIN, "extension", "Open area, soil volume, surface: one added design variable. Pit size is not in the open inventory: "
              "municipal spec or a tape survey of ~30 pits in Porta. Once sealed surfaces drain onto the tree's soil, the "
              "canopy benefit fades and soil infiltration controls runoff (Marrazzo & Raimondi 2025, model). A 0.72 m\u00b2 pit draining ~200 m\u00b2 "
              "kept ~11% of its runoff; ~90% needs a pit of 2.5-8% of its catchment (Grey et al. 2018)."),
             ("SOIL", SOIL, "parameter", "2-3 pit-soil options (e.g. standard vs structural soil) from the literature, with "
              "sensitivity. Structural soil: ~78:22 stone:soil, 30-35% porosity (Bartens et al. 2008). No stratigraphy data exists under the streets."),
             ("CARBON", INK, "output", "Reported, not optimised: carbon lost when mature planes are replaced by young trees. "
              "LiDAR allometry or i-Tree Eco.")]
    y = 160
    for head, col, tag, txt in cards:
        p, hh = para(860, y + 66, txt, 640, 17)
        hgt = max(hh + 62, 100)
        b += rect(830, y, 710, hgt, col, rx=10, op=0.08) + rect(830, y, 6, hgt, col, rx=0)
        b += t(860, y + 38, head, 22, col, "bold") + chip(1000, y + 18, tag, col) + p
        y += hgt + 12
    tk, _ = para(60, 796, "Hypothesis for the extension: the pit could link the goals, turning street runoff into water for transpiration. Mixed evidence: "
                                "trees transpired the equivalent of 17% of their catchment's runoff, but the trench did not raise it (Thom et al. 2020).", 1480, 19, weight="bold")
    save("B1_tree_system", "If broader: from the crown to the tree as a system",
         "Backup slide: one added design variable (the pit), soil as a parameter, carbon as an output", b + tk,
         "Park et al. 2026 (transpiration vs shade); Pace et al. 2025 (soil moisture); Mannucci et al. 2025 (irrigation trade-off); "
         "data_inventory_barcelona.md A1, B4. Bartens et al. 2008; Marrazzo & Raimondi 2025; Grey et al. 2018; Thom et al. 2020, 2022 (all read).")


# ---- 8. Transferability: what a new site costs
def fig_transfer():
    cities = [("Barcelona", "calibration", TREE, 730), ("Florence", "1st choice", WARN, 860),
              ("Mataro", "fallback", RAIN, 990), ("Bologna", "dropped", MUTED, 1120)]
    b = "".join(t(x, 196, name, 19, col, "bold", "middle") + t(x, 216, sub, 14, MUTED, anchor="middle")
                for name, sub, col, x in cities)
    b += t(1180, 206, "What it costs to move the method", 17, INK, "bold")
    rows = [("Boundary, buildings, DTM", "domain, building shadows, flow routing", [1, 1, 1, .5],
             "OSM plus a municipal or national terrain product nearly everywhere"),
            ("Tree inventory: species + position", "baseline stock and the positions to replace", [1, 1, .5, 1],
             "140,404 / 82,324 / 87,285 trees. Mataro: species and positions published, but in separate files"),
            ("Classified leaf-on point cloud", "crown, crown base, LAI proxy from gap fraction", [1, 0, 1, .5],
             "THE binding input. Florence has rasters only; ICGC covers all Catalonia"),
            ("Design rainfall (IDF)", "design storms T = 2, 10 yr (T = 1 only in Barcelona)", [1, 1, 1, 0],
             "Barcelona PDISBA, Florence a 1 km a-n grid, Mataro a full 5-120 min table of its own"),
            ("Pluvial flood map", "where runoff matters: the hotspot target", [1, .5, 0, 0],
             "NO Catalan city has one: the ACA pluvial polygon IS the municipal boundary"),
            ("Weather file (EPW)", "UTCI inputs and design hours", [1, .5, 1, .5],
             "TMYx verified for Spain; the airport-vs-centre bias is a stated limit everywhere"),
            ("Measured species traits", "trait table and gap-filling classes", [.5, .5, .5, .5],
             "40% in Barcelona, 19% in Florence. Porta-measured species cover 52% of Mataro streets"),
            ("Leaf calendar + storm season", "LAI per month, storm weighting", [1, .5, 1, .5],
             "City-specific - but Mataro inherits Barcelona's calendar and storm months unchanged"),
            ("Policy cap + replacement palette", "the feasible species set", [.5, .5, .5, .5],
             "The 15% cap is Barcelona's own; Sabadell proposes one, Florence has none")]
    y = 238
    for name, sub, v, cost in rows:
        hard = v[1] < 1 or v[2] < 1
        b += rect(45, y - 6, 1510, 50, WARN if hard else TREE, op=0.07)
        b += t(60, y + 16, name, 19, INK, "bold") + t(60, y + 36, sub, 15, MUTED)
        for (_, _, col, x), val in zip(cities, v):
            b += ball(x, y + 20, val, col, 14)
        p, _ = para(1180, y + 24, cost, 370, 15, fill=INK)
        b += p
        y += 52
    for i, (val, lab) in enumerate(((1, "available"), (0.5, "to confirm / to derive"), (0, "looked for, not found"))):
        b += ball(66 + i * 160, y + 24, val, INK, 10) + t(84 + i * 160, y + 30, lab, 14, MUTED)
    cards = [("SITE-AGNOSTIC KERNELS", TREE, "flow routing · sun and shadow geometry · SCS-CN runoff"),
             ("LOCAL IN EVERY DATA MODULE", WARN, "site adapter · design days and OP_BARE · calibrated s and IDF · leaf calendar · palette and cap"),
             ("DESIGN MODE NEEDS LESS", RAIN, "the designer supplies the positions; an EPW, terrain, traits, an IDF curve and a leaf calendar stay mandatory")]
    x, w = 540, 325
    for head, col, txt in cards:
        p, _ = para(x + 18, y + 48, txt, w - 36, 15, fill=INK)
        b += rect(x, y + 8, w, 112, col, rx=10, op=0.1) + t(x + 18, y + 34, head, 17, col, "bold") + p
        x += w + 20
    save("16_transferability", "The code travels, the evidence does not",
         "What the method needs at a new site: Porta (calibration) vs three transfer options, verified 19 Oct", b,
         "data_inventory_barcelona.md A1, A3, A7, B1-B2, C4, D1-D2, G; data_inventory.md B1, B3, B5-B7, F1, F3, F5-F7; "
         "topic_decision.md 6.1 (trait coverage); methodology.md 4 validation (iii) (routing vs RESCCUE depth); "
         "transfer_species_overlap.csv; catalan_transfer_city.md (ACA 3rd-cycle Annex 8 Taula 1; ICGC per-point GPS "
         "dates, sampled clips); Esbri et al. 2026 (storm months); phenology_palette.csv; notes/transferability.md.")

# ---- 11. Backup: the 22-city Catalan LiDAR screening
def fig_catalonia_lidar():
    """Backup slide: when was each Catalan city flown, and is its cloud classified?
    Data: databases/catalonia_lidar_dates.csv (see its header for provenance and limits)."""
    rows = [r for r in csv.DictReader(ln for ln in open(ROOT / "databases/catalonia_lidar_dates.csv",
                                                        encoding="utf-8") if not ln.startswith("#"))]
    porta = next(r for r in rows if r["city"].startswith("Porta"))
    same = [r for r in rows if r is not porta and r["flight_date"] == "2021-09-26" and r["note"].startswith("same")]
    ok = [r for r in rows if r is not porta and r not in same and r["classified"] == "yes"]
    unc = [r for r in rows if r["classified"] == "no" and r["leaf_on"] != "no"]
    off = [r for r in rows if r["leaf_on"] == "no"]

    def entry(x, y, r, col, show_density=True):
        name = r["city"].replace(" de Llobregat", "").replace(" i la Geltru", "").replace(" del Valles", "")
        name = name.replace("Porta Barcelona (control)", "Porta, Barcelona — control")
        d = r["flight_date"]
        if r["second_date"]:
            d += " + " + r["second_date"][5:]
        sub = d + (f"   {r['density_excl_overlap']} pts/m²" if show_density and r["density_excl_overlap"] else "")
        return t(x, y, name, 17, col, "bold") + t(x, y + 19, sub, 14, MUTED)

    b = ""
    # band 1: the same-mission group
    b += rect(45, 170, 1510, 104, TREE, op=0.1) + rect(45, 170, 6, 104, TREE, rx=0)
    b += t(70, 198, "SAME MISSION DAY AS PORTA — 26 September 2021", 19, TREE, "bold")
    b += t(70, 222, "zero season, sensor or campaign-year difference from the calibration site", 15, MUTED)
    for i, r in enumerate([porta] + same):
        x = 70 + i * 370
        b += entry(x, 252, r, TREE if r is not porta else INK)

    # band 2: leaf-on and classified
    b += rect(45, 292, 1510, 300, TREE, op=0.05) + rect(45, 292, 6, 300, TREE, rx=0)
    b += t(70, 320, f"LEAF-ON AND CLASSIFIED — {len(ok)} more cities, other 2021–22 missions", 19, TREE, "bold")
    b += t(70, 344, "usable for the gap-fraction LAI proxy; densities exclude the class-12 overlap strips", 15, MUTED)
    for i, r in enumerate(ok):
        x, yy = 70 + (i % 4) * 370, 376 + (i // 4) * 54
        b += entry(x, yy, r, INK)

    # band 3: the exclusions
    b += rect(45, 610, 735, 150, WARN, op=0.1) + rect(45, 610, 6, 150, WARN, rx=0)
    b += t(70, 638, f"LEAF-ON BUT UNCLASSIFIED — {len(unc)}", 19, WARN, "bold")
    b += t(70, 662, "no ground / vegetation / building classes in the clip: no gap fraction", 15, MUTED)
    for i, r in enumerate(unc):
        b += entry(70 + i * 235, 690, r, WARN, show_density=False)
    b += t(70, 740, "Figueres is excluded by classification, not by phenology: April is leaf-on for 6 of the 8 palette species",
           14, MUTED)

    b += rect(810, 610, 745, 150, MUTED, op=0.1) + rect(810, 610, 6, 150, MUTED, rx=0)
    b += t(835, 638, f"LEAF-OFF — {len(off)}", 19, MUTED, "bold")
    b += t(835, 662, "ruled out on season, and unclassified as well", 15, MUTED)
    for i, r in enumerate(off):
        b += entry(835 + i * 235, 690, r, MUTED, show_density=False)
    b += t(835, 740, "November: outside the May-October leaf-on window of every palette species", 14, MUTED)

    # the caveat belongs on the slide, not only in the source line
    cav, _ = para(70, 792, "How to read this: each date is from ONE 150x150 m clip at the city centre, so it is the "
                  "date AT THE SAMPLED CLIP, not across the city. Rubi and Granollers split two missions inside a "
                  "single clip, and a mission boundary runs through Porta's own tile.", 1470, 15, fill=INK)
    b += rect(45, 768, 1510, 70, WARN, op=0.08) + rect(45, 768, 6, 70, WARN, rx=0) + cav

    save("B2_catalonia_lidar", "22 Catalan cities, screened on the one input that decides a transfer",
         "ICGC Territorial LiDAR v3: the per-sheet metadata gives only the flight YEAR, so each date was read from "
         "PER-POINT GPS time in the cloud itself", b,
         "databases/catalonia_lidar_dates.csv (see its header). LIMIT: one 150x150 m clip per city (~0.0225 km2) in "
         "municipalities of 10-100+ km2 — read each date as 'at the sampled clip', not 'the city'; Rubi and Granollers "
         "split missions inside one clip. Control: the Porta clip returned 867,739 points, 100% 2021-09-26, agreeing "
         "with the date derived by a different route in data_inventory_barcelona.md section G. Leaf-on judged against "
         "databases/traits/phenology_palette.csv. Full screening: notes/catalan_transfer_city.md.")


# ---- Slide 1. Title, over the site itself
def fig_title():
    """Full-bleed photo of the Porta allotments, with the title over a scrim.

    The photo file sits next to the SVG and is referenced relatively, so both the headless render and
    an SVG editor resolve it. PHOTO CREDIT IS UNCONFIRMED (see the outline): check it before the booklet."""
    g = ('<defs><linearGradient id="scrim" x1="0" y1="0" x2="1" y2="0">'
         '<stop offset="0" stop-color="#0B1A20" stop-opacity="0.86"/>'
         '<stop offset="0.52" stop-color="#0B1A20" stop-opacity="0.52"/>'
         '<stop offset="1" stop-color="#0B1A20" stop-opacity="0.04"/></linearGradient>'
         '<linearGradient id="foot" x1="0" y1="0" x2="0" y2="1">'
         '<stop offset="0" stop-color="#0B1A20" stop-opacity="0"/>'
         '<stop offset="1" stop-color="#0B1A20" stop-opacity="0.75"/></linearGradient></defs>')
    b = (f'<image x="0" y="0" width="{W}" height="{H}" preserveAspectRatio="xMidYMid slice" '
         'href="01_title_photo.webp"/>'
         f'<rect width="{W}" height="{H}" fill="url(#scrim)"/>'
         f'<rect x="0" y="{H - 150}" width="{W}" height="150" fill="url(#foot)"/>')
    b += rect(80, 300, 88, 6, "#FFFFFF", rx=0)
    b += t(80, 410, "Shade and Sponge", 86, "#FFFFFF", "bold")
    b += para(80, 470, "A computational method for choosing which species replace Barcelona's plane trees, "
                       "and where — scored on summer heat and on storm runoff.", 820, 28, fill="#E8EEF0")[0]
    b += t(80, 596, "MaCAD, IAAC  ·  Tutor session, 20 October 2026", 22, "#9FB4BC")
    b += t(80, 820, "Horts urbans de Porta, Carrer d'Alcúdia × Carrer de la Maladeta, Nou Barris — "
                    "the bare crowns in the foreground are the plane trees this thesis is about.", 17, "#C6D3D8")
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
           f'width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="{FONT}">'
           f'<rect width="{W}" height="{H}" fill="#0B1A20"/>{g}{b}</svg>')
    out = OUT / "01_title.svg"
    out.write_text(svg, encoding="utf-8")
    to_png(out, scale=1)
    print("wrote", out.relative_to(ROOT))


# ---- Slide 2. The thesis in one sentence
def fig_one_sentence():
    def panel(x, w, col, head, lines, big=None):
        s = rect(x, 180, w, 300, col, rx=12, op=0.08) + rect(x, 180, w, 6, col, rx=0)
        s += t(x + 22, 218, head, 18, col, "bold")
        yy = 262
        if big:
            s += t(x + 22, yy, big, 34, col, "bold")
            yy += 46
        for ln in lines:
            p, hh = para(x + 22, yy, ln, w - 44, 19)
            s += p
            yy += hh + 12
        return s

    b = panel(60, 420, INK, "1  THE DECISION", [
        "Which of 7 candidate species goes at each position, as the planes come out.",
        "Positions are given: the existing pits."], "832 plane positions")
    b += panel(590, 420, HEAT, "2  TWO SCORES, SEPARATELY", [
        "f1  pedestrian heat stress: mean UTCI over 12–17 h on a hot design day (decided 19 Oct; the peak hour saturates).",
        "f2  event runoff volume: design storms T = 1, 2 and 10 yr."])
    b += panel(1120, 420, TREE, "3  THE ANSWER", [
        "A Pareto front: every layout on it is optimal, and the shape of the front is the trade-off itself.",
        "Plus the price of each goal, in the other."], "the trade-off")
    for x1, x2 in ((490, 578), (1020, 1108)):
        b += line(x1, 330, x2, 330, MUTED, 3, arrow=True)

    b += rect(60, 520, 1480, 112, RAIN, rx=12, op=0.07)
    b += t(82, 556, "CONSTRAINTS, NOT OBJECTIVES", 16, RAIN, "bold")
    b += t(82, 592, "≤ 15% per species  ·  Shannon diversity floor  ·  no invasive or pest-host species  "
                    "·  crown clearance from façades", 21)
    b += t(82, 618, "The city's own rules bound the search; they are not things the optimiser trades away.", 16, MUTED)

    b += t(60, 700, "What it is NOT", 18, WARN, "bold")
    for i, (h, d) in enumerate((
            ("not a flood model", "hotspots come from the city's own depth map, not from my routing"),
            ("not a city-wide plan", "one 0.84 km² neighbourhood, calibrated, with the transfer cost stated"),
            ("not a species ranking", "a layout is scored, not a species: the same tree is good or bad by where it stands"))):
        x = 60 + i * 500
        b += t(x, 740, h, 20, INK, "bold") + para(x, 772, d, 460, 17, fill=MUTED)[0]

    save("02_one_sentence", "species × position → heat + runoff → trade-off",
         "The whole thesis in one line, and its boundaries", b,
         "notes/topic_decision.md section 7; notes/methodology.md sections 1, 6 and 7; shade_sponge/README.md.")


# ---- Slide 3. Two hazards, one street, one decision
def fig_problem():
    def col(x, w, color, head, items):
        s = rect(x, 170, w, 480, color, rx=12, op=0.08) + rect(x, 170, w, 6, color, rx=0)
        s += t(x + 22, 208, head, 18, color, "bold")
        yy = 258
        for big, small in items:
            s += t(x + 22, yy, big, 32, color, "bold")
            p, hh = para(x + 22, yy + 32, small, w - 44, 18, fill=INK)
            s += p
            yy += 32 + hh + 26
        return s

    b = col(60, 480, RAIN, "RAIN", [
        ("45% → 72%", "sealed surface of the municipality, 1956–2009"),
        ("~3 storms a year", "exceed 60 mm/h in their first 20 minutes, and flood streets where the sewer lacks capacity"),
        ("T = 10 yr", "is what the sewer is sized for, per the city resilience atlas: above that, the surface carries the water")])
    b += col(570, 480, HEAT, "HEAT", [
        ("among the highest", "urban-heat-island mortality burdens in Europe (Iungman et al. 2023)"),
        ("UTCI > 32 °C", "strong heat stress for a pedestrian; on the hottest day even full shade is above it in 5 of 6 afternoon hours"),
        ("+1.36 °C", "Porta's summer surface-temperature anomaly against the city")])
    b += col(1080, 460, TREE, "THE DECISION ALREADY TAKEN", [
        ("15%", "maximum share of any one species, under the tree master plan"),
        ("27.6%", "share of Platanus x acerifolia among Barcelona's 145,176 street trees, and 29% inside Porta, so many must go"),
        ("6 + 1 species", "named by the city as replacements, plus Styphnolobium from the press")])

    b += rect(60, 684, 1480, 96, INK, rx=12, op=0.06)
    b += t(82, 722, "The two hazards and the decision land on the same streets, in the same years.", 24, INK, "bold")
    b += t(82, 756, "That is the opening: not \"trees are good\", but a replacement programme that has to be decided "
                    "species by species, position by position.", 18, MUTED)
    save("03_problem", "Two hazards, one street, one decision",
         "Why this is a design decision and not a slogan", b,
         "Barcelona Resilience Atlas (sealed surface, citing Barcelona Regional; storm frequency); notes/city_screening.md "
         "(sewer return period); Iungman et al. 2023; Bröde et al. 2012 (UTCI classes); notes/site_selection.md "
         "(Porta anomaly); tree master plan via BCNROC, databases/data_inventory_barcelona.md D1 (press figures conflict).")


# ---- Slide 7. Heat evidence, and what the model cannot see
def fig_heat_evidence():
    def block(x, w, color, head, items):
        s = rect(x, 170, w, 520, color, rx=12, op=0.08) + rect(x, 170, w, 6, color, rx=0)
        s += t(x + 22, 208, head, 18, color, "bold")
        yy = 250
        for h, d in items:
            s += t(x + 22, yy, h, 21, INK, "bold")
            p, hh = para(x + 22, yy + 26, d, w - 44, 17, fill=MUTED)
            s += p
            yy += 26 + hh + 22
        return s

    b = block(60, 730, TREE, "WHAT A TREE ACTUALLY DOES", [
        ("Shade, through mean radiant temperature",
         "MRT is the term a crown changes most; the sun–shade UTCI gap on hot afternoons is 2.3–4.7 °C in full "
         "shade — a lower bound for a real crown (scripts/heat_bounds.py)."),
        ("Leaf area sets how much sun gets through",
         "τ = exp(−k · LAI) with k = 0.5 (Beer–Lambert, as in Peng et al. 2026) — k is an ASSUMPTION: leaf-angle "
         "differences alone moved MRT by up to 9.5 °C (Li 2023). Same geometry, "
         "different species, different shade."),
        ("Transpiration cools the air more — but needs water",
         "1.15 °C against 0.43 °C for shade (Park 2026). In Porta it counts for less, on two separate Rahman et al. "
         "(2019) findings: per leaf area transpiration is lowest in Mediterranean climates, and it is ~10x lower "
         "for trees in paved pits than over grass."),
        ("A heatwave can take the leaf area away",
         "Platanus lost roughly 30–50% of its plant area index after a > 41 °C heatwave (Sanusi & Livesley 2020) "
         "→ a low-LAI plane variant in the sensitivity runs.")])
    b += block(830, 710, WARN, "WHAT THE MODEL CANNOT SEE (AND HOW I ANSWER IT)", [
        ("Ladybug ignores evapotranspiration",
         "so it likely underestimates vegetation cooling by about 2–3 °C UTCI (Mannucci et al. 2025). In a paved "
         "Mediterranean street that error is smaller than elsewhere, which is why I accept it."),
        ("Model error 1–2 °C",
         "so I compare the ranking of layouts, not absolute degrees. The optimiser only ever needs the ranking."),
        ("\"Share of points above 32 °C\" saturates",
         "on the hottest El Prat day even full shade is ≥ 32 °C in 5 of 6 afternoon hours (2 of 6 on the hot-week day, "
         "3 of 6 on the design day). So the metric is the mean UTCI over 12–17 h on a design cooling day — decided 19 Oct — with the hottest real day as a check."),
        ("Night is outside the design hour",
         "dense clusters trap heat at night (Zölch et al. 2019). Stated as a limit, not modelled.")])

    b += t(60, 740, "So the heat objective is a ranking of layouts on a design afternoon — not a temperature forecast.",
           24, INK, "bold")
    b += t(60, 776, "A fast shade x transmissivity proxy scores every layout; Ladybug Tier 1 (point UTCI on a 2 m grid) "
                    "and Honeybee Tier 2 check the shortlist. Infrared City would replace Tier 1 if access is granted.", 18, MUTED)
    save("07_heat_evidence", "Heat: what a tree can do, and what my model cannot see",
         "The evidence behind f1, and the honest boundary around it", b,
         "notes/methodology.md sections 3 and 6; notes/decisions/heat_objective.md; notes/method_heat_validation.md; "
         "Peng et al. 2026, Park 2026, Rahman et al. 2019, Mannucci et al. 2025, Sanusi & Livesley 2020, "
         "Zölch et al. 2019, Bröde et al. 2012 (matrix ids in notes/lit/literature_matrix.csv).")


# ---- Slide 17. Limits stated first, and what would unblock the thesis
def fig_limits_asks():
    items = ""
    yy = 244
    for h, d in (("Hazard index, not water depth",
                  "the site was chosen on an index; our own routing is not a flood map (ROC AUC 0.52 against RESCCUE)"),
                 ("Volume only", "no sewer, no routing to outlets, no ponding, and no peak flow"),
                 ("The LiDAR LAI proxy is probably low", "so canopy storage is underestimated, and s is the same for every species"),
                 ("One hypothesis withdrawn (19 Oct)", "H3 could not fail: with a full crown at every storm the falling percentage is arithmetic, so it is a declared boundary, not a test"),
                 ("Runoff may not separate the palettes", "if the best palette stays under Δmin = 91 m³ the runoff half of H1 is \"not resolved\" — which is still a result"),
                 ("Surface temperature ≠ pedestrian UTCI", "and the EPW is the airport, not the street; the design hour misses the night"),
                 ("Most palette species have no measured traits", "ranges and sensitivity instead — and that gap is itself a finding")):
        items += t(82, yy, h, 20, INK, "bold")
        para_svg, hh = para(82, yy + 25, d, 816, 17, fill=MUTED)
        items += para_svg
        yy += 25 + hh + 8
    box_h = yy - 170 - 6
    b = rect(60, 170, 860, box_h, WARN, rx=12, op=0.07) + rect(60, 170, 860, 6, WARN, rx=0)
    b += t(82, 208, "LIMITS I STATE", 18, WARN, "bold") + items

    b += rect(960, 170, 580, box_h, TREE, rx=12, op=0.08) + rect(960, 170, 580, 6, TREE, rx=0)
    b += t(982, 208, "WHAT WOULD UNBLOCK ME", 18, TREE, "bold")
    yy = 256
    for n, (h, d) in enumerate((
            ("The RESCCUE depth maps, usable in a thesis",
             "the T10/T100 tables are public; what I lack is a licence statement for thesis use"),
            ("Access to Infrared City",
             "it would replace the fast heat proxy inside the optimiser, with Ladybug kept as the cross-check"),
            ("The Florence point cloud",
             "the decisive missing input for the transfer case (Florence also has a 1 h IDF floor and an NC-ND licence)"))):
        b += t(982, yy, f"{n + 1}.  {h}", 21, INK, "bold")
        para_svg, hh = para(982, yy + 27, d, 536, 17, fill=MUTED)
        b += para_svg
        yy += 27 + hh + 30

    b += t(60, 738, "Plan to 18 December", 18, INK, "bold")
    weeks = (("21 Oct – 3 Nov", "LiDAR trees, trait table, runoff validation"),
             ("4 – 17 Nov", "Ladybug Tier 1, heat proxy calibration"),
             ("18 Nov – 1 Dec", "optimisation S2–S4, Tier 2 checks"),
             ("2 – 10 Dec", "Sant Antoni and the transfer city, sensitivity"),
             ("11 – 18 Dec", "booklet, figures, final presentation"))
    for i, (wk, what) in enumerate(weeks):
        x = 60 + i * 300
        b += rect(x, 756, 282, 62, INK, rx=8, op=0.06)
        b += t(x + 14, 780, wk, 16, INK, "bold") + para(x + 14, 800, what, 258, 14, fill=MUTED)[0]
    save("17_limits_asks", "What I cannot do yet, and what would unblock me",
         "Limits first, then three asks and the plan to 18 December", b,
         "notes/methodology.md sections 10 and 11; notes/decisions/hypothesis_tests.md and runoff_metric_sensitivity.md; "
         "notes/resccue_data_request.md; notes/firenze_lidar_request.md; notes/todo_manual.md; "
         "scripts/compare_resccue_runoff.py (AUC 0.52).")


# ---- Slide 11. The research question, part by part
def fig_research_question():
    b = rect(60, 160, 1480, 340, INK, rx=12, op=0.05)
    b += t(84, 206, "In Porta, as plane trees are replaced under the city's tree plan,", 26, MUTED)
    b += t(84, 250, "which replacement species and positions jointly reduce", 30, INK, "bold")
    b += rect(84, 278, 700, 96, HEAT, rx=10, op=0.10)
    b += t(104, 310, "(a)  pedestrian heat stress", 23, HEAT, "bold")
    b += t(104, 342, "mean UTCI over 12–17 h on a hot design day, sun-exposed routes", 19)
    b += rect(816, 278, 700, 96, RAIN, rx=10, op=0.10)
    b += t(836, 310, "(b)  event runoff volume", 23, RAIN, "bold")
    b += t(836, 342, "sealed street surfaces, 1-, 2- and 10-year PDISBA design storms", 19)
    b += t(84, 418, "How large is the trade-off between the two,", 30, INK, "bold")
    b += t(84, 456, "compared with the current trees, a like-for-like replacement with the city's named palette, "
                    "and single-objective layouts?", 22)
    b += t(84, 484, "Without those three baselines the question is not answerable — they are scenarios S0, S1 and S2/S3.", 16, MUTED)

    b += t(60, 560, "Every term is fixed before the runs", 18, TREE, "bold")
    for i, (h, d) in enumerate((
            ("WHERE", "Porta, Nou Barris: 0.84 km², 832 plane positions, the city's own replacement palette"),
            ("WHAT IS CHOSEN", "one species per position — the positions themselves are given by the existing pits"),
            ("AGAINST WHAT", "S0 the trees standing today · S1 like-for-like · S2/S3 each single-objective optimum"))):
        x = 60 + i * 500
        b += t(x, 598, h, 16, MUTED, "bold")
        b += para(x, 628, d, 460, 19)[0]

    b += rect(60, 700, 1480, 88, TREE, rx=12, op=0.08)
    b += t(84, 736, "Changed on 19 Oct (your decision):", 18, TREE, "bold")
    b += para(84, 766, "the heat metric is the 12–17 h mean, not the peak summer hour — at the peak even full shade "
              "is above 32 °C in 5 of 6 afternoon hours, so the metric saturated and no layout could show a benefit.",
              1430, 19)[0]
    save("11_research_question", "The research question, part by part",
         "v5, 19 Oct — what is chosen, against what, measured how", b,
         "notes/topic_decision.md sections 7 and 8; notes/decisions/heat_objective.md (DECIDED 19 Oct); "
         "notes/methodology.md section 7 (scenarios S0-S4).")


# ---- Slide 12. Two hypotheses, and the one that was withdrawn
def fig_hypotheses():
    def row(y, color, tag, title, claim, test, note, dead=False):
        h = 185
        s = rect(60, y, 1480, h, color, rx=12, op=0.05 if dead else 0.07) + rect(60, y, 8, h, color, rx=0)
        s += t(96, y + 40, tag, 17, color, "bold")
        tt, _ = para(96, y + 78, title, 300, 25, fill=MUTED if dead else INK, weight="bold")
        s += tt
        if dead:
            s += line(96, y + 70, 96 + 0.52 * 25 * min(len(title), 23), y + 70, MUTED, 2.5)
        s += para(430, y + 44, claim, 520, 19, fill=MUTED if dead else INK)[0]
        s += t(990, y + 30, "TEST" if not dead else "WHAT HAPPENS TO IT", 14, MUTED, "bold")
        s += para(990, y + 58, test, 520, 18, fill=MUTED)[0]
        if note:
            s += para(430, y + 146, note, 1080, 17, fill=color, weight="bold")[0]
        return s

    b = row(158, TREE, "H1  ·  SYNERGY", "Both goals at once",
            "For the same number and size class of trees, trait-based layouts beat a like-for-like replacement "
            "on both objectives: crown size and LAI drive shading and interception alike.",
            "S4 against S1, on both objectives.",
            "Decision rule fixed first: Δmin = 91 m³. Today's exploratory best is 78 m³ → it would be reported \"not resolved\".")
    b += row(360, HEAT, "H2  ·  TRADE-OFF", "Species, not places",
             "The heat-optimal and the runoff-optimal layout differ mainly in species — leaf habit and "
             "transpiration — so the Pareto front is not a single point.",
             "Species composition of S2 against S3, at the same fixed positions.",
             "Positions are given, so this is a claim about composition, measured by a dissimilarity fixed in advance.")
    b += row(562, MUTED, "H3  ·  WITHDRAWN, 19 Oct", "Benefit shrinks with T",
             "It was a hypothesis until the model showed it is an identity: with I = min(P, S) and every crown full "
             "at every design storm, the falling percentage is arithmetic, not a result.",
             "Kept as a declared validity boundary: the benefit is small at the sewer design level (T = 10 yr), and "
             "extreme events such as 6 Sept 2018 are outside what trees can affect.",
             None, dead=True)

    b += rect(60, 752, 900, 70, INK, rx=12, op=0.06)
    b += t(84, 780, "Removing it is a result, not a retreat", 19, INK, "bold")
    b += t(84, 808, "a claim the model cannot fail is not a hypothesis", 17, MUTED)
    b += rect(990, 752, 550, 70, WARN, rx=12, op=0.10)
    b += t(1014, 780, "Question for the tutor", 17, WARN, "bold")
    b += t(1014, 808, "is declaring it a boundary the right call?", 19)
    save("12_hypotheses", "Two hypotheses — and the one I took out",
         "H1 and H2 are testable; H3 was withdrawn on 19 Oct because the model cannot fail it", b,
         "notes/topic_decision.md section 8 (v5, user decision 19 Oct); notes/decisions/hypothesis_tests.md; "
         "notes/decisions/runoff_metric_sensitivity.md; notes/methodology.md section 7.")


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    fig_title()               # slide 1
    fig_one_sentence()        # slide 2
    fig_problem()             # slide 3
    fig_lit_map()             # slide 5
    fig_runoff_evidence()     # slide 6
    fig_heat_evidence()       # slide 7
    fig_traits()              # slide 8
    fig_gap()                 # slide 9
    fig_palette()             # slide 10
    fig_research_question()   # slide 11
    fig_hypotheses()          # slide 12
    fig_method()              # slide 13
    fig_transfer()            # slide 16
    fig_limits_asks()         # slide 17
    fig_tree_system()         # backup B1
    fig_catalonia_lidar()     # backup B2
