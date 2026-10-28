<script setup>
import { onMounted, watch } from 'vue'
import { state, load, switchSite, scenario, label, layoutEff, runLive, runArea, setAddMode, addedCsv, startDrawing, finishArea,
  cancelDrawing, clearArea, setAreaAll, fillAreaSpots, panels, ui, MIN_SPACING_M, MONTHS, BALANCED, LIVE, AREA } from './store.js'
import MapView from './components/MapView.vue'
import PriorityTriangle from './components/PriorityTriangle.vue'
import TradeoffChart from './components/TradeoffChart.vue'
import KpiPanel from './components/KpiPanel.vue'
import TreeInspector from './components/TreeInspector.vue'
import ComparePanel from './components/ComparePanel.vue'
import CoverCounter from './components/CoverCounter.vue'
import PanelHandle from './components/PanelHandle.vue'
import BarriPicker from './components/BarriPicker.vue'

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
    const w = scenario.value?.weights
    if (w) state.scenarioId === AREA ? runArea(w) : runLive(w)
  },
)
</script>

<template>
  <div v-if="state.error" class="msg">{{ state.error }}</div>
  <div v-else-if="!state.meta" class="msg">Loading site…</div>
  <div v-else class="app" :style="{ '--lw': panels.leftOpen ? panels.leftW + 'px' : '0px', '--rw': panels.rightOpen ? panels.rightW + 'px' : '0px' }">
    <header>
      <b>Shade and sponge</b>
      <span class="muted">{{ state.meta.site.name }}, Barcelona</span>
      <span class="spacer"></span>
      <span class="ctl muted">Palette</span>
      <span class="seg" role="group" aria-label="Species palette">
        <button :class="{ on: state.site !== 'porta-barcelona' }" @click="switchSite('porta')">City (7)</button>
        <button :class="{ on: state.site === 'porta-barcelona' }" @click="switchSite('porta-barcelona')">Barcelona (34)</button>
      </span>
      <template v-if="state.site !== 'porta-barcelona'">
        <span class="ctl muted">New trees at</span>
        <span class="seg" role="group" aria-label="Size of the new trees">
          <button :class="{ on: state.site === 'porta-segona' }" aria-label="About 10 years after planting"
                  title="Second trunk class (41–80 cm perimeter): median 9.7 years after planting for the dated palette trees"
                  @click="switchSite('porta-segona')">≈ 10 years</button>
          <button :class="{ on: state.site === 'porta' }" aria-label="Established trees"
                  title="Third trunk class (81–110 cm perimeter): the thesis comparison at equal trunk size"
                  @click="switchSite('porta')">Established</button>
        </span>
      </template>
      <span class="seg" role="group" aria-label="Colour theme">
        <button v-for="[t, l] in [['auto', 'Auto'], ['light', 'Light'], ['dark', 'Dark']]" :key="t" :class="{ on: ui.theme === t }"
                :aria-pressed="ui.theme === t" :title="t === 'auto' ? 'Follow the system setting' : `${l} theme`" @click="ui.theme = t">{{ l }}</button>
      </span>
    </header>

    <aside v-show="panels.leftOpen" class="left">
      <details class="group" open>
        <summary>Neighbourhood <span class="muted">{{ state.barri }}</span></summary>
        <section><BarriPicker /></section>
      </details>
      <section>
        <h3>1 · Scenario</h3>
        <div class="btns">
          <button :class="{ on: state.scenarioId === 'S0_current' }" @click="state.scenarioId = 'S0_current'">Today</button>
          <button :class="{ on: state.scenarioId === 'S1a_city_0' }" @click="state.scenarioId = 'S1a_city_0'">City rule</button>
          <button :class="{ on: state.scenarioId.startsWith('S4') || state.scenarioId === LIVE }" @click="state.scenarioId = BALANCED">Optimised</button>
          <button v-if="state.area" :class="{ on: state.scenarioId === AREA }" @click="state.scenarioId = AREA">Project area</button>
          <button class="ghost" :class="{ on: state.scenarioId === 'S1_random_0' }" title="A random palette under the same rules: what optimisation adds over chance"
                  @click="state.scenarioId = 'S1_random_0'">Random</button>
        </div>
        <p class="sub">Priorities <span class="muted">· click to re-optimise</span></p>
        <PriorityTriangle />
        <p v-if="state.busy" class="small accent">Optimising…</p>
        <p v-if="state.liveError" class="small danger">{{ state.liveError }}</p>
        <details class="how"><summary>How it works</summary>
          <p class="small muted">Dots are precomputed layouts with exact scores (filled blue = on the trade-off front). A click anywhere else re-optimises
            in your browser: the result is an estimate. The same applies inside a project area.</p>
        </details>
      </section>

      <section>
        <h3>2 · Project area <span class="muted">{{ state.area ? `${state.area.all ? state.area.idx.length + state.area.keptIdx.length + ' trees' : state.area.idx.length + ' planes'}` : 'whole site' }}</span></h3>
        <div class="btns">
          <button v-if="!state.drawing" @click="startDrawing">{{ state.area ? 'Redraw' : 'Draw an area' }}</button>
          <button v-if="state.drawing" :disabled="state.draft.length < 3" @click="finishArea">Finish ({{ state.draft.length }} corners)</button>
          <button v-if="state.drawing" @click="cancelDrawing">Cancel</button>
          <button v-if="state.area && !state.drawing" @click="clearArea">Whole site</button>
        </div>
        <template v-if="state.area && !state.drawing">
          <label class="check"><input type="checkbox" :checked="state.area.all" :disabled="!state.area.idx.length"
                 @change="setAreaAll($event.target.checked)" />
            Replace all {{ state.area.idx.length + state.area.keptIdx.length }} trees, not only the {{ state.area.idx.length }} planes</label>
          <p v-if="state.area.all" class="small accent">New trees are scored at the selected size, today's at theirs: replacing young or healthy
            trees looks like a gain that takes years to arrive. Check "≈ 10 years".</p>
          <div class="btns">
            <button :disabled="!state.area.spotIdx.length" @click="fillAreaSpots">Fill the {{ state.area.spotIdx.length }} free spots</button>
          </div>
        </template>
        <details class="how"><summary>How it works</summary>
          <p class="small muted">Trees are replaced where a dead tree, a project or a street rebuild opens the ground. Draw that place: only the
            trees inside are replaced and compared, today's trees stay everywhere else. Free spots are sidewalks of at least 2.5 m with room
            for a tree by the 2011 guide's spacing, away from the crossings, traffic signals, parking entrances and bus stops mapped in OpenStreetMap (still an upper bound: driveways, lamps and services are not in the data); each gets
            its sidewalk's size class.</p>
        </details>
      </section>

      <section>
        <h3>3 · Add trees <span class="muted">{{ state.added.length ? `${state.added.length} added` : '' }}</span></h3>
        <div class="btns">
          <button :class="{ on: state.addMode }" @click="setAddMode(!state.addMode)">{{ state.addMode ? 'Stop adding' : 'Add trees' }}</button>
          <button v-if="state.added.length" @click="downloadAdded">Download CSV</button>
          <button v-if="state.added.length" @click="clearAdded">Clear</button>
        </div>
        <p v-if="state.addMode" class="small muted">Click open ground or a green free spot. Each tree gets the best species for the current
          priorities (change it in the inspector). Warns under {{ MIN_SPACING_M }} m from another tree (assumption).</p>
        <p v-if="state.addMsg" class="small accent">{{ state.addMsg }}</p>
      </section>

      <details class="group">
        <summary>Rules and species <span class="muted">{{ Math.round(state.share * 100) }}% cap{{ state.minEff ? ` · ≥ ${state.minEff} species` : '' }}{{ state.exclude.length ? ` · ${state.exclude.length} excluded` : '' }}</span></summary>
        <section>
          <h3>Max share per species <span class="muted">{{ Math.round(state.share * 100) }}%</span></h3>
          <input type="range" min="0.05" max="0.3" step="0.01" v-model.number="state.share" aria-label="Maximum share per species" />
          <p class="small muted">Of all {{ state.pot.n_total.toLocaleString('en') }} street trees; the city tree plan sets 15%.</p>
        </section>
        <section>
          <h3>Diversity floor <span class="muted">{{ state.minEff ? `≥ ${state.minEff} effective species` : 'off' }}</span></h3>
          <label class="check"><input type="checkbox" :checked="state.minEff > 0"
                 @change="state.minEff = $event.target.checked ? Math.min(8, state.pot.species.length - state.exclude.length - 1) : 0" />
            Keep a minimum Shannon diversity</label>
          <input v-if="state.minEff" type="range" min="2" :max="state.pot.species.length - state.exclude.length" step="1" v-model.number="state.minEff"
                 aria-label="Minimum effective number of species" />
          <p class="small muted">exp(Shannon H) of the replanted positions. This layout: {{ layoutEff?.toFixed(1) }}.</p>
        </section>
        <section>
          <h3>Species <span class="muted">untick to exclude</span></h3>
          <p v-if="state.meta.palette_kind === 'barcelona'" class="small muted">Colour = leaf habit (ochre deciduous, green evergreen, olive semi-deciduous); darker = larger crown.</p>
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
      </details>

      <details class="group">
        <summary>Map display <span class="muted">{{ MONTHS[state.month - 1] }}{{ state.overlay ? ' · ' + state.meta.overlays.find((o) => o.id === state.overlay)?.label.split(' (')[0] : '' }}</span></summary>
        <section>
          <label class="check"><input type="checkbox" v-model="state.showStreets" /> Sidewalks and free spots</label>
          <p class="small muted">Brown = façade, dark = kerb: the sidewalk is the band between them. Green dots = free spots, light to dark =
            small / medium / large tree.</p>
          <h3 class="mt">Overlay</h3>
          <select v-model="state.overlay" aria-label="Map overlay">
            <option value="">None</option>
            <option v-for="o in state.meta.overlays" :key="o.id" :value="o.id">{{ o.label }}</option>
          </select>
          <h3 class="mt">Month <span class="muted">{{ MONTHS[state.month - 1] }}</span></h3>
          <input type="range" min="1" max="12" step="1" v-model.number="state.month" aria-label="Month" />
          <p class="small muted">Crown opacity follows each species' leaf calendar.</p>
        </section>
      </details>

      <details class="group">
        <summary>Data and sources</summary>
        <p class="small muted sources">
          Street trees: Ajuntament de Barcelona, Open Data BCN (CC BY 4.0) ·
          LiDAR crowns, terrain, building heights: ICGC 2021–2022 (CC BY 4.0) ·
          Sidewalks: 1:1000 base map, Ajuntament de Barcelona (CC BY 4.0) ·
          Building footprints, neighbourhood outlines (provisional) and basemap: © OpenStreetMap contributors (ODbL); basemap tiles OpenFreeMap (light) and © CARTO (dark) ·
          Flood-hazard index: Barcelona Resilience Atlas, Barcelona Regional (derived threshold; licence not stated) ·
          Design storms: PDISBA rainfall study · Storm months: Esbrí, Rigo and Llasat ·
          Interception calibration: Anys and Weiler 2024 data (CC BY-NC 4.0).
          Thesis prototype (MaCAD, IAAC); heat is a shade proxy, not UTCI.
          <a href="https://github.com/giofox96/shade-and-sponge" target="_blank" rel="noopener">Code and method</a>
        </p>
      </details>
    </aside>

    <main>
      <div class="tabs seg" role="tablist" aria-label="View">
        <button role="tab" :aria-selected="!state.compare" :class="{ on: !state.compare }" @click="state.compare = false">Map</button>
        <button role="tab" :aria-selected="state.compare" :class="{ on: state.compare }" @click="state.compare = true">Compare side by side</button>
      </div>
      <ComparePanel v-if="state.compare" />
      <MapView v-else :key="state.site" />
      <PanelHandle side="left" />
      <PanelHandle side="right" />
    </main>

    <aside v-show="panels.rightOpen" class="right">
      <section><h3>Canopy cover</h3><CoverCounter /></section>
      <section>
        <h3>Results</h3>
        <p class="small muted scen">{{ label(scenario) }}</p>
        <KpiPanel />
      </section>
      <details class="group" open>
        <summary>Trade-off</summary>
        <section><TradeoffChart /></section>
      </details>
      <section><h3>Selected tree</h3><TreeInspector /></section>
    </aside>
  </div>
</template>
