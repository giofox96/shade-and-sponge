<script setup>
// v0.2.0 guided flow (notes/tutor_feedback_24nov.md §3e, restyled 27 Nov): one screen per step, sliding sideways like pages,
// a guide that talks in short lines, big toggles and big numbers. Every step only calls what the expert panel calls;
// "Expert" in the header shows all settings at once. Colours and type follow the slides (Earth palette, IBM Plex Sans).
import { computed, ref, watch, h, onBeforeUnmount } from 'vue'
import { download } from '../exporter.js'
import { state, ui, startDrawing, finishArea, cancelDrawing, setAreaAll, fillAreaSpots, fillableSpots, spotClass, areaCover,
  layoutEff, configJson, switchSite, savedProject, loadConfig, costs, projectCost, runArea, AREA } from '../store.js'
import BarriPicker from './BarriPicker.vue'
import PriorityTriangle from './PriorityTriangle.vue'
import KpiPanel from './KpiPanel.vue'
import RulesPanel from './RulesPanel.vue'
import Icon from './Icon.vue'

const STEPS = ['Welcome', 'Where', 'Today', 'Trees', 'Priorities', 'Result', 'Compare', 'Report', 'Save']
const A = computed(() => state.area)
const dir = ref('next')
const go = (k) => {
  const to = Math.max(0, Math.min(STEPS.length - 1, k))
  dir.value = to >= ui.step ? 'next' : 'back'
  ui.step = to
}
const canNext = computed(() => ui.step === 0 || !!A.value?.metrics)

// what each step shows on the map and in the views
watch(() => ui.step, (k) => {
  if (k === 2) Object.assign(state, { scenarioId: 'S0_current', showStreets: true })
  if (k >= 3 && k <= 6 && A.value?.metrics) state.scenarioId = AREA
  state.showSchedule = k === 3
  state.view = k === 7 ? 'report' : 'map'
}, { immediate: true })

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
  if (state.area) go(5)
}
function saveCfg() {
  const a = Object.assign(document.createElement('a'), { download: `shade_sponge_${state.site}_config.json`,
    href: URL.createObjectURL(new Blob([configJson()], { type: 'application/json' })) })
  a.click()
  URL.revokeObjectURL(a.href)
}
const printReport = () => window.print()

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
</script>

<template>
  <div class="guide" :class="{ full: ui.step === 0, wide: ui.step === 7, above: state.showSchedule && ui.step !== 0 }">
    <Transition :name="dir" mode="out-in">
      <!-- 0 · welcome: centred, big -->
      <section v-if="ui.step === 0" key="0" class="card hero">
        <div class="sprout" aria-hidden="true"><span></span><i></i><i></i></div>
        <h1>Which trees for this street?</h1>
        <p class="lead">Draw the street you are redesigning. I compare the trees you could plant there on summer shade, winter sun
          and flooding, against what the city plants today.</p>
        <div class="row">
          <button class="big primary" @click="go(1)">Start <span aria-hidden="true">→</span></button>
          <button v-if="saved?.area" class="big ghost" @click="resume">Resume last project</button>
        </div>
      </section>

      <!-- 1 · where -->
      <section v-else-if="ui.step === 1" key="1" class="card">
        <p class="say">Where are you working?</p>
        <p class="hint">Pick the neighbourhood, then click on the map around your street. Close the shape with
          <b>Finish</b>, a right-click or Enter.</p>
        <BarriPicker class="barri" />
        <div class="row">
          <button v-if="!state.drawing" class="big primary" @click="startDrawing"><Icon name="edit" />{{ A ? 'Redraw' : 'Draw the area' }}</button>
          <template v-else>
            <button class="big primary" :disabled="state.draft.length < 3" @click="finishArea">Finish · {{ state.draft.length }} corners</button>
            <button class="big ghost" @click="cancelDrawing">Cancel</button>
          </template>
        </div>
        <p v-if="state.addMsg" class="hint accent">{{ state.addMsg }}</p>
        <p v-if="A?.metrics" class="pop good">Got it: {{ A.inPlanes.length + A.keptIdx.length }} street trees in your area.</p>
      </section>

      <!-- 2 · today -->
      <section v-else-if="ui.step === 2 && A" key="2" class="card">
        <p class="say">Here is what grows there today.</p>
        <div class="stats">
          <div><b><Count :to="A.inPlanes.length + A.keptIdx.length" /></b><span class="lbl">street trees</span></div>
          <div><b><Count :to="A.inPlanes.length" /></b><span class="lbl">plane trees</span></div>
          <div v-if="spots"><b><Count :to="spots.free" /></b><span class="lbl">free spots</span></div>
          <div v-if="areaCover"><b><Count :to="areaCover.today" :digits="1" />%</b><span class="lbl">canopy · target 30%</span></div>
        </div>
        <p v-if="spots?.conditional" class="hint">{{ spots.conditional }} more spots are possible if a sign, a lamp or a buried service is moved.</p>
      </section>

      <!-- 3 · trees -->
      <section v-else-if="ui.step === 3 && A" key="3" class="card">
        <p class="say">Which trees do you change?</p>
        <div class="toggles">
          <button class="tog" :class="{ on: !A.all }" @click="setAreaAll(false)"><Icon name="swap" /><b>Only the plane trees</b><small>{{ A.inPlanes.length }} trees</small></button>
          <button class="tog" :class="{ on: A.all }" :disabled="!A.inPlanes.length" @click="setAreaAll(true)"><Icon name="swap" /><b>All street trees</b><small>{{ A.inPlanes.length + A.keptIdx.length }} trees</small></button>
          <button class="tog" :disabled="!fillableSpots().length" @click="fillAreaSpots"><Icon name="fill" /><b>Plant the free spots</b><small>{{ fillableSpots().length }} spots</small></button>
          <button v-if="spots?.conditional" class="tog" :class="{ on: state.useConditional }" @click="state.useConditional = !state.useConditional">
            <Icon name="alert" /><b>Use conditional spots</b><small>check them on site</small></button>
        </div>
        <p class="hint">The table below lists every tree: set <b>Keep</b>, <b>Move</b> or <b>Replace</b> with a reason if you know better.</p>
      </section>

      <!-- 4 · priorities -->
      <section v-else-if="ui.step === 4 && A" key="4" class="card">
        <p class="say">What matters most on this street?</p>
        <div class="toggles">
          <button v-for="[name, sub, icon, w] in GOALS" :key="name" class="tog" :class="{ on: goalOn(w) }" @click="pickGoal(w)">
            <Icon :name="icon" /><b>{{ name }}</b><small>{{ sub }}</small></button>
        </div>
        <p v-if="state.busy" class="hint accent pulse">Choosing the species…</p>
        <p v-if="state.liveError" class="hint danger">{{ state.liveError }}</p>
        <details class="more"><summary>Fine-tune on the triangle</summary><PriorityTriangle /></details>
        <details class="more"><summary>Species and rules</summary>
          <div class="row"><button class="pill" :class="{ on: state.site !== 'porta-barcelona' }" @click="switchSite('porta')">City palette · 7</button>
            <button class="pill" :class="{ on: state.site === 'porta-barcelona' }" @click="switchSite('porta-barcelona')">Barcelona · 30</button></div>
          <RulesPanel />
        </details>
      </section>

      <!-- 5 · result -->
      <section v-else-if="ui.step === 5 && A && head" key="5" class="card">
        <p class="say">Here is the street with the new trees.</p>
        <div class="stats">
          <div :class="head.summer >= 0 ? 'up' : 'down'"><b><Count :to="head.summer" sign />%</b><span class="lbl">summer shade</span></div>
          <div :class="head.litres >= 0 ? 'up' : 'down'"><b><Count :to="Math.abs(head.litres)" /> L</b><span class="lbl">{{ head.litres >= 0 ? 'less' : 'more' }} water to flood spots</span></div>
          <div v-if="areaCover" :class="areaCover.now >= areaCover.today ? 'up' : 'down'"><b><Count :to="areaCover.now" :digits="1" />%</b><span class="lbl">canopy (was {{ areaCover.today.toFixed(1) }}%)</span></div>
          <div><b><Count :to="layoutEff ?? 0" :digits="1" /></b><span class="lbl">effective species</span></div>
        </div>
        <p class="hint">Compared with today's trees in the area, one hot day and one 2-year storm. Click a tree on the map to see why it got its species.</p>
      </section>

      <!-- 6 · compare -->
      <section v-else-if="ui.step === 6 && A && head" key="6" class="card">
        <p class="say">And against what the city would plant?</p>
        <div class="stats">
          <div v-if="head.city != null" :class="head.city >= 0 ? 'up' : 'down'"><b><Count :to="head.city / 1000" :digits="1" sign />k</b><span class="lbl">m²·h summer shade vs city</span></div>
          <div v-if="head.cityLitres != null" :class="head.cityLitres >= 0 ? 'up' : 'down'"><b><Count :to="Math.abs(head.cityLitres)" /> L</b><span class="lbl">{{ head.cityLitres >= 0 ? 'less' : 'more' }} water than the city's mix</span></div>
        </div>
        <details class="more"><summary>Every number</summary><KpiPanel /></details>
        <details class="more" open><summary>Cost <span class="muted">· direct costs (CYPE), change them to yours</span></summary>
          <div class="cost">
            <label>€ per new tree <input type="number" min="0" step="10" v-model.number="costs.tree" /></label>
            <label>€ per transplant <input type="number" min="0" step="10" v-model.number="costs.move" /></label>
            <label>€ per object moved <input type="number" min="0" step="10" v-model.number="costs.object" /></label>
          </div>
          <p v-if="projectCost?.known && projectCost.total" class="pop">≈ € <Count :to="projectCost.total" /> · € {{ Math.round(projectCost.perTree).toLocaleString('en') }} per tree</p>
          <p v-else class="hint">Enter a price for each item to see the total.</p>
        </details>
      </section>

      <!-- 7 · report (the page itself is in the main view) -->
      <section v-else-if="ui.step === 7 && A" key="7" class="card slim">
        <p class="say">Your one-page report.</p>
        <div class="row"><button class="big primary" @click="printReport">Print or save as PDF</button></div>
      </section>

      <!-- 8 · save -->
      <section v-else-if="ui.step === 8 && A" key="8" class="card">
        <p class="say">Take it with you.</p>
        <div class="toggles">
          <button class="tog" @click="saveCfg"><Icon name="layers" /><b>Save project</b><small>open it again later</small></button>
          <button class="tog" @click="download('dxf')"><Icon name="building" /><b>CAD</b><small>DXF</small></button>
          <button class="tog" @click="download('gpkg')"><Icon name="terrain" /><b>GIS</b><small>GeoPackage</small></button>
          <button class="tog" @click="state.showSchedule = !state.showSchedule"><Icon name="more" /><b>Tree table</b><small>CSV</small></button>
        </div>
        <p class="hint">Your project is also kept in this browser.</p>
      </section>

      <section v-else key="x" class="card">
        <p class="say">First, draw your street.</p>
        <div class="row"><button class="big primary" @click="go(1)">Go to step 1</button></div>
      </section>
    </Transition>

    <nav v-if="ui.step > 0" class="dots" aria-label="Steps">
      <button class="arrow" :disabled="ui.step === 0" aria-label="Back" @click="go(ui.step - 1)">←</button>
      <button v-for="(s, k) in STEPS.slice(1)" :key="s" class="dot" :class="{ on: ui.step === k + 1, done: k + 1 < ui.step }"
              :disabled="k + 1 > 1 && !A?.metrics" :aria-label="`Step ${k + 1}: ${s}`" :title="s" @click="go(k + 1)"></button>
      <button class="arrow next" :disabled="ui.step === STEPS.length - 1 || !canNext" aria-label="Next" @click="go(ui.step + 1)">→</button>
    </nav>
  </div>
</template>

<style scoped>
.guide { position: absolute; left: 20px; bottom: 20px; width: min(440px, calc(100% - 40px)); max-height: calc(100% - 40px); z-index: 7;
  display: flex; flex-direction: column; gap: 10px; pointer-events: none; }
.guide > * { pointer-events: auto; }
.guide.full { inset: 0; width: auto; max-height: none; align-items: center; justify-content: center; left: 0; bottom: 0;
  background: color-mix(in srgb, var(--bg) 82%, transparent); backdrop-filter: blur(3px); }
.guide.wide { width: 320px; }
.guide.above { bottom: calc(42% + 14px); max-height: calc(58% - 34px); } /* over the tree table */
.guide.above .card { max-height: calc(58vh - 140px); }
.card { background: var(--panel); border: 0.5px solid var(--line); border-radius: 18px; padding: 22px 24px; overflow: auto;
  box-shadow: 0 10px 30px rgba(42, 38, 34, 0.14); max-height: calc(100vh - 200px); }
.card.slim { padding: 16px 20px; }
.hero { max-width: 620px; text-align: center; padding: 40px 44px; }
h1 { font-size: 40px; line-height: 1.1; margin: 10px 0 14px; letter-spacing: -0.02em; animation: rise 0.6s ease both 0.15s; }
.lead { font-size: 18px; line-height: 1.5; color: var(--muted); margin: 0 auto 26px; animation: rise 0.6s ease both 0.3s; }
.say { font-size: 26px; line-height: 1.2; font-weight: 600; margin: 0 0 10px; letter-spacing: -0.01em; animation: rise 0.45s ease both; }
.say::before { content: ''; display: inline-block; width: 10px; height: 10px; border-radius: 50%; background: var(--good);
  margin-right: 10px; vertical-align: middle; animation: blink 1.6s ease-in-out infinite; }
.hint { font-size: 14px; color: var(--muted); line-height: 1.45; margin: 10px 0 0; animation: rise 0.45s ease both 0.1s; }
.pop { font-size: 16px; font-weight: 600; margin: 12px 0 0; animation: pop 0.4s ease both; }
.row { display: flex; gap: 10px; flex-wrap: wrap; justify-content: inherit; margin-top: 12px; }
.hero .row { justify-content: center; }
button.big { font-size: 17px; padding: 12px 22px; border-radius: 999px; display: inline-flex; gap: 8px; align-items: center; }
button.primary { background: var(--accent); color: var(--bg); border-color: var(--accent); font-weight: 600; transition: transform 0.15s; }
button.primary:hover:not(:disabled) { transform: translateY(-1px); }
button.ghost { background: transparent; }
.pill { border-radius: 999px; padding: 6px 14px; }
.toggles { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-top: 6px; }
.tog { display: grid; grid-template-columns: 26px 1fr; grid-template-rows: auto auto; column-gap: 8px; text-align: left; padding: 14px;
  border-radius: 14px; border: 1.5px solid var(--line); background: var(--bg); transition: border-color 0.2s, transform 0.15s, background 0.2s;
  animation: rise 0.45s ease both; }
.tog:nth-child(2) { animation-delay: 0.06s; } .tog:nth-child(3) { animation-delay: 0.12s; } .tog:nth-child(4) { animation-delay: 0.18s; }
.tog:hover:not(:disabled) { transform: translateY(-2px); border-color: var(--muted); }
.tog.on { border-color: var(--good); background: color-mix(in srgb, var(--good) 12%, var(--bg)); }
.tog :deep(svg) { grid-row: span 2; width: 22px; height: 22px; align-self: center; }
.tog b { font-size: 15px; } .tog small { color: var(--muted); font-size: 12px; }
.stats { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-top: 8px; }
.stats > div { background: var(--bg); border-radius: 14px; padding: 14px; animation: rise 0.45s ease both; }
.stats > div:nth-child(2) { animation-delay: 0.08s; } .stats > div:nth-child(3) { animation-delay: 0.16s; } .stats > div:nth-child(4) { animation-delay: 0.24s; }
.stats b { display: block; font-size: 34px; line-height: 1.1; letter-spacing: -0.02em; font-variant-numeric: tabular-nums; }
.stats .lbl { display: block; font-size: 13px; color: var(--muted); }
.stats .up b { color: var(--good); } .stats .down b { color: var(--bad); }
.more { margin-top: 12px; font-size: 14px; } .more summary { cursor: pointer; color: var(--accent); }
.cost { display: grid; gap: 6px; font-size: 14px; margin-top: 8px; }
.cost label { display: flex; justify-content: space-between; align-items: center; gap: 8px; }
.cost input { width: 100px; font-size: 15px; padding: 4px 8px; border-radius: 8px; }
.barri { margin-top: 6px; }
.dots { display: flex; align-items: center; gap: 8px; align-self: flex-start; background: var(--panel); border: 0.5px solid var(--line);
  border-radius: 999px; padding: 6px 10px; box-shadow: 0 4px 14px rgba(42, 38, 34, 0.1); }
.dot { width: 10px; height: 10px; padding: 0; border-radius: 50%; border: 0; background: var(--line); transition: width 0.3s, background 0.3s; }
.dot.done { background: var(--muted); }
.dot.on { width: 26px; border-radius: 6px; background: var(--accent); }
.arrow { border-radius: 50%; width: 34px; height: 34px; padding: 0; font-size: 16px; }
.arrow.next:not(:disabled) { background: var(--accent); color: var(--bg); border-color: var(--accent); }
.pulse { animation: blink 1s ease-in-out infinite; }
/* the sprout on the welcome screen: a trunk that grows, two leaves that open */
.sprout { position: relative; width: 60px; height: 70px; margin: 0 auto; }
.sprout span { position: absolute; left: 28px; bottom: 0; width: 4px; height: 0; background: var(--good); border-radius: 2px;
  animation: grow 0.8s ease forwards 0.1s; }
.sprout i { position: absolute; bottom: 34px; width: 22px; height: 12px; background: var(--good); border-radius: 12px 0;
  transform: scale(0); animation: leaf 0.5s ease forwards 0.8s; }
.sprout i:first-of-type { left: 8px; transform-origin: right bottom; }
.sprout i:last-of-type { left: 30px; border-radius: 0 12px; transform-origin: left bottom; animation-delay: 1s; }
/* page-to-page: the next step slides in from the right, the previous one leaves to the left */
.next-enter-active, .next-leave-active, .back-enter-active, .back-leave-active { transition: transform 0.35s cubic-bezier(.2, .8, .2, 1), opacity 0.3s; }
.next-enter-from, .back-leave-to { transform: translateX(60px); opacity: 0; }
.next-leave-to, .back-enter-from { transform: translateX(-60px); opacity: 0; }
@keyframes rise { from { transform: translateY(10px); opacity: 0; } to { transform: none; opacity: 1; } }
@keyframes pop { 0% { transform: scale(0.9); opacity: 0; } 60% { transform: scale(1.04); opacity: 1; } 100% { transform: none; } }
@keyframes blink { 50% { opacity: 0.35; } }
@keyframes grow { to { height: 48px; } }
@keyframes leaf { to { transform: scale(1); } }
@media (prefers-reduced-motion: reduce) { * { animation: none !important; transition: none !important; } }
@media (max-width: 700px) { h1 { font-size: 30px; } .say { font-size: 21px; } .stats b { font-size: 26px; } .toggles, .stats { grid-template-columns: 1fr; } }
</style>
