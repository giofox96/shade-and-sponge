// Shared state: site data exported by `python -m shade_sponge.web_export`, plus what the user has selected.
import { reactive, computed } from 'vue'
import { optimise, proxySums, fitLine } from './optimize.js'
import { loadGrid, pointPotentials } from './pointpot.js'

export const MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
export const BALANCED = 'S4_s0.50_w0.25_r0.25'
export const LIVE = 'live'

export const state = reactive({
  site: 'porta',
  meta: null,
  trees: null,
  pot: null,
  scenarioId: BALANCED,
  overlay: 'sun_winter',
  month: 7,
  selected: null, // index into positions
  error: null,
  // live optimisation
  share: 0.15,
  exclude: [],
  live: null, // { weights, layout, metrics, counts, ms, version }
  busy: false,
  liveError: null,
  // designer: trees added on the map
  addMode: false,
  added: [], // { lon, lat, x, y, pot: { summer, winter, water, fit }, species (palette index), auto, warn }
  addMsg: null,
  addedVersion: 0,
})

let grid = null
let treeXY = null // [x, y] of every existing street tree, for the spacing check
export const MIN_SPACING_M = 4 // ASSUMPTION: warn when a new tree is closer than this to another tree (no source yet)

export async function load(site = state.site) {
  const base = `./data/${site}/`
  try {
    const [meta, trees, pot] = await Promise.all(
      ['meta.json', 'trees.json', 'potentials.json'].map((f) => fetch(base + f).then((r) => r.json())),
    )
    Object.assign(state, { meta, trees, pot, site, share: pot.max_share })
  } catch (e) {
    state.error = `Couldn't load the site data (${e.message}). Run python -m shade_sponge.web_export first.`
  }
}

// Switch dataset (e.g. city palette 'porta' vs Barcelona shortlist 'porta-barcelona') and reset the view
export async function switchSite(site) {
  Object.assign(state, { scenarioId: BALANCED, live: null, selected: null, exclude: [], liveError: null, meta: null, added: [], addMsg: null })
  grid = null
  await load(site)
}

export const dataUrl = (file) => `./data/${state.site}/${file}`

export function currentLayout() {
  if (state.scenarioId === LIVE && state.live) return state.live.layout
  return state.trees.layouts[state.scenarioId] ?? state.trees.layouts.S0_current
}

export const scenario = computed(() => {
  if (state.scenarioId === LIVE && state.live) return { id: LIVE, group: 'live', ...state.live }
  return state.meta?.scenarios.find((s) => s.id === state.scenarioId)
})

export function label(s) {
  if (!s) return ''
  if (s.id === 'S0_current') return 'Current trees (mature planes)'
  if (s.id.startsWith('S1')) return `Random palette #${s.id.split('_').pop()}`
  const [a, b, c] = s.weights.map((w) => +w.toFixed(2))
  return `${s.id === LIVE ? 'Live estimate' : 'Optimised'}: summer ${a}, winter ${b}, runoff ${c}`
}

// Mean of the 10 random-palette layouts: the reference for "what a trait-blind replacement gives"
export const randomMean = computed(() => {
  const r = state.meta?.scenarios.filter((s) => s.group === 'S1') ?? []
  if (!r.length) return null
  const keys = Object.keys(r[0].metrics)
  return Object.fromEntries(keys.map((k) => [k, r.reduce((a, s) => a + s.metrics[k], 0) / r.length]))
})

// Calibration of live estimates: exact metric (full raster model) vs summed single-tree potentials, over the saved
// palette layouts (random #0 + 15 optimised). R² says how far to trust each estimate.
const PROXY = { shade_summer_m2h: 'shade_summer', shade_winter_m2h: 'shade_winter', runoff_hot_m3: 'water', runoff_m3: 'water', interception_m3: 'water' }
export const calibration = computed(() => {
  if (!state.meta) return null
  const saved = state.meta.scenarios.filter((s) => s.in_layouts && s.id !== 'S0_current')
  const sums = saved.map((s) => proxySums(state.pot, state.trees.layouts[s.id]))
  return Object.fromEntries(
    Object.entries(PROXY).map(([m, p]) => [m, fitLine(sums.map((x) => x[p]), saved.map((s) => s.metrics[m]))]),
  )
})

export async function runLive(weights) {
  state.busy = true
  state.liveError = null
  const res = await optimise(state.pot, weights, { share: state.share, exclude: state.exclude, extra: state.added })
  state.busy = false
  if (res.error) {
    state.liveError = res.error
    return
  }
  res.layout.slice(state.pot.fit.length).forEach((j, k) => Object.assign(state.added[k], { species: j, auto: true }))
  res.layout = res.layout.slice(0, state.pot.fit.length)
  const sums = proxySums(state.pot, res.layout)
  const metrics = Object.fromEntries(Object.entries(calibration.value).map(([m, c]) => [m, c.a + c.b * sums[PROXY[m]]]))
  const counts = Object.fromEntries(state.pot.species.map((s, j) => [s, res.layout.filter((x) => x === j).length]))
  state.live = { weights, layout: res.layout, metrics, counts, ms: res.ms, version: (state.live?.version ?? 0) + 1 }
  state.scenarioId = LIVE
}

// ---- designer mode: add trees -------------------------------------------------------------------------------
export async function setAddMode(on) {
  state.addMode = on
  state.addMsg = null
  if (on && !grid) {
    state.addMsg = 'Loading the site grid…'
    grid = await loadGrid(dataUrl(state.meta.grid.file), state.meta.grid)
    const p = state.trees.positions
    const k = state.trees.kept
    treeXY = [...p.lon.map((lon, i) => grid.toXY(lon, p.lat[i])), ...k.lon.map((lon, i) => grid.toXY(lon, k.lat[i]))]
    state.addMsg = null
  }
}

// weights on screen (live, precomputed optimised) or balanced
const weightsNow = () => (state.scenarioId === LIVE ? state.live?.weights : scenario.value?.weights) ?? [0.5, 0.25, 0.25]

// best fitting, allowed species for the current weights, scored like the optimiser (potentials normalised by their maxima)
function recommend(q) {
  const w = weightsNow()
  const mx = ['shade_summer', 'shade_winter', 'water'].map((k) => Math.max(...state.pot[k].flat()))
  let best = -1
  let bs = -Infinity
  state.pot.species.forEach((s, j) => {
    if (!q.fit[j] || state.exclude.includes(s)) return
    const z = [q.summer[j] / mx[0], -q.winter[j] / mx[1], q.water[j] / mx[2]]
    const sc = w.reduce((a, wk, n) => a + wk * z[n], 0) + 1e-3 * z.reduce((a, b) => a + b, 0)
    if (sc > bs) [best, bs] = [j, sc]
  })
  return best
}

export function addTreeAt(lon, lat) {
  const q = pointPotentials(grid, state.meta, lon, lat)
  if (!q.inSite) return void (state.addMsg = q.onRoof ? "That's a roof: pick open ground." : 'Outside the site: pick open ground in Porta.')
  if (q.facade_m < 1) return void (state.addMsg = 'Against a building (under 1 m): pick open ground.')
  const near = Math.min(...[...treeXY, ...state.added.map((a) => [a.x, a.y])].map(([x, y]) => Math.hypot(x - q.x, y - q.y)))
  const warn = []
  if (near < MIN_SPACING_M) warn.push(`${near.toFixed(1)} m from another tree (under ${MIN_SPACING_M} m)`)
  if (q.facade_m < 2) warn.push(`only ${q.facade_m.toFixed(1)} m to the nearest building`)
  const tree = { lon, lat, x: q.x, y: q.y, pot: { summer: q.summer, winter: q.winter, water: q.water, fit: q.fit }, warn,
    sun_summer: q.sun_summer, sun_winter: q.sun_winter, drains_to_hotspot: q.drains_to_hotspot }
  tree.species = recommend(tree.pot)
  tree.auto = true
  state.added.push(tree)
  state.addedVersion++
  state.selected = `a${state.added.length - 1}`
  state.addMsg = null
}

export function setAddedSpecies(k, j) {
  Object.assign(state.added[k], j == null ? { species: recommend(state.added[k].pot), auto: true } : { species: j, auto: false })
  state.addedVersion++
}

export function removeAdded(k) {
  state.added.splice(k, 1)
  state.selected = null
  state.addedVersion++
}

// Metrics shown: the layout's (exact or live estimate) plus the added trees, through the calibration slopes
const DELTA = { shade_summer_m2h: 'summer', shade_winter_m2h: 'winter', runoff_hot_m3: 'water', runoff_m3: 'water', interception_m3: 'water' }
export const shownMetrics = computed(() => {
  const base = scenario.value?.metrics
  if (!base || !state.added.length) return base
  state.addedVersion // dependency
  return Object.fromEntries(Object.entries(base).map(([m, v]) => {
    const k = DELTA[m]
    const d = state.added.reduce((a, t) => a + (t.species >= 0 ? t.pot[k][t.species] : 0), 0)
    return [m, v + (k ? calibration.value[m].b * d : 0)]
  }))
})

export function addedCsv() {
  const o = state.meta.grid.origin
  const rows = state.added.map((t, k) => {
    const s = state.meta.palette[t.species]
    return [`new_${k + 1}`, t.lon.toFixed(6), t.lat.toFixed(6), (t.x - o[0]).toFixed(2), (t.y - o[1]).toFixed(2), s.species,
      s.crown_diam_m, s.height_m, s.crown_base_m, s.lai, t.auto ? 'recommended' : 'designer'].join(',')
  })
  return ['tree_id,lon,lat,x,y,species,crown_diam_m,height_m,crown_base_m,lai,choice', ...rows].join(String.fromCharCode(10))
}

export const hexToRgb = (h) => [1, 3, 5].map((i) => parseInt(h.slice(i, i + 2), 16))
