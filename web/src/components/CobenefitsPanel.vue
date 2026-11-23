<script setup>
// Co-benefits of the selected layout: reported, not optimised (scripts/cobenefits.py, notes/cobenefits_plan.md). Only sites
// whose meta.json has a `cobenefits` entry (scripts/web_export_cobenefits.py: Barcelona palette, established trees).
import { computed } from 'vue'
import { state } from '../store.js'

const C = computed(() => state.meta?.cobenefits)
const COLS = [['this', 'this layout'], ['S1a_city_0', 'city 2026 mix'], ['S1b_obs_0', 'city practice']]
const cols = computed(() => COLS.map(([id, name]) => ({ name, r: C.value?.base[id === 'this' ? state.scenarioId : id] })))
const ROWS = [
  ['Tree diversity', 'effective species', (r) => r.eff_species.toFixed(1), 'Effective number of species, exp(Shannon), over the replaced positions; today = 1 (all planes)'],
  ['Pollen load', '% of today', (r) => `${Math.round(r.pollen_lo)}–${Math.round(r.pollen_hi)}`,
    'Allergenic load (Cariñanos et al. 2014), as a range: species without a published score counted as 0 and as the scale maximum'],
  ['Carbon stock', '% of today', (r) => Math.round(r.carbon), 'Above-ground carbon from height × crown (Jucker et al. 2017), at the same trunk class as the shade results'],
]
// every diversity floor run for the selected weights, with the no-floor run first (the layouts on the map are the no-floor ones)
const floors = computed(() => {
  const id = state.scenarioId, b = C.value?.base[id]
  if (!b || !id.startsWith('S4')) return []
  return [{ f: 'none', r: b }, ...Object.entries(C.value.floors ?? {}).sort(([a], [b]) => a - b) // integer-like keys ('10', '20') come first in JS objects
    .map(([f, d]) => ({ f, r: d[id] })).filter((x) => x.r)]
})
</script>

<template>
  <template v-if="C">
    <p v-if="!cols[0].r" class="note">Shown for today, the saved optimised layouts and draw #0 of the city layouts; select one of those.</p>
    <table v-else class="kpi">
      <thead><tr><th></th><th v-for="c in cols" :key="c.name">{{ c.name }}</th></tr></thead>
      <tbody>
        <tr v-for="[name, unit, f, tip] in ROWS" :key="name" :title="tip">
          <td>{{ name }} <span class="u">{{ unit }}</span></td>
          <td v-for="c in cols" :key="c.name" class="num">{{ c.r ? f(c.r) : '–' }}</td>
        </tr>
      </tbody>
    </table>
    <template v-if="floors.length > 1">
      <h4>Diversity floor: what each minimum costs</h4>
      <table class="kpi">
        <thead><tr><th>floor</th><th>species</th><th>summer shade</th><th>pollen</th><th>carbon</th></tr></thead>
        <tbody>
          <tr v-for="x in floors" :key="x.f">
            <td>{{ x.f === 'none' ? 'none (map)' : x.f }}</td>
            <td class="num">{{ x.r.eff_species.toFixed(1) }}</td>
            <td class="num">{{ x.r.summer != null ? x.r.summer.toFixed(1) + '%' : '–' }}</td>
            <td class="num">{{ Math.round(x.r.pollen_lo) }}–{{ Math.round(x.r.pollen_hi) }}%</td>
            <td class="num">{{ Math.round(x.r.carbon) }}%</td>
          </tr>
        </tbody>
      </table>
      <p class="note">Same weights, optimised again with a minimum number of effective species (exp of Shannon diversity).
        9.4 = the city's 2026 mix, 10 = Santamour's 10% species cap (1 / 0.10), 15.6 = what the city actually plants, 20 = test.
        All % of today. The city's layouts reach 96–97% summer shade.</p>
    </template>
    <p class="note">Evaluation indicators, not optimised. Today's planes = 100%.</p>
  </template>
  <p v-else class="note">Co-benefits are computed for the Barcelona palette with established trees only.</p>
</template>

<style scoped>
.kpi { width: 100%; border-collapse: collapse; font-size: 12px; }
.kpi th { font-weight: 500; color: var(--muted); text-align: right; padding: 2px 4px; }
.kpi td { padding: 4px; border-top: 0.5px solid var(--line); }
.num { text-align: right; white-space: nowrap; }
.u { color: var(--muted); font-size: 11px; display: block; }
h4 { font-size: 12px; font-weight: 500; margin: 12px 0 4px; }
.note { font-size: 11px; color: var(--muted); margin: 6px 0 0; line-height: 1.45; }
</style>
