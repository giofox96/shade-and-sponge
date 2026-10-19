<script setup>
// Selected tree: an existing plane position (index) or a designer-added tree ('a<k>'). Shows its context (sun, water)
// and what each palette species would deliver there; added trees can switch species or be removed.
import { computed } from 'vue'
import { state, MONTHS, currentLayout, setAddedSpecies, removeAdded } from '../store.js'

const added = computed(() => (typeof state.selected === 'string' ? Number(state.selected.slice(1)) : null))
const t = computed(() => (added.value != null ? state.added[added.value] : null))
const i = computed(() => (added.value == null ? state.selected : null))
const lay = computed(() => (state.live?.version, currentLayout()))
const sp = computed(() => {
  if (t.value) return state.meta.palette[t.value.species]
  return i.value == null ? null : state.meta.palette[lay.value[i.value]]
})
// context and potentials, from the exported positions or from the in-browser point calculation
const ctx = computed(() => {
  if (t.value) return { id: `new ${added.value + 1}`, ...t.value }
  const p = state.trees.positions
  return { id: p.tree_id[i.value], sun_summer: p.sun_summer[i.value], sun_winter: p.sun_winter[i.value],
    drains_to_hotspot: p.drains_to_hotspot[i.value], water_convergence_m2: p.water_convergence_m2[i.value] }
})
const options = computed(() =>
  state.pot.species.map((name, j) => {
    const P = t.value ? t.value.pot : { summer: state.pot.shade_summer[i.value], winter: state.pot.shade_winter[i.value],
      water: state.pot.water[i.value], fit: state.pot.fit[i.value] }
    return { j, name, color: state.meta.palette[j].color, summer: P.summer[j], winter: P.winter[j], water: P.water[j] * 1000,
      fits: P.fit[j] === 1, chosen: sp.value?.species === name }
  }),
)
const pc = (v) => `${Math.round(100 * v)}%`
</script>

<template>
  <div v-if="state.selected == null || !sp" class="empty">
    Click a tree on the map to see why it got its species{{ state.addMode ? ', or click open ground to add one' : '' }}.
  </div>
  <div v-else>
    <div class="head">
      <span class="dot" :style="{ background: sp.color }"></span>
      <b>{{ sp.species }}</b>
      <span v-if="t" class="badge">{{ t.auto ? 'added · recommended' : 'added · your choice' }}</span>
    </div>
    <div class="muted">{{ t ? 'New tree' : 'Position' }} {{ ctx.id }} · {{ sp.leaf_habit }}</div>
    <p v-for="w in t?.warn ?? []" :key="w" class="warn">{{ w }}</p>
    <dl>
      <dt>Summer sun</dt><dd>{{ pc(ctx.sun_summer) }} of 12–17 h</dd>
      <dt>Winter sun</dt><dd>{{ pc(ctx.sun_winter) }} of 10–15 h</dd>
      <dt>Drains to hotspot</dt><dd>{{ pc(ctx.drains_to_hotspot) }} of nearby ground</dd>
      <template v-if="ctx.water_convergence_m2 != null">
        <dt>Water convergence</dt><dd>{{ ctx.water_convergence_m2.toLocaleString('en') }} m² upstream</dd>
      </template>
    </dl>
    <div class="leaf" :title="sp.leaf_basis">
      <span v-for="(f, m) in sp.leaf" :key="m" :class="{ now: m === state.month - 1 }">
        <i :style="{ height: 4 + 14 * f + 'px', background: sp.color }"></i>{{ MONTHS[m][0] }}
      </span>
    </div>
    <table class="opt">
      <thead><tr><th>If planted here</th><th>summer</th><th>winter</th><th>water</th></tr></thead>
      <tbody>
        <tr v-for="o in options" :key="o.name" :class="{ chosen: o.chosen, nofit: !o.fits, pick: t && o.fits }"
            @click="t && o.fits && setAddedSpecies(added, o.j)">
          <td><span class="dot" :style="{ background: o.color }"></span>{{ o.name.split(' ').slice(0, 2).join(' ') }}<span v-if="!o.fits" class="muted"> (no space)</span></td>
          <td>{{ Math.round(o.summer) }}</td><td>{{ Math.round(o.winter) }}</td><td>{{ Math.round(o.water) }}</td>
        </tr>
      </tbody>
    </table>
    <p class="muted small">Shade in m²·h on sunlit ground (summer is a benefit, winter a cost); water in litres intercepted per storm over ground that drains to a hotspot. Single-tree estimates, without overlaps.<template v-if="t"> Click a row to plant that species.</template></p>
    <div v-if="t" class="btns">
      <button v-if="!t.auto" @click="setAddedSpecies(added, null)">Use recommended</button>
      <button @click="removeAdded(added)">Remove tree</button>
    </div>
  </div>
</template>

<style scoped>
.empty { color: var(--muted); font-size: 12px; }
.head { display: flex; align-items: center; gap: 6px; font-size: 14px; flex-wrap: wrap; }
.badge { font-size: 11px; background: var(--hover); color: var(--accent); padding: 1px 6px; border-radius: 4px; }
.warn { font-size: 11px; color: #854f0b; background: #faeeda; padding: 3px 6px; border-radius: 4px; margin: 4px 0; }
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
.opt tr.pick { cursor: pointer; }
.opt tr.pick:hover td { background: var(--hover); }
.btns { display: flex; gap: 6px; margin-top: 8px; }
</style>
