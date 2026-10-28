// Shared state: site data exported by `python -m shade_sponge.web_export`, plus what the user has selected.
import { reactive, computed } from 'vue'
import { optimise, proxySums, fitLine, effSpecies, caps } from './optimize.js'
import { loadGrid, pointPotentials, crownPotential } from './pointpot.js'

export const MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
export const BALANCED = 'S4_s0.50_w0.25_r0.25'
export const LIVE = 'live'
export const AREA = 'area'

export const state = reactive({
  site: 'porta',
  meta: null,
  trees: null,
  pot: null,
  scenarioId: BALANCED,
  compare: false, // side-by-side columns (today | city rule | optimised) instead of the 3D map
  // project area: only the plane positions inside a drawn polygon are replaced; outside, today's trees stay
  drawing: false,
  draft: [], // [lon, lat] vertices while drawing
  area: null, // { poly, idx, weights, layout, metrics, counts, city: { metrics, counts }, ms }
  overlay: 'sun_winter',
  month: 7,
  selected: null, // index into positions
  error: null,
  // live optimisation
  share: 0.15,
  exclude: [],
  minEff: 0, // diversity floor, effective number of species among planted positions (0 = off)
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
  Object.assign(state, { scenarioId: BALANCED, live: null, selected: null, exclude: [], minEff: 0, liveError: null, meta: null, added: [], addMsg: null, area: null, drawing: false, draft: [] })
  grid = null
  planePotCache.clear()
  planeScale = null
  await load(site)
}

export const dataUrl = (file) => `./data/${state.site}/${file}`

export function currentLayout() {
  if (state.scenarioId === AREA && state.area) return areaLayout(state.area.layout)
  if (state.scenarioId === LIVE && state.live) return state.live.layout
  return state.trees.layouts[state.scenarioId] ?? state.trees.layouts.S0_current
}

// Effective number of species (exp of Shannon H) among the plane positions of the layout on screen
export const layoutEff = computed(() => state.pot && state.trees && effSpecies(currentLayout(), state.pot.species.length))

export const scenario = computed(() => {
  if (state.scenarioId === AREA && state.area) return { id: AREA, group: 'area', ...state.area }
  if (state.scenarioId === LIVE && state.live) return { id: LIVE, group: 'live', ...state.live }
  return state.meta?.scenarios.find((s) => s.id === state.scenarioId)
})

export function label(s) {
  if (!s) return ''
  if (s.id === 'S0_current') return 'Current trees (mature planes)'
  if (s.id === AREA) {
    const [a, b, c] = s.weights.map((w) => +w.toFixed(2))
    return `Project area, ${s.idx.length} planes replaced: summer ${a}, winter ${b}, runoff ${c}`
  }
  if (s.id.startsWith('S1a')) return `City rule (2026 mix) #${s.id.split('_').pop()}`
  if (s.id.startsWith('S1')) return `Random palette #${s.id.split('_').pop()}`
  const [a, b, c] = s.weights.map((w) => +w.toFixed(2))
  return `${s.id === LIVE ? 'Live estimate' : 'Optimised'}: summer ${a}, winter ${b}, runoff ${c}`
}

// Mean of the 10 city-rule layouts (S1a, the 2026 mix within the sizing rule): the thesis baseline
export const cityMean = computed(() => {
  const r = state.meta?.scenarios.filter((s) => s.group === 'S1a') ?? []
  if (!r.length) return null
  const keys = Object.keys(r[0].metrics)
  return Object.fromEntries(keys.map((k) => [k, r.reduce((a, s) => a + s.metrics[k], 0) / r.length]))
})

// "vs city rule" reference: the whole-site S1a mean, or the city rule inside the project area (estimate)
export const baseline = computed(() => (state.scenarioId === AREA && state.area ? state.area.city.metrics : cityMean.value))

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
  if (state.area) return runArea(weights)
  state.busy = true
  state.liveError = null
  const res = await optimise(state.pot, weights, { share: state.share, exclude: state.exclude, extra: state.added, minEff: state.minEff })
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
    await ensureGrid()
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
    if (!k || v == null) return [m, v] // e.g. canopy cover: no per-tree potential, left as it is
    const d = state.added.reduce((a, t) => a + (t.species >= 0 ? t.pot[k][t.species] : 0), 0)
    return [m, v + calibration.value[m].b * d]
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

// ---- project area: replace only the plane positions inside a drawn polygon ----------------------------------
// Estimates, like the live layouts: today's exact metrics + calibration slope × Σ (potential of the new species −
// potential of today's tree) over the positions in the area. Today's planes are scored with their measured crown
// (trees.json) and the plane's median LAI (ASSUMPTION: per-tree LAI is not exported). Canopy cover is not estimated.
async function ensureGrid() {
  if (grid) return
  grid = await loadGrid(dataUrl(state.meta.grid.file), state.meta.grid)
  const p = state.trees.positions
  const k = state.trees.kept
  treeXY = [...p.lon.map((lon, i) => grid.toXY(lon, p.lat[i])), ...k.lon.map((lon, i) => grid.toXY(lon, k.lat[i]))]
}

function insidePoly(lon, lat, poly) {
  let inside = false
  for (let a = 0, b = poly.length - 1; a < poly.length; b = a++) {
    const [xa, ya] = poly[a]
    const [xb, yb] = poly[b]
    if ((ya > lat) !== (yb > lat) && lon < ((xb - xa) * (lat - ya)) / (yb - ya) + xa) inside = !inside
  }
  return inside
}

// Full-length layout: today's trees everywhere, the area's species at its positions
export function areaLayout(sub) {
  const full = [...state.trees.layouts.S0_current]
  state.area.idx.forEach((i, k) => (full[i] = sub[k]))
  return full
}

export function startDrawing() {
  Object.assign(state, { drawing: true, draft: [], compare: false, addMode: false,
    addMsg: 'Click on the map to place the corners of the project area, then press Finish.' })
}
export function addVertex(lon, lat) {
  state.draft = [...state.draft, [lon, lat]]
}
export function cancelDrawing() {
  Object.assign(state, { drawing: false, draft: [], addMsg: null })
}
export function clearArea() {
  Object.assign(state, { area: null, drawing: false, draft: [], addMsg: null })
  if (state.scenarioId === AREA) state.scenarioId = BALANCED
}

const planePotCache = new Map()
function planePot(i) {
  if (!planePotCache.has(i)) {
    const p = state.trees.positions
    const plane = state.meta.palette.find((s) => !s.in_palette)
    const [x, y] = grid.toXY(p.lon[i], p.lat[i])
    planePotCache.set(i, p.s0_crown_diam_m[i] > 0
      ? crownPotential(grid, state.meta.model, x, y,
        { ...plane, crown_diam_m: p.s0_crown_diam_m[i], height_m: p.s0_height_m[i], crown_base_m: p.s0_crown_base_m[i] })
      : { summer: 0, winter: 0, water: 0 })
  }
  return planePotCache.get(i)
}

const POT_KEY = { shade_summer: 'summer', shade_winter: 'winter', water: 'water' }
// Today's planes are scored with the browser formulas and a median LAI, which can sit off the calibration line of the
// palette potentials (Python). Scale them per metric so that the line, fed with every plane, gives today's exact value:
// k_m = ((S0_m − a_m) / b_m) / Σ_all plane potential. An area with no positions then returns today exactly, and an area
// with every position returns the live estimate of a full replacement.
let planeScale = null
function planeScales() {
  if (planeScale) return planeScale
  const s0 = state.meta.scenarios.find((s) => s.id === 'S0_current').metrics
  const all = { shade_summer: 0, shade_winter: 0, water: 0 }
  state.trees.positions.lon.forEach((_, i) => {
    const q = planePot(i)
    for (const k in all) all[k] += q[POT_KEY[k]]
  })
  planeScale = Object.fromEntries(Object.entries(calibration.value).map(([m, c]) => [m, (s0[m] - c.a) / c.b / all[PROXY[m]]]))
  return planeScale
}

// Metrics of "today's trees outside, new trees inside": sums[k] = Σ potential of the new trees in the area
function areaMetrics(idx, sums) {
  const s0 = state.meta.scenarios.find((s) => s.id === 'S0_current').metrics
  const k = planeScales()
  const today = { shade_summer: 0, shade_winter: 0, water: 0 }
  idx.forEach((i) => {
    const q = planePot(i)
    for (const key in today) today[key] += q[POT_KEY[key]]
  })
  return Object.fromEntries(Object.keys(s0).map((m) =>
    [m, PROXY[m] ? s0[m] + calibration.value[m].b * (sums[PROXY[m]] - k[m] * today[PROXY[m]]) : null]))
}

// City rule inside the area: the expected value of the S1a draw (2026 mix weights among the fitting mix species;
// any fitting species if none of the mix fits, as layout.s1a_layout's last resort)
function areaCity(idx) {
  const pot = state.pot
  const cap = caps(pot, state.share, state.exclude)
  let w = pot.species.map((s) => state.meta.s1a_mix?.[s] ?? 0)
  const probs = () => idx.map((i) => {
    let ww = pot.species.map((_, j) => (pot.fit[i][j] ? w[j] : 0))
    if (!ww.some((v) => v > 0)) ww = pot.species.map((_, j) => pot.fit[i][j])
    const tot = ww.reduce((a, b) => a + b, 0)
    return ww.map((v) => v / tot)
  })
  // the 15% cap, as in the exact S1a draws: shrink the weight of any species whose expected count exceeds its room
  let P = probs()
  for (let it = 0; it < 20; it++) {
    const n = pot.species.map((_, j) => P.reduce((a, p) => a + p[j], 0))
    const over = n.map((v, j) => (v > cap[j] + 0.5 ? cap[j] / v : 1))
    if (over.every((f) => f === 1)) break
    w = w.map((v, j) => v * over[j])
    P = probs()
  }
  const sums = { shade_summer: 0, shade_winter: 0, water: 0 }
  const counts = Object.fromEntries(pot.species.map((s) => [s, 0]))
  idx.forEach((i, r) => P[r].forEach((v, j) => {
    if (!v) return
    for (const k in sums) sums[k] += v * pot[k][i][j]
    counts[pot.species[j]] += v
  }))
  return { metrics: areaMetrics(idx, sums), counts: Object.fromEntries(Object.entries(counts).map(([s, n]) => [s, Math.round(n)])) }
}

export async function finishArea() {
  if (state.draft.length < 3) return void (state.addMsg = 'An area needs at least three corners.')
  const poly = state.draft
  const p = state.trees.positions
  const idx = p.lon.map((lon, i) => (insidePoly(lon, p.lat[i], poly) ? i : -1)).filter((i) => i >= 0)
  if (!idx.length) return void (state.addMsg = 'No plane positions inside that area: draw it around some street trees.')
  state.addMsg = 'Loading the site grid…'
  await ensureGrid()
  Object.assign(state, { drawing: false, draft: [], addMsg: null })
  state.area = { poly, idx, weights: weightsNow(), layout: [], metrics: null, counts: {}, city: areaCity(idx) }
  await runArea(state.area.weights)
}

export async function runArea(weights) {
  const { idx } = state.area
  const pot = state.pot
  const sub = { ...pot, fit: idx.map((i) => pot.fit[i]) }
  for (const k of ['shade_summer', 'shade_winter', 'water']) sub[k] = idx.map((i) => pot[k][i])
  state.busy = true
  state.liveError = null
  const res = await optimise(sub, weights, { share: state.share, exclude: state.exclude, minEff: state.minEff })
  state.busy = false
  if (res.error) return void (state.liveError = res.error)
  const sums = { shade_summer: 0, shade_winter: 0, water: 0 }
  res.layout.forEach((j, k) => {
    for (const key in sums) sums[key] += sub[key][k][j]
  })
  const counts = Object.fromEntries(pot.species.map((s, j) => [s, res.layout.filter((x) => x === j).length]))
  Object.assign(state.area, { weights, layout: res.layout, metrics: areaMetrics(idx, sums), counts, ms: res.ms,
    version: (state.area.version ?? 0) + 1 })
  state.scenarioId = AREA
}
