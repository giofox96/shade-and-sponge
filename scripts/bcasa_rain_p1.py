"""Observed rainfall at BCASA gauge P1 (Centre Pau Casals, Canyelles, Nou Barris; the gauge nearest to Porta), 2016-2026,
compared with the PDISBA design storms used by the runoff module (databases/barcelona/pdisba_idf_city.csv).
Source: Barcelona Cicle de l'Aigua (BCASA), rain-gauge tips of 0.1 mm with decisecond time, file Pluja2016-2026.accdb,
delivered 12 Nov 2026 (last record 12 Nov 2026). Restricted data (academic use, no sharing): the raw file and the
per-event list stay in the gitignored raw folder; only the aggregated tables below go into the repo.
Method (BCASA's own note in InformacioPluja.xlsx): depth = 0.1 mm x tips; n-minute intensity = tips in the last n minutes
x 60/n. Periods the operator flagged as anomalous (Anomalies table) are dropped. Events are split by >= 6 h without a tip
and kept if >= 1 mm (ASSUMPTION: common inter-event dry period). Empirical return periods: Gringorten plotting position
on calendar-year maxima (2026 is a partial year, Jan-12 Nov, and is included).
Usage: python scripts/bcasa_rain_p1.py [path to .accdb (needs mdb-export) or to a CSV export of table Pluja]
Outputs: databases/barcelona/bcasa_p1_annual_max.csv, bcasa_p1_vs_pdisba.csv, bcasa_p1_event_months.csv;
raw/bcasa_pluja/p1_events.csv (gitignored)."""
import io, subprocess, sys
import numpy as np, pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "databases/barcelona"
RAW = DB / "raw/bcasa_pluja"
GAUGE = 1                                   # Identificador of P1 Centre Pau Casals (Canyelles)
DUR = [5, 10, 20, 30, 60, 120]              # minutes
IETD, MIN_MM = 6 * 3600, 1.0                # ASSUMPTION: event split and minimum depth


def table(src, name):
    if src.suffix == ".accdb":
        txt = subprocess.run(["mdb-export", "-D", "%Y-%m-%d %H:%M:%S", str(src), name], capture_output=True, text=True).stdout
        return pd.read_csv(io.StringIO(txt))
    return pd.read_csv(src.with_name(f"{name}.csv") if name == "Anomalies" else src)


def main(src):
    p = table(src, "Pluja")
    p = p[p.Identificador == GAUGE]
    t = (pd.to_datetime(p.INSTANT, format="mixed") + pd.to_timedelta(p.DECISEG * 100, unit="ms")).sort_values()
    a = table(src, "Anomalies")
    a = a[a.Identificador == GAUGE]
    bad = np.zeros(len(t), bool)
    for r in a.itertuples():
        bad |= ((t >= pd.to_datetime(r.INI_ANM)) & (t <= pd.to_datetime(r.FIN_ANM))).values
    t = t[~bad].reset_index(drop=True)
    s = (t - pd.Timestamp("2016-01-01")).dt.total_seconds().values
    # sliding n-minute depth ending at each tip
    depth = {d: (np.arange(len(s)) - np.searchsorted(s, s - d * 60, side="right") + 1) * 0.1 for d in DUR}
    ev = np.concatenate([[0], np.cumsum(np.diff(s) >= IETD)])
    e = pd.DataFrame({"ev": ev, "t": t, **{f"i{d}": depth[d] * 60 / d for d in DUR}})
    g = e.groupby("ev")
    E = pd.DataFrame({"start": g.t.min(), "end": g.t.max(), "depth_mm": g.size() * 0.1,
                      **{f"i{d}_mmh": g[f"i{d}"].max() for d in DUR}})
    E = E[E.depth_mm >= MIN_MM].round({c: 2 for c in E.columns if c not in ("start", "end")})
    E["duration_h"] = ((E.end - E.start).dt.total_seconds() / 3600).round(2)
    RAW.mkdir(parents=True, exist_ok=True)
    E.to_csv(RAW / "p1_events.csv", index=False)

    # calendar-year maxima, with the anomaly days per year
    days_bad = pd.Series(0.0, index=range(2016, 2027))
    for r in a.itertuples():
        for y, n in pd.Series(pd.date_range(pd.to_datetime(r.INI_ANM).normalize(), pd.to_datetime(r.FIN_ANM).normalize())).dt.year.value_counts().items():
            days_bad[y] += n
    E["year"] = E.start.dt.year
    am = E.groupby("year").agg(n_events=("depth_mm", "size"), total_mm=("depth_mm", "sum"),
                               **{f"max_i{d}_mmh": (f"i{d}_mmh", "max") for d in DUR})
    am["anomaly_days"] = days_bad.reindex(am.index).values
    am.round(1).to_csv(DB / "bcasa_p1_annual_max.csv")

    # PDISBA design intensity vs observed: how many events reached it, and the empirical T of that intensity
    idf = pd.read_csv(DB / "pdisba_idf_city.csv")
    n_years = (s[-1] - s[0]) / (365.25 * 86400) - days_bad.sum() / 365.25
    rows = []
    for r in idf[idf.duration_min.isin(DUR)].itertuples():
        x = np.sort(am[f"max_i{r.duration_min}_mmh"].values)[::-1]
        m = (x >= r.design_intensity_mmh).sum()
        rows.append({"duration_min": r.duration_min, "T_years": r.T_years, "pdisba_mmh": r.design_intensity_mmh,
                     "events_reaching": int((E[f"i{r.duration_min}_mmh"] >= r.design_intensity_mmh).sum()),
                     "per_year_obs": round((E[f"i{r.duration_min}_mmh"] >= r.design_intensity_mmh).sum() / n_years, 2),
                     "years_with_max_reaching": int(m), "n_years": len(x),
                     "obs_max_mmh": x[0], "obs_median_annual_max_mmh": round(float(np.median(x)), 1)})
    pd.DataFrame(rows).to_csv(DB / "bcasa_p1_vs_pdisba.csv", index=False)

    # month of the events that reached the PDISBA T = 1 yr, 60-min intensity (vs storm_months.csv)
    thr = idf.set_index(["T_years", "duration_min"]).design_intensity_mmh[(1, 60)]
    big = E[E.i60_mmh >= thr]
    mo = pd.DataFrame({"events_all": E.start.dt.month.value_counts(), "events_ge_T1_60min": big.start.dt.month.value_counts()})
    mo = mo.reindex(range(1, 13)).fillna(0).astype(int).rename_axis("month")
    mo["share_ge_T1_pct"] = (100 * mo.events_ge_T1_60min / max(len(big), 1)).round(1)
    mo.to_csv(DB / "bcasa_p1_event_months.csv")
    print(f"tips {len(t)}, dropped {bad.sum()}, events {len(E)}, effective years {n_years:.2f}")
    print(am.round(1).to_string()); print(pd.DataFrame(rows).to_string()); print(mo.to_string())


if __name__ == "__main__":
    main(Path(sys.argv[1]) if len(sys.argv) > 1 else RAW / "Pluja2016-2026.accdb")
