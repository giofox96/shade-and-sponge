"""GhPython component 'SAVE': writes the UTCI of every test point and hour to a CSV.
Inputs:
  folder   text, Item Access: the full path of exchange/from_gh (created if missing)
  scenario text, Item Access: S0 or S4 (same as in LOAD)
  pts      List Access: the test points from LOAD
  utci     List Access: the UTCI output of LB UTCI Comfort, FLATTENED (one data collection per point)
  run      Item Access: a Button (writes once per click)
Output:
  info     what was written"""
import csv, os, datetime

info = "click the button to save"
if run:
    if len(pts) != len(utci):
        info = "NOT SAVED: %d points but %d UTCI series. Flatten the utci input (right-click > Flatten)." % (len(pts), len(utci))
    else:
        if not os.path.isdir(folder):
            os.makedirs(folder)
        path = os.path.join(folder, "utci_%s_%s.csv" % (str(scenario).strip().upper(), datetime.date.today().strftime("%Y%m%d")))
        with open(path, "w") as f:
            w = csv.writer(f, lineterminator="\n")
            w.writerow(["scenario", "hour", "point_id", "x", "y", "z", "utci_C"])
            for i, (p, dc) in enumerate(zip(pts, utci)):
                for dt, v in zip(dc.datetimes, dc.values):
                    w.writerow([scenario, str(dt), i, round(p.X, 2), round(p.Y, 2), round(p.Z, 2), round(float(v), 3)])
        info = "saved %d points x %d hours to %s" % (len(pts), len(utci[0].values), path)
