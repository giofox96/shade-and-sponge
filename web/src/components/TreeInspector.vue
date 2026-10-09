<script setup>
// Selected position: its context (sun, water) and what each palette species would deliver there.
import { computed } from 'vue'
import { state, MONTHS } from '../store.js'

const i = computed(() => state.selected)
const lay = computed(() => state.trees.layouts[state.scenarioId] ?? state.trees.layouts.S0_current)
const sp = computed(() => (i.value == null ? null : state.meta.palette[lay.value[i.value]]))
const p = computed(() => state.trees.positions)
const options = computed(() =>
  state.pot.species.map((name, j) => ({
    name,
    color: state.meta.palette[j].color,
    summer: state.pot.shade_summer[i.value][j],
    winter: state.pot.shade_winter[i.value][j],
    water: state.pot.water[i.value][j] * 1000,
    fits: state.pot.fit[i.value][j] === 1,
    chosen: sp.value?.species === name,
  })),
)
const pc = (v) => `${Math.round(100 * v)}%`
</script>

<template>
  <div v-if="i == null" class="empty">Click a tree on the map to see why it got its species.</div>
  <div v-else>
    <div class="head">
      <span class="dot" :style="{ background: sp.color }"></span>
      <b>{{ sp.species }}</b>
    </div>
    <div class="muted">Position {{ p.tree_id[i] }} · {{ sp.leaf_habit }}</div>
    <dl>
      <dt>Summer sun</dt><dd>{{ pc(p.sun_summer[i]) }} of 12–17 h</dd>
      <dt>Winter sun</dt><dd>{{ pc(p.sun_winter[i]) }} of 10–15 h</dd>
      <dt>Drains to hotspot</dt><dd>{{ pc(p.drains_to_hotspot[i]) }} of nearby ground</dd>
      <dt>Water convergence</dt><dd>{{ p.water_convergence_m2[i].toLocaleString('en') }} m² upstream</dd>
    </dl>
    <div class="leaf" :title="sp.leaf_basis">
      <span v-for="(f, m) in sp.leaf" :key="m" :class="{ now: m === state.month - 1 }">
        <i :style="{ height: 4 + 14 * f + 'px', background: sp.color }"></i>{{ MONTHS[m][0] }}
      </span>
    </div>
    <table class="opt">
      <thead><tr><th>If planted here</th><th>summer</th><th>winter</th><th>water</th></tr></thead>
      <tbody>
        <tr v-for="o in options" :key="o.name" :class="{ chosen: o.chosen, nofit: !o.fits }">
          <td><span class="dot" :style="{ background: o.color }"></span>{{ o.name.split(' ')[0] }}<span v-if="!o.fits" class="muted"> (no space)</span></td>
          <td>{{ Math.round(o.summer) }}</td><td>{{ Math.round(o.winter) }}</td><td>{{ Math.round(o.water) }}</td>
        </tr>
      </tbody>
    </table>
    <p class="muted small">Shade in m²·h on sunlit ground (summer is a benefit, winter a cost); water in litres intercepted per storm over ground that drains to a hotspot. Single-tree estimates, without overlaps.</p>
  </div>
</template>

<style scoped>
.empty { color: var(--muted); font-size: 12px; }
.head { display: flex; align-items: center; gap: 6px; font-size: 14px; }
.dot { display: inline-block; width: 9px; height: 9px; border-radius: 50%; margin-right: 4px; }
.muted { color: var(--muted); }
.small { font-size: 11px; line-height: 1.45; }
dl { display: grid; grid-template-columns: auto 1fr; gap: 2px 10px; font-size: 12px; margin: 8px 0; }
dt { color: var(--muted); }
dd { margin: 0; text-align: right; }
.leaf { display: flex; justify-content: space-between; align-items: flex-end; height: 32px; font-size: 10px; color: var(--muted); margin: 6px 0; }
.leaf span { display: flex; flex-direction: column; align-items: center; gap: 2px; width: 14px; }
.leaf i { width: 8px; border-radius: 2px; opacity: 0.8; }
.leaf .now { color: var(--text); font-weight: 500; }
.opt { width: 100%; border-collapse: collapse; font-size: 12px; margin-top: 4px; }
.opt th { font-weight: 500; color: var(--muted); text-align: right; padding: 2px 4px; }
.opt th:first-child, .opt td:first-child { text-align: left; }
.opt td { text-align: right; padding: 3px 4px; border-top: 0.5px solid var(--line); }
.opt tr.chosen td { background: var(--hover); font-weight: 500; }
.opt tr.nofit td { color: var(--muted); }
</style>
