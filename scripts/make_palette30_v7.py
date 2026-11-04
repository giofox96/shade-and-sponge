"""Backup slide for the 10 Nov deck: the 30-species Barcelona palette against the 7-species palette, Porta + 32 barris,
each barri optimised on its own (python -m shade_sponge "<barri>" --palette=barcelona --size=exact --trunk=TERCERA).
Input: databases/barcelona/barris_summary_barcelona.csv and the per-barri tool_v0_summary_*_barcelona_sizeexact_trunkTERCERA.csv.
Output: slides/fig_v7/res_07_palette30.svg/.png. Run from scripts/: python make_palette30_v7.py
"""
import re, unicodedata
import pandas as pd
import make_infographics as mi
from make_infographics import t, para, rect, save, ROOT, INK, MUTED, GRID, HEAT, TREE, WARN

mi.OUT = ROOT / "slides/fig_v7"
DB = ROOT / "databases/barcelona"
TAG = "_barcelona_sizeexact_trunkTERCERA"
slug = lambda n: re.sub(r"[^a-z0-9]+", "-", unicodedata.normalize("NFKD", n).encode("ascii", "ignore").decode().lower()).strip("-")


def species_totals(d):
    """Trees per species in each barri's best palette-30 layout (the one in barris_summary_barcelona.csv)."""
    tot = pd.Series(dtype=float)
    for r in d.itertuples():
        f = DB / (f"tool_v0_summary{TAG}.csv" if r.barri == "Porta" else f"tool_v0_summary_{slug(r.barri)}{TAG}.csv")
        s = pd.read_csv(f).set_index("scenario").loc[r.best_layout30]
        n = pd.to_numeric(s.iloc[list(s.index).index("eff_species") + 1:-1], errors="coerce").dropna()
        tot = tot.add(n, fill_value=0)
    return tot.sort_values(ascending=False)


def fig():
    d = pd.read_csv(DB / "barris_summary_barcelona.csv")
    b32 = d[d.barri != "Porta"]
    sp = species_totals(d)
    d = d.sort_values("summer_pct_tool_palette30").reset_index(drop=True)
    b = ""
    # left: dumbbell, summer shade of today, palette 7 -> palette 30
    x0, x1, lo, hi, y0, dy = 330, 900, 65, 110, 205, 18.5
    X = lambda v: x0 + (v - lo) / (hi - lo) * (x1 - x0)
    for v in range(70, 111, 10):
        b += f'<line x1="{X(v)}" y1="{y0 - 12}" x2="{X(v)}" y2="{y0 + len(d) * dy}" stroke="{GRID}" stroke-width="1"/>'
        b += t(X(v), y0 + len(d) * dy + 22, f"{v}%", 14, MUTED, anchor="middle")
    b += f'<line x1="{X(100)}" y1="{y0 - 12}" x2="{X(100)}" y2="{y0 + len(d) * dy}" stroke="{INK}" stroke-width="1.5" stroke-dasharray="4 4"/>'
    b += t(X(100) + 6, y0 - 16, "today", 14, INK, anchor="start")
    for i, r in d.iterrows():
        y = y0 + i * dy
        name = r.barri if len(r.barri) <= 30 else r.barri[:28] + "…"
        bold = r.barri in ("Porta", "Sant Andreu")
        b += t(x0 - 12, y + 5, name, 13, INK, "bold" if bold else "normal", anchor="end")
        col = HEAT if r.diff_pts < 0 else TREE
        b += f'<line x1="{X(r.summer_pct_tool_palette7)}" y1="{y}" x2="{X(r.summer_pct_tool_palette30)}" y2="{y}" stroke="{col}" stroke-width="2.5"/>'
        b += f'<circle cx="{X(r.summer_pct_tool_palette7)}" cy="{y}" r="5" fill="{MUTED}"/>'
        b += f'<circle cx="{X(r.summer_pct_tool_palette30)}" cy="{y}" r="6" fill="{col}"/>'
    yl = 172
    b += f'<circle cx="{x0}" cy="{yl - 5}" r="5" fill="{MUTED}"/>' + t(x0 + 12, yl, "7 species (deck)", 14, MUTED)
    b += f'<circle cx="{x0 + 170}" cy="{yl - 5}" r="6" fill="{TREE}"/>' + t(x0 + 182, yl, "30 species", 14, TREE)
    b += t(60, yl, "Summer shade, % of today", 14, INK, "bold")
    # right: key numbers
    xr = 980
    med, mn, mx = b32.diff_pts.median(), b32.diff_pts.min(), b32.diff_pts.max()
    lo_b, hi_b = b32.loc[b32.diff_pts.idxmin(), "barri"], b32.loc[b32.diff_pts.idxmax(), "barri"]
    b += rect(xr, 165, 560, 170, TREE, rx=12, op=0.08) + f'<rect x="{xr}" y="165" width="8" height="170" fill="{TREE}"/>'
    b += t(xr + 34, 235, f"+{med:.1f} pts".replace(".", "."), 52, TREE, "bold")
    b += para(xr + 34, 275, f"median summer-shade gain over the 7-species palette, 32 barris (range {mn:+.1f} {lo_b} to "
              f"{mx:+.1f} {hi_b}); Porta {d.set_index('barri').loc['Porta', 'diff_pts']:+.1f}", 500, 17)[0]
    wmin, wmax = d.winter_pct_tool_palette30.min(), d.winter_pct_tool_palette30.max()
    rmin, rmax = d.runoff_hot_change_pct_palette30.min(), d.runoff_hot_change_pct_palette30.max()
    b += rect(xr, 360, 560, 120, WARN, rx=12, op=0.08) + f'<rect x="{xr}" y="360" width="8" height="120" fill="{WARN}"/>'
    b += t(xr + 34, 398, "The price: winter shade", 19, WARN, "bold")
    b += para(xr + 34, 428, f"{wmin:.0f}–{wmax:.0f}% of today's winter shade (more evergreens). Runoff at the flood hotspots "
              f"changes {rmin:+.1f} to {rmax:+.1f}%: not resolved.", 500, 16)[0]
    b += t(xr, 520, "Most planted species (best layouts, all 33)", 17, INK, "bold")
    top = sp.head(5)
    for i, (k, n) in enumerate(top.items()):
        y = 555 + i * 32
        b += t(xr, y, k, 15, INK) + rect(xr + 230, y - 14, 300 * n / top.iloc[0], 18, TREE, rx=3, op=0.85)
        b += t(xr + 238 + 300 * n / top.iloc[0], y, f"{n:,.0f}", 14, MUTED)
    b += para(xr, 735, "Each barri is optimised alone (no city-wide cap): the city-wide LP still uses 7 species. Firmiana "
              "is 'medium' in the 2011 guide but its measured crown is 9 m, over the guide's 4–6 m.", 560, 14, fill=MUTED)[0]
    save("res_07_palette30", "Backup: a wider palette, 30 species",
         "Same rules, the city's catalogue instead of 7 species: more summer shade in 31 of 32 barris, more winter shade too",
         b, "databases/barcelona/barris_summary_barcelona.csv and tool_v0_summary_*_barcelona_sizeexact_trunkTERCERA.csv "
         "(PR #89). 30 species = the 2011 street-tree guide catalogue minus its 4 'avoid' species; equal-trunk traits (TERCERA) "
         "from the city pool of LiDAR trees for every species. Heat = effective-shade proxy, not UTCI.")
    print(sp.head(5).to_string(), f"\nmedian {med}, range {mn}..{mx}, gains {int((b32.diff_pts > 0).sum())}/32")


if __name__ == "__main__":
    fig()
