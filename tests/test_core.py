"""Data-free checks of the tool core (run in CI: python -m pytest -q tests). Only tracked CSVs are read, no raw data."""
import numpy as np
from shade_sponge import heat, layout, runoff, season, topo


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


def test_diversity_floor():
    rng = np.random.default_rng(0)
    score = rng.random((60, 5)) + np.array([2, 1.5, 0, 0, 0])   # two species dominate without a floor
    cap, fit = np.full(5, 40), np.ones((60, 5), bool)
    free = layout.assign(score, cap, fit)
    assert layout.eff_species(free, 5) < 2.1
    div = layout.assign(score, cap, fit, min_eff=4)
    assert layout.eff_species(div, 5) >= 4 and np.bincount(div, minlength=5).max() <= 40
    assert score[np.arange(60), div].sum() <= score[np.arange(60), free].sum()


def test_size_fits():
    sp = ["Pyrus calleryana", "Melia azedarach", "Tipuana tipu", "Unlisted sp."]
    pos = ["small", "medium", "large", "check", "none"]
    ex = layout.size_fits(pos, sp, "exact")
    assert ex[:3, :3].tolist() == np.eye(3, dtype=bool).tolist()
    assert ex[3].all() and ex[:, 3].all() and not ex[4, :3].any()
    am = layout.size_fits(pos, sp, "at_most")
    assert am[2].all() and am[1, :2].all() and not am[1, 2] and not am[0, 1:3].any()


def test_s1a_mix_respects_fit_and_cap():
    import pandas as pd
    pal = pd.DataFrame(dict(species=["Celtis australis", "Jacaranda mimosifolia", "Pyrus calleryana"]))
    fit = np.ones((50, 3), bool)
    fit[:10] = [False, True, True]                       # Celtis does not fit the first 10 positions
    ch = layout.s1a_layout(pal, np.array([30, 50, 50]), fit, np.random.default_rng(0))
    assert np.all(fit[np.arange(50), ch])                # every choice fits
    assert (ch == 0).sum() <= 30 and (ch == 1).sum() == 0   # cap holds; Jacaranda is not in the 2026 mix


def test_s1a_keeps_fit_when_cap_is_tight():
    import pandas as pd
    pal = pd.DataFrame(dict(species=["Celtis australis", "Tipuana tipu"]))
    fit = np.ones((40, 2), bool)
    fit[30:] = [True, False]                             # the last 10 positions fit only Celtis
    for seed in range(5):
        ch = layout.s1a_layout(pal, np.array([10, 40]), fit, np.random.default_rng(seed))
        assert np.all(fit[np.arange(40), ch])            # the tight cap goes to the positions that need it


def test_taxon_shares():
    import pandas as pd
    t = pd.DataFrame(dict(species=["Tipuana tipu"] * 3 + ["Styphnolobium japonicum"] * 3 + ["Celtis australis"] * 4))
    d = layout.taxon_shares(t)
    assert d["max_genus"] == "Celtis" and abs(d["max_genus_pct"] - 40) < 1e-9
    assert d["max_family"] == "Fabaceae" and abs(d["max_family_pct"] - 60) < 1e-9   # two legume genera together


def test_in_area_and_add_cap(tmp_path):
    import pandas as pd
    (tmp_path / "a.geojson").write_text('{"type": "FeatureCollection", "features": [{"type": "Feature", "properties": {}, '
                                        '"geometry": {"type": "Polygon", "coordinates": [[[2.17, 41.43], [2.18, 41.43], [2.18, 41.44], [2.17, 41.44], '
                                        '[2.17, 41.43]]]}}]}')           # GeoJSON = WGS84, around Porta
    pos = pd.DataFrame(dict(x=[431000, 431000, 433000], y=[4587000, 4590000, 4587000]))   # EPSG:25831
    assert layout.in_area(pos, tmp_path / "a.geojson").tolist() == [True, False, False]
    assert layout.add_cap(np.array([10, 0]), 100, 20).tolist() == [13, 3]              # floor(18) − floor(15)


def test_priority_ranks_peers():
    import pandas as pd
    from shade_sponge import health
    n = 12
    t = pd.DataFrame(dict(tree_id=range(n + 2), sp="A", size_category=["SEGONA"] * n + ["EXEMPLAR", "SEGONA"],
                          crown_area_m2=list(range(1, n + 1)) + [5, 0], gap_fraction=0.3, flag=["ok"] * (n + 1) + ["no_crown_detected"]))
    p = health.priority(t).set_index("tree_id")
    assert p.vigour_deficit[0] > p.vigour_deficit[n - 1]           # smaller crown among its peers = weaker
    assert p.peer_group[0] == "species_class" and p.peer_group[n] == "species"   # one EXEMPLAR: compared within the species
    assert p.vigour_deficit[n + 1] == 1 and p.age[n] == 1 and p.priority.between(0, 1).all()
