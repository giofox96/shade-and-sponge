<script setup>
// v0.2.0 guided flow (notes/tutor_feedback_24nov.md §3e; restyled and reworked after the 27 Nov user tests).
// Steps slide sideways; inside a step, its pages slide vertically (no dropdowns: testers never opened them). A short tour
// points at what to do on each step the first time (coach.js; "?" replays it). Every action calls the expert panel's code.
import { computed, ref, watch, h, onBeforeUnmount, onMounted } from 'vue'
import { download } from '../exporter.js'
import { state, ui, startDrawing, finishArea, cancelDrawing, setAreaAll, fillAreaSpots, fillableSpots, spotClass, areaCover,
  layoutEff, configJson, savedProject, loadConfig, costs, projectCost, runArea, setAddMode, AREA } from '../store.js'
import { startCoach, coach, stop as stopCoach, tips, setTips } from '../coach.js'
import BarriPicker from './BarriPicker.vue'
import PriorityTriangle from './PriorityTriangle.vue'
import KpiPanel from './KpiPanel.vue'
import RulesPanel from './RulesPanel.vue'
import Icon from './Icon.vue'
import CoachMarks from './CoachMarks.vue'
import InfoTip from './InfoTip.vue'
import ArcGauge from './ArcGauge.vue'

// steps and, for each, its vertical pages
const STEPS = [
  ['Welcome', ['']], ['Where', ['']], ['Today', ['What grows there', 'How to read the map']], ['Replace', ['']], ['Add', ['']],
  ['Priorities', ['Goal', 'Fine-tune', 'Species and rules']], ['Result', ['']], ['Compare', ['Against the city', 'Every number', 'Cost']],
  ['Report', ['']], ['Save', ['']],
]
const A = computed(() => state.area)
const dir = ref('next')
const sub = ref(0)
const pages = computed(() => STEPS[ui.step][1])
const go = (k) => {
  const to = Math.max(0, Math.min(STEPS.length - 1, k))
  dir.value = to >= ui.step ? 'next' : 'back'
  ui.step = to
  sub.value = 0
}
const goSub = (k) => {
  if (k < 0 || k >= pages.value.length) return
  dir.value = k > sub.value ? 'down' : 'up'
  sub.value = k
}
const canNext = computed(() => ui.step === 0 || !!A.value?.metrics)
const nextName = computed(() => STEPS[ui.step + 1]?.[0])

// what each step shows on the map and in the views
watch(() => ui.step, (k) => {
  if (k === 2) Object.assign(state, { scenarioId: 'S0_current', showStreets: true, showSpots: true })
  if (k >= 3 && k <= 7 && A.value?.metrics) state.scenarioId = AREA
  if (k !== 3 && k !== 4) state.showSchedule = false
  if (k !== 4 && state.addMode) setAddMode(false)
  state.view = k === 8 ? 'report' : 'map'
  tour(k)
}, { immediate: false })

// the first-visit tour of each step (targets are CSS selectors; a missing one is skipped)
const TOURS = {
  1: [{ sel: '.guide .barri .find', text: 'Type the name of your neighbourhood, or click it on the little map.' },
      { sel: '.guide .draw', text: 'Then press here and click on the big map around your street, corner by corner.' }],
  2: [{ sel: '.guide .stats', text: 'What grows there today. Big numbers are counts in your area.' },
      { sel: '.guide .vnav', text: 'Some steps have more than one page: use these arrows to go down.' },
      { sel: '.guide .go-next', text: 'When you are ready, go to the next step here.' }],
  3: [{ sel: '.guide .toggles', text: 'Choose which trees the tool may replace.' },
      { sel: '.guide .use-schedule', text: 'Or decide tree by tree in the table.' }],
  4: [{ sel: '.guide .toggles', text: 'Choose where new trees can go: the free spots, more spots after a field check, or anywhere you click.' }],
  5: [{ sel: '.guide .toggles', text: 'Pick what matters most. The tool chooses the species again for each choice.' },
      { sel: '.guide .vnav', text: 'Go down for the fine-tuning triangle and the species rules.' }],
  6: [{ sel: '.guide .stats', text: 'Green means better than today, rust means worse.' },
      { sel: '.maplibregl-canvas', text: 'Click any tree on the map to see why it got its species.' }],
}
const tour = (k, force = false) => TOURS[k] && startCoach(`step${k}`, TOURS[k], force)
const SCHEDULE_TOUR = [
  { sel: '.schedule tbody tr', text: 'Each row is one tree in your area. Click it to find the tree on the map.' },
  { sel: '.schedule tbody tr select', text: 'Action: Keep it, Move it, or Replace it. "Replace" in grey is what the tool proposes.' },
  { sel: '.schedule tbody tr td:nth-child(6) select', text: 'Reason: why you act on this tree (dead, pests, works…). It goes into the report.' },
  { sel: '.schedule [role=tab]:nth-child(2)', text: 'The Spots tab lists the empty places: set Add to plant one, Leave empty to keep it free.' },
]
function useSchedule() {
  state.showSchedule = true
  startCoach('schedule', SCHEDULE_TOUR, true)
}
onMounted(() => tour(ui.step))
// the area is drawn: the step-1 tips have done their job
watch(() => !!A.value?.metrics, (on) => on && coach.name === 'step1' && stopCoach())

const spots = computed(() => {
  if (!A.value) return null
  const c = { free: 0, conditional: 0, blocked: 0 }
  A.value.spotIdx.forEach((s) => (c[spotClass(s)] = (c[spotClass(s)] ?? 0) + 1))
  return c
})
// the project autosaved in this browser
const saved = savedProject()
async function resume() {
  await loadConfig(saved)
  if (state.area) go(6)
}
function saveCfg() {
  const a = Object.assign(document.createElement('a'), { download: `shade_sponge_${state.site}_config.json`,
    href: URL.createObjectURL(new Blob([configJson()], { type: 'application/json' })) })
  a.click()
  URL.revokeObjectURL(a.href)
}
const printReport = () => window.dispatchEvent(new Event('print-report')) // ReportView prints itself in a clean window

// where new trees go
const addChoice = ref('none')
async function pickAdd(c) {
  addChoice.value = c
  setAddMode(c === 'click')
  if (state.added.length) { // a new choice starts from no added trees
    Object.assign(state, { added: [], selected: null })
    state.addedVersion++
    if (c === 'none' || c === 'click') await runArea(A.value.weights)
  }
  if (c !== 'free' && c !== 'more') return
  state.useConditional = c === 'more'
  await fillAreaSpots()
}

// priorities as four big choices (weights summer shade · winter sun · runoff); the triangle stays for anything in between
const GOALS = [
  ['Balanced', 'a bit of everything', 'sun', [0.5, 0.25, 0.25]],
  ['Cooler summers', 'as much shade as possible', 'sun', [1, 0, 0]],
  ['Winter sun', 'shade in summer, light in winter', 'sunlow', [0.5, 0.5, 0]],
  ['Less flooding', 'hold rain where water gathers', 'drop', [0.25, 0, 0.75]],
]
const goalOn = (w) => A.value?.weights && w.every((v, i) => Math.abs(v - A.value.weights[i]) < 0.01)
const pickGoal = (w) => A.value && runArea(w)

// the area's headline numbers (the trees it replaces, on their own)
const head = computed(() => {
  const L = A.value?.local
  if (!L) return null
  const pct = (m) => (L[m]?.today ? (100 * L[m].delta) / L[m].today : 0)
  return { summer: pct('shade_summer_m2h'), winter: pct('shade_winter_m2h'), litres: -1000 * (L.runoff_hot_m3?.delta ?? 0),
    city: A.value.city?.metrics ? A.value.metrics.shade_summer_m2h - A.value.city.metrics.shade_summer_m2h : null,
    cityLitres: A.value.city?.metrics ? -1000 * (A.value.metrics.runoff_hot_m3 - A.value.city.metrics.runoff_hot_m3) : null }
})
const LEGEND = [['Deciduous', 'Bare in winter', '#b08a2e'], ['Evergreen', 'Green all year', '#5e8f55'], ['Semi-deciduous', 'Loses part of its leaves', '#a3a35a']]
// the spot discs as drawn on the map (MapView 'spots' and 'spot-centres')
const SPOT_SIZES = [['Small spot', 'Room for a small tree', '#a8d66e'], ['Medium spot', 'Room for a medium tree', '#5caa32'], ['Large spot', 'Room for a large tree', '#286e14']]
const SPOT_DOTS = [['White centre', 'Free: plant it', '#ffffff'], ['Amber centre', 'A sign, lamp or bollard to move first', '#eb961e'],
  ['Orange centre', 'A buried service under the pit', '#e67814'], ['Red centre', 'Blocked: no tree here', '#b22c22']]

// a number that counts up to its value when it appears or changes
const Count = {
  props: { to: Number, digits: { type: Number, default: 0 }, sign: Boolean },
  setup(p) {
    const v = ref(0)
    let raf
    const run = (to, from) => {
      cancelAnimationFrame(raf)
      const t0 = performance.now()
      const tick = (t) => {
        const k = Math.min(1, (t - t0) / 700)
        v.value = from + (to - from) * (1 - (1 - k) ** 3)
        if (k < 1) raf = requestAnimationFrame(tick)
      }
      raf = requestAnimationFrame(tick)
    }
    watch(() => p.to, (to, from) => run(to ?? 0, from ?? 0), { immediate: true })
    onBeforeUnmount(() => cancelAnimationFrame(raf))
    return () => h('span', (p.sign && v.value > 0 ? '+' : v.value < 0 ? '−' : '') +
      Math.abs(v.value).toLocaleString('en', { minimumFractionDigits: p.digits, maximumFractionDigits: p.digits }))
  },
}
const key = computed(() => `${ui.step}.${sub.value}`)
const eur = (v) => Number(v).toLocaleString('en', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
const COSTS = [['tree', 'per new tree', 'New pit on a free spot, planting included (CYPE price base, direct cost)'],
  ['move', 'per transplant', 'Young-tree transplant (CYPE JSP020, direct cost)'],
  ['object', 'per object moved', 'Dismantling and re-installing a traffic sign without the post (CYPE DTM030 + TSV050, direct cost)']]
</script>

<template>
  <div class="guide" :class="{ full: ui.step === 0, slimside: ui.step === 8, above: state.showSchedule && ui.step !== 0 }">
    <Transition :name="dir" mode="out-in">
      <!-- 0 · welcome: centred, big -->
      <section v-if="ui.step === 0" :key="key" class="card hero">
        <div class="sprout" aria-hidden="true"><b></b><span></span><i></i><i></i><i></i><i></i></div>
        <h1>Which trees for this street?</h1>
        <p class="lead">Draw the street you are redesigning. I compare the trees you could plant there on summer shade, winter sun
          and flooding, against what the city plants today.</p>
        <div class="row">
          <button class="big primary go-next" @click="go(1)">Start <span aria-hidden="true">→</span></button>
          <button v-if="saved?.area" class="big ghost" @click="resume">Resume last project</button>
        </div>
        <div class="tipq" role="group" aria-label="Show tips">
          <span>Show me tips along the way?</span>
          <button :class="{ on: tips.on }" :aria-pressed="tips.on" @click="setTips(true)">Yes</button>
          <button :class="{ on: !tips.on }" :aria-pressed="!tips.on" @click="setTips(false)">No</button>
        </div>
      </section>

      <!-- 1 · where -->
      <section v-else-if="ui.step === 1" :key="key" class="card">
        <p class="say">Where are you working?</p>
        <BarriPicker class="barri" />
        <div class="row">
          <button v-if="!state.drawing" class="big primary draw" @click="startDrawing"><Icon name="edit" />{{ A ? 'Redraw the area' : 'Draw the area' }}</button>
          <template v-else>
            <button class="big primary" :disabled="state.draft.length < 3" @click="finishArea">Finish ({{ state.draft.length }} corners)</button>
            <button class="big ghost" @click="cancelDrawing">Cancel</button>
          </template>
        </div>
        <p v-if="state.drawing" class="hint">Click on the map around your street, corner by corner. Close it with <b>Finish</b>, a right-click or Enter.</p>
        <p v-if="state.addMsg" class="hint accent">{{ state.addMsg }}</p>
        <p v-if="A?.metrics" class="pop good">Got it: {{ A.inPlanes.length + A.keptIdx.length }} street trees in your area.</p>
      </section>

      <!-- 2 · today: numbers, then how to read the map -->
      <section v-else-if="ui.step === 2 && A && sub === 0" :key="key" class="card">
        <p class="say">Here is what grows there today</p>
        <div class="stats">
          <div><Icon name="park" /><b><Count :to="A.inPlanes.length + A.keptIdx.length" /></b><span class="lbl">street trees</span></div>
          <div><Icon name="swap" /><b><Count :to="A.inPlanes.length" /></b><span class="lbl">plane trees, the ones the city replaces</span></div>
          <div v-if="spots"><Icon name="fill" /><b><Count :to="spots.free" /></b><span class="lbl">free spots for new trees</span></div>
          <div v-if="areaCover"><ArcGauge class="gauge" :value="areaCover.today" /><b><Count :to="areaCover.today" :digits="1" />%</b><span class="lbl">canopy cover, target 30%</span></div>
        </div>
        <p v-if="spots?.conditional" class="hint">{{ spots.conditional }} more spots are possible if a sign, a lamp or a buried service is moved.</p>
      </section>
      <section v-else-if="ui.step === 2 && A && sub === 1" :key="key" class="card">
        <p class="say">How to read the map</p>
        <p class="lgh">Trees</p>
        <ul class="legend">
          <li v-for="[k, txt, c] in LEGEND" :key="k"><span class="sw" :style="{ background: c }"></span><div><b>{{ k }}</b><small>{{ txt }}</small></div></li>
        </ul>
        <p class="lgh">Planting spots</p>
        <ul class="legend">
          <li v-for="[k, txt, c] in SPOT_SIZES" :key="k"><span class="sw disc" :style="{ background: c }"><i></i></span><div><b>{{ k }}</b><small>{{ txt }}</small></div></li>
        </ul>
        <ul class="legend">
          <li v-for="[k, txt, c] in SPOT_DOTS" :key="k"><span class="sw disc" style="background: #5caa32"><i :style="{ background: c }"></i></span><div><b>{{ k }}</b><small>{{ txt }}</small></div></li>
        </ul>
      </section>

      <!-- 3 · replace -->
      <section v-else-if="ui.step === 3 && A" :key="key" class="card">
        <p class="say">Which trees do you change?</p>
        <div class="toggles">
          <button class="tog" :class="{ on: !A.all }" @click="setAreaAll(false)"><Icon name="swap" /><b>Only the plane trees</b><small>{{ A.inPlanes.length }} trees</small></button>
          <button class="tog" :class="{ on: A.all }" :disabled="!A.inPlanes.length" @click="setAreaAll(true)"><Icon name="swap" /><b>All street trees</b><small>{{ A.inPlanes.length + A.keptIdx.length }} trees</small></button>
        </div>
        <button class="big ghost use-schedule" @click="useSchedule"><Icon name="more" />Decide tree by tree in the table</button>
      </section>

      <!-- 4 · add -->
      <section v-else-if="ui.step === 4 && A" :key="key" class="card">
        <p class="say">Where do you want to add trees?</p>
        <div class="toggles">
          <button class="tog" :class="{ on: addChoice === 'none' }" @click="pickAdd('none')"><Icon name="swap" /><b>Nowhere</b><small>only replace</small></button>
          <button class="tog" :class="{ on: addChoice === 'free' }" :disabled="!spots?.free" @click="pickAdd('free')"><Icon name="fill" /><b>On the free spots</b><small>{{ spots?.free ?? 0 }} spots</small></button>
          <button class="tog" :class="{ on: addChoice === 'more' }" :disabled="!spots?.conditional" @click="pickAdd('more')"><Icon name="alert" /><b>Also after a field check</b><small>+{{ spots?.conditional ?? 0 }} conditional spots</small></button>
          <button class="tog" :class="{ on: addChoice === 'click' }" @click="pickAdd('click')"><Icon name="add" /><b>Where I click</b><small>on the map</small></button>
        </div>
        <p v-if="addChoice === 'click'" class="hint">Click on the map: green ground takes a tree, amber with a warning. {{ state.added.length }} added so far.</p>
        <p v-if="state.addMsg" class="hint accent">{{ state.addMsg }}</p>
        <button class="big ghost use-schedule" @click="useSchedule"><Icon name="more" />Choose spot by spot in the table</button>
      </section>

      <!-- 5 · priorities: goal, triangle, rules -->
      <section v-else-if="ui.step === 5 && A && sub === 0" :key="key" class="card">
        <p class="say">What matters most on this street?</p>
        <div class="toggles">
          <button v-for="[name, s, icon, w] in GOALS" :key="name" class="tog" :class="{ on: goalOn(w) }" @click="pickGoal(w)">
            <Icon :name="icon" /><b>{{ name }}</b><small>{{ s }}</small></button>
        </div>
        <p v-if="state.busy" class="hint accent pulse">Choosing the species…</p>
        <p v-if="state.liveError" class="hint danger">{{ state.liveError }}</p>
      </section>
      <section v-else-if="ui.step === 5 && A && sub === 1" :key="key" class="card">
        <p class="say">Anything in between</p>
        <p class="hint">Click inside the triangle: each corner is one goal at 100%.</p>
        <PriorityTriangle />
      </section>
      <section v-else-if="ui.step === 5 && A && sub === 2" :key="key" class="card">
        <p class="say">Species and rules</p>
        <RulesPanel />
      </section>

      <!-- 6 · result -->
      <section v-else-if="ui.step === 6 && A && head" :key="key" class="card">
        <p class="say">Here is the street with the new trees<InfoTip>Against today's trees in the area: one hot summer day for shade, one 2-year, 1-hour storm for water.</InfoTip></p>
        <div class="stats">
          <div :class="head.summer >= 0 ? 'up' : 'down'"><Icon name="sun" /><b><Count :to="head.summer" sign />%</b><span class="lbl">summer shade</span></div>
          <div :class="head.litres >= 0 ? 'up' : 'down'"><Icon name="drop" /><b><Count :to="Math.abs(head.litres)" /> L</b><span class="lbl">{{ head.litres >= 0 ? 'less' : 'more' }} water to flood spots</span></div>
          <div v-if="areaCover" :class="areaCover.now >= areaCover.today ? 'up' : 'down'"><ArcGauge class="gauge" :value="areaCover.now" /><b><Count :to="areaCover.now" :digits="1" />%</b><span class="lbl">canopy (was {{ areaCover.today.toFixed(1) }}%)</span></div>
          <div><Icon name="park" /><b><Count :to="layoutEff ?? 0" :digits="1" /></b><span class="lbl">effective species</span></div>
        </div>
      </section>

      <!-- 7 · compare: city, every number, cost -->
      <section v-else-if="ui.step === 7 && A && head && sub === 0" :key="key" class="card">
        <p class="say">And against what the city would plant?<InfoTip>The city's mix: the species it actually planted in place of plane trees in recent years, on the same positions.</InfoTip></p>
        <div class="stats">
          <div v-if="head.city != null" :class="head.city >= 0 ? 'up' : 'down'"><Icon name="sun" /><b><Count :to="head.city / 1000" :digits="1" sign />k</b><span class="lbl">m²·h summer shade vs the city's mix</span></div>
          <div v-if="head.cityLitres != null" :class="head.cityLitres >= 0 ? 'up' : 'down'"><Icon name="drop" /><b><Count :to="Math.abs(head.cityLitres)" /> L</b><span class="lbl">{{ head.cityLitres >= 0 ? 'less' : 'more' }} water than the city's mix</span></div>
        </div>
      </section>
      <section v-else-if="ui.step === 7 && A && sub === 1" :key="key" class="card">
        <p class="say">Every number</p>
        <KpiPanel compact />
      </section>
      <section v-else-if="ui.step === 7 && A && sub === 2" :key="key" class="card">
        <p class="say">What it costs<InfoTip>Direct costs from the CYPE construction price base, without overhead, profit or VAT; watering is not included. Change them to your own: they stay in this browser.</InfoTip></p>
        <div class="cost">
          <label v-for="[k, what, src] in COSTS" :key="k"><span class="eur">€</span>
            <input type="number" min="0" step="0.01" :value="costs[k] == null ? '' : Number(costs[k]).toFixed(2)"
                   @change="costs[k] = $event.target.value === '' ? null : Math.round(100 * Number($event.target.value)) / 100" />
            <span>{{ what }}</span><InfoTip>{{ src }}</InfoTip></label>
        </div>
        <div v-if="projectCost?.known && projectCost.total" class="total">
          <p><b>€ {{ eur(projectCost.total) }}</b> in total</p>
          <p>€ {{ eur(projectCost.perTree) }} per tree</p>
        </div>
      </section>

      <!-- 8 · report (the page itself fills the main view) -->
      <section v-else-if="ui.step === 8 && A" :key="key" class="card slim">
        <p class="say">Your one-page report</p>
        <div class="row"><button class="big primary" @click="printReport">Print or save as PDF</button></div>
      </section>

      <!-- 9 · save -->
      <section v-else-if="ui.step === 9 && A" :key="key" class="card">
        <p class="say">Take it with you</p>
        <div class="toggles">
          <button class="tog" @click="saveCfg"><Icon name="layers" /><b>Save project</b><small>open it again later</small></button>
          <button class="tog" @click="download('dxf')"><Icon name="building" /><b>CAD</b><small>DXF</small></button>
          <button class="tog" @click="download('gpkg')"><Icon name="terrain" /><b>GIS</b><small>GeoPackage</small></button>
          <button class="tog" @click="state.showSchedule = !state.showSchedule"><Icon name="more" /><b>Tree table</b><small>CSV</small></button>
        </div>
        <p class="hint">Your project is also kept in this browser.</p>
      </section>

      <section v-else :key="key" class="card">
        <p class="say">First, draw your street</p>
        <div class="row"><button class="big primary" @click="go(1)">Go to step 1</button></div>
      </section>
    </Transition>

    <!-- inside a step: its pages, up and down -->
    <div v-if="ui.step > 0 && pages.length > 1" class="vnav" aria-label="Pages of this step">
      <button :disabled="sub === 0" aria-label="Previous page" @click="goSub(sub - 1)">↑</button>
      <button v-for="(p, k) in pages" :key="p" class="vdot" :class="{ on: sub === k }" :title="p" @click="goSub(k)">{{ p }}</button>
      <button :disabled="sub === pages.length - 1" aria-label="Next page" @click="goSub(sub + 1)">↓</button>
    </div>

    <!-- between steps -->
    <nav v-if="ui.step > 0" class="dots" aria-label="Steps">
      <button class="arrow" aria-label="Back" @click="go(ui.step - 1)">←</button>
      <button v-for="(s, k) in STEPS.slice(1)" :key="s[0]" class="dot" :class="{ on: ui.step === k + 1, done: k + 1 < ui.step }"
              :disabled="k + 1 > 1 && !A?.metrics" :aria-label="`Step ${k + 1}: ${s[0]}`" :title="s[0]" @click="go(k + 1)"></button>
      <button v-if="nextName" class="next-big go-next" :class="{ ready: canNext }" :disabled="!canNext" @click="go(ui.step + 1)">
        Next: {{ nextName }} <span aria-hidden="true">→</span></button>
      <button class="help" title="Show the tips for this step again" aria-label="Show the tips again" @click="tour(ui.step, true)">?</button>
    </nav>
    <CoachMarks />
  </div>
</template>

<style scoped>
.guide { position: absolute; left: 20px; bottom: 20px; width: min(460px, calc(100% - 40px)); max-height: calc(100% - 40px); z-index: 7;
  display: flex; flex-direction: column; gap: 10px; pointer-events: none; transition: bottom 0.45s cubic-bezier(.2, .8, .2, 1); }
.guide > * { pointer-events: auto; }
.guide.full { inset: 0; width: auto; max-height: none; align-items: center; justify-content: center; left: 0; bottom: 0;
  background: color-mix(in srgb, var(--bg) 82%, transparent); backdrop-filter: blur(3px); }
.guide.slimside { width: 400px; }
/* the docked tree table sits right of the guide; only on a narrow screen does the guide go over it */
@media (max-width: 1000px) {
  .guide.above { bottom: calc(42% + 26px); max-height: calc(58% - 46px); }
  .guide.above .card { max-height: calc(58vh - 160px); }
}
.card { background: var(--panel); border: 0.5px solid var(--line); border-radius: 18px; padding: 22px 24px; overflow: auto;
  box-shadow: 0 10px 30px rgba(42, 38, 34, 0.14); max-height: calc(100vh - 230px); }
.card.slim { padding: 16px 20px; }
.hero { max-width: 620px; text-align: center; padding: 40px 44px; }
h1 { font-size: 40px; line-height: 1.1; margin: 10px 0 14px; letter-spacing: -0.02em; animation: rise 0.6s ease both 0.15s; }
.lead { font-size: 18px; line-height: 1.5; color: var(--muted); margin: 0 auto 26px; animation: rise 0.6s ease both 0.3s; }
.say { font-size: 26px; line-height: 1.2; font-weight: 600; margin: 0 0 12px; letter-spacing: -0.01em; animation: rise 0.45s ease both; }
.say::before { content: ''; display: inline-block; width: 10px; height: 10px; border-radius: 50%; background: var(--good);
  margin-right: 10px; vertical-align: middle; animation: blink 1.6s ease-in-out infinite; }
.hint { font-size: 14px; color: var(--muted); line-height: 1.45; margin: 12px 0 0; animation: rise 0.45s ease both 0.1s; }
.pop { font-size: 18px; font-weight: 600; margin: 12px 0 0; animation: pop 0.4s ease both; }
.row { display: flex; gap: 10px; flex-wrap: wrap; justify-content: inherit; margin-top: 12px; }
.hero .row { justify-content: center; }
button.big { font-size: 17px; padding: 12px 22px; border-radius: 999px; display: inline-flex; gap: 8px; align-items: center; }
button.primary { background: var(--accent); color: var(--bg); border-color: var(--accent); font-weight: 600; transition: transform 0.15s; }
button.primary:hover:not(:disabled) { transform: translateY(-1px); }
button.ghost { background: transparent; }
.use-schedule { margin-top: 14px; width: 100%; justify-content: center; font-size: 15px !important; }
.toggles { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
.tog { display: grid; grid-template-columns: 26px 1fr; grid-template-rows: auto auto; column-gap: 8px; text-align: left; padding: 14px;
  border-radius: 14px; border: 1.5px solid var(--line); background: var(--bg); transition: border-color 0.2s, transform 0.15s, background 0.2s;
  animation: rise 0.45s ease both; }
.tog:nth-child(2) { animation-delay: 0.06s; } .tog:nth-child(3) { animation-delay: 0.12s; } .tog:nth-child(4) { animation-delay: 0.18s; }
.tog:hover:not(:disabled) { transform: translateY(-2px); border-color: var(--muted); }
.tog.on { border-color: var(--good); background: color-mix(in srgb, var(--good) 12%, var(--bg)); }
.tog :deep(svg) { grid-row: span 2; width: 22px; height: 22px; align-self: center; }
.tog b { font-size: 15px; } .tog small { color: var(--muted); font-size: 12px; }
.stats { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
.stats > div { position: relative; background: var(--bg); border-radius: 14px; padding: 14px 14px 12px; animation: rise 0.45s ease both; }
.stats > div:nth-child(2) { animation-delay: 0.08s; } .stats > div:nth-child(3) { animation-delay: 0.16s; } .stats > div:nth-child(4) { animation-delay: 0.24s; }
.stats :deep(svg) { position: absolute; top: 12px; right: 12px; width: 22px; height: 22px; opacity: 0.55; }
.stats :deep(svg.gauge) { width: 46px; height: 29px; opacity: 1; top: 10px; right: 10px; }
.stats b { display: block; font-size: 34px; line-height: 1.1; letter-spacing: -0.02em; font-variant-numeric: tabular-nums; }
.stats .lbl { display: block; font-size: 13px; color: var(--muted); margin-top: 2px; }
.stats .up b { color: var(--good); } .stats .down b { color: var(--bad); }
.legend { list-style: none; padding: 0; margin: 0 0 6px; display: grid; gap: 8px; }
.lgh { font-size: 12px; text-transform: uppercase; letter-spacing: 0.06em; color: var(--muted); margin: 10px 0 6px; }
.legend li { display: flex; gap: 12px; align-items: center; animation: rise 0.4s ease both; }
.legend li div { display: flex; flex-direction: column; line-height: 1.2; }
.legend small { font-size: 12px; color: var(--muted); }
.legend b { font-size: 15px; }
.sw { width: 16px; height: 16px; border-radius: 50%; display: inline-block; flex: none; align-self: center; }
.sw.disc { width: 22px; height: 22px; display: grid; place-items: center; opacity: 0.85; }
.sw.disc i { width: 6px; height: 6px; border-radius: 50%; background: #fff; box-shadow: 0 0 0 1px rgba(0, 0, 0, 0.15); }
.cost { display: grid; gap: 8px; font-size: 15px; }
.cost label { display: grid; grid-template-columns: 14px 110px 1fr auto; align-items: center; gap: 8px; }
.cost input { width: 110px; font-size: 16px; padding: 6px 10px; border-radius: 10px; text-align: right; font-variant-numeric: tabular-nums; }
.total { margin-top: 14px; animation: pop 0.4s ease both; } .total p { margin: 2px 0; font-size: 15px; } .total b { font-size: 22px; }
.barri { margin-top: 4px; }
.vnav, .dots { display: flex; align-items: center; gap: 8px; align-self: stretch; min-height: 52px; background: var(--panel);
  border: 0.5px solid var(--line); border-radius: 999px; padding: 6px 8px; box-shadow: 0 4px 14px rgba(42, 38, 34, 0.1); }
.vnav button { border-radius: 999px; padding: 8px 12px; font-size: 14px; }
.vnav .vdot { flex: 1 1 auto; white-space: nowrap; padding: 8px 10px; font-size: 13px; }
.vnav > button:first-child, .vnav > button:last-child { width: 38px; height: 38px; padding: 0; flex: none; }
.vdot.on { background: var(--accent); color: var(--bg); border-color: var(--accent); }
.dot { width: 10px; height: 10px; padding: 0; border-radius: 50%; border: 0; background: var(--line); transition: width 0.3s, background 0.3s; }
.dot.done { background: var(--muted); }
.dot.on { width: 26px; border-radius: 6px; background: var(--accent); }
.arrow, .help { border-radius: 50%; width: 38px; height: 38px; padding: 0; font-size: 16px; flex: none; }
.next-big { border-radius: 999px; padding: 10px 16px; font-size: 15px; font-weight: 600; margin-left: auto; white-space: nowrap; }
.tipq { display: flex; gap: 8px; align-items: center; justify-content: center; margin-top: 22px; font-size: 15px; color: var(--muted); animation: rise 0.6s ease both 0.5s; }
.tipq button { border-radius: 999px; padding: 6px 16px; }
.tipq button.on { background: var(--good); border-color: var(--good); color: #fff; }
.next-big.ready { background: var(--accent); color: var(--bg); border-color: var(--accent); animation: nudge 2.4s ease-in-out infinite 1.5s; }
.pulse { animation: blink 1s ease-in-out infinite; }
/* the sprout on the welcome screen: a trunk that grows, two leaves that open */
.sprout { position: relative; width: 90px; height: 96px; margin: 0 auto; animation: settle 0.9s ease forwards 3.3s; }
.sprout span { position: absolute; left: 43px; bottom: 0; width: 4px; height: 0; background: #7a5a3a; border-radius: 2px;
  animation: grow 1.3s cubic-bezier(.3, .7, .3, 1) forwards 0.1s; }
.sprout i { position: absolute; width: 22px; height: 12px; background: var(--good); border-radius: 12px 0; transform: scale(0);
  animation: leaf 0.55s ease forwards 1.2s, fade 0.5s ease forwards 2.9s; }
.sprout i:nth-of-type(odd) { left: 22px; transform-origin: right bottom; }
.sprout i:nth-of-type(even) { left: 46px; border-radius: 0 12px; transform-origin: left bottom; }
.sprout i:nth-of-type(1) { bottom: 26px; } .sprout i:nth-of-type(2) { bottom: 34px; animation-delay: 1.45s, 2.9s; }
.sprout i:nth-of-type(3) { bottom: 44px; animation-delay: 1.7s, 2.9s; } .sprout i:nth-of-type(4) { bottom: 52px; animation-delay: 1.95s, 2.9s; }
/* the crown opens behind the leaves: from a sprout to a tree */
.sprout b { position: absolute; left: 13px; bottom: 34px; width: 64px; height: 58px; border-radius: 50%; background: var(--good);
  transform: scale(0); transform-origin: 50% 90%; animation: crown 0.9s cubic-bezier(.2, .8, .2, 1.2) forwards 2.5s; }
/* steps slide sideways like pages; a step's own pages slide up and down */
.next-enter-active, .next-leave-active, .back-enter-active, .back-leave-active,
.down-enter-active, .down-leave-active, .up-enter-active, .up-leave-active { transition: transform 0.4s cubic-bezier(.2, .8, .2, 1), opacity 0.3s; }
.next-enter-from, .back-leave-to { transform: translateX(60px); opacity: 0; }
.next-leave-to, .back-enter-from { transform: translateX(-60px); opacity: 0; }
.down-enter-from, .up-leave-to { transform: translateY(40px); opacity: 0; }
.down-leave-to, .up-enter-from { transform: translateY(-40px); opacity: 0; }
@keyframes rise { from { transform: translateY(10px); opacity: 0; } to { transform: none; opacity: 1; } }
@keyframes pop { 0% { transform: scale(0.9); opacity: 0; } 60% { transform: scale(1.04); opacity: 1; } 100% { transform: none; } }
@keyframes blink { 50% { opacity: 0.35; } }
@keyframes grow { to { height: 62px; } }
@keyframes crown { to { transform: scale(1); } }
@keyframes fade { to { opacity: 0; } }
@keyframes settle { to { transform: scale(0.8); } }
@keyframes leaf { to { transform: scale(1); } }
@keyframes nudge { 0%, 80%, 100% { transform: none; } 88% { transform: translateX(4px); } 94% { transform: translateX(-2px); } }
@media (prefers-reduced-motion: reduce) { * { animation: none !important; transition: none !important; } }
@media (max-width: 700px) { h1 { font-size: 30px; } .say { font-size: 21px; } .stats b { font-size: 26px; } .toggles, .stats { grid-template-columns: 1fr; } }
</style>
