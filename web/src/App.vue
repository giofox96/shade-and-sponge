<script setup>
import { onMounted, watch } from 'vue'
import { state, load, switchSite, scenario, label, layoutEff, runLive, runArea, setAddMode, addedCsv, startDrawing, finishArea,
  cancelDrawing, clearArea, MIN_SPACING_M, MONTHS, BALANCED, LIVE, AREA } from './store.js'
import MapView from './components/MapView.vue'
import PriorityTriangle from './components/PriorityTriangle.vue'
import TradeoffChart from './components/TradeoffChart.vue'
import KpiPanel from './components/KpiPanel.vue'
import TreeInspector from './components/TreeInspector.vue'
import ComparePanel from './components/ComparePanel.vue'
import CoverCounter from './components/CoverCounter.vue'

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
  () => [state.share, state.exclude.length, state.minEff],
  () => {
    const w = state.scenarioId === LIVE || state.scenarioId === AREA ? scenario.value?.weights : scenario.value?.weights
    if (w) state.scenarioId === AREA ? runArea(w) : runLive(w)
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
        <button :class="{ on: state.site !== 'porta-barcelona' }" @click="switchSite('porta')">City palette (7)</button>
        <button :class="{ on: state.site === 'porta-barcelona' }" @click="switchSite('porta-barcelona')">Barcelona shortlist</button>
      </span>
      <span v-if="state.site !== 'porta-barcelona'" class="seg" role="group" aria-label="Size of the replacement trees">
        <button :class="{ on: state.site === 'porta-segona' }" aria-label="About 10 years after planting" title="Second trunk class (41–80 cm perimeter): median 9.7 years after planting for the dated palette trees"
                @click="switchSite('porta-segona')">≈ 10 years</button>
        <button :class="{ on: state.site === 'porta' }" aria-label="Established trees" title="Third trunk class (81–110 cm perimeter): the thesis comparison at equal trunk size"
                @click="switchSite('porta')">Established</button>
      </span>
      <span class="muted">{{ label(scenario) }}</span>
    </header>

    <aside class="left">
      <section>
        <h3>Layout</h3>
        <div class="btns">
          <button :class="{ on: state.scenarioId === 'S0_current' }" @click="state.scenarioId = 'S0_current'">Current trees</button>
          <button :class="{ on: state.scenarioId === 'S1a_city_0' }" @click="state.scenarioId = 'S1a_city_0'">City rule</button>
          <button :class="{ on: state.scenarioId === 'S1_random_0' }" @click="state.scenarioId = 'S1_random_0'">Random palette</button>
          <button :class="{ on: state.scenarioId.startsWith('S4') }" @click="state.scenarioId = BALANCED">Optimised</button>
          <button v-if="state.area" :class="{ on: state.scenarioId === AREA }" @click="state.scenarioId = AREA">Project area</button>
        </div>
        <div class="btns">
          <button :class="{ on: state.compare }" :aria-pressed="state.compare" @click="state.compare = !state.compare">{{ state.compare ? 'Back to the map' : 'Compare side by side' }}</button>
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
        <h3>Project area <span class="muted">{{ state.area ? `${state.area.idx.length} planes` : 'whole site' }}</span></h3>
        <div class="btns">
          <button v-if="!state.drawing" @click="startDrawing">{{ state.area ? 'Redraw area' : 'Draw area' }}</button>
          <button v-if="state.drawing" :disabled="state.draft.length < 3" @click="finishArea">Finish ({{ state.draft.length }} corners)</button>
          <button v-if="state.drawing" @click="cancelDrawing">Cancel</button>
          <button v-if="state.area && !state.drawing" @click="clearArea">Whole site</button>
        </div>
        <p class="muted small">Trees are replaced only where a project, a dead tree or a street rebuild opens the ground. Draw that area:
          only the plane positions inside are replaced and compared; today's trees stay everywhere else.</p>
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
        <h3>Diversity floor <span class="muted">{{ state.minEff ? `≥ ${state.minEff} effective species` : 'off' }}</span></h3>
        <label class="small"><input type="checkbox" :checked="state.minEff > 0"
               @change="state.minEff = $event.target.checked ? Math.min(8, state.pot.species.length - state.exclude.length - 1) : 0" />
          Keep a minimum Shannon diversity</label>
        <input v-if="state.minEff" type="range" min="2" :max="state.pot.species.length - state.exclude.length" step="1" v-model.number="state.minEff"
               aria-label="Minimum effective number of species" />
        <p class="muted small">Effective number of species = exp(Shannon H) of the replanted positions. This layout: {{ layoutEff?.toFixed(1) }}. Changing it re-optimises live.</p>
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

    <main><ComparePanel v-if="state.compare" /><MapView v-else :key="state.site" /></main>

    <aside class="right">
      <section><h3>Canopy cover</h3><CoverCounter /></section>
      <section><h3>Results</h3><KpiPanel /></section>
      <section><h3>Trade-off</h3><TradeoffChart /></section>
      <section><h3>Selected tree</h3><TreeInspector /></section>
    </aside>
  </div>
</template>
