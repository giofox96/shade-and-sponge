"""Summarise TMYx EPW files for Barcelona: source period, completeness, wind (speed, direction), summer Ta/RH, DDY cooling day.

Usage: python scripts/bcn_epw_summary.py [EPW ...]   (default databases/barcelona/weather/*.epw) -> databases/barcelona/epw_summary.csv
Files (not committed; licence not confirmed, see notes/decisions/weather_forcing.md), from climate.onebuilding.org:
  https://climate.onebuilding.org/WMO_Region_6_Europe/ESP_Spain/CT_Catalonia/<name>.zip, names
  ESP_CT_Barcelona-El.Prat.AP.081810_TMYx.2009-2023 | ...2011-2025 | ESP_CT_Barcelona.081800_TMYx.2011-2025 (city station)
Needs: pip install ladybug-core. Time: EPW standard time (UTC+1). Summer = Jun-Aug. Missing codes: Ta 99.9, RH 999, wind speed 999, direction 999.
"""
import sys, csv, pathlib, statistics as st
from ladybug.epw import EPW
from ladybug.ddy import DDY

ROOT = pathlib.Path(__file__).resolve().parents[1]
MISSING = dict(dry_bulb_temperature=99.9, relative_humidity=999, wind_speed=999, wind_direction=999)


def summarise(p):
    p = pathlib.Path(p); e = EPW(str(p))
    comments = ""
    for ln in open(p, encoding="latin-1"):
        if ln.startswith("COMMENTS 1"):
            comments = ln.strip().split(",", 1)[1].strip('"')
            break
    period = comments.split("Period of Record=")[1].split(";")[0] if "Period of Record=" in comments else ""
    summer = [i for i in range(8760) if 151 * 24 <= i < 243 * 24]  # 1 Jun-31 Aug (non-leap)
    ta, rh, ws = e.dry_bulb_temperature.values, e.relative_humidity.values, e.wind_speed.values
    wd = e.wind_direction.values
    r = dict(epw_file=p.name, source_period=period, lat=e.location.latitude, lon=e.location.longitude, elevation_m=e.location.elevation,
             n_hours=len(ta),
             missing_Ta=sum(v == 99.9 for v in ta), missing_RH=sum(v == 999 for v in rh),
             missing_wind_speed=sum(v == 999 for v in ws), missing_wind_dir=sum(v == 999 for v in wd),
             calm_hours_dir0_speed0=sum(1 for s, d in zip(ws, wd) if s == 0 and d == 0),
             ws_mean=round(st.mean(ws), 2), ws_median=round(st.median(ws), 2), ws_p10=round(sorted(ws)[876], 2), ws_max=max(ws),
             summer_Ta_mean=round(st.mean(ta[i] for i in summer), 2), summer_Ta_max=max(ta[i] for i in summer),
             summer_RH_mean=round(st.mean(rh[i] for i in summer), 1),
             summer_ws_mean=round(st.mean(ws[i] for i in summer), 2),
             summer_ws_p10_1217h=round(sorted(ws[i] for i in summer if 12 <= i % 24 <= 17)[int(0.1 * len(summer) / 4)], 2))
    ddy = p.with_suffix(".ddy")
    if ddy.exists():
        for dd in DDY.from_ddy_file(str(ddy)).design_days:
            if dd.name.endswith("Ann Clg .4% Condns DB=>MWB"):
                r["ddy_cooling04_Tmax"] = max(dd.hourly_dry_bulb.values)
                r["ddy_cooling04_wind10m"] = dd.hourly_wind_speed.values[14]
    return r


if __name__ == "__main__":
    paths = sys.argv[1:] or sorted(str(x) for x in (ROOT / "databases/barcelona/weather").glob("*.epw"))
    rows = [summarise(x) for x in paths]
    cols = sorted({k for r in rows for k in r}, key=lambda k: list(rows[0]).index(k) if k in rows[0] else 99)
    with open(ROOT / "databases/barcelona/epw_summary.csv", "w", newline="") as f:
        w = csv.DictWriter(f, cols); w.writeheader(); w.writerows(rows)
    for r in rows: print(r)
