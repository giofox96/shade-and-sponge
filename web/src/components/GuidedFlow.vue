<script setup>
// v0.2.0 guided flow (notes/tutor_feedback_24nov.md §3e): the same functions as expert mode, one step at a time.
// Every step only calls what the expert panel already calls; "Expert mode" in the header shows all settings at once.
import { computed, watch } from 'vue'
import { download } from '../exporter.js'
import { state, ui, startDrawing, finishArea, cancelDrawing, setAreaAll, fillAreaSpots, fillableSpots, spotClass, areaCover,
  layoutEff, configJson, switchSite, AREA } from '../store.js'
import BarriPicker from './BarriPicker.vue'
import PriorityTriangle from './PriorityTriangle.vue'
import KpiPanel from './KpiPanel.vue'
import CoverCounter from './CoverCounter.vue'

const STEPS = ['Project area', 'Today', 'Trees to act on', 'Priorities', 'Result', 'Compare', 'Report', 'Save and export']
const A = computed(() => state.area)
const canNext = computed(() => ui.step > 0 || !!A.value)
const go = (k) => (ui.step = Math.max(0, Math.min(STEPS.length - 1, k)))

// what each step shows on the map and in the views
watch(() => ui.step, (k) => {
  if (k === 1) Object.assign(state, { scenarioId: 'S0_current', showStreets: true })
  if (k >= 2 && k <= 5 && A.value?.metrics) state.scenarioId = AREA
  if (k === 2) state.showSchedule = true
  if (k === 6) state.showSchedule = false // the report page needs the whole view
  state.view = k === 6 ? 'report' : state.view === 'report' ? 'map' : state.view
}, { immediate: true })

const spots = computed(() => {
  if (!A.value) return null
  const c = { free: 0, conditional: 0, blocked: 0 }
  A.value.spotIdx.forEach((s) => (c[spotClass(s)] = (c[spotClass(s)] ?? 0) + 1))
  return c
})
const msg = computed(() => state.addMsg)
const printReport = () => window.print()
function saveCfg() {
  const a = Object.assign(document.createElement('a'), { download: `shade_sponge_${state.site}_config.json`,
    href: URL.createObjectURL(new Blob([configJson()], { type: 'application/json' })) })
  a.click()
  URL.revokeObjectURL(a.href)
}
</script>

<template>
  <nav class="steps" aria-label="Steps">
    <ol>
      <li v-for="(s, k) in STEPS" :key="s" :class="{ on: ui.step === k, done: k < ui.step }">
        <button :disabled="k > 0 && !A" :aria-current="ui.step === k ? 'step' : null" @click="go(k)">{{ k + 1 }} · {{ s }}</button>
      </li>
    </ol>
  </nav>

  <section v-if="ui.step === 0">
    <h3>1 · Choose the place and draw the project area</h3>
    <BarriPicker />
    <p class="small">Click on the map to place the corners of the street or block you are working on; right-click, Enter or
      "Finish" closes it. Only the trees inside are replaced and compared; today's trees stay everywhere else.</p>
    <div class="btns">
      <button v-if="!state.drawing" @click="startDrawing">{{ A ? 'Redraw the area' : 'Draw the area' }}</button>
      <button v-if="state.drawing" :disabled="state.draft.length < 3" @click="finishArea">Finish ({{ state.draft.length }} corners)</button>
      <button v-if="state.drawing" @click="cancelDrawing">Cancel</button>
    </div>
    <p v-if="msg" class="small accent">{{ msg }}</p>
    <p v-if="A" class="small good">Area set: {{ A.inPlanes.length }} plane trees, {{ A.keptIdx.length }} other street trees, {{ A.spotIdx.length }} spots.</p>
  </section>

  <section v-else-if="ui.step === 1 && A">
    <h3>2 · What is there today</h3>
    <ul class="facts">
      <li><b>{{ A.inPlanes.length + A.keptIdx.length }}</b> street trees, of which <b>{{ A.inPlanes.length }}</b> plane trees</li>
      <li v-if="spots"><b>{{ spots.free }}</b> free spots, <b>{{ spots.conditional }}</b> conditional (an object or a buried service in the way), <b>{{ spots.blocked ?? 0 }}</b> blocked</li>
      <li v-if="areaCover"><b>{{ areaCover.today.toFixed(1) }}%</b> canopy cover in the area ({{ Math.round(areaCover.area_m2).toLocaleString('en') }} m²); the plan's target is 30%</li>
    </ul>
    <p class="small muted">The map shows today's trees. Click a tree or a spot to see it in the schedule below.</p>
  </section>

  <section v-else-if="ui.step === 2 && A">
    <h3>3 · Which trees do you act on?</h3>
    <p class="small">By default the plane trees are replaced. In the schedule below, mark a tree Keep, Move or Replace (with a reason),
      or leave it to the tool.</p>
    <label class="check"><input type="checkbox" :checked="A.all" :disabled="!A.inPlanes.length" @change="setAreaAll($event.target.checked)" />
      Replace all {{ A.inPlanes.length + A.keptIdx.length }} street trees, not only the planes</label>
    <label v-if="spots?.conditional" class="check"><input type="checkbox" v-model="state.useConditional" />
      Also use the {{ spots.conditional }} conditional spots (check them on site)</label>
    <div class="btns">
      <button :disabled="!fillableSpots().length" @click="fillAreaSpots">Plant the {{ fillableSpots().length }} free spots</button>
      <button @click="state.showSchedule = !state.showSchedule">{{ state.showSchedule ? 'Hide' : 'Show' }} the schedule</button>
    </div>
  </section>

  <section v-else-if="ui.step === 3 && A">
    <h3>4 · What matters most here?</h3>
    <p class="small">Click inside the triangle: towards summer shade (cooler streets), winter sun (no shade when it is cold) or runoff
      (less water reaching the flood hotspots). The layout is optimised again at each click.</p>
    <PriorityTriangle />
    <p v-if="state.busy" class="small accent">Optimising…</p>
    <p v-if="state.liveError" class="small danger">{{ state.liveError }}</p>
    <p class="sub">Species palette</p>
    <div class="btns">
      <button :class="{ on: state.site !== 'porta-barcelona' }" @click="switchSite('porta')">City (7)</button>
      <button :class="{ on: state.site === 'porta-barcelona' }" @click="switchSite('porta-barcelona')">Barcelona (30)</button>
    </div>
    <details class="how"><summary>Advanced</summary>
      <p class="small muted">Species cap, diversity floor and species on/off are in Expert mode (header). They stay applied when you come back.</p>
    </details>
  </section>

  <section v-else-if="ui.step === 4 && A">
    <h3>5 · Result</h3>
    <p class="small muted">The new trees are on the map; the schedule lists them. Diversity of the new trees: {{ layoutEff?.toFixed(1) }} effective species.</p>
    <CoverCounter />
  </section>

  <section v-else-if="ui.step === 5 && A">
    <h3>6 · Compare with the city's practice</h3>
    <p class="small">"vs city practice" = the city's 2026 planting mix on the same positions. The project-area table gives the area on its own.</p>
    <KpiPanel />
  </section>

  <section v-else-if="ui.step === 6 && A">
    <h3>7 · Report</h3>
    <p class="small">One page with the area, the numbers and plain sentences. Print it or save it as PDF.</p>
    <div class="btns"><button @click="printReport">Print / PDF</button></div>
  </section>

  <section v-else-if="ui.step === 7 && A">
    <h3>8 · Save and export</h3>
    <div class="btns">
      <button title="The whole project: area, actions, added trees, rules, priorities" @click="saveCfg">Save project</button>
      <button @click="download('dxf')">CAD (DXF)</button>
      <button @click="download('gpkg')">GIS (GeoPackage)</button>
      <button @click="state.showSchedule = true">Schedule (CSV, load)</button>
    </div>
    <p class="small muted">DXF and GeoPackage hold the layout on screen in EPSG:25831 metres. "Load" in the schedule reopens a saved project.</p>
  </section>

  <section v-else>
    <p class="small">Draw a project area first (step 1).</p>
  </section>

  <div class="nav">
    <button :disabled="ui.step === 0" @click="go(ui.step - 1)">Back</button>
    <button class="primary" :disabled="ui.step === STEPS.length - 1 || !canNext" @click="go(ui.step + 1)">Next</button>
  </div>
</template>

<style scoped>
.steps ol { list-style: none; margin: 0 0 8px; padding: 0; display: flex; flex-wrap: wrap; gap: 4px; }
.steps button { font-size: 11px; padding: 3px 6px; }
.steps li.on button { border-color: var(--accent); color: var(--accent); font-weight: 600; }
.steps li.done button { color: var(--muted); }
.facts { padding-left: 18px; margin: 6px 0; font-size: 13px; line-height: 1.5; }
.nav { display: flex; justify-content: space-between; margin-top: 12px; position: sticky; bottom: 0; background: var(--panel); padding: 8px 0; }
.primary { font-weight: 600; }
.good { color: var(--good); }
</style>
