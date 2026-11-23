import csv, datetime as dt, sys
import matplotlib, matplotlib.ticker; matplotlib.use("Agg")
import matplotlib.pyplot as plt, matplotlib.dates as md
from matplotlib.patches import Patch
src, out = sys.argv[1], sys.argv[2]
rows = list(csv.DictReader(open(src, encoding="utf-8")))
col = {"Claude cloud": "#3D6AB0", "Claude via OMEN": "#3F8A4A", "Giovanni": "#C0602F"}
d = lambda s: dt.datetime.strptime(s, "%Y-%m-%d")
ink, muted, grid = "#2A2622", "#6B655E", "#E4E0D8"
fig, ax = plt.subplots(figsize=(13, 9.5), dpi=150)
fig.patch.set_facecolor("#FCFCFB"); ax.set_facecolor("#FCFCFB")
prev = None; ys = []; k = 0
for r in rows:
    if r["group"] != prev: k += 1; prev = r["group"]
    ys.append(k); k += 1
n = k; prev = None
for i, r in enumerate(rows):
    y = n - 1 - ys[i]; s, e = d(r["start"]), d(r["end"]) + dt.timedelta(days=1)
    c = col[r["where"]]
    if r["group"] != prev:
        prev = r["group"]
        ax.axhline(y + 1.5, color=grid, lw=0.8)
        ax.text(d("2026-11-22") - dt.timedelta(days=0.3), y + 0.9, r["group"].upper(), fontsize=8, color=muted, fontweight="bold", ha="right", va="center")
    if r["status"] == "milestone":
        ax.plot(s + dt.timedelta(hours=12), y, marker="D", ms=9, color=c, mec="#FCFCFB", mew=2)
    else:
        kw = dict(color=c, height=0.55, edgecolor="#FCFCFB", linewidth=2)
        if r["status"] in ("optional", "buffer"): kw.update(alpha=0.35, hatch="///")
        ax.barh(y, e - s, left=s, **kw)
    label = r["task"] + ("  (optional)" if r["status"] == "optional" else "")
    ax.text(d("2026-11-22") - dt.timedelta(days=0.3), y, label, ha="right", va="center", fontsize=8.5, color=ink)
ax.set_yticks([]); ax.set_ylim(-0.8, n + 0.3)
ax.set_xlim(d("2026-11-22"), d("2026-12-17"))
ax.xaxis.set_major_locator(md.DayLocator()); ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, p: md.num2date(v).strftime("%d %b" if md.num2date(v).day in (1, 22) else "%d")))
ax.tick_params(axis="x", labelsize=7.5, colors=muted, length=0, labeltop=True)
for day in range(26):
    x = d("2026-11-22") + dt.timedelta(days=day)
    if x.weekday() >= 5: ax.axvspan(x, x + dt.timedelta(days=1), color="#F2F0EA", zorder=0)
today = d("2026-11-23")
ax.axvline(today, color=ink, lw=1, ls=(0, (2, 2)))
ax.text(today, -0.7, " today 23 Nov", fontsize=7.5, color=ink, va="bottom")
for x in ("2026-11-30", "2026-12-07", "2026-12-14"): ax.axvline(d(x), color=grid, lw=0.8, zorder=0)
for s in ax.spines.values(): s.set_visible(False)
ax.set_title("Schedule to the final presentation, 15 Dec 2026 (shaded columns = weekends)", fontsize=12, color=ink, loc="left", pad=28)
ax.legend(handles=[Patch(color=v, label=k) for k, v in col.items()] + [Patch(facecolor="#BBBBBB", alpha=0.35, hatch="///", label="optional / buffer")],
          loc="lower center", bbox_to_anchor=(0.5, -0.07), ncol=4, frameon=False, fontsize=8.5)
plt.tight_layout(); plt.savefig(out, facecolor=fig.get_facecolor())
