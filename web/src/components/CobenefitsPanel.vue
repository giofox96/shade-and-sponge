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
const floors = computed(() => Object.entries(C.value?.floors ?? {}).map(([f, d]) => ({ f, r: d[state.scenarioId] })).filter((x) => x.r))
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
    <p v-for="x in floors" :key="x.f" class="note">
      With a diversity floor of {{ x.f }} effective species: {{ x.r.eff_species.toFixed(1) }} species,
      pollen {{ Math.round(x.r.pollen_lo) }}–{{ Math.round(x.r.pollen_hi) }}%, carbon {{ Math.round(x.r.carbon) }}% of today.
    </p>
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
.note { font-size: 11px; color: var(--muted); margin: 6px 0 0; line-height: 1.45; }
</style>
