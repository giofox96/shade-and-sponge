"""Backup slide for the midterm deck: the 17 Nov HiGHS figure (make_flowcharts_v9.flow_highs), updated to the 30-species
palette and with the acronyms spelled out in the sources. Reuses the v9 drawing; only the changed strings are swapped.
Timing re-measured 23 Nov: the same transportation LP (scipy.optimize.linprog, method="highs") at 832 × 30 solves in
~0.16 s with an integral answer (2,825 × 30: ~0.8 s) on the cloud container.
Output: slides/midterm/fig/flow_07_highs.svg/.png. Run from scripts/: python make_midterm_highs.py
"""
import make_infographics as mi
import make_flowcharts_v9 as v9
from make_infographics import ROOT

mi.OUT = ROOT / "slides/midterm/fig"
SWAP = {"Porta: 832 positions × 7 species": "Porta: 832 positions × 30 species",
        "Porta: 0.06 s · whole city: ~10 s": "Porta, 30 species: about 0.2 s"}
SRC = ("HiGHS: open-source solver for linear programming (LP) and mixed-integer programming (MIP); the name has no "
       "official expansion (highs.dev; Huangfu & Hall 2018, Math. Prog. Comp. 10:119–142), called through SciPy. "
       "Example scores are illustrative.")
_t, _save = v9.t, v9.save
v9.t = lambda x, y, s, *a, **k: _t(x, y, SWAP.get(s, s), *a, **k)
v9.save = lambda name, title, sub, body, src: _save(name, title, sub, body, SRC)

if __name__ == "__main__":
    v9.flow_highs()
