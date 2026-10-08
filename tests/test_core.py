"""Data-free checks of the tool core (run in CI: python -m pytest -q tests). Only tracked CSVs are read, no raw data."""
import numpy as np
from shade_sponge import heat, runoff, season, topo


def test_scs_bounds():
    p = np.linspace(0, 100, 201)
    q = runoff.scs(p, 80)
    ia = 0.2 * 25.4 * (1000 / 80 - 10)
    assert np.all(q[p <= ia] == 0)                       # no runoff below the initial abstraction
    assert np.all(q <= p) and np.all(np.diff(q) >= 0)    # never more than the rain, grows with the rain


def test_routing_downhill_and_mass():
    z = np.tile(np.arange(20.0), (15, 1))                # plane rising with the column index
    z[7, 10] = -5.0                                      # a pit: must still drain
    recv, order = topo.route(z)
    zf, inner = z.ravel(), np.zeros(z.shape, bool)
    inner[1:-1, 1:-1] = True
    assert np.all(recv[inner.ravel()] >= 0)               # every inner cell drains somewhere
    ok = (recv >= 0) & (np.arange(z.size) != 7 * 20 + 10)
    assert np.all(zf[recv[ok]] < zf[ok])                 # off the pit, water only flows downhill
    acc = topo.accumulate(recv, order, np.ones(z.shape))
    assert acc.ravel()[recv < 0].sum() == z.size         # all water leaves through the outlets


def test_leaf_factor_bounds():
    f = season.factor(list(season.PHEN.index) + ["Unknown species"], 1, r_off=0.5)
    assert np.all((f >= 0.5) & (f <= 1.0)) and f[-1] == 1.0


def test_sun_noon_july_barcelona():
    alt, az = heat.sun(41.4, 2.17, 196, 12.0)            # 15 July, ~solar noon: altitude ≈ 90 − 41.4 + 21.5
    assert 68 < np.degrees(alt) < 72 and abs(np.degrees(az) - 180) < 3
