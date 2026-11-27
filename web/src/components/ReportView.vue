<script setup>
// One-page report of the project area (v0.2.0; redone after the 27 Nov user tests: charts, maps, and a PDF of the page
// only). Scripted sentences from the numbers on screen, no LLM. "Print or save as PDF" opens the page alone in a new window.
import { computed, ref, reactive, watch, onMounted, onBeforeUnmount } from 'vue'
import { state, areaCover, layoutEff, label, scenario, projectCost, currentLayout, keptReplaced, costs, dataUrl } from '../store.js'
import { collect } from '../exporter.js'
import Icon from './Icon.vue'
import ArcGauge from './ArcGauge.vue'

const A = computed(() => state.area)
const s0 = computed(() => state.meta.scenarios.find((s) => s.id === 'S0_current').metrics)
const n = (v, d = 0) => Math.abs(v).toLocaleString('en', { maximumFractionDigits: d })
const eur = (v) => Number(v).toLocaleString('en', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
const short = (v) => Math.abs(v).toLocaleString('en', Math.abs(v) >= 1000 ? { notation: 'compact', maximumFractionDigits: 1 } : { maximumFractionDigits: 1 })
const pct = (a, b) => (b ? (100 * a) / b : 0)
// change of the area against today (its own trees) and against the city's practice on the same positions
const rows = computed(() => {
  const L = A.value?.local, M = A.value?.metrics, C = A.value?.city?.metrics
  if (!L || !M) return null
  const vsCity = (k) => (C ? M[k] - C[k] : null)
  return {
    summer: { d: L.shade_summer_m2h.delta, p: pct(L.shade_summer_m2h.delta, L.shade_summer_m2h.today), c: vsCity('shade_summer_m2h') },
    winter: { d: L.shade_winter_m2h.delta, p: pct(L.shade_winter_m2h.delta, L.shade_winter_m2h.today), c: vsCity('shade_winter_m2h') },
    hot: { d: L.runoff_hot_m3.delta, c: vsCity('runoff_hot_m3') },
    rain: { d: L.interception_m3?.delta ?? 0 },
  }
})
// the versions compared (user 27 Nov: "the three versions, and dynamic": pick which ones the report shows)
const VERSIONS = [['today', 'Today'], ['tool', 'This project'], ['city', "City's mix"]]
const show = reactive({ today: true, tool: true, city: true })
// bars: today, the tool, the city's mix, for the trees of the area on their own
const bars = computed(() => {
  const L = A.value?.local, M = A.value?.metrics, C = A.value?.city?.metrics
  if (!L || !M) return []
  const row = (k, name, unit, good) => {
    const today = L[k].today, tool = today + L[k].delta, city = C ? today + (C[k] - s0.value[k]) : null
    const vals = [['Today', today, 'today'], ['This project', tool, 'tool'], ...(city != null ? [["City's mix", city, 'city']] : [])].filter((v) => show[v[2]])
    return { name, unit, good, vals, max: Math.max(today, tool, city ?? 0, 1e-9) }
  }
  return [row('shade_summer_m2h', 'Summer shade', 'm²·h', 'more is better'), row('shade_winter_m2h', 'Winter shade', 'm²·h', 'less is better'),
    ...(L.interception_m3 ? [row('interception_m3', 'Rain held by the crowns', 'm³', 'more is better')] : [])].filter((r) => r.max > 0.01) // nothing to show
})
const trees = computed(() => (A.value ? A.value.idx.length + A.value.keptRows.length : 0))
const pal = computed(() => state.meta.palette)
const colorOf = (sp) => pal.value.find((p) => p.species === sp && p.in_palette)?.color
const mix = computed(() => {
  const c = A.value?.counts ?? {}
  const tot = Object.values(c).reduce((a, b) => a + b, 0) || 1
  return Object.entries(c).filter(([, k]) => k > 0).sort((a, b) => b[1] - a[1])
    .map(([s, k]) => ({ s, k, w: (100 * k) / tot, color: colorOf(s) ?? '#999' }))
})
const better = computed(() => {
  const r = rows.value
  if (!r) return { up: [], down: [] }
  const up = [], down = []
  // a change smaller than these counts as unchanged (1 m²·h of shade, 1 litre, 0.05 pts of cover)
  const put = (v, eps, good, name) => Math.abs(v) >= eps && (v * good > 0 ? up : down).push(name)
  put(r.summer.d, 1, 1, 'summer shade')
  put(r.winter.d, 1, -1, 'winter sun')
  put(r.hot.d, 0.001, -1, 'water reaching the flood hotspots')
  if (areaCover.value) put(areaCover.value.now - areaCover.value.today, 0.05, 1, 'canopy cover')
  return { up, down }
})
// small plans of one version: the area outline and its trees (new ones in their species colour, kept ones grey)
function planOf(kind) {
  if (!A.value) return null
  const P = state.trees.positions, K = state.trees.kept, lay = currentLayout(), city = kind === 'city'
  const repl = keptReplaced(city), cityPl = new Map(A.value.idx.map((i, k) => [i, A.value.city?.planeLayout?.[k]]))
  const pts = A.value.poly
  const lat0 = pts[0][1], kx = Math.cos((lat0 * Math.PI) / 180)
  const xs = pts.map((q) => q[0] * kx), ys = pts.map((q) => q[1])
  const [x0, x1, y0, y1] = [Math.min(...xs), Math.max(...xs), Math.min(...ys), Math.max(...ys)]
  const s = Math.min(300 / (x1 - x0), 220 / (y1 - y0))
  const f = (lon, lat) => [(lon * kx - x0) * s + (300 - (x1 - x0) * s) / 2, (y1 - lat) * s + (220 - (y1 - y0) * s) / 2]
  const planeSp = (i) => (city ? (cityPl.has(i) ? cityPl.get(i) : lay[i]) : lay[i])
  const dots = [
    ...A.value.inPlanes.map((i) => ({ q: f(P.lon[i], P.lat[i]), c: pal.value[planeSp(i)]?.in_palette ? pal.value[planeSp(i)].color : '#9a968b', r: 3.2 })),
    ...A.value.keptIdx.map((k) => ({ q: f(K.lon[k], K.lat[k]), c: repl.has(k) ? pal.value[repl.get(k)].color : '#c9c4b8', r: 2.6 })),
    ...(city ? [] : state.added.map((t) => ({ q: f(t.lon, t.lat), c: pal.value[t.species]?.color ?? '#3F663E', r: 3.2, ring: true }))),
  ]
  return { d: 'M' + pts.map((q) => f(...q).map((v) => v.toFixed(1)).join(',')).join('L') + 'Z', dots }
}
const plans = computed(() => VERSIONS.filter(([k]) => k !== 'today' && show[k] && (k !== 'city' || A.value?.city)).map(([k, l]) => ({ k, l, p: planOf(k) })))
const today = new Date().toLocaleDateString('en-GB', { day: 'numeric', month: 'long', year: 'numeric' })

// ---- the big map, in EPSG:25831 metres (the exporter's own records): buildings, sidewalk edges, trees, spots ----------
const geo = ref(null)
watch(() => [A.value?.version, state.addedVersion, state.scenarioId], async () => { geo.value = A.value ? await collect() : null }, { immediate: true })
const MARGIN = 25 // m around the area
const layers = reactive({ under: 'none', trees: true, spots: true })
const map = computed(() => {
  const g = geo.value
  if (!g?.area) return null
  const xs = g.area.map((v) => v[0]), ys = g.area.map((v) => v[1])
  const box = [Math.min(...xs) - MARGIN, Math.min(...ys) - MARGIN, Math.max(...xs) + MARGIN, Math.max(...ys) + MARGIN]
  const P = (pts) => pts.map(([x, y]) => `${x.toFixed(1)},${(-y).toFixed(1)}`).join(' ')
  const inBox = ([x, y]) => x >= box[0] && x <= box[2] && y >= box[1] && y <= box[3]
  const G = state.meta.grid
  return {
    box, vb: `${box[0]} ${-box[3]} ${box[2] - box[0]} ${box[3] - box[1]}`, w: box[2] - box[0], h: box[3] - box[1],
    area: P(g.area),
    bld: g.buildings.filter((b) => b.rings[0].some(inBox)).map((b) => P(b.rings[0])),
    edges: g.edges.filter((e) => e.line.some(inBox)).map((e) => ({ d: P(e.line), kind: e.kind })),
    trees: g.trees.map((t) => ({ x: t.xy[0], y: -t.xy[1], r: Math.max(1, t.crown_diam_m / 2), c: t.status === 'existing' ? null : colorOf(t.species), ring: t.status === 'new_added' })),
    spots: g.spots.map((s) => ({ x: s.xy[0], y: -s.xy[1] })),
    grid: { x: G.x0, y: -G.y1, w: G.W * G.res, h: G.H * G.res },
    orto: `https://geoserveis.icgc.cat/servei/catalunya/orto-territorial/wms?REQUEST=GetMap&SERVICE=WMS&VERSION=1.3.0&LAYERS=ortofoto_color_vigent&STYLES=&CRS=EPSG:25831&BBOX=${box.map((v) => v.toFixed(0)).join(',')}&WIDTH=1600&HEIGHT=${Math.round((1600 * (box[3] - box[1])) / (box[2] - box[0]))}&FORMAT=image/jpeg`,
  }
})
const UNDER = computed(() => [['none', 'Nothing'], ['orto', 'Orthophoto'], ...(state.meta.overlays ?? []).map((o) => [o.id, o.label.replace(/ \(.*\)$/, '')])])
const underFile = computed(() => state.meta.overlays?.find((o) => o.id === layers.under)?.file)
// where the area is: its centre, in degrees and in EPSG:25831 metres
const centre = computed(() => {
  if (!A.value || !geo.value?.area) return null
  const m = (a, k) => a.reduce((s, v) => s + v[k], 0) / a.length
  return { lat: m(A.value.poly, 1), lon: m(A.value.poly, 0), x: m(geo.value.area, 0), y: m(geo.value.area, 1) }
})

// ---- key maps: the city's barris with this one marked, and the barri with the area --------------------------------
const barris = ref(null)
onMounted(async () => { barris.value = await fetch('./data/barris.geojson').then((r) => r.json()).catch(() => null) })
function fit(rings, W, H, pad = 6) {
  const all = rings.flat(), kx = Math.cos((41.4 * Math.PI) / 180)
  const xs = all.map((q) => q[0] * kx), ys = all.map((q) => q[1])
  const [x0, x1, y0, y1] = [Math.min(...xs), Math.max(...xs), Math.min(...ys), Math.max(...ys)]
  const s = Math.min((W - 2 * pad) / (x1 - x0), (H - 2 * pad) / (y1 - y0))
  const ox = (W - (x1 - x0) * s) / 2, oy = (H - (y1 - y0) * s) / 2
  const f = ([lon, lat]) => [(lon * kx - x0) * s + ox, (y1 - lat) * s + oy]
  return { f, d: (r) => 'M' + r.map((q) => f(q).map((v) => v.toFixed(1)).join(',')).join('L') + 'Z' }
}
const outer = (g) => (g.type === 'Polygon' ? [g.coordinates[0]] : g.coordinates.map((p) => p[0]))
const keys = computed(() => {
  const fc = barris.value
  if (!fc || !A.value) return null
  const me = fc.features.find((b) => b.properties.site && state.site.startsWith(b.properties.site))
  const city = fit(fc.features.flatMap((b) => outer(b.geometry)), 200, 180)
  const c = city.f([centre.value?.lon ?? A.value.poly[0][0], centre.value?.lat ?? A.value.poly[0][1]])
  const near = me ? fit(outer(me.geometry), 200, 180) : null
  return {
    city: fc.features.map((b) => ({ d: outer(b.geometry).map(city.d).join(''), on: b === me })), dot: c,
    name: me?.properties.name ?? state.meta.site.name,
    barri: near && outer(me.geometry).map(near.d).join(''), area: near && near.d(A.value.poly),
  }
})

// ---- species donut with the names around it, on leader lines (user 27 Nov) ------------------------------------------
const pie = computed(() => {
  const m = mix.value, tot = m.reduce((a, x) => a + x.k, 0)
  if (!tot) return null
  const cx = 260, cy = 120, R = 82, r = 50
  let a = -Math.PI / 2
  const at = (ang, rad) => [cx + rad * Math.cos(ang), cy + rad * Math.sin(ang)]
  const slices = m.map((x) => {
    const a0 = a, a1 = (a += (2 * Math.PI * x.k) / tot), big = a1 - a0 > Math.PI ? 1 : 0, mid = (a0 + a1) / 2
    const [p0, p1, q1, q0] = [at(a0, R), at(a1, R), at(a1, r), at(a0, r)]
    const d = m.length === 1 ? `M${cx - R},${cy}a${R},${R} 0 1,0 ${2 * R},0a${R},${R} 0 1,0 ${-2 * R},0M${cx - r},${cy}a${r},${r} 0 1,1 ${2 * r},0a${r},${r} 0 1,1 ${-2 * r},0`
      : `M${p0}A${R},${R} 0 ${big},1 ${p1}L${q1}A${r},${r} 0 ${big},0 ${q0}Z`
    return { ...x, d, mid, right: Math.cos(mid) >= 0, y: at(mid, R + 14)[1] }
  })
  // labels: each side sorted top to bottom, at least 15 units apart
  for (const right of [true, false]) {
    const side = slices.filter((s) => s.right === right).sort((p, q) => p.y - q.y)
    side.forEach((s, k) => (s.ly = Math.max(s.y, k ? side[k - 1].ly + 15 : 8)))
    const over = side.length ? side[side.length - 1].ly - 236 : 0
    if (over > 0) side.forEach((s) => (s.ly -= over))
  }
  return { cx, cy, slices: slices.map((s) => {
    const [ex, ey] = at(s.mid, R + 4), lx = cx + (s.right ? R + 34 : -R - 34)
    return { ...s, line: `M${ex.toFixed(1)},${ey.toFixed(1)}L${(cx + (s.right ? 1 : -1) * (R + 22)).toFixed(1)},${s.ly.toFixed(1)}L${lx.toFixed(1)},${s.ly.toFixed(1)}`,
      lx: lx + (s.right ? 4 : -4), anchor: s.right ? 'start' : 'end' }
  }) }
})

// ---- what the cost is made of ---------------------------------------------------------------------------------------
const costParts = computed(() => {
  const c = projectCost.value
  if (!c?.known || !c.total) return []
  return [['New trees', c.n.replace + c.n.add, costs.tree, '#5e8f55'], ['Transplants', c.n.move, costs.move, '#b08a2e'],
    ['Objects moved', c.n.object, costs.object, '#7A776E']]
    .filter(([, k, u]) => k && u).map(([l, k, u, color]) => ({ l, k, u, color, v: k * u, w: (100 * k * u) / c.total }))
})

// print the report alone: a new window with the page and the app's styles; colours kept (bars vanished in the PDF)
const page = ref(null)
function printReport() {
  const w = window.open('', '_blank', 'width=900,height=1200')
  if (!w) return window.print() // pop-ups blocked: print the app view instead
  const styles = [...document.querySelectorAll('style, link[rel=stylesheet]')].map((e) => e.outerHTML).join('')
  w.document.write(`<!doctype html><html data-theme="light"><head><meta charset="utf-8"><title>Project area report</title>${styles}
    <style>body{background:#fff;margin:0}*{-webkit-print-color-adjust:exact!important;print-color-adjust:exact!important}
    .report{position:static!important;max-width:none!important;padding:24px 28px!important;overflow:visible!important}
    .noprint{display:none!important}section{break-inside:avoid}@page{size:A4;margin:12mm}</style></head><body>${page.value.outerHTML}</body></html>`)
  w.document.close()
  w.onload = () => { w.focus(); w.print() }
}
onMounted(() => window.addEventListener('print-report', printReport))
onBeforeUnmount(() => window.removeEventListener('print-report', printReport))
</script>

<template>
  <article ref="page" class="report">
    <template v-if="A && rows">
      <div class="top">
        <div>
          <h1>Project area report</h1>
          <p class="muted">{{ state.meta.site.name }}, Barcelona, {{ today }}</p>
          <p class="muted small">Shade and sponge v0.2.0; {{ label(scenario) }}; Barcelona palette, 30 species</p>
          <dl v-if="centre" class="coords">
            <dt>Centre</dt><dd>{{ centre.lat.toFixed(5) }}° N, {{ centre.lon.toFixed(5) }}° E</dd>
            <dt>EPSG:25831</dt><dd>X {{ n(centre.x) }} m, Y {{ n(centre.y) }} m</dd>
          </dl>
        </div>
        <div v-if="keys" class="keys">
          <figure>
            <svg viewBox="0 0 200 180" role="img" aria-label="Key map of Barcelona">
              <path v-for="(b, i) in keys.city" :key="i" :d="b.d" :class="['kb', { on: b.on }]" />
              <circle :cx="keys.dot[0]" :cy="keys.dot[1]" r="4" class="kdot" />
            </svg>
            <figcaption>Barcelona</figcaption>
          </figure>
          <figure v-if="keys.barri">
            <svg viewBox="0 0 200 180" role="img" :aria-label="`Key map of ${keys.name}`">
              <path :d="keys.barri" class="kb on" /><path :d="keys.area" class="karea" />
            </svg>
            <figcaption>{{ keys.name }}</figcaption>
          </figure>
        </div>
      </div>

      <section class="tiles">
        <div :class="rows.summer.d >= 0 ? 'up' : 'down'"><Icon name="sun" /><b>{{ rows.summer.d >= 0 ? '+' : '−' }}{{ n(rows.summer.p) }}%</b><span>summer shade</span></div>
        <div :class="rows.winter.d <= 0 ? 'up' : 'down'"><Icon name="sunlow" /><b>{{ rows.winter.d >= 0 ? '+' : '−' }}{{ n(rows.winter.p) }}%</b><span>winter shade</span></div>
        <div :class="rows.hot.d <= 0 ? 'up' : 'down'"><Icon name="drop" /><b>{{ short(1000 * rows.hot.d) }} L</b><span>{{ rows.hot.d <= 0 ? 'less' : 'more' }} water to flood spots</span></div>
        <div v-if="areaCover" :class="areaCover.now >= areaCover.today ? 'up' : 'down'"><ArcGauge class="tg" :value="areaCover.now" /><b>{{ areaCover.now.toFixed(1) }}%</b><span>canopy, was {{ areaCover.today.toFixed(1) }}%</span></div>
      </section>

      <section v-if="map">
        <h2>The area</h2>
        <div class="layers noprint" role="group" aria-label="Map layers">
          <label>Under the map <select v-model="layers.under"><option v-for="[v, l] in UNDER" :key="v" :value="v">{{ l }}</option></select></label>
          <label><input v-model="layers.trees" type="checkbox" /> Trees</label>
          <label><input v-model="layers.spots" type="checkbox" /> Free spots</label>
        </div>
        <svg class="bigmap" :viewBox="map.vb" role="img" aria-label="Map of the project area with buildings, sidewalks and trees">
          <defs><clipPath id="rclip"><rect :x="map.box[0]" :y="-map.box[3]" :width="map.w" :height="map.h" /></clipPath></defs>
          <g clip-path="url(#rclip)">
            <image v-if="layers.under === 'orto'" :href="map.orto" :x="map.box[0]" :y="-map.box[3]" :width="map.w" :height="map.h" preserveAspectRatio="none" />
            <image v-else-if="underFile" :href="dataUrl(underFile)" :x="map.grid.x" :y="map.grid.y" :width="map.grid.w" :height="map.grid.h"
                   preserveAspectRatio="none" opacity="0.7" style="image-rendering: pixelated" />
            <polygon v-for="(b, i) in map.bld" :key="'b' + i" :points="b" class="bld" :class="{ onorto: layers.under === 'orto' }" />
            <polyline v-for="(e, i) in map.edges" :key="'e' + i" :points="e.d" :class="['edge', e.kind]" />
            <polygon :points="map.area" class="area" />
            <template v-if="layers.spots"><circle v-for="(s, i) in map.spots" :key="'s' + i" :cx="s.x" :cy="s.y" r="1.6" class="spot" /></template>
            <template v-if="layers.trees">
              <circle v-for="(t, i) in map.trees" :key="'t' + i" :cx="t.x" :cy="t.y" :r="t.r" :fill="t.c ?? '#c9c4b8'" :class="['tree', { old: !t.c, ring: t.ring }]" />
            </template>
          </g>
          <g class="scale" :transform="`translate(${map.box[0] + 6} ${-map.box[1] - 6}) scale(${map.w / 400})`">
            <rect x="0" y="-3" :width="20 * 400 / map.w" height="3" /><rect :x="20 * 400 / map.w" y="-3" :width="20 * 400 / map.w" height="3" class="w" />
            <text x="0" y="-6">0</text><text :x="40 * 400 / map.w" y="-6" text-anchor="end">40 m</text>
          </g>
        </svg>
        <p class="legend small"><span><i class="lg new"></i>new tree, colour of its species</span><span><i class="lg old"></i>tree kept</span>
          <span><i class="lg spot"></i>free spot</span><span><i class="lg area"></i>project area</span></p>
        <p><template v-if="areaCover">{{ n(areaCover.area_m2) }} m², </template>{{ A.inPlanes.length + A.keptIdx.length }} street trees
          ({{ A.inPlanes.length }} plane trees), {{ A.spotIdx.length }} planting spots. <b>{{ trees }} trees are replaced</b><template v-if="state.added.length">
          and <b>{{ state.added.length }} new trees are planted</b></template>.</p>
        <p class="chips"><span v-for="u in better.up" :key="u" class="chip good">▲ {{ u }}</span><span v-for="d in better.down" :key="d" class="chip bad">▼ {{ d }}</span></p>
      </section>

      <section>
        <h2>The versions compared</h2>
        <div class="vers noprint" role="group" aria-label="Versions in the report">
          <button v-for="[k, l] in VERSIONS" :key="k" :class="['chip', k, { on: show[k] }]" :aria-pressed="show[k]"
                  :disabled="k === 'city' && !A.city" @click="show[k] = !show[k]">{{ l }}</button>
        </div>
        <div v-for="b in bars" :key="b.name" class="bars">
          <p class="bname"><b>{{ b.name }}</b> <span class="muted">{{ b.unit }}, {{ b.good }}</span></p>
          <div v-for="[name, v, kind] in b.vals" :key="name" class="bar">
            <span class="bl">{{ name }}</span>
            <span class="track"><span :class="['fill', kind]" :style="{ width: (100 * v) / b.max + '%' }"></span></span>
            <span class="bv">{{ short(v) }}</span>
          </div>
        </div>
        <p class="small muted">{{ n(-1000 * rows.hot.d) }} litres {{ rows.hot.d <= 0 ? 'less' : 'more' }} water reach the flood hotspots in the
          2-year, 1-hour design storm<template v-if="rows.hot.c != null">; {{ n(-1000 * rows.hot.c) }} litres {{ rows.hot.c <= 0 ? 'less' : 'more' }} than the city's mix</template>.</p>
        <div v-if="plans.length" class="plans">
          <figure v-for="p in plans" :key="p.k">
            <svg class="plan" viewBox="0 0 300 220" role="img" :aria-label="`Plan of the area, ${p.l}`">
              <path :d="p.p.d" class="outline" />
              <circle v-for="(t, i) in p.p.dots" :key="i" :cx="t.q[0]" :cy="t.q[1]" :r="t.r" :fill="t.c" :stroke="t.ring ? '#2A2622' : 'none'" stroke-width="1" />
            </svg>
            <figcaption>{{ p.l }}<template v-if="p.k === 'city'">, the most likely species at each position</template></figcaption>
          </figure>
        </div>
      </section>

      <section v-if="areaCover">
        <h2>Canopy cover</h2>
        <div class="arcs">
          <figure><ArcGauge :value="areaCover.today" :size="170" /><figcaption><b>{{ areaCover.today.toFixed(1) }}%</b> today</figcaption></figure>
          <figure><ArcGauge :value="areaCover.now" :size="170" /><figcaption><b>{{ areaCover.now.toFixed(1) }}%</b> with this project</figcaption></figure>
        </div>
        <p class="small muted">The notch is the city's 30% target; the arc runs from 0 to 50%. {{ short(areaCover.crowns_m2) }} m² of crowns with this project.</p>
      </section>

      <section v-if="pie">
        <h2>Species planted <span class="muted">{{ layoutEff?.toFixed(1) }} effective species</span></h2>
        <svg class="pie" viewBox="0 0 520 244" role="img" aria-label="Species planted, as a donut chart">
          <path v-for="s in pie.slices" :key="s.s" :d="s.d" :fill="s.color" class="slice"><title>{{ s.s }}: {{ s.k }}</title></path>
          <text :x="pie.cx" :y="pie.cy - 2" text-anchor="middle" class="pc">{{ mix.reduce((a, m) => a + m.k, 0) }}</text>
          <text :x="pie.cx" :y="pie.cy + 13" text-anchor="middle" class="ps">trees</text>
          <g v-for="s in pie.slices" :key="'l' + s.s">
            <path :d="s.line" class="leader" />
            <text :x="s.lx" :y="s.ly + 4" :text-anchor="s.anchor" class="pl"><tspan font-style="italic">{{ s.s }}</tspan> {{ s.k }}</text>
          </g>
        </svg>
      </section>

      <section v-if="costParts.length">
        <h2>Cost</h2>
        <p class="big">€ {{ eur(projectCost.total) }}</p>
        <div class="cbar"><span v-for="c in costParts" :key="c.l" :style="{ width: c.w + '%', background: c.color }" :title="c.l"></span></div>
        <ul class="clist">
          <li v-for="c in costParts" :key="c.l"><i :style="{ background: c.color }"></i><span>{{ c.l }}</span>
            <span class="muted">{{ c.k }} at € {{ eur(c.u) }} each</span><b>€ {{ eur(c.v) }}</b></li>
        </ul>
        <p class="small muted"><template v-if="projectCost.perTree">€ {{ eur(projectCost.perTree) }} per tree. </template><template
          v-if="projectCost.perShade">€ {{ eur(projectCost.perShade) }} per 1,000 m²·h of summer shade gained. </template>
          Direct costs (CYPE price base), no VAT or overhead, watering not priced.</p>
      </section>

      <section>
        <h2>Limits</h2>
        <p class="small muted">Estimates from single-tree potentials calibrated on full model runs. Heat is a shade proxy, not UTCI; runoff is
          the season-weighted 2-year, 1-hour design storm. New trees are scored at their established size. Validated for Porta (Barcelona).
          Free spots are an upper bound: check them on site. Orthophoto © ICGC (CC BY 4.0); barris © Ajuntament de Barcelona (CC BY 4.0).
          Method and data: github.com/giofox96/shade-and-sponge.</p>
      </section>
    </template>
    <p v-else>Draw a project area and run it to get the report.</p>
  </article>
</template>

<style scoped>
.report { position: absolute; inset: 0; overflow: auto; padding: 64px max(32px, calc(50% - 420px)) 120px 440px; background: var(--bg, #fff); line-height: 1.5; }
.report * { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
.top { display: flex; justify-content: space-between; gap: 20px; align-items: flex-start; }
h1 { font-size: 30px; margin: 0 0 4px; letter-spacing: -0.02em; }
h2 { font-size: 16px; margin: 26px 0 8px; }
h2 .muted { font-weight: 400; margin-left: 6px; }
.coords { display: grid; grid-template-columns: auto 1fr; gap: 0 10px; font-size: 12px; margin: 10px 0 0; }
.coords dt { color: var(--muted); } .coords dd { margin: 0; font-variant-numeric: tabular-nums; }
.keys { display: flex; gap: 10px; flex: none; }
figure { margin: 0; }
figcaption { font-size: 11px; color: var(--muted); text-align: center; }
.keys svg { width: 150px; height: 135px; background: var(--panel); border-radius: 12px; }
.kb { fill: var(--bg); stroke: var(--line); stroke-width: 0.6; } .kb.on { fill: color-mix(in srgb, var(--good) 30%, var(--bg)); stroke: var(--good); stroke-width: 1; }
.kdot { fill: #b22c22; stroke: #fff; stroke-width: 1.5; }
.karea { fill: #b22c22; fill-opacity: 0.7; stroke: #b22c22; stroke-width: 1; }
.tiles { display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; margin-top: 18px; }
.tiles > div { position: relative; background: var(--panel); border-radius: 14px; padding: 14px; }
.tiles :deep(svg) { position: absolute; top: 12px; right: 12px; width: 20px; height: 20px; opacity: 0.55; }
.tiles :deep(svg.tg) { width: 40px; height: 25px; opacity: 1; }
.tiles b { display: block; font-size: 28px; letter-spacing: -0.02em; }
.tiles span { font-size: 12px; color: var(--muted); }
.tiles .up b { color: var(--good); } .tiles .down b { color: var(--bad); }
.layers { display: flex; flex-wrap: wrap; gap: 14px; align-items: center; font-size: 13px; margin-bottom: 6px; }
.layers select { font: inherit; margin-left: 4px; }
.bigmap { width: 100%; height: auto; display: block; background: var(--panel); border-radius: 12px; }
.bld { fill: #dedad1; stroke: #b9b4a8; stroke-width: 0.6; vector-effect: non-scaling-stroke; }
.bld.onorto { fill: none; stroke: rgba(255, 255, 255, 0.7); }
.edge { fill: none; stroke: #8d887c; stroke-width: 0.7; vector-effect: non-scaling-stroke; } .edge.kerb { stroke: #b9b4a8; }
.area { fill: none; stroke: #283f66; stroke-width: 2; stroke-dasharray: 6 4; vector-effect: non-scaling-stroke; }
.tree { fill-opacity: 0.85; stroke: rgba(0, 0, 0, 0.35); stroke-width: 0.6; vector-effect: non-scaling-stroke; }
.tree.old { fill-opacity: 0.7; } .tree.ring { stroke: #2a2622; stroke-width: 1.6; }
.spot { fill: #5caa32; stroke: #fff; stroke-width: 1; vector-effect: non-scaling-stroke; }
.scale rect { fill: #2a2622; } .scale rect.w { fill: #fff; stroke: #2a2622; stroke-width: 0.5; }
.scale text { font-size: 9px; fill: #2a2622; }
.legend { display: flex; flex-wrap: wrap; gap: 14px; margin: 6px 0 0; color: var(--muted); }
.lg { display: inline-block; width: 10px; height: 10px; border-radius: 50%; margin-right: 5px; vertical-align: -1px; }
.lg.new { background: #5e8f55; } .lg.old { background: #c9c4b8; } .lg.spot { background: #5caa32; width: 6px; height: 6px; }
.lg.area { border: 1.5px dashed #283f66; border-radius: 2px; }
.chips { display: flex; flex-wrap: wrap; gap: 6px; }
.chip { font-size: 12px; padding: 3px 10px; border-radius: 999px; background: var(--panel); }
.chip.good { color: var(--good); } .chip.bad { color: var(--bad); }
.vers { display: flex; gap: 6px; margin-bottom: 10px; }
.vers .chip { border: 1px solid var(--line); opacity: 0.55; }
.vers .chip.on { opacity: 1; border-color: currentColor; }
.vers .today { color: #6f6b61; } .vers .tool { color: var(--good); } .vers .city { color: #8C6A24; }
.bars { margin-bottom: 12px; }
.bname { margin: 0 0 4px; font-size: 14px; }
.bname .muted { margin-left: 6px; }
.bar { display: grid; grid-template-columns: 120px 1fr 70px; align-items: center; gap: 10px; font-size: 13px; margin: 3px 0; }
.track { height: 14px; background: var(--panel); border-radius: 7px; overflow: hidden; }
.fill { display: block; height: 100%; border-radius: 7px; }
.fill.today { background: #9a968b; } .fill.tool { background: var(--good); } .fill.city { background: #8C6A24; }
.bv { text-align: right; font-variant-numeric: tabular-nums; }
.plans { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 12px; margin-top: 12px; }
.plan { width: 100%; height: auto; background: var(--panel); border-radius: 12px; }
.outline { fill: color-mix(in srgb, var(--accent) 8%, transparent); stroke: var(--accent); stroke-width: 1.5; }
.arcs { display: flex; gap: 30px; }
.arcs figcaption { font-size: 13px; color: var(--text); margin-top: 4px; } .arcs b { font-size: 20px; }
.pie { width: 100%; height: auto; display: block; }
.slice { stroke: var(--bg); stroke-width: 1; }
.leader { fill: none; stroke: var(--muted); stroke-width: 0.7; }
.pl { font-size: 11px; fill: var(--text); } .pc { font-size: 22px; font-weight: 700; fill: var(--text); } .ps { font-size: 11px; fill: var(--muted); }
.big { font-size: 26px; font-weight: 700; margin: 0 0 8px; }
.cbar { display: flex; height: 18px; border-radius: 9px; overflow: hidden; gap: 2px; }
.clist { list-style: none; padding: 0; margin: 8px 0; font-size: 13px; }
.clist li { display: grid; grid-template-columns: 14px 120px 1fr auto; gap: 10px; align-items: center; padding: 3px 0; border-bottom: 0.5px solid var(--line); }
.clist i { width: 10px; height: 10px; border-radius: 2px; } .clist b { font-variant-numeric: tabular-nums; text-align: right; }
@media (max-width: 900px) { .report { padding: 64px 20px 120px; } .tiles { grid-template-columns: 1fr 1fr; } .top { flex-direction: column; } }
</style>
