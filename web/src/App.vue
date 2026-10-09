<script setup>
import { onMounted, watch } from 'vue'
import { state, load, switchSite, scenario, label, runLive, setAddMode, addedCsv, MIN_SPACING_M, MONTHS, BALANCED, LIVE } from './store.js'
import MapView from './components/MapView.vue'
import PriorityTriangle from './components/PriorityTriangle.vue'
import TradeoffChart from './components/TradeoffChart.vue'
import KpiPanel from './components/KpiPanel.vue'
import TreeInspector from './components/TreeInspector.vue'

onMounted(() => load())

function downloadAdded() {
  const a = Object.assign(document.createElement('a'), { download: `added_trees_${state.site}.csv`,
    href: URL.createObjectURL(new Blob([addedCsv()], { type: 'text/csv' })) })
  a.click()
  URL.revokeObjectURL(a.href)
}
function clearAdded() {
  state.added = []
  state.selected = null
  state.addedVersion++
}

// Constraints changed: re-optimise live with the weights on screen (live or a precomputed optimised layout)
watch(
  () => [state.share, state.exclude.length],
  () => {
    const w = state.scenarioId === LIVE ? state.live?.weights : scenario.value?.weights
    if (w) runLive(w)
  },
)
</script>

<template>
  <div v-if="state.error" class="msg">{{ state.error }}</div>
  <div v-else-if="!state.meta" class="msg">Loading site…</div>
  <div v-else class="app">
    <header>
      <b>Shade and sponge</b>
      <span class="muted">Street-tree replacement in {{ state.meta.site.name }}, Barcelona · 832 plane-tree positions</span>
      <span class="spacer"></span>
      <span class="seg" role="group" aria-label="Species palette">
        <button :class="{ on: state.site === 'porta' }" @click="switchSite('porta')">City palette (6)</button>
        <button :class="{ on: state.site === 'porta-barcelona' }" @click="switchSite('porta-barcelona')">Barcelona shortlist</button>
      </span>
      <span class="muted">{{ label(scenario) }}</span>
    </header>

    <aside class="left">
      <section>
        <h3>Layout</h3>
        <div class="btns">
          <button :class="{ on: state.scenarioId === 'S0_current' }" @click="state.scenarioId = 'S0_current'">Current trees</button>
          <button :class="{ on: state.scenarioId === 'S1_random_0' }" @click="state.scenarioId = 'S1_random_0'">Random palette</button>
          <button :class="{ on: state.scenarioId.startsWith('S4') }" @click="state.scenarioId = BALANCED">Optimised</button>
        </div>
      </section>
      <section>
        <h3>Priorities</h3>
        <PriorityTriangle />
        <p class="muted small">Dots: precomputed optimal layouts (exact scores; blue = on the trade-off front). Click anywhere else to re-optimise live in your browser (estimate).</p>
        <p v-if="state.busy" class="small accent">Optimising…</p>
        <p v-if="state.liveError" class="small danger">{{ state.liveError }}</p>
      </section>
      <section>
        <h3>Design <span class="muted">{{ state.added.length }} added</span></h3>
        <div class="btns">
          <button :class="{ on: state.addMode }" @click="setAddMode(!state.addMode)">{{ state.addMode ? 'Stop adding' : 'Add trees' }}</button>
          <button v-if="state.added.length" @click="downloadAdded">Download CSV</button>
          <button v-if="state.added.length" @click="clearAdded">Clear</button>
        </div>
        <p v-if="state.addMode" class="muted small">Click open ground on the map. Each new tree gets the best species for the current priorities (change it in the inspector); live re-optimisation includes it. Warns under {{ MIN_SPACING_M }} m from another tree (assumption). No sidewalk data yet: you decide where planting is possible.</p>
        <p v-if="state.addMsg" class="small accent">{{ state.addMsg }}</p>
      </section>
      <section>
        <h3>Max share per species <span class="muted">{{ Math.round(state.share * 100) }}%</span></h3>
        <input type="range" min="0.05" max="0.3" step="0.01" v-model.number="state.share" />
        <p class="muted small">Of all {{ state.pot.n_total.toLocaleString('en') }} street trees, as in the city tree plan (15%). Changing it re-optimises live.</p>
      </section>
      <section>
        <h3>Map layer</h3>
        <select v-model="state.overlay">
          <option value="">None</option>
          <option v-for="o in state.meta.overlays" :key="o.id" :value="o.id">{{ o.label }}</option>
        </select>
      </section>
      <section>
        <h3>Month <span class="muted">{{ MONTHS[state.month - 1] }}</span></h3>
        <input type="range" min="1" max="12" step="1" v-model.number="state.month" />
        <p class="muted small">Crown opacity follows each species' leaf calendar.</p>
      </section>
      <section>
        <h3>Species <span class="muted">untick to exclude</span></h3>
        <p v-if="state.meta.palette_kind === 'barcelona'" class="muted small">Colour = leaf habit (blue deciduous, orange evergreen, violet semi-deciduous); darker = larger crown.</p>
        <ul class="legend">
          <li v-for="p in state.meta.palette" :key="p.species">
            <input v-if="p.in_palette" type="checkbox" :value="p.species" :checked="!state.exclude.includes(p.species)"
                   :aria-label="`Allow ${p.species}`"
                   @change="state.exclude = $event.target.checked ? state.exclude.filter((x) => x !== p.species) : [...state.exclude, p.species]" />
            <span class="dot" :style="{ background: p.color }"></span>{{ p.species }}
            <span class="muted">{{ p.in_palette ? p.leaf_habit.split(' ')[0] : 'current' }}</span>
          </li>
        </ul>
      </section>
      <section class="sources small muted">
        <h3>Data and sources</h3>
        Street trees, neighbourhoods: Ajuntament de Barcelona, Open Data BCN (CC BY 4.0) ·
        LiDAR crowns, terrain, building heights: ICGC 2021–2022 (CC BY 4.0) ·
        Building footprints and basemap: © OpenStreetMap contributors (ODbL), OpenFreeMap ·
        Flood-hazard index: Barcelona Resilience Atlas, Barcelona Regional (shown as a derived threshold; licence not stated) ·
        Design storms: PDISBA rainfall study · Storm months: Esbrí, Rigo and Llasat 2026 ·
        Interception calibration: Anys and Weiler 2024 data (CC BY-NC 4.0).
        Thesis prototype (MaCAD, IAAC); heat is a shade proxy, not UTCI.
        <a href="https://github.com/giofox96/shade-and-sponge" target="_blank" rel="noopener">Code and method</a>
      </section>
    </aside>

    <main><MapView :key="state.site" /></main>

    <aside class="right">
      <section><h3>Results</h3><KpiPanel /></section>
      <section><h3>Trade-off</h3><TradeoffChart /></section>
      <section><h3>Selected tree</h3><TreeInspector /></section>
    </aside>
  </div>
</template>
