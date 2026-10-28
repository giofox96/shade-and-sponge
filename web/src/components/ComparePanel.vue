<script setup>
// Side-by-side comparison: today | city rule (S1a) | optimised. Each column draws every street-tree crown to scale
// (plane positions coloured by species, kept trees grey) and lists the headline metrics against today.
import { computed } from 'vue'
import { state, scenario, cityMean, label, areaLayout, keptReplaced, BALANCED, LIVE, AREA } from '../store.js'

const ROWS = [
  ['shade_summer_m2h', 'Summer shade', 'm²·h', 1],
  ['shade_winter_m2h', 'Winter shade', 'm²·h', -1],
  ['runoff_hot_m3', 'Runoff to hotspots', 'm³', -1],
  ['runoff_m3', 'Total runoff', 'm³', -1],
  ['canopy_pct', 'Canopy cover', '%', 1],
]
const find = (id) => state.meta.scenarios.find((s) => s.id === id)
const PLANE_COLOR = '#444441' // today's planes, as 'Current trees' in the trade-off chart (kept trees stay grey)

// Local metres from WGS84 (equirectangular around the site centre): enough for a 1 km site
const proj = computed(() => {
  const [lon0, lat0] = state.meta.site.center
  const kx = 111320 * Math.cos((lat0 * Math.PI) / 180), ky = 110540
  return (lon, lat) => [(lon - lon0) * kx, (lat0 - lat) * ky]
})
const keptAll = computed(() => {
  const k = state.trees.kept
  return k.lon.map((lon, i) => [...proj.value(lon, k.lat[i]), k.crown_diam_m[i] / 2, k.species[i]])
})
const kept = keptAll // all kept trees, for the bounding box and the 'Today' column
const pos = computed(() => state.trees.positions.lon.map((lon, i) => proj.value(lon, state.trees.positions.lat[i])))
// the project area's outline in local metres, when an area is on screen
const areaPts = computed(() => (state.scenarioId === AREA && state.area ? state.area.poly.map(([lon, lat]) => proj.value(lon, lat)) : null))
const areaPath = computed(() => areaPts.value?.map((p) => p.join(',')).join(' '))
// frame: the whole site, or the project area with a 25 m margin
const viewBox = computed(() => {
  if (areaPts.value) {
    const xs = areaPts.value.map((p) => p[0]), ys = areaPts.value.map((p) => p[1])
    const [x0, x1, y0, y1] = [Math.min(...xs) - 25, Math.max(...xs) + 25, Math.min(...ys) - 25, Math.max(...ys) + 25]
    return `${x0} ${y0} ${x1 - x0} ${y1 - y0}`
  }
  const xs = [...kept.value, ...pos.value].map((p) => p[0]), ys = [...kept.value, ...pos.value].map((p) => p[1])
  const [x0, x1, y0, y1] = [Math.min(...xs), Math.max(...xs), Math.min(...ys), Math.max(...ys)]
  return `${x0 - 10} ${y0 - 10} ${x1 - x0 + 20} ${y1 - y0 + 20}`
})

// kept trees in a column: an area that replaces every tree draws the replaced ones with their new species
function keptIn(repl) {
  return keptAll.value.filter((_, i) => !repl.has(i))
}
function keptNew(repl) {
  const pal = state.meta.palette
  return [...repl.entries()].map(([i, j]) => ({ x: keptAll.value[i][0], y: keptAll.value[i][1], r: pal[j].crown_diam_m / 2, c: pal[j].color }))
}
function crowns(layout) {
  const P = state.trees.positions, pal = state.meta.palette
  return pos.value.map(([x, y], i) => {
    const p = pal[layout[i]]
    return { x, y, r: (p.in_palette ? p.crown_diam_m : P.s0_crown_diam_m[i]) / 2, c: p.in_palette ? p.color : PLANE_COLOR }
  })
}
// Today: every tree in its species colour (palette species as in the palette, planes dark, other species light grey)
const OTHER_COLOR = '#c9c6bd'
const colorOf = computed(() => {
  const m = new Map(state.meta.palette.filter((p) => p.in_palette).map((p) => [p.species, p.color]))
  return (sp) => m.get(sp) ?? OTHER_COLOR
})
const inArea = (x, y) => {
  const P = areaPts.value
  if (!P) return true
  let ins = false
  for (let a = 0, b = P.length - 1; a < P.length; b = a++) {
    const [xa, ya] = P[a], [xb, yb] = P[b]
    if ((ya > y) !== (yb > y) && x < ((xb - xa) * (y - ya)) / (yb - ya) + xa) ins = !ins
  }
  return ins
}
const todayKept = computed(() => keptAll.value.map(([x, y, r, sp]) => ({ x, y, r, c: colorOf.value(sp), sp })))
// species present today (in the project area, if one is drawn), most common first; the plane counts its positions
const todayMix = computed(() => {
  const n = new Map()
  const plane = state.meta.palette.find((p) => !p.in_palette)
  pos.value.forEach(([x, y], i) => {
    if (inArea(x, y)) n.set(plane.species, (n.get(plane.species) ?? 0) + 1)
  })
  keptAll.value.forEach(([x, y, , sp]) => inArea(x, y) && n.set(sp, (n.get(sp) ?? 0) + 1))
  const rows = [...n.entries()].sort((a, b) => b[1] - a[1])
  const tot = rows.reduce((a, [, v]) => a + v, 0)
  const top = rows.slice(0, 8)
  const rest = rows.slice(8).reduce((a, [, v]) => a + v, 0)
  const col = (sp) => (sp === plane.species ? PLANE_COLOR : colorOf.value(sp))
  return [...top.map(([sp, v]) => ({ species: sp, short: sp.replace(/\s*×\s*/, ' ').split(' ').slice(0, 2).join(' '), n: v, w: (100 * v) / tot, color: col(sp) })),
    ...(rest ? [{ species: 'other species', short: `${rows.length - 8} other species`, n: rest, w: (100 * rest) / tot, color: OTHER_COLOR }] : [])]
})

function mix(counts) {
  const n = Object.values(counts ?? {}).reduce((a, b) => a + b, 0)
  return state.meta.palette.filter((p) => counts?.[p.species]).map((p) => ({ ...p, n: counts[p.species], w: (100 * counts[p.species]) / n }))
}

const columns = computed(() => {
  if (!state.meta || !state.trees) return []
  const s0 = find('S0_current'), s1 = find('S1a_city_0')
  const L = state.trees.layouts
  const none = new Map()
  const today = { title: 'Today', sub: 'Measured trees, by species', metrics: s0.metrics, counts: null, crowns: crowns(L.S0_current),
    kept: [], keptNew: [], todayKept: true }
  const A = state.scenarioId === AREA && state.area
  if (A) {
    return [today,
      s1 && { title: 'City rule', sub: `In the project area (${A.idx.length} positions): expected 2026 mix · map: draw #0`,
              metrics: A.city.metrics, counts: A.city.counts, crowns: crowns(areaLayout(A.idx.map((i) => L.S1a_city_0[i]))), live: true,
              kept: keptIn(keptReplaced(true)), keptNew: keptNew(keptReplaced(true)) },
      { title: 'Optimised', sub: label(scenario.value), metrics: A.metrics, counts: A.counts, crowns: crowns(areaLayout(A.layout)), live: true,
        kept: keptIn(keptReplaced()), keptNew: keptNew(keptReplaced()) },
    ].filter(Boolean)
  }
  const optId = state.scenarioId === LIVE || state.scenarioId.startsWith('S4') ? state.scenarioId : BALANCED
  const opt = optId === LIVE ? scenario.value : find(optId)
  const optLayout = optId === LIVE ? state.live.layout : state.trees.layouts[optId]
  return [
    today,
    s1 && { title: 'City rule', sub: 'Metrics: mean of 10 draws of the 2026 mix · map and mix: draw #0', metrics: cityMean.value,
            counts: s1.counts, crowns: crowns(L.S1a_city_0), kept: keptIn(none), keptNew: [] },
    { title: 'Optimised', sub: label(opt), metrics: opt.metrics, counts: opt.counts, crowns: crowns(optLayout), live: optId === LIVE,
      kept: keptIn(none), keptNew: [] },
  ].filter(Boolean)
})
const today = computed(() => find('S0_current')?.metrics ?? {})
const pct = (a, b) => (b ? 100 * (a / b - 1) : 0)
// change vs today: relative % for amounts, percentage points for canopy cover (already a share)
const delta = (k, a, b) => (k === 'canopy_pct' ? a - b : pct(a, b))
const fmtDelta = (k, v) => `${v > 0 ? '+' : ''}${v.toFixed(k === 'canopy_pct' || Math.abs(v) < 1 ? 1 : 0)}${k === 'canopy_pct' ? ' pts' : '%'}`
const fmtVal = (k, v) => (v == null ? '—' : k === 'canopy_pct' ? v.toFixed(1) : Math.round(v).toLocaleString('en'))
const tone = (v, sign) => (Math.abs(v) < 0.05 ? '' : v * sign > 0 ? 'good' : 'bad')
const stage = computed(() => (state.meta?.run?.trunk_class === 'SEGONA' ? 'replacements at about 10 years' : 'replacements established'))
</script>

<template>
  <div class="compare">
    <p class="head muted small">{{ state.scenarioId === AREA && state.area ? `${state.area.idx.length} of ${state.trees.positions.lon.length} plane positions replaced (project area; today's trees elsewhere)` : `All ${state.trees.positions.lon.length} plane positions` }}, {{ stage }}. Crowns drawn to scale. Today: every tree in its species colour (planes dark, species outside the palette light grey; hover for the name).
      Other columns: new trees in colour, kept trees grey.
      Heat is a shade proxy, not UTCI; canopy cover is a relative disc measure, compare between columns only.</p>
    <div class="cols">
      <section v-for="c in columns" :key="c.title" class="col">
        <h3>{{ c.title }}</h3>
        <p class="muted small sub">{{ c.sub }}</p>
        <svg :viewBox="viewBox" class="mini" role="img" :aria-label="`Tree crowns, ${c.title}`">
          <template v-if="c.todayKept">
            <circle v-for="(t, i) in todayKept" :key="'t' + i" :cx="t.x" :cy="t.y" :r="t.r" :fill="t.c" fill-opacity="0.8"><title>{{ t.sp }}</title></circle>
          </template>
          <circle v-for="(k, i) in c.kept" :key="'k' + i" :cx="k[0]" :cy="k[1]" :r="k[2]" class="kept" />
          <circle v-for="(t, i) in c.keptNew" :key="'n' + i" :cx="t.x" :cy="t.y" :r="t.r" :fill="t.c" fill-opacity="0.75" />
          <polygon v-if="areaPath" :points="areaPath" class="area" />
          <circle v-for="(t, i) in c.crowns" :key="i" :cx="t.x" :cy="t.y" :r="t.r" :fill="t.c" fill-opacity="0.75">
            <title v-if="c.todayKept">{{ t.c === PLANE_COLOR ? 'Platanus × acerifolia' : '' }}</title></circle>
        </svg>
        <table class="kpi">
          <tr v-for="[k, name, unit, sign] in ROWS" :key="k">
            <td>{{ name }}</td>
            <td class="num">{{ c.live && k === 'canopy_pct' ? '—' : fmtVal(k, c.metrics?.[k]) }} <span class="u">{{ unit }}</span></td>
            <td class="num" :class="c.title === 'Today' || c.metrics?.[k] == null ? '' : tone(delta(k, c.metrics[k], today[k]), sign)">
              {{ c.title === 'Today' || c.metrics?.[k] == null || (c.live && k === 'canopy_pct') ? '' : fmtDelta(k, delta(k, c.metrics[k], today[k])) }}</td>
          </tr>
        </table>
        <template v-if="c.todayKept">
          <div class="mix" aria-label="Species present today">
            <span v-for="m in todayMix" :key="m.species" :style="{ width: m.w + '%', background: m.color }" :title="`${m.species}: ${m.n}`"></span>
          </div>
          <p class="muted small">{{ state.scenarioId === AREA && state.area ? 'In the project area' : 'Whole site' }}: plane positions and the other street trees with LiDAR crowns.</p>
          <ul class="mixlist small">
            <li v-for="m in todayMix" :key="m.species"><span class="dot" :style="{ background: m.color }"></span>{{ m.short }} {{ m.n }}</li>
          </ul>
        </template>
        <div v-if="c.counts" class="mix" :aria-label="`Species mix, ${c.title}`">
          <span v-for="m in mix(c.counts)" :key="m.species" :style="{ width: m.w + '%', background: m.color }" :title="`${m.species}: ${m.n}`"></span>
        </div>
        <ul v-if="c.counts" class="mixlist small">
          <li v-for="m in mix(c.counts)" :key="m.species"><span class="dot" :style="{ background: m.color }"></span>{{ m.short }} {{ m.n }}</li>
        </ul>
      </section>
    </div>
  </div>
</template>

<style scoped>
.compare { height: 100%; overflow: auto; padding: 12px 16px; box-sizing: border-box; background: var(--bg, #fff); }
.head { margin: 0 0 8px; }
.cols { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 14px; }
.col { min-width: 0; }
.col h3 { margin: 0; font-size: 14px; }
.sub { margin: 2px 0 6px; min-height: 2.6em; }
.mini { width: 100%; height: auto; max-height: 46vh; background: #f4f3ef; border-radius: 4px; display: block; }
.kept { fill: #b4b2a9; fill-opacity: 0.55; }
.area { fill: none; stroke: #185fa5; stroke-width: 1.5; vector-effect: non-scaling-stroke; stroke-dasharray: 6 3; }
.kpi { width: 100%; border-collapse: collapse; font-size: 12px; margin-top: 8px; }
.kpi td { padding: 3px 4px; border-top: 0.5px solid var(--line, #ddd); }
.num { text-align: right; white-space: nowrap; }
.u { color: var(--muted, #777); font-size: 11px; }
.good { color: #3b6d11; }
.bad { color: #a32d2d; }
.mix { display: flex; height: 10px; border-radius: 3px; overflow: hidden; margin: 8px 0 4px; gap: 1px; }
.mixlist { list-style: none; padding: 0; margin: 0; display: flex; flex-wrap: wrap; gap: 2px 10px; }
.dot { display: inline-block; width: 8px; height: 8px; border-radius: 50%; margin-right: 4px; }
</style>
