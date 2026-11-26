<script setup>
// Headline numbers of the selected layout, compared with the current trees and with the mean city-practice layout (S1b).
import { computed } from 'vue'
import { state, scenario, baseline, calibration, shownMetrics, LIVE, AREA } from '../store.js'

const ROWS = [
  ['shade_summer_m2h', 'Summer shade', 'm²·h', 1],
  ['shade_winter_m2h', 'Winter shade', 'm²·h', -1],
  ['runoff_hot_m3', 'Runoff to hotspots', 'm³', -1],
  ['runoff_m3', 'Total runoff', 'm³', -1],
]
const s0 = computed(() => state.meta?.scenarios.find((s) => s.id === 'S0_current'))
const pct = (a, b) => (b ? (100 * (a / b - 1)) : 0)
const fmt = (v) => `${v > 0 ? '+' : ''}${v.toFixed(Math.abs(v) < 1 ? 1 : 0)}%`
const good = (v, sign) => (Math.abs(v) < 0.05 ? '' : v * sign > 0 ? 'good' : 'bad')

const rows = computed(() =>
  ROWS.map(([k, name, unit, sign]) => {
    const v = shownMetrics.value?.[k] ?? 0
    return { k, name, unit, sign, v, vs0: pct(v, s0.value?.metrics[k]), vcity: pct(v, baseline.value?.[k]) }
  }),
)
// the project area on its own: absolute values of the trees it replaces, today and after (street-segment scale)
const LOCAL = [
  ['shade_summer_m2h', 'Summer shade', 'm²·h', 1, true],
  ['shade_winter_m2h', 'Winter shade', 'm²·h', -1, true],
  ['interception_m3', 'Rain held by the crowns', 'm³', 1, true],
  ['runoff_hot_m3', 'Water reaching the flood hotspots', 'm³', -1, false],
  ['runoff_m3', 'Total runoff', 'm³', -1, false],
]
const local = computed(() => {
  const A = state.scenarioId === AREA ? state.area : null
  if (!A?.local) return null
  const n = A.idx.length + A.keptRows.length
  return { n, rows: LOCAL.filter(([k]) => A.local[k]).map(([k, name, unit, sign, own]) => {
    const { today, delta } = A.local[k]
    return { name, unit, sign, own, today, after: today + delta, delta, pct: own && today ? (100 * delta) / today : null, perTree: n ? (1000 * delta) / n : 0 }
  }) }
})
// the headline for a designer: how much less water reaches the flood hotspots in the design storm, in litres
const hotLitres = computed(() => (local.value ? -1000 * (state.area.local.runoff_hot_m3?.delta ?? 0) : null))
const num = (v) => v.toLocaleString('en', { maximumFractionDigits: Math.abs(v) < 100 ? 1 : 0 }) // small volumes keep a decimal
const sgn = (v) => `${v > 0 ? '+' : v < 0 ? '−' : '±'}${num(Math.abs(v))}`
const mix = computed(() => {
  const c = scenario.value?.counts ?? {}
  const n = Object.values(c).reduce((a, b) => a + b, 0)
  return state.meta.palette.filter((p) => c[p.species]).map((p) => ({ ...p, n: c[p.species], w: (100 * c[p.species]) / n }))
})
const isLive = computed(() => state.scenarioId === LIVE || state.scenarioId === AREA || state.added.length > 0)
const r2 = (k) => calibration.value?.[k]?.r2.toFixed(2)
const winterRange = computed(() => {
  const v = (state.meta?.sensitivity ?? []).map((r) => r.free_gain_winter_pct)
  return v.length ? [Math.min(...v), Math.max(...v)] : null
})
</script>

<template>
  <table class="kpi">
    <thead><tr><th></th><th>value</th><th>vs current</th><th title="Mean of the 10 city-practice layouts (the mix the city planted in place of planes 2018–2026, within the sizing rule)">vs city practice</th></tr></thead>
    <tbody>
      <tr v-for="r in rows" :key="r.name">
        <td>{{ r.name }}</td>
        <td class="num" :title="isLive ? `estimate: R² ${calibration[r.k].r2.toFixed(2)} on the saved layouts` : ''">{{ isLive ? '≈ ' : '' }}{{ Math.round(r.v).toLocaleString('en') }} <span class="u">{{ r.unit }}</span></td>
        <td class="num" :class="good(r.vs0, r.sign)">{{ fmt(r.vs0) }}</td>
        <td class="num" :class="good(r.vcity, r.sign)">{{ fmt(r.vcity) }}</td>
      </tr>
    </tbody>
  </table>
  <template v-if="local">
    <p class="sub">In the project area <span class="u">· its {{ local.n }} replaced trees on their own</span></p>
    <table class="kpi">
      <thead><tr><th></th><th>today</th><th>after</th><th>change</th></tr></thead>
      <tbody>
        <tr v-for="r in local.rows" :key="r.name">
          <td>{{ r.name }}</td>
          <td class="num">{{ r.own ? num(r.today) : '' }}</td>
          <td class="num">{{ r.own ? num(r.after) : '' }}</td>
          <td class="num" :class="good(r.delta, r.sign)">≈ {{ sgn(r.delta) }} <span class="u">{{ r.unit }}</span>
            <br><span class="u">{{ r.own ? `${r.pct > 0 ? '+' : ''}${r.pct.toFixed(0)}%` : `${sgn(r.perTree)} L per tree` }}</span></td>
        </tr>
      </tbody>
    </table>
    <p v-if="hotLitres != null" class="hot">
      <b :class="hotLitres > 0 ? 'good' : hotLitres < 0 ? 'bad' : ''">{{ num(Math.abs(Math.round(hotLitres))) }} litres {{ hotLitres >= 0 ? 'less' : 'more' }}</b>
      water reach the flood hotspots in the design storm (T2, 1 h, season-weighted), with these trees instead of today's.
    </p>
  </template>
  <div v-if="mix.length" class="mix" aria-label="Species mix of the replaced positions">
    <span v-for="m in mix" :key="m.species" :style="{ width: m.w + '%', background: m.color }" :title="`${m.species}: ${m.n}`"></span>
  </div>
  <p v-if="state.added.length" class="note live">Includes {{ state.added.length }} added tree{{ state.added.length > 1 ? 's' : '' }}, estimated with the same calibration.</p>
  <p v-if="state.scenarioId === AREA" class="note live">
    Project area: {{ state.area.all ? `all ${state.area.idx.length + state.area.keptIdx.length} trees` : `${state.area.idx.length} plane positions` }}
    replaced, today's trees everywhere else. "vs city practice" = the mix the city planted in place of planes 2018–2026, on the same positions (expected value).
    New trees are scored at the selected stage ({{ state.meta.run?.trunk_class === 'SEGONA' ? '≈ 10 years' : 'established' }}), today's at their measured
    size, so replacing young trees shows a gain that only arrives as the new ones grow. Estimates from single-tree potentials,
    calibrated on the saved layouts.
  </p>
  <p v-if="state.scenarioId === LIVE" class="note live">
    Live estimate in {{ state.live.ms }} ms: summed single-tree potentials, calibrated on the 16 saved layouts
    (R² summer {{ r2('shade_summer_m2h') }}, winter {{ r2('shade_winter_m2h') }}, hotspot runoff {{ r2('runoff_hot_m3') }}).
    Exact values need a run of the Python tool.
  </p>
  <p class="note">
    Heat is a shade proxy, not UTCI; runoff is the season-weighted T2-60 storm.
    <template v-if="winterRange">The winter gain of trading summer-only for balanced weights ranges {{ winterRange[1] }}% to {{ winterRange[0] }}% across the sensitivity runs.</template>
  </p>
</template>

<style scoped>
.kpi { width: 100%; border-collapse: collapse; font-size: 12px; }
.kpi th { font-weight: 500; color: var(--muted); text-align: right; padding: 2px 4px; }
.kpi td { padding: 4px; border-top: 0.5px solid var(--line); }
.num { text-align: right; white-space: nowrap; }
.u { color: var(--muted); font-size: 11px; }
.mix { display: flex; height: 10px; border-radius: 3px; overflow: hidden; margin: 10px 0 4px; gap: 1px; }
.sub { font-size: 12px; margin: 12px 0 4px; }
.hot { font-size: 12px; margin: 6px 0 0; }
.note.live { color: var(--accent); }
.note { font-size: 11px; color: var(--muted); margin: 6px 0 0; line-height: 1.45; }
</style>
