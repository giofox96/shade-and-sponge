<script setup>
// Headline numbers of the selected layout, compared with the current trees and with the mean random palette.
import { computed } from 'vue'
import { state, scenario, randomMean, calibration, shownMetrics, LIVE } from '../store.js'

const ROWS = [   // the marker carries the deck's meaning colour: ochre = sun / shade, ink blue = water
  ['shade_summer_m2h', 'Summer shade', 'm²·h', 1, 'var(--sun-fill)'],
  ['shade_winter_m2h', 'Winter shade', 'm²·h', -1, 'var(--sun-fill)'],
  ['runoff_hot_m3', 'Runoff to hotspots', 'm³', -1, 'var(--water)'],
  ['runoff_m3', 'Total runoff', 'm³', -1, 'var(--water)'],
]
const s0 = computed(() => state.meta?.scenarios.find((s) => s.id === 'S0_current'))
const pct = (a, b) => (b ? (100 * (a / b - 1)) : 0)
const fmt = (v) => `${v > 0 ? '+' : ''}${v.toFixed(Math.abs(v) < 1 ? 1 : 0)}%`
const good = (v, sign) => (Math.abs(v) < 0.05 ? '' : v * sign > 0 ? 'good' : 'bad')

const rows = computed(() =>
  ROWS.map(([k, name, unit, sign, color]) => {
    const v = shownMetrics.value?.[k] ?? 0
    return { k, name, unit, sign, color, v, vs0: pct(v, s0.value?.metrics[k]), vrnd: pct(v, randomMean.value?.[k]) }
  }),
)
const mix = computed(() => {
  const c = scenario.value?.counts ?? {}
  const n = Object.values(c).reduce((a, b) => a + b, 0)
  return state.meta.palette.filter((p) => c[p.species]).map((p) => ({ ...p, n: c[p.species], w: (100 * c[p.species]) / n }))
})
const isLive = computed(() => state.scenarioId === LIVE || state.added.length > 0)
const r2 = (k) => calibration.value?.[k]?.r2.toFixed(2)
const winterRange = computed(() => {
  const v = (state.meta?.sensitivity ?? []).map((r) => r.free_gain_winter_pct)
  return v.length ? [Math.min(...v), Math.max(...v)] : null
})
</script>

<template>
  <table class="kpi">
    <thead><tr><th></th><th>value</th><th>vs current</th><th>vs random</th></tr></thead>
    <tbody>
      <tr v-for="r in rows" :key="r.name">
        <td><i class="mark" :style="{ background: r.color }"></i>{{ r.name }}</td>
        <td class="num" :title="isLive ? `estimate: R² ${calibration[r.k].r2.toFixed(2)} on the saved layouts` : ''">{{ isLive ? '≈ ' : '' }}{{ Math.round(r.v).toLocaleString('en') }} <span class="u">{{ r.unit }}</span></td>
        <td class="num" :class="good(r.vs0, r.sign)">{{ fmt(r.vs0) }}</td>
        <td class="num" :class="good(r.vrnd, r.sign)">{{ fmt(r.vrnd) }}</td>
      </tr>
    </tbody>
  </table>
  <div v-if="mix.length" class="mix" aria-label="Species mix of the replaced positions">
    <span v-for="m in mix" :key="m.species" :style="{ width: m.w + '%', background: m.color }" :title="`${m.species}: ${m.n}`"></span>
  </div>
  <p v-if="state.added.length" class="note live">Includes {{ state.added.length }} added tree{{ state.added.length > 1 ? 's' : '' }}, estimated with the same calibration.</p>
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
.kpi th { font: 400 10px var(--mono); letter-spacing: 0.06em; text-transform: uppercase; color: var(--muted); text-align: right; padding: 2px 4px; }
.kpi td { padding: 4px; border-top: 0.5px solid var(--line); }
.num { text-align: right; white-space: nowrap; }
.u { color: var(--muted); font-size: 10px; }
.mark { display: inline-block; width: 3px; height: 11px; border-radius: 1px; margin-right: 6px; vertical-align: -1px; }
.good { color: var(--accent); }
.good::before { content: '✓ '; font-size: 9px; }
.bad { color: var(--heat); }
.bad::before { content: '✕ '; font-size: 9px; }
.mix { display: flex; height: 10px; border-radius: 3px; overflow: hidden; margin: 10px 0 4px; gap: 1px; }
.note.live { color: var(--accent); }
.note { font-size: 11px; color: var(--muted); margin: 6px 0 0; line-height: 1.45; }
</style>
