<script setup>
// Neighbourhood picker: a mini-map of Barcelona's 73 barris (click one) plus a dropdown grouped by district.
// Only barris where the tool has been run (property `site`, scripts/make_barris_web.py) open on the map.
import { computed, onMounted, ref } from 'vue'
import { state, switchSite } from '../store.js'

const W = 240
const fc = ref(null)
const hover = ref(null)
onMounted(async () => {
  try {
    fc.value = await fetch('./data/barris.geojson').then((r) => r.json())
  } catch {
    fc.value = { features: [] }
  }
})

// equirectangular projection fitted to the city, enough for a thumbnail
const proj = computed(() => {
  const pts = (fc.value?.features ?? []).flatMap((f) => rings(f.geometry).flat())
  if (!pts.length) return null
  const lons = pts.map((p) => p[0]), lats = pts.map((p) => p[1])
  const [x0, x1, y0, y1] = [Math.min(...lons), Math.max(...lons), Math.min(...lats), Math.max(...lats)]
  const k = Math.cos(((y0 + y1) / 2) * Math.PI / 180)
  const s = (W - 8) / ((x1 - x0) * k)
  return { f: ([lon, lat]) => [4 + (lon - x0) * k * s, 4 + (y1 - lat) * s], h: (y1 - y0) * s + 8 }
})
function rings(g) {
  return g.type === 'Polygon' ? g.coordinates : g.type === 'MultiPolygon' ? g.coordinates.flat() : []
}
const barris = computed(() => {
  if (!proj.value) return []
  return fc.value.features.map((f) => ({
    ...f.properties,
    d: rings(f.geometry).map((r) => 'M' + r.map((p) => proj.value.f(p).map((v) => v.toFixed(1)).join(',')).join('L') + 'Z').join(''),
  }))
})
const districts = computed(() => {
  const g = {}
  for (const b of barris.value) (g[b.district ?? 'Other'] ??= []).push(b)
  return Object.entries(g).sort(([a], [b]) => a.localeCompare(b))
})
const info = computed(() => barris.value.find((b) => b.name === (hover.value ?? state.barri)))

function pick(name) {
  const b = barris.value.find((x) => x.name === name)
  if (!b) return
  state.barri = name
  if (!b.site) return
  const site = state.site.endsWith('-barcelona') ? `${b.site}-barcelona` : b.site
  if (site !== state.site) switchSite(site)
}
</script>

<template>
  <div v-if="proj">
    <svg :viewBox="`0 0 ${W} ${proj.h.toFixed(0)}`" class="mini" role="img" aria-label="Map of Barcelona's neighbourhoods: click one to select it">
      <path v-for="b in barris" :key="b.name" :d="b.d" :class="{ ready: b.site, on: b.name === state.barri }"
            @click="pick(b.name)" @mouseenter="hover = b.name" @mouseleave="hover = null">
        <title>{{ b.name }}{{ b.site ? '' : ' (not computed yet)' }}</title>
      </path>
    </svg>
    <select :value="state.barri" aria-label="Neighbourhood" @change="pick($event.target.value)">
      <optgroup v-for="[d, list] in districts" :key="d" :label="d">
        <option v-for="b in list" :key="b.name" :value="b.name">{{ b.name }}{{ b.site ? '' : ' · not computed yet' }}</option>
      </optgroup>
    </select>
    <p v-if="info" class="small muted">
      <b class="ink">{{ info.name }}</b><template v-if="info.district"> · {{ info.district }}</template>
      <template v-if="info.planes != null"> · {{ info.planes.toLocaleString('en') }} planes of {{ info.street_trees.toLocaleString('en') }} street trees</template>
    </p>
    <p v-if="!barris.find((b) => b.name === state.barri)?.site" class="small warn">
      Not computed yet. The map still shows {{ state.meta.site.name }}. Running a barri needs its LiDAR crowns, sidewalk widths
      and site bundle (city-wide plan, §6).
    </p>
    <p class="small muted legend"><span><span class="sw ready"></span> computed</span><span><span class="sw"></span> not yet</span></p>
    <p class="small muted">Outlines: {{ fc.source }}</p>
  </div>
</template>

<style scoped>
.mini { width: 100%; max-width: 260px; display: block; margin: 0 auto 6px; }
path { fill: var(--line); stroke: var(--panel); stroke-width: 0.6; cursor: pointer; }
path:hover { fill: var(--stone); }
path.ready { fill: var(--accent); }
path.ready:hover { fill: #557f53; }
path.on { fill: var(--stone); stroke: var(--text); stroke-width: 1.6; }
path.ready.on { fill: var(--accent); }
.ink { color: var(--text); font-weight: 600; }
.warn { color: var(--heat); }
.legend { display: flex; gap: 12px; }
.legend > span { display: inline-flex; align-items: center; gap: 4px; }
.sw { display: inline-block; width: 10px; height: 10px; border-radius: 2px; background: var(--line); }
.sw.ready { background: var(--accent); }
</style>
