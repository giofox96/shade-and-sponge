<script setup>
import { onMounted } from 'vue'
import { state, load, scenario, label, MONTHS, BALANCED } from './store.js'
import MapView from './components/MapView.vue'
import PriorityTriangle from './components/PriorityTriangle.vue'
import TradeoffChart from './components/TradeoffChart.vue'
import KpiPanel from './components/KpiPanel.vue'
import TreeInspector from './components/TreeInspector.vue'

onMounted(() => load())
</script>

<template>
  <div v-if="state.error" class="msg">{{ state.error }}</div>
  <div v-else-if="!state.meta" class="msg">Loading site…</div>
  <div v-else class="app">
    <header>
      <b>Shade and sponge</b>
      <span class="muted">Street-tree replacement in {{ state.meta.site.name }}, Barcelona · 832 plane-tree positions</span>
      <span class="spacer"></span>
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
        <p class="muted small">Each point is a precomputed optimal layout for those weights. Blue points are on the trade-off front.</p>
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
        <h3>Species</h3>
        <ul class="legend">
          <li v-for="p in state.meta.palette" :key="p.species">
            <span class="dot" :style="{ background: p.color }"></span>{{ p.species }}
            <span class="muted">{{ p.in_palette ? `cap ${p.cap}` : 'current' }}</span>
          </li>
        </ul>
      </section>
    </aside>

    <main><MapView /></main>

    <aside class="right">
      <section><h3>Results</h3><KpiPanel /></section>
      <section><h3>Trade-off</h3><TradeoffChart /></section>
      <section><h3>Selected tree</h3><TreeInspector /></section>
    </aside>
  </div>
</template>
