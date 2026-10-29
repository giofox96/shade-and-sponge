<script setup>
// Species cards: one botanical card per palette species, with a freely licensed photo (web/public/species/, from
// scripts/fetch_species_photos.py) and a dashboard of the traits the tool uses (meta.json → palette). The profile
// drawing is to one scale on every card, with a 1.7 m person, so the species compare at a glance.
import { computed, ref } from 'vue'
import { state, MONTHS, currentLayout } from '../store.js'

// Trunk classes of the inventory, 2011 street-tree guide p. 18 (shade_sponge/health.py); diameter = perimeter / π
const TRUNK = { SEGONA: [41, 80], TERCERA: [81, 110] }
const SIZE = { small: 'Small', medium: 'Medium', large: 'Large' }
const PERSON_M = 1.7 // scale figure only

const photos = ref({})
fetch('./species/photos.json').then((r) => (r.ok ? r.json() : {})).then((j) => (photos.value = j)).catch(() => {})

const sort = ref('palette')
const counts = computed(() => {
  const n = new Array(state.meta.palette.length).fill(0)
  for (const j of currentLayout()) n[j]++
  return n
})
const maxH = computed(() => Math.max(...state.meta.palette.map((p) => p.height_m)))
const maxLai = computed(() => Math.max(...state.meta.palette.map((p) => p.lai)))
const cards = computed(() => {
  const c = state.meta.palette.map((p, j) => ({ ...p, j, n: counts.value[j], photo: photos.value[p.species] }))
  const key = { height: 'height_m', crown: 'crown_diam_m', lai: 'lai', used: 'n' }[sort.value]
  return key ? c.sort((a, b) => b[key] - a[key]) : c
})
const trunk = (cls) => {
  const r = TRUNK[cls]
  if (!r) return { v: 'mixed', sub: 'all trunk classes (too few trees in one)' }
  return { v: `Ø ${Math.round(r[0] / Math.PI)}–${Math.round(r[1] / Math.PI)} cm`, sub: `${r[0]}–${r[1]} cm perimeter (${cls.toLowerCase()} class)` }
}
// profile drawing: 120 × 100 viewBox, ground at y = 94, metres → px at one scale for all cards
const S = computed(() => 84 / Math.max(maxH.value, 10))
const prof = (p) => {
  const s = S.value, cx = 70, g = 94
  return { s, cx, g, rx: (p.crown_diam_m / 2) * s, ry: ((p.height_m - p.crown_base_m) / 2) * s,
    cy: g - ((p.height_m + p.crown_base_m) / 2) * s, base: g - p.crown_base_m * s, top: g - p.height_m * s }
}
const evergreen = (h) => h.startsWith('evergreen')
</script>

<template>
  <div class="cards-view">
    <div class="bar">
      <div>
        <h2>Species</h2>
        <p class="small muted">The {{ state.meta.palette.length }} species of this palette, with the traits the tool uses: medians of the
          Porta trees measured by LiDAR (ICGC 2021). Same drawing scale on every card.</p>
      </div>
      <label class="small muted">Sort
        <select v-model="sort" aria-label="Sort species">
          <option value="palette">Palette order</option>
          <option value="used">Trees in this layout</option>
          <option value="height">Height</option>
          <option value="crown">Crown width</option>
          <option value="lai">LAI</option>
        </select>
      </label>
    </div>
    <div class="grid">
      <article v-for="p in cards" :key="p.species + p.j" class="card">
        <figure class="photo">
          <img v-if="p.photo" :src="`./species/${p.photo.file}`" :alt="`${p.species}, photo`" loading="lazy" />
          <div v-else class="nophoto small muted">No free photo yet</div>
          <figcaption v-if="p.photo" class="credit">
            <a :href="p.photo.page" target="_blank" rel="noopener">{{ p.photo.author }}</a>,
            <a v-if="p.photo.licence_url" :href="p.photo.licence_url" target="_blank" rel="noopener">{{ p.photo.licence }}</a>
            <template v-else>{{ p.photo.licence }}</template>, Wikimedia Commons
          </figcaption>
        </figure>
        <div class="body">
          <div class="title">
            <span class="dot" :style="{ background: p.color }"></span>
            <b><i>{{ p.species }}</i></b>
          </div>
          <div class="tags small">
            <span class="tag">{{ evergreen(p.leaf_habit) ? '● ' : '○ ' }}{{ p.leaf_habit }}</span>
            <span v-if="!p.in_palette" class="tag">today's tree, not in the palette</span>
            <span v-if="p.n" class="tag accent">{{ p.n.toLocaleString('en') }} in this layout</span>
          </div>

          <div class="dash">
            <svg class="profile" viewBox="0 0 120 100" role="img"
                 :aria-label="`Profile: ${p.height_m.toFixed(1)} m tall, crown ${p.crown_diam_m.toFixed(1)} m wide from ${p.crown_base_m.toFixed(1)} m`">
              <template v-for="d in [prof(p)]" :key="'d'">
                <line class="ground" x1="2" :y1="d.g" x2="118" :y2="d.g" />
                <line class="tick" x1="4" :y1="d.top" x2="10" :y2="d.top" />
                <line class="tick" x1="7" :y1="d.top" x2="7" :y2="d.g" />
                <text class="lbl" x="12" :y="d.top + 3">{{ p.height_m.toFixed(1) }} m</text>
                <rect class="trunk" :x="d.cx - 1.2" :y="d.base - 2" width="2.4" :height="d.g - d.base + 2" />
                <ellipse :cx="d.cx" :cy="d.cy" :rx="d.rx" :ry="d.ry" :fill="p.color" :fill-opacity="0.35 + 0.15 * p.lai" />
                <line class="tick" :x1="d.cx - d.rx" :y1="d.cy" :x2="d.cx + d.rx" :y2="d.cy" />
                <g class="person" :transform="`translate(${d.cx + Math.max(d.rx, 8) + 6} ${d.g}) scale(${(PERSON_M * d.s) / 10})`">
                  <circle cx="0" cy="-9" r="1" /><line x1="0" y1="-8" x2="0" y2="-4" /><line x1="0" y1="-4" x2="-1.2" y2="0" />
                  <line x1="0" y1="-4" x2="1.2" y2="0" /><line x1="-1.4" y1="-6.8" x2="1.4" y2="-6.8" />
                </g>
              </template>
            </svg>

            <ul class="kpis">
              <li>
                <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3v18M8 7l4-4 4 4M8 17l4 4 4-4" /></svg>
                <span><b>{{ p.height_m.toFixed(1) }} m</b><small>height</small></span>
              </li>
              <li>
                <svg viewBox="0 0 24 24" aria-hidden="true"><ellipse cx="12" cy="10" rx="9" ry="5" /><path d="M3 18h18M6 15.5 3 18l3 2.5M18 15.5l3 2.5-3 2.5" /></svg>
                <span><b>{{ p.crown_diam_m.toFixed(1) }} m</b><small>crown width</small></span>
              </li>
              <li>
                <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 21V9M12 9c-4 0-6-3-6-6 4 0 6 3 6 6Zm0 0c4 0 6-3 6-6-4 0-6 3-6 6ZM5 21h14" /></svg>
                <span><b>{{ p.crown_base_m.toFixed(1) }} m</b><small>clear trunk</small></span>
              </li>
              <li>
                <svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="8" /><circle cx="12" cy="12" r="4.5" /><circle cx="12" cy="12" r="1.2" /></svg>
                <span><b>{{ trunk(p.trunk_class).v }}</b><small :title="trunk(p.trunk_class).sub">trunk</small></span>
              </li>
              <li class="wide" :title="'Leaf area index: leaf area per unit of crown ground area (LiDAR proxy)'">
                <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 8h16M4 12h16M4 16h16" /><path d="M7 5c2 0 3 1 3 3M14 9c2 0 3 1 3 3M8 13c2 0 3 1 3 3" /></svg>
                <span><b>LAI {{ p.lai.toFixed(2) }}</b>
                  <span class="pips" aria-hidden="true"><i v-for="k in 5" :key="k" :class="{ on: p.lai >= (k - 0.5) * (maxLai / 5) }" :style="{ background: p.color }"></i></span>
                </span>
              </li>
              <li v-if="p.size_class">
                <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 20h18M3 20V8M21 20V8M8 20v-6M16 20v-6" /></svg>
                <span><b>{{ SIZE[p.size_class] }}</b><small>sidewalk size class</small></span>
              </li>
              <li v-if="p.cap != null">
                <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 18h16M7 18V9M12 18V5M17 18v-6" /></svg>
                <span><b>≤ {{ p.cap.toLocaleString('en') }}</b><small>trees (15% cap)</small></span>
              </li>
            </ul>
          </div>

          <div class="leaf" :title="p.leaf_basis">
            <span v-for="(f, m) in p.leaf" :key="m" :class="{ now: m === state.month - 1 }">
              <i :style="{ height: 3 + 16 * f + 'px', background: p.color }"></i>{{ MONTHS[m][0] }}
            </span>
          </div>
          <p class="small muted src">Leaf on: {{ p.leaf_basis }}</p>
        </div>
      </article>
    </div>
    <p class="small muted foot">Height, crown width, clear trunk (crown base) and LAI: medians of the LiDAR-measured Porta trees of the
      trunk class shown (the thesis compares species at equal trunk size); the LAI is a LiDAR proxy, not a measured value. Trunk
      classes and sidewalk size classes: Barcelona street-tree guide 2011. Photos: Wikimedia Commons, each under the licence shown.</p>
  </div>
</template>

<style scoped>
.cards-view { height: 100%; overflow: auto; padding: 54px 16px 16px; box-sizing: border-box; background: var(--bg); }
.bar { display: flex; justify-content: space-between; align-items: flex-end; gap: 12px; margin-bottom: 12px; flex-wrap: wrap; }
.bar h2 { font-size: 16px; font-weight: 500; margin: 0; }
.bar p { max-width: 60ch; }
.bar label { display: flex; align-items: center; gap: 6px; }
.bar select { width: auto; }
.grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 14px; }
.card { background: var(--panel); border: 0.5px solid var(--line); border-radius: 8px; overflow: hidden; display: flex; flex-direction: column; }
.photo { margin: 0; position: relative; aspect-ratio: 16 / 10; background: var(--hover); }
.photo img { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; display: block; }
.nophoto { display: flex; align-items: center; justify-content: center; height: 100%; }
.credit { position: absolute; left: 0; right: 0; bottom: 0; font-size: 10px; line-height: 1.3; padding: 10px 8px 4px;
  color: #F2F0EA; background: linear-gradient(transparent, rgba(0, 0, 0, 0.65)); overflow: hidden; white-space: nowrap; text-overflow: ellipsis; }
.credit a { color: inherit; }
.body { padding: 10px 12px 12px; }
.title { display: flex; align-items: center; gap: 6px; font-size: 14px; }
.tags { display: flex; flex-wrap: wrap; gap: 4px; margin: 6px 0 8px; }
.tag { background: var(--hover); padding: 1px 6px; border-radius: 4px; color: var(--muted); }
.tag.accent { color: var(--accent); }
.dash { display: grid; grid-template-columns: 110px 1fr; gap: 8px; align-items: start; }
.profile { width: 110px; height: auto; background: var(--map-bg); border-radius: 4px; }
.profile .ground { stroke: var(--muted); stroke-width: 0.8; }
.profile .tick { stroke: var(--muted); stroke-width: 0.6; }
.profile .lbl { font-size: 7px; fill: var(--muted); font-family: var(--mono); }
.profile .trunk { fill: var(--muted); }
.profile .person { stroke: var(--text); fill: none; stroke-width: 0.5; }
.profile .person circle { fill: var(--text); }
.kpis { list-style: none; padding: 0; margin: 0; display: grid; grid-template-columns: 1fr 1fr; gap: 6px 8px; }
.kpis li { display: flex; gap: 6px; align-items: center; min-width: 0; }
.kpis li.wide { grid-column: 1 / -1; }
.kpis svg { width: 20px; height: 20px; flex: none; stroke: var(--good); fill: none; stroke-width: 1.5; stroke-linecap: round; stroke-linejoin: round; }
.kpis b { display: block; font-size: 13px; font-weight: 500; font-variant-numeric: tabular-nums; }
.kpis small { display: block; font-size: 10px; color: var(--muted); }
.pips { display: inline-flex; gap: 2px; margin-left: 2px; }
.pips i { width: 14px; height: 5px; border-radius: 2px; opacity: 0.2; }
.pips i.on { opacity: 0.9; }
.kpis li.wide span { display: flex; align-items: center; gap: 8px; }
.leaf { display: flex; justify-content: space-between; align-items: flex-end; height: 34px; font-size: 10px; color: var(--muted); margin: 10px 0 2px; }
.leaf span { display: flex; flex-direction: column; align-items: center; gap: 2px; width: 14px; }
.leaf i { width: 8px; border-radius: 2px; opacity: 0.8; }
.leaf .now { color: var(--text); font-weight: 500; }
.src { margin: 2px 0 0; }
.foot { margin-top: 14px; max-width: 90ch; }
.dot { display: inline-block; width: 9px; height: 9px; border-radius: 50%; flex: none; }
.small { font-size: 11px; line-height: 1.45; }
.muted { color: var(--muted); }
</style>
