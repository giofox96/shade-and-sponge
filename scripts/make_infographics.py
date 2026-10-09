"""Infographics for the 20 Oct talk (literature review + method): 1600x900 SVG (editable) + PNG (Google Slides).

Numbers come from notes/lit/literature_matrix.csv, notes/lit/species_measurements.csv,
databases/traits/porta_trait_table.csv and notes/methodology.md; every figure prints its sources.
"*" = assessed from the abstract only. PNG export uses headless Edge/Chrome (no extra Python packages).
Output: slides/fig/*.svg, slides/fig/*.png
"""
import csv, re, shutil, subprocess, tempfile, pathlib, textwrap
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


def to_png(svg):
    exe = next((e for e in (r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
                            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                            shutil.which("msedge"), shutil.which("chrome")) if e and pathlib.Path(e).exists()), None)
    if not exe:
        print("  no Edge/Chrome found: PNG skipped")
        return
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as prof:   # Edge may still hold profile files
        subprocess.run([exe, "--headless", "--disable-gpu", "--hide-scrollbars", f"--user-data-dir={prof}",
                        f"--screenshot={svg.with_suffix('.png')}", f"--window-size={W},{H}",
                        "--force-device-scale-factor=2", svg.as_uri()], capture_output=True, timeout=60)


# ---- 1. What the review covers
def fig_lit_map():
    rows = list(csv.DictReader(open(ROOT / "notes/lit/literature_matrix.csv", encoding="utf-8")))
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
    b, y, x0, k = "", 170, 480, 22
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
    b += t(x, 540, str(len(rows) - n_full), 72, MUTED, "bold") + t(x, 572, "from abstracts (full text pending)", 21, MUTED)
    tk, _ = para(1150, 650, "Two large literatures, runoff and heat. The bridge between them, species traits judged on "
                            "both goals at once, is thin: that is where this thesis sits.", 390, 21, weight="bold")
    save("01_lit_map", "What the literature review covers", f"{len(rows)} sources screened in 9 themes (7-9 Oct 2026)",
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
    b += t(sx(23.9), 205 + H + 44, "global median 23.9%, forests (de Mello 2024*)", 13, MUTED, anchor="middle")
    for r in m.itertuples():
        star = "*" if r.read_level == "abstract" else ""
        b += t(60, y + 20, r.species, 18, italic=True)
        b += t(60, y + 38, f"{ctx.get(r.source, '')} ({r.source}{star})", 12, MUTED)
        b += rect(sx(r.lo), y + 8, max(sx(r.hi) - sx(r.lo), 8), 22, RAIN, rx=4)
        lab = f"{r.lo:.3g}" if r.lo == r.hi else f"{r.lo:.3g}-{r.hi:.3g}"
        b += t(sx(r.hi) + 10, y + 26, lab + "%", 17, INK, "bold", halo=True)
        y += step
    n1, _ = para(60, y + 70, "Surface storage varies threefold across 20 urban species, 0.51-1.81 mm per unit leaf + stem area; "
                             "Platanus 0.87, Pyrus calleryana 0.51 (Xiao & McPherson 2016). Metrics differ (event vs annual): "
                             "read as ranges, not as a ranking.", 800, 16, fill=MUTED)
    b += n1
    x = 960
    b += t(x, 175, "...but the benefit fades as storms grow", 22, RAIN, "bold")
    cards = [("31-49% \u2192 26-46%", "runoff cut by green infrastructure, 0.25-yr \u2192 1-yr storm", "Liu et al. 2026, dense catchment, no trees"),
             ("28% \u2192 14%", "runoff cut by combined NbS, 2-yr \u2192 50-yr storm", "Esraz-Ul-Zannat et al. 2024, review"),
             ("3.5-4% of runoff", "avoided by 31 street trees (shown by removal); peak flow unchanged", "Selbig et al. 2021*; Coville et al. 2022, paired catchment"),
             ("85% → 62%", "rain held by a 40-yr Zelkova crown, 2-yr → 25-yr 5-min storm", "Xiao & McPherson 2016, model; leaf-off only 16-26%")]
    y = 200
    for big, sub, src in cards:
        b += rect(x, y, 580, 130, RAIN, op=0.08) + rect(x, y, 6, 130, RAIN, rx=0)
        b += t(x + 28, y + 48, big, 32, RAIN, "bold") + t(x + 28, y + 82, sub, 17) + t(x + 28, y + 110, src, 14, MUTED)
        y += 148
    save("02_runoff_evidence", "Trees intercept rain: species differ, and the effect fades with storm size",
         "Runoff side of the review (bucket B1-B2)", b,
         "notes/lit/species_measurements.csv (first-hand values only); literature_matrix.csv rows 1-3, 5, 7-11, 24, 32, 34. * abstract only.")


# ---- 3. Shared drivers and trade-offs between heat and runoff
def fig_traits():
    xh, xr, cw = 370, 975, 565
    b = rect(xh, 150, cw, 44, HEAT, op=0.12) + t(xh + 18, 179, "HEAT: shade + transpiration", 20, HEAT, "bold")
    b += rect(xr, 150, cw, 44, RAIN, op=0.12) + t(xr + 18, 179, "RUNOFF: canopy interception", 20, RAIN, "bold")
    bands = [("HELP BOTH", TREE, [
        ("Leaf area (LAI, crown density)",
         "Canopy density is the strongest driver of cooling (Rahman et al. 2019*); LAI and crown width matter most for shade (Speak et al. 2020*)",
         "Interception rises with LAI / PAI (Anys & Weiler 2024); leaf-area density drives storage capacity (Baptista et al. 2018)"),
        ("Crown size",
         "Big, dense crowns with a low base give the best shade and comfort (Helletsgruber et al. 2020)",
         "About 66 L of runoff avoided per m\u00b2 of canopy per leaf-on season (Selbig et al. 2021*; Coville et al. 2022)")]),
        ("PULL APART", WARN, [
        ("Leaf habit and season",
         "Dense LAI is best in summer, sparse LAI in winter (Peng et al. 2026); evergreen street trees were the weakest summer option for both heat and runoff (Wu et al. 2024)",
         "Bare crowns hold far less rain: a Zelkova holds 85% of a 2-yr storm in leaf, 16% leaf-off (Xiao & McPherson 2016); Barcelona's intense storms come mainly in autumn (Resilience Atlas)"),
        ("Water use",
         "Transpiration cools the air more than shade: 1.15 vs 0.43 \u00b0C (Park et al. 2026); diffuse-porous Platanus transpires 2-3x ring-porous species (Bachofen et al. 2025)",
         "Dry soils before a storm give ~10% more runoff reduction; wet soils give more cooling (Pace et al. 2025)")]),
        ("LIMITS", MUTED, [
        ("Context",
         "Surface material can outweigh tree traits for surface cooling (Kaluarachchi et al. 2020*)",
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
    save("03_heat_runoff_traits", "Same tree, two jobs: which traits help both, and where they conflict",
         "Heat and runoff evidence side by side (buckets B1, B7, B8)", b + tk,
         "literature_matrix.csv rows 1, 3, 6, 9-11, 13, 38-40, 42, 43, 45, 53, 56; Barcelona Resilience Atlas. * abstract only.")


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
            ("This thesis", "Plane-tree replacement in Porta, Barcelona: species and positions for UTCI and runoff", [1, 1, 1, 1])]
    y = 240
    for name, sub, v in rows:
        me = name == "This thesis"
        if me:
            b += rect(45, y - 6, 1510, 60, TREE, op=0.1)
        b += t(60, y + 20, name, 21, TREE if me else INK, "bold")
        s, _ = para(60, y + 44, sub, 760, 16, fill=MUTED)
        b += s
        for x, val, col in zip(cx, v, (HEAT, RAIN, TREE, INK)):
            b += ball(x, y + 28, val, col, 16)
        y += 60
    b += legend_balls(60, y + 20)
    save("04_gap_matrix", "No method yet chooses species and positions for heat and runoff together",
         "Closest precedents from the review vs this thesis", b,
         "literature_matrix.csv rows 18, 28, 51-53, 56, 62, 69 (all read in full). Half ball: Wu = surface temperature, not UTCI; "
         "Cortinovis = heat index, not UTCI; Hao = positions only; Shaamala = crown shape only; Peng = generic LAI classes. Still to screen: Tan et al. 2026.")


# ---- 5. Data gap for the replacement palette
def fig_palette():
    tr = pd.read_csv(ROOT / "databases/traits/porta_trait_table.csv").set_index("species")
    palette = ["Platanus \u00d7 acerifolia", "Celtis australis", "Melia azedarach", "Pyrus calleryana",
               "Jacaranda mimosifolia", "Tipuana tipu", "Brachychiton populneus"]

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
             ("Tipuana tipu", 4): ("c", "Tipuana: PET -15.6 °C, second-hand only (Santos Nouri et al. 2018, cited in Silva et al. 2025)"),
             ("Jacaranda mimosifolia", 3): ("d", "Jacaranda: 15.3% interception for a small tree, city-scale model, second-hand (Xiao & McPherson 2003, cited in Huang et al. 2017)"),
             ("Brachychiton populneus", 4): ("e", "Brachychiton, Jacaranda: water use only, second-hand (McCarthy et al. 2011 via Berland et al. 2017; Pataki et al. 2011 via Thom et al. 2022)"),
             ("Jacaranda mimosifolia", 4): ("e", "Brachychiton, Jacaranda: water use only, second-hand (McCarthy et al. 2011 via Berland et al. 2017; Pataki et al. 2011 via Thom et al. 2022)")}
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
        y += 56 if not cur else 70
    b += legend_balls(60, y + 10)
    b += "".join(t(60, y + 40 + 18 * j, f"({k}) {v}", 14, MUTED) for j, (k, v) in enumerate(dict.fromkeys(notes.values())))
    tk, _ = para(60, y + 70 + 18 * len(set(notes.values())), "Every candidate's crown can be measured on site. Rain storage is measured for one candidate (Pyrus), "
                              "plus Celtis through a congener; cooling values are only modelled or second-hand. The method fills the gaps "
                              "with trait proxies and sensitivity ranges, and reports them as a finding.", 1480, 19, weight="bold")
    save("05_palette_data_gap", "The replacement palette: crowns we can measure, rain and cooling mostly not",
         "Plane tree vs the six replacement species the city names (all already grow in Porta)", b + tk,
         "databases/traits/porta_trait_table.csv (ICGC LiDAR 2021; 3TF v1.3; BROT 2.0; notes/lit/species_measurements.csv). "
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
        "Pareto front: heat vs runoff", "Scenarios S0-S4", "Tests H1-H3", "Transfer: Sant Antoni, Florence"], "planned", MUTED)
    for x1, y1, x2, y2 in ((350, 460, 398, 460), (660, 380, 708, 300), (660, 540, 708, 620),
                           (1070, 300, 1118, 400), (1070, 620, 1118, 520), (1320, 460, 1368, 460)):
        b += line(x1, y1, x2, y2, MUTED, 2.5, arrow=True)
    v, _ = para(60, 800, "Validation: interception vs Freiburg field data (done); runoff vs the Selbig 2021 field benchmark "
                         "(same order, done); Ladybug fast vs detailed runs; sensitivity on every assumed parameter.", 1480, 17, fill=MUTED)
    save("06_method_pipeline", "Method: from LiDAR trees to a heat-runoff trade-off",
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
    save("07_tree_system_backup", "If broader: from the crown to the tree as a system",
         "Backup slide: one added design variable (the pit), soil as a parameter, carbon as an output", b + tk,
         "Park et al. 2026 (transpiration vs shade); Pace et al. 2025 (soil moisture); Mannucci et al. 2025 (irrigation trade-off); "
         "data_inventory_barcelona.md A1, B4. Bartens et al. 2008; Marrazzo & Raimondi 2025; Grey et al. 2018; Thom et al. 2020, 2022 (all read).")


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    fig_lit_map()
    fig_runoff_evidence()
    fig_traits()
    fig_gap()
    fig_palette()
    fig_method()
    fig_tree_system()
