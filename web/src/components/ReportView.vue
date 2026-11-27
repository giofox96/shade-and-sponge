<script setup>
// One-page report of the project area (v0.2.0, step 7): scripted sentences from the numbers on screen, no LLM; printable.
import { computed } from 'vue'
import { state, areaCover, layoutEff, label, scenario, projectCost } from '../store.js'

const A = computed(() => state.area)
const s0 = computed(() => state.meta.scenarios.find((s) => s.id === 'S0_current').metrics)
const n = (v, d = 0) => Math.abs(v).toLocaleString('en', { maximumFractionDigits: d })
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
const trees = computed(() => (A.value ? A.value.idx.length + A.value.keptRows.length : 0))
const mix = computed(() => Object.entries(A.value?.counts ?? {}).filter(([, k]) => k > 0).sort((a, b) => b[1] - a[1]))
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
const today = new Date().toLocaleDateString('en-GB', { day: 'numeric', month: 'long', year: 'numeric' })
</script>

<template>
  <article class="report">
    <template v-if="A && rows">
      <h1>Project area report</h1>
      <p class="muted">{{ state.meta.site.name }}, Barcelona · {{ today }} · Shade and sponge v0.2.0 · {{ label(scenario) }} ·
        palette {{ state.meta.palette_kind === 'barcelona' ? 'Barcelona (30 species)' : 'City (7 species)' }}</p>

      <h2>The area</h2>
      <p><template v-if="areaCover">{{ n(areaCover.area_m2) }} m², </template>{{ A.inPlanes.length + A.keptIdx.length }} street trees
        ({{ A.inPlanes.length }} plane trees), {{ A.spotIdx.length }} planting spots. {{ trees }} trees are replaced<template v-if="state.added.length">
        and {{ state.added.length }} new trees are planted</template>.</p>

      <h2>What changes</h2>
      <ul>
        <li><b>Summer shade {{ rows.summer.d >= 0 ? '+' : '−' }}{{ n(rows.summer.p) }}%</b> compared with today's trees in the area
          ({{ rows.summer.d >= 0 ? '+' : '−' }}{{ n(rows.summer.d) }} m²·h on a hot day)<template v-if="rows.summer.c != null">;
          {{ n(rows.summer.c) }} m²·h {{ rows.summer.c >= 0 ? 'more' : 'less' }} than the city's practice on the same positions</template>.</li>
        <li><b>Winter sun:</b> winter shade {{ rows.winter.d >= 0 ? 'rises' : 'falls' }} by {{ n(rows.winter.p) }}% ({{ n(rows.winter.d) }} m²·h)<template v-if="rows.winter.c != null">;
          {{ n(rows.winter.c) }} m²·h {{ rows.winter.c >= 0 ? 'more' : 'less' }} than the city's practice</template>.</li>
        <li><b v-if="Math.abs(rows.hot.d) < 0.001">No change in the water reaching the flood hotspots</b><b v-else>{{ n(-1000 * rows.hot.d) }} litres {{ rows.hot.d < 0 ? 'less' : 'more' }} water reach the flood hotspots</b> in the design
          storm (2-year, 1 hour)<template v-if="rows.hot.c != null">; {{ n(-1000 * rows.hot.c) }} litres {{ rows.hot.c <= 0 ? 'less' : 'more' }} than the city's practice</template>.
          The crowns hold {{ n(rows.rain.d, 1) }} m³ {{ rows.rain.d >= 0 ? 'more' : 'less' }} rain.</li>
        <li v-if="areaCover"><b>Canopy cover {{ areaCover.today.toFixed(1) }}% → {{ areaCover.now.toFixed(1) }}%</b> of the area (target 30%).</li>
      </ul>
      <p><b>Better:</b> {{ better.up.join(', ') || 'nothing' }}. <b>Worse:</b> {{ better.down.join(', ') || 'nothing' }}.</p>

      <template v-if="projectCost?.known && projectCost.total">
        <h2>Cost</h2>
        <p>≈ € {{ n(projectCost.total) }} ({{ projectCost.n.replace + projectCost.n.add }} new trees, {{ projectCost.n.move }} transplants,
          {{ projectCost.n.object }} objects moved)<template v-if="projectCost.perTree">, € {{ n(projectCost.perTree) }} per tree</template><template
          v-if="projectCost.perShade">, € {{ n(projectCost.perShade) }} per 1,000 m²·h of summer shade gained</template>. Unit prices entered by the user.</p>
      </template>

      <h2>Species</h2>
      <p>{{ mix.map(([s, k]) => `${s} ${k}`).join(' · ') }}. Diversity: {{ layoutEff?.toFixed(1) }} effective species.</p>

      <h2>Limits</h2>
      <p class="small">Estimates from single-tree potentials calibrated on full model runs. Heat is a shade proxy, not UTCI; runoff is the
        season-weighted 2-year, 1-hour design storm. New trees are scored at their established size. Validated for Porta (Barcelona).
        Free spots are an upper bound: check them on site. Method and data: github.com/giofox96/shade-and-sponge.</p>
    </template>
    <p v-else>Draw a project area and run it (steps 1–5) to get the report.</p>
  </article>
</template>

<style scoped>
.report { position: absolute; inset: 0; overflow: auto; padding: 56px 32px 32px; background: var(--bg, #fff); max-width: 820px; line-height: 1.5; }
h1 { font-size: 22px; margin: 0 0 4px; }
h2 { font-size: 15px; margin: 18px 0 4px; }
ul { padding-left: 18px; }
@media print {
  .report { position: static; padding: 0; max-width: none; }
}
</style>
