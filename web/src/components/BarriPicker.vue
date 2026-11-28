<script setup>
// Neighbourhood picker: a mini-map of Barcelona's 73 barris (click one) plus a dropdown grouped by district.
// Only barris where the tool has been run (property `site`, scripts/make_barris_web.py) open on the map.
import { computed, onMounted, ref } from 'vue'
import { state, switchSite, city } from '../store.js'

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
// whole-city results (city.json): fill = method minus city practice (S1b), in points of today's summer shade
const res = (name) => city.data?.barris?.[name]
const gain = (name) => { const r = res(name); return r && r.summer_pct_method != null && r.summer_pct_s1b != null ? r.summer_pct_method - r.summer_pct_s1b : null }
function fillOf(name) {
  const r = res(name)
  if (r?.add_only) return 'var(--accent, #283F66)'
  const g = gain(name)
  if (g == null) return null
  const t = Math.max(0, Math.min(1, g / 10))                 // 0 → 10+ points
  return `rgb(${Math.round(214 - t * 151)}, ${Math.round(224 - t * 122)}, ${Math.round(205 - t * 143)})`   // pale sage → #3F663E
}
const infoRes = computed(() => info.value && res(info.value.name))
const pct = (v) => (v == null ? '–' : v.toFixed(1) + '%')

function pick(name) {
  const b = barris.value.find((x) => x.name === name)
  if (!b) return
  state.barri = name
  if (!b.site) return
  if (!state.site.startsWith(b.site)) switchSite(b.site)   // keeps the palette / tree-size variant of the same barri
}
</script>

<template>
  <div v-if="proj">
    <svg :viewBox="`0 0 ${W} ${proj.h.toFixed(0)}`" class="mini" role="img" aria-label="Map of Barcelona's neighbourhoods: click one to select it">
      <path v-for="b in barris" :key="b.name" :d="b.d" :class="{ ready: b.site, on: b.name === state.barri }"
            :style="fillOf(b.name) && !b.site ? { fill: fillOf(b.name) } : null"
            @click="pick(b.name)" @mouseenter="hover = b.name" @mouseleave="hover = null">
        <title>{{ b.name }}{{ b.site ? '' : res(b.name) ? (gain(b.name) != null ? ` (method − city practice: ${gain(b.name).toFixed(1)} pts)` : ' (shade added in free spots)') : ' (not computed yet)' }}</title>
      </path>
    </svg>
    <!-- type to search: the browser suggests matching names; Enter or a pick selects it -->
    <input class="find" type="search" list="barri-names" placeholder="Search a neighbourhood…" aria-label="Search a neighbourhood"
           @change="pick($event.target.value)" />
    <datalist id="barri-names"><option v-for="b in barris" :key="b.name" :value="b.name">{{ b.district }}</option></datalist>
    <select :value="state.barri" aria-label="Neighbourhood" @change="pick($event.target.value)">
      <optgroup v-for="[d, list] in districts" :key="d" :label="d">
        <option v-for="b in list" :key="b.name" :value="b.name">{{ b.name }}{{ b.site || res(b.name) ? '' : ' · not computed yet' }}</option>
      </optgroup>
    </select>
    <p v-if="info" class="small muted">
      <b class="ink">{{ info.name }}</b><template v-if="info.district"> · {{ info.district }}</template>
      <template v-if="info.planes != null"> · {{ info.planes.toLocaleString('en') }} planes of {{ info.street_trees.toLocaleString('en') }} street trees</template>
    </p>
    <table v-if="infoRes && !infoRes.add_only" class="small res">
      <tr><td>Method (own barri)</td><td>{{ pct(infoRes.summer_pct_method) }}</td></tr>
      <tr><td>City practice (S1b)</td><td>{{ pct(infoRes.summer_pct_s1b) }}</td></tr>
      <tr><td>City announced mix (S1a)</td><td>{{ pct(infoRes.summer_pct_s1a) }}</td></tr>
      <tr><td>Method, city-wide LP</td><td>{{ pct(infoRes.summer_pct_citylp) }}</td></tr>
      <tr><td colspan="2" class="muted">Summer shade of the street trees, % of today, every plane replaced.</td></tr>
    </table>
    <table v-else-if="infoRes?.add_only" class="small res">
      <tr><td colspan="2"><b>No planes: shade added</b> in {{ infoRes.spots }} free spots</td></tr>
      <tr><td>Method</td><td>+{{ pct(infoRes.summer_added_pct_method) }}</td></tr>
      <tr><td>City practice (S1b)</td><td>+{{ pct(infoRes.summer_added_pct_s1b) }}</td></tr>
      <tr><td>City announced mix (S1a)</td><td>+{{ pct(infoRes.summer_added_pct_s1a) }}</td></tr>
    </table>
    <p v-else-if="!barris.find((b) => b.name === state.barri)?.site" class="small warn">
      Not computed yet. The map still shows {{ state.meta.site.name }}. Running a barri needs its LiDAR crowns, sidewalk widths
      and site bundle (city-wide plan, §6).
    </p>
    <p class="small muted legend"><span><span class="sw ready"></span> full tool</span><span><span class="sw grad"></span> method − practice, 0 → 10 pts</span><span><span class="sw add"></span> shade added</span><span><span class="sw"></span> not computed</span></p>
    <p class="small muted">Outlines: {{ fc.source }}</p>
  </div>
</template>

<style scoped>
.mini { width: 100%; max-width: 260px; display: block; margin: 0 auto 6px; }
path { fill: var(--line); stroke: var(--panel); stroke-width: 0.6; cursor: pointer; }
path:hover { fill: var(--kept); }
path.ready { fill: var(--good); }
path.ready:hover { fill: var(--good); fill-opacity: 0.8; }
path.on { fill: var(--kept); stroke: var(--text); stroke-width: 1.6; }
path.ready.on { fill: var(--good); }
.ink { color: var(--text); font-weight: 600; }
.find { width: 100%; box-sizing: border-box; padding: 8px 12px; border-radius: 999px; border: 1px solid var(--line); background: var(--bg); color: var(--text); font: inherit; margin-bottom: 6px; }
.warn { color: var(--bad); }
.legend { display: flex; gap: 12px; }
.legend > span { display: inline-flex; align-items: center; gap: 4px; }
.sw { display: inline-block; width: 10px; height: 10px; border-radius: 2px; background: var(--line); }
.sw.ready { background: var(--good); }
.sw.grad { background: linear-gradient(90deg, rgb(214, 224, 205), rgb(63, 102, 62)); width: 22px; }
.sw.add { background: var(--accent, #283F66); }
.legend { flex-wrap: wrap; }
.res { width: 100%; border-collapse: collapse; margin: 4px 0 6px; }
.res td { padding: 2px 0; }
.res td + td { text-align: right; font-variant-numeric: tabular-nums; }
</style>
