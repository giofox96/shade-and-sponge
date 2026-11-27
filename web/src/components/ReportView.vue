<script setup>
// One-page report of the project area (v0.2.0; redone after the 27 Nov user tests: charts, a plan, and a PDF of the page
// only). Scripted sentences from the numbers on screen, no LLM. "Print or save as PDF" opens the page alone in a new window.
import { computed, ref, onMounted, onBeforeUnmount } from 'vue'
import { state, areaCover, layoutEff, label, scenario, projectCost, currentLayout, keptReplaced } from '../store.js'
import Icon from './Icon.vue'

const A = computed(() => state.area)
const s0 = computed(() => state.meta.scenarios.find((s) => s.id === 'S0_current').metrics)
const n = (v, d = 0) => Math.abs(v).toLocaleString('en', { maximumFractionDigits: d })
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
// bars: today, the tool, the city's mix, for the trees of the area on their own
const bars = computed(() => {
  const L = A.value?.local, M = A.value?.metrics, C = A.value?.city?.metrics
  if (!L || !M) return []
  const row = (k, name, unit, good) => {
    const today = L[k].today, tool = today + L[k].delta, city = C ? today + (C[k] - s0.value[k]) : null
    const max = Math.max(today, tool, city ?? 0, 1e-9)
    return { name, unit, good, vals: [['Today', today, 'today'], ['This project', tool, 'tool'], ...(city != null ? [["City's mix", city, 'city']] : [])], max }
  }
  return [row('shade_summer_m2h', 'Summer shade', 'm²·h', 'more is better'), row('shade_winter_m2h', 'Winter shade', 'm²·h', 'less is better'),
    ...(L.interception_m3 ? [row('interception_m3', 'Rain held by the crowns', 'm³', 'more is better')] : [])].filter((r) => r.max > 0.01) // nothing to show
})
const trees = computed(() => (A.value ? A.value.idx.length + A.value.keptRows.length : 0))
const pal = computed(() => state.meta.palette)
const mix = computed(() => {
  const c = A.value?.counts ?? {}
  const tot = Object.values(c).reduce((a, b) => a + b, 0) || 1
  return Object.entries(c).filter(([, k]) => k > 0).sort((a, b) => b[1] - a[1])
    .map(([s, k]) => ({ s, k, w: (100 * k) / tot, color: pal.value.find((p) => p.species === s)?.color ?? '#999' }))
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
// plan: the area outline and its trees (new ones in their species colour, kept ones grey), fitted to a 300 x 220 box
const plan = computed(() => {
  if (!A.value) return null
  const P = state.trees.positions, K = state.trees.kept, lay = currentLayout(), repl = keptReplaced()
  const pts = A.value.poly
  const lat0 = pts[0][1], kx = Math.cos((lat0 * Math.PI) / 180)
  const xs = pts.map((q) => q[0] * kx), ys = pts.map((q) => q[1])
  const [x0, x1, y0, y1] = [Math.min(...xs), Math.max(...xs), Math.min(...ys), Math.max(...ys)]
  const s = Math.min(300 / (x1 - x0), 220 / (y1 - y0))
  const f = (lon, lat) => [(lon * kx - x0) * s + (300 - (x1 - x0) * s) / 2, (y1 - lat) * s + (220 - (y1 - y0) * s) / 2]
  const dots = [
    ...A.value.inPlanes.map((i) => ({ q: f(P.lon[i], P.lat[i]), c: pal.value[lay[i]]?.in_palette ? pal.value[lay[i]].color : '#9a968b', r: 3.2 })),
    ...A.value.keptIdx.map((k) => ({ q: f(K.lon[k], K.lat[k]), c: repl.has(k) ? pal.value[repl.get(k)].color : '#c9c4b8', r: 2.6 })),
    ...state.added.map((t) => ({ q: f(t.lon, t.lat), c: pal.value[t.species]?.color ?? '#3F663E', r: 3.2, ring: true })),
  ]
  return { d: 'M' + pts.map((q) => f(...q).map((v) => v.toFixed(1)).join(',')).join('L') + 'Z', dots }
})
const today = new Date().toLocaleDateString('en-GB', { day: 'numeric', month: 'long', year: 'numeric' })

// print the report alone: a new window with the page and the app's styles
const page = ref(null)
function printReport() {
  const w = window.open('', '_blank', 'width=900,height=1200')
  if (!w) return window.print() // pop-ups blocked: print the app view instead
  const styles = [...document.querySelectorAll('style, link[rel=stylesheet]')].map((e) => e.outerHTML).join('')
  w.document.write(`<!doctype html><html data-theme="light"><head><meta charset="utf-8"><title>Project area report</title>${styles}
    <style>body{background:#fff;margin:0}.report{position:static!important;max-width:none!important;padding:24px 28px!important;overflow:visible!important}
    @page{size:A4;margin:12mm}</style></head><body>${page.value.outerHTML}</body></html>`)
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
          <p class="muted">{{ state.meta.site.name }}, Barcelona · {{ today }} · Shade and sponge v0.2.0</p>
          <p class="muted small">{{ label(scenario) }} · Barcelona palette, 30 species</p>
        </div>
        <svg v-if="plan" class="plan" viewBox="0 0 300 220" role="img" aria-label="Plan of the area with its trees">
          <path :d="plan.d" class="outline" />
          <circle v-for="(t, i) in plan.dots" :key="i" :cx="t.q[0]" :cy="t.q[1]" :r="t.r" :fill="t.c" :stroke="t.ring ? '#2A2622' : 'none'" stroke-width="1" />
        </svg>
      </div>

      <section class="tiles">
        <div :class="rows.summer.d >= 0 ? 'up' : 'down'"><Icon name="sun" /><b>{{ rows.summer.d >= 0 ? '+' : '−' }}{{ n(rows.summer.p) }}%</b><span>summer shade</span></div>
        <div :class="rows.winter.d <= 0 ? 'up' : 'down'"><Icon name="sunlow" /><b>{{ rows.winter.d >= 0 ? '+' : '−' }}{{ n(rows.winter.p) }}%</b><span>winter shade</span></div>
        <div :class="rows.hot.d <= 0 ? 'up' : 'down'"><Icon name="drop" /><b>{{ short(1000 * rows.hot.d) }} L</b><span>{{ rows.hot.d <= 0 ? 'less' : 'more' }} water to flood spots</span></div>
        <div v-if="areaCover" :class="areaCover.now >= areaCover.today ? 'up' : 'down'"><Icon name="layers" /><b>{{ areaCover.now.toFixed(1) }}%</b><span>canopy, was {{ areaCover.today.toFixed(1) }}%</span></div>
      </section>

      <section>
        <h2>The area</h2>
        <p><template v-if="areaCover">{{ n(areaCover.area_m2) }} m², </template>{{ A.inPlanes.length + A.keptIdx.length }} street trees
          ({{ A.inPlanes.length }} plane trees), {{ A.spotIdx.length }} planting spots. <b>{{ trees }} trees are replaced</b><template v-if="state.added.length">
          and <b>{{ state.added.length }} new trees are planted</b></template>.</p>
        <p class="chips"><span v-for="u in better.up" :key="u" class="chip good">▲ {{ u }}</span><span v-for="d in better.down" :key="d" class="chip bad">▼ {{ d }}</span></p>
      </section>

      <section>
        <h2>Today, this project and the city's mix</h2>
        <div v-for="b in bars" :key="b.name" class="bars">
          <p class="bname"><b>{{ b.name }}</b> <span class="muted">· {{ b.unit }}, {{ b.good }}</span></p>
          <div v-for="[name, v, kind] in b.vals" :key="name" class="bar">
            <span class="bl">{{ name }}</span>
            <span class="track"><span :class="['fill', kind]" :style="{ width: (100 * v) / b.max + '%' }"></span></span>
            <span class="bv">{{ short(v) }}</span>
          </div>
        </div>
        <p class="small muted">{{ n(-1000 * rows.hot.d) }} litres {{ rows.hot.d <= 0 ? 'less' : 'more' }} water reach the flood hotspots in the
          2-year, 1-hour design storm<template v-if="rows.hot.c != null">; {{ n(-1000 * rows.hot.c) }} litres {{ rows.hot.c <= 0 ? 'less' : 'more' }} than the city's mix</template>.</p>
      </section>

      <section v-if="areaCover">
        <h2>Canopy cover</h2>
        <div class="gauge">
          <span class="g-today" :style="{ width: Math.min(100, (100 * areaCover.today) / 40) + '%' }"></span>
          <span class="g-now" :style="{ width: Math.min(100, (100 * areaCover.now) / 40) + '%' }"></span>
          <span class="g-target" :style="{ left: (100 * 30) / 40 + '%' }"><i>target 30%</i></span>
        </div>
        <p class="small muted">{{ areaCover.today.toFixed(1) }}% today → {{ areaCover.now.toFixed(1) }}% with this project ({{ short(areaCover.crowns_m2) }} m² of crowns).</p>
      </section>

      <section>
        <h2>Species planted <span class="muted">· {{ layoutEff?.toFixed(1) }} effective species</span></h2>
        <div class="mix"><span v-for="m in mix" :key="m.s" :style="{ width: m.w + '%', background: m.color }" :title="`${m.s}: ${m.k}`"></span></div>
        <ul class="mixlist"><li v-for="m in mix" :key="m.s"><span class="sw" :style="{ background: m.color }"></span><i>{{ m.s }}</i> {{ m.k }}</li></ul>
      </section>

      <section v-if="projectCost?.known && projectCost.total">
        <h2>Cost</h2>
        <p class="big">≈ € {{ n(projectCost.total) }}</p>
        <p class="small">{{ projectCost.n.replace + projectCost.n.add }} new trees, {{ projectCost.n.move }} transplants,
          {{ projectCost.n.object }} objects moved<template v-if="projectCost.perTree"> · € {{ n(projectCost.perTree) }} per tree</template><template
          v-if="projectCost.perShade"> · € {{ n(projectCost.perShade) }} per 1,000 m²·h of summer shade gained</template>.
          Direct costs (CYPE price base), no VAT or overhead, watering not priced.</p>
      </section>

      <section>
        <h2>Limits</h2>
        <p class="small muted">Estimates from single-tree potentials calibrated on full model runs. Heat is a shade proxy, not UTCI; runoff is
          the season-weighted 2-year, 1-hour design storm. New trees are scored at their established size. Validated for Porta (Barcelona).
          Free spots are an upper bound: check them on site. Method and data: github.com/giofox96/shade-and-sponge.</p>
      </section>
    </template>
    <p v-else>Draw a project area and run it to get the report.</p>
  </article>
</template>

<style scoped>
.report { position: absolute; inset: 0; overflow: auto; padding: 64px max(32px, calc(50% - 400px)) 120px 380px; background: var(--bg, #fff); line-height: 1.5; }
.top { display: flex; justify-content: space-between; gap: 20px; align-items: flex-start; }
h1 { font-size: 30px; margin: 0 0 4px; letter-spacing: -0.02em; }
h2 { font-size: 16px; margin: 22px 0 8px; }
.plan { width: 300px; height: 220px; flex: none; background: var(--panel); border-radius: 14px; }
.outline { fill: color-mix(in srgb, var(--accent) 8%, transparent); stroke: var(--accent); stroke-width: 1.5; }
.tiles { display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; margin-top: 18px; }
.tiles > div { position: relative; background: var(--panel); border-radius: 14px; padding: 14px; }
.tiles :deep(svg) { position: absolute; top: 12px; right: 12px; width: 20px; height: 20px; opacity: 0.55; }
.tiles b { display: block; font-size: 28px; letter-spacing: -0.02em; }
.tiles span { font-size: 12px; color: var(--muted); }
.tiles .up b { color: var(--good); } .tiles .down b { color: var(--bad); }
.chips { display: flex; flex-wrap: wrap; gap: 6px; }
.chip { font-size: 12px; padding: 3px 10px; border-radius: 999px; background: var(--panel); }
.chip.good { color: var(--good); } .chip.bad { color: var(--bad); }
.bars { margin-bottom: 12px; }
.bname { margin: 0 0 4px; font-size: 14px; }
.bar { display: grid; grid-template-columns: 110px 1fr 60px; align-items: center; gap: 8px; font-size: 13px; margin: 3px 0; }
.track { height: 14px; background: var(--panel); border-radius: 7px; overflow: hidden; }
.fill { display: block; height: 100%; border-radius: 7px; }
.fill.today { background: #9a968b; } .fill.tool { background: var(--good); } .fill.city { background: #8C6A24; }
.bv { text-align: right; font-variant-numeric: tabular-nums; }
.gauge { position: relative; height: 18px; background: var(--panel); border-radius: 9px; margin: 8px 0 22px; }
.gauge span { position: absolute; left: 0; top: 0; bottom: 0; border-radius: 9px; }
.g-now { background: var(--good); opacity: 0.85; } .g-today { background: #9a968b; z-index: 1; height: 6px; top: 6px !important; }
.g-target { width: 2px; background: var(--text); top: -4px !important; bottom: -4px !important; }
.g-target i { position: absolute; top: 24px; left: -30px; font-size: 11px; white-space: nowrap; font-style: normal; color: var(--muted); }
.mix { display: flex; height: 16px; border-radius: 8px; overflow: hidden; gap: 1px; }
.mixlist { list-style: none; padding: 0; columns: 2; font-size: 13px; margin: 8px 0 0; }
.sw { display: inline-block; width: 10px; height: 10px; border-radius: 50%; margin-right: 6px; }
.big { font-size: 26px; font-weight: 700; margin: 0; }
@media (max-width: 900px) { .report { padding: 64px 20px 120px; } .tiles { grid-template-columns: 1fr 1fr; } .top { flex-direction: column; } }
</style>
