"""Bounding check for the heat objective f1: UTCI in full sun vs full shade at candidate design hours (no geometry, trees or grid).

Usage: python scripts/heat_bounds.py [EPW ...]     (default: databases/barcelona/weather/*.epw; see bcn_epw_summary.py for download)
Needs: pip install ladybug-core ladybug-comfort.  Writes databases/barcelona/heat_design_hours.csv.
Time convention: hours are the EPW hour labels in the file's standard time (TMYx El Prat: UTC+1, no DST), 12..17 = 12:00-17:59 standard
time = about 13:00-18:59 CEST in summer. Days: hottest TMYx day, middle day of the EPW 'Summer - Week Nearest Max Temperature',
the DDY 0.4% cooling day (`DDY` file next to the EPW); plus the DDY heating design day at hour 12 as the winter hour.
MRT: ladybug_comfort OutdoorSolarCal, fraction_body_exposed 1 (sun) / 0 (shade); surface temperature = air temperature,
sky_exposure 1, floor_reflectance 0.25 (all ASSUMPTION; ladybug defaults). Shade here = no direct beam, full sky diffuse (shade MRT is therefore an upper bound and the sun-shade gap a lower bound for a tree crown, which also cuts diffuse sky).
Wind: UTCI takes the 10 m METEOROLOGICAL speed (ladybug_comfort docstring: 1.5 x the speed felt at ground in the Fiala model), so no pedestrian-height input.
  UTCI_* = EPW 10 m speed as is (what LB UTCI Comfort does). UTCI_*_citywind = speed at 10 m over 'city' terrain, WindProfile('city','country') power law (sensitivity).
  wind_ped = same profile at 1.5 m, for information only (not used in UTCI).
"""
import sys, pathlib, csv
from ladybug.epw import EPW
from ladybug.ddy import DDY
from ladybug.windprofile import WindProfile
from ladybug.dt import DateTime
from ladybug_comfort.collection.solarcal import OutdoorSolarCal
from ladybug_comfort.utci import universal_thermal_climate_index as utci

ROOT = pathlib.Path(__file__).resolve().parents[1]
H_PED = 1.5
HOURS = range(12, 18)


def mrt_utci(loc, dni, dhi, hir, ta, rh, w10, hours, days):
    """Rows for (label, day-of-year index or None, hour) using full-year or 24 h collections; idx = d*24+h."""
    wp = WindProfile("city", "country")
    mrt = {k: OutdoorSolarCal(loc, dni, dhi, hir, ta, f, 1, 0.25).mean_radiant_temperature.values
           for k, f in (("sun", 1), ("shade", 0))}
    rows = []
    for label, d in days:
        for h in hours:
            i = d * 24 + h
            wc = wp.calculate_wind(w10.values[i], 10)
            r = dict(day=label, hour=h, Ta=ta.values[i], RH=rh.values[i], wind_10m=w10.values[i], wind_10m_city=wc,
                     wind_ped=wp.calculate_wind(w10.values[i], H_PED))
            for k in mrt:
                r[f"MRT_{k}"] = mrt[k][i]
                r[f"UTCI_{k}"] = utci(ta.values[i], mrt[k][i], w10.values[i], rh.values[i])
                r[f"UTCI_{k}_citywind"] = utci(ta.values[i], mrt[k][i], wc, rh.values[i])
            rows.append(r)
    return rows


def table(epw_path):
    epw = EPW(epw_path)
    ta = epw.dry_bulb_temperature
    vals = ta.values
    hot = max(range(365), key=lambda d: max(vals[d * 24:(d + 1) * 24]))
    mid = None
    for ln in open(epw_path, encoding="latin-1"):
        if ln.startswith("TYPICAL/EXTREME"):
            f = [x.strip() for x in ln.split(",")]
            m, d = [int(x) for x in f[f.index("Summer - Week Nearest Max Temperature For Period") + 2].split("/")]
            mid = DateTime(m, d).doy - 1 + 3  # start day + 3 = middle of the 7-day week
            break
    days = [(f"hottest TMYx day (doy {hot + 1})", hot)]
    if mid is not None:
        days.append((f"middle of hottest TMYx week (doy {mid + 1})", mid))
    rows = mrt_utci(epw.location, epw.direct_normal_radiation, epw.diffuse_horizontal_radiation,
                    epw.horizontal_infrared_radiation_intensity, ta, epw.relative_humidity, epw.wind_speed, HOURS, days)
    ddy = pathlib.Path(epw_path).with_suffix(".ddy")
    if ddy.exists():
        want = {"Ann Clg .4% Condns DB=>MWB": ("DDY cooling 0.4% DB", HOURS), "Ann Htg 99.6% Condns DB": ("DDY heating 99.6%", [12])}
        for dd in DDY.from_ddy_file(str(ddy)).design_days:
            key = dd.name.split(" ", 1)[1]
            if key in want:
                dni, dhi = dd.hourly_solar_radiation[:2]
                rows += mrt_utci(dd.location, dni, dhi, dd.hourly_horizontal_infrared, dd.hourly_dry_bulb,
                                 dd.hourly_relative_humidity, dd.hourly_wind_speed, want[key][1], [(want[key][0], 0)])
    return pathlib.Path(epw_path).name, rows


if __name__ == "__main__":
    paths = sys.argv[1:] or sorted(str(p) for p in (ROOT / "databases/barcelona/weather").glob("*.epw"))
    allrows = []
    for p in paths:
        name, rows = table(p)
        for r in rows:
            r.update(epw_file=name, time_convention="EPW standard time UTC+1 (no DST); CEST = +1 h")
            allrows.append(r)
    cols = ["epw_file", "day", "hour", "time_convention", "Ta", "RH", "wind_10m", "wind_10m_city", "wind_ped", "MRT_shade", "MRT_sun", "UTCI_shade", "UTCI_sun", "UTCI_shade_citywind", "UTCI_sun_citywind"]
    with open(ROOT / "databases/barcelona/heat_design_hours.csv", "w", newline="") as f:
        w = csv.DictWriter(f, cols, extrasaction="ignore"); w.writeheader()
        for r in allrows:
            w.writerow({k: (round(v, 2) if isinstance(v, float) else v) for k, v in r.items()})
    print(len(allrows), "rows")
