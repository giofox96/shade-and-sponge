// Shared state: site data exported by `python -m shade_sponge.web_export`, plus what the user has selected.
import { reactive, computed, watch } from 'vue'
import { optimise, proxySums, fitLine, effSpecies, caps } from './optimize.js'
import { loadGrid, pointPotentials, crownPotential } from './pointpot.js'

export const MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
export const BALANCED = 'S4_s0.50_w0.25_r0.25'
export const LIVE = 'live'
export const AREA = 'area'

export const state = reactive({
  site: 'porta',
  barri: 'Porta', // neighbourhood picked in BarriPicker (only barris with exported data change `site`)
  meta: null,
  trees: null,
  pot: null,
  scenarioId: BALANCED,
  view: 'map', // 'map' | 'compare' (side-by-side columns: today | city rule | optimised) | 'species' (botanical cards)
  speciesScope: 'site', // Species tab: 'site' (whole neighbourhood) or 'area' (the project area, when one is drawn)
  // project area: only the plane positions inside a drawn polygon are replaced; outside, today's trees stay
  drawing: false,
  editing: false, // moving the corners of the project area (draft holds the polygon being edited)
  draft: [], // [lon, lat] vertices while drawing
  area: null, // { poly, idx, keptIdx, spotIdx, all, weights, layout, keptLayout, metrics, counts, city, ms }
  buildingOpacity: 1, // Map display slider: 1 = solid, lower = see-through buildings
  showStreets: true, // sidewalk edges (facades, kerbs) and free planting spots on the map
  overlay: '', // none by default: sidewalks and free spots read better (the sun / water layers are in Map display)
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
  Object.assign(state, { scenarioId: BALANCED, live: null, selected: null, exclude: [], minEff: 0, liveError: null, meta: null, added: [], addMsg: null, area: null, drawing: false, editing: false, draft: [], addMode: false }) // the new site's grid loads with the next Add trees
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
    const n = s.idx.length + (s.all ? s.keptIdx.length : 0)
    return `Project area, ${n} ${s.all ? 'trees' : 'planes'} replaced: summer ${a}, winter ${b}, runoff ${c}`
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
export const baseline = computed(() => (state.scenarioId === AREA && state.area?.city ? state.area.city.metrics : cityMean.value))

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
  state.addMsg = null
  if (on && !grid) {
    state.addMsg = 'Loading the site grid…'
    await ensureGrid()
    state.addMsg = null
  }
  state.addMode = on // after the grid: the map draws where trees can go from it
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

// Where "Add trees" accepts a click, as an RGBA canvas on the site grid (row 0 = north): open ground in the site, not a
// roof, at least 1 m from a building. Amber where the click is accepted with a warning: under 2 m from a building or under
// MIN_SPACING_M from another tree. The same rules as addTreeAt, inside the project area when there is one.
export function addableMask() {
  if (!grid) return null
  const { W, H, flags, facade, res } = grid
  const near = new Uint8Array(W * H)
  const R = MIN_SPACING_M / res
  for (const [x, y] of [...treeXY, ...state.added.map((a) => [a.x, a.y])]) {
    const c0 = (x - grid.x0) / res, r0 = (grid.y1 - y) / res
    for (let r = Math.max(0, Math.floor(r0 - R)); r <= Math.min(H - 1, Math.ceil(r0 + R)); r++)
      for (let c = Math.max(0, Math.floor(c0 - R)); c <= Math.min(W - 1, Math.ceil(c0 + R)); c++)
        if (Math.hypot(c + 0.5 - c0, r + 0.5 - r0) < R) near[r * W + c] = 1
  }
  // with a project area, only the cells inside it (cell centres, in grid metres)
  const poly = state.area?.poly.map(([lon, lat]) => grid.toXY(lon, lat))
  const inArea = (k) => !poly || insidePoly(grid.x0 + ((k % W) + 0.5) * res, grid.y1 - (Math.floor(k / W) + 0.5) * res, poly)
  const cv = document.createElement('canvas')
  Object.assign(cv, { width: W, height: H })
  const ctx = cv.getContext('2d')
  const img = ctx.createImageData(W, H)
  for (let k = 0; k < W * H; k++) {
    if ((flags[k] & 5) !== 1 || facade[k] < 10 || !inArea(k)) continue
    img.data.set(near[k] || facade[k] < 20 ? [230, 160, 30, 120] : [70, 190, 80, 120], 4 * k)
  }
  ctx.putImageData(img, 0, 0)
  return cv
}

export function addTreeAt(lon, lat) {
  const q = pointPotentials(grid, state.meta, lon, lat)
  if (!q.inSite) return void (state.addMsg = q.onRoof ? "That's a roof: pick open ground." : 'Outside the site: pick open ground in Porta.')
  if (q.facade_m < 1) return void (state.addMsg = 'Against a building (under 1 m): pick open ground.')
  if (state.area && !insidePoly(lon, lat, state.area.poly)) return void (state.addMsg = 'Outside the project area: add trees inside it, or use Whole site.')
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

// ---- project area: replace only the trees inside a drawn polygon ---------------------------------------------
// Rows to decide: the plane positions inside (always) and, with "replace all trees", the other street trees inside.
// Free planting spots inside can be filled as added trees. Estimates, like the live layouts: today's exact metrics +
// calibration slope × Σ (potential of the new species − potential of today's tree) over the rows. Today's trees are
// scored in the browser from their measured crown (planes: the plane's median LAI, ASSUMPTION; other trees: their LiDAR
// LAI) and rescaled per metric so that every plane, fed to the calibration line, reproduces today exactly.
async function ensureGrid() {
  if (grid) return
  grid = await loadGrid(dataUrl(state.meta.grid.file), state.meta.grid)
  const p = state.trees.positions
  const k = state.trees.kept
  treeXY = [...p.lon.map((lon, i) => grid.toXY(lon, p.lat[i])), ...k.lon.map((lon, i) => grid.toXY(lon, k.lat[i]))]
}

export function insidePoly(lon, lat, poly) {
  let inside = false
  for (let a = 0, b = poly.length - 1; a < poly.length; b = a++) {
    const [xa, ya] = poly[a]
    const [xb, yb] = poly[b]
    if ((ya > lat) !== (yb > lat) && lon < ((xb - xa) * (lat - ya)) / (yb - ya) + xa) inside = !inside
  }
  return inside
}

// Sizing rule, as layout.fits(size_rule="exact"): the species' class must equal the position's sidewalk class;
// "check" (no facade-bounded sidewalk) and species without a class are not filtered; "none" (< 2.5 m) fits nothing
const sizeFits = (cls, sp) => !cls || cls === 'check' || !sp.size_class || (cls !== 'none' && sp.size_class === cls)
function withSizeRule(fit, cls) {
  const sp = state.meta.palette.filter((s) => s.in_palette)
  const f = fit.map((v, j) => (v && sizeFits(cls, sp[j]) ? 1 : 0))
  if (!f.some(Boolean)) f[sp.reduce((m, s, j) => (s.crown_diam_m < sp[m].crown_diam_m ? j : m), 0)] = 1 // as the tool's last resort
  return f
}

// Full-length plane layout: today's trees everywhere, the area's species at its plane positions
export function areaLayout(sub) {
  const full = [...state.trees.layouts.S0_current]
  state.area.idx.forEach((i, k) => (full[i] = sub[k] ?? full[i])) // today's species until the new area is optimised
  return full
}
// kept tree index -> new palette species, for the kept trees an area replaces (empty unless "replace all trees")
export function keptReplaced(useCity = false) {
  const A = state.area
  if (!A?.all) return new Map()
  const src = useCity ? A.city.keptLayout : A.keptLayout
  return new Map(A.keptIdx.map((k, r) => [k, src?.[r]]).filter(([, j]) => j != null))
}

export function startDrawing() {
  Object.assign(state, { drawing: true, editing: false, draft: [], view: 'map', addMode: false,
    addMsg: 'Click on the map to place the corners of the project area. Right-click, Enter or Space closes it.' })
}
export function addVertex(lon, lat) {
  state.draft = [...state.draft, [lon, lat]]
}
export function cancelDrawing() {
  Object.assign(state, { drawing: false, draft: [], addMsg: null })
}
export function clearArea() {
  Object.assign(state, { area: null, drawing: false, editing: false, draft: [], addMsg: null })
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
const ONES = Array(12).fill(1)
function keptToday(k) {
  const t = state.trees.kept
  const [x, y] = grid.toXY(t.lon[k], t.lat[k])
  return crownPotential(grid, state.meta.model, x, y, { crown_diam_m: t.crown_diam_m[k], height_m: t.height_m[k],
    crown_base_m: t.crown_base_m[k], lai: t.lai[k], leaf: state.meta.leaf_by_species?.[t.species[k]] ?? ONES })
}

const POT_KEY = { shade_summer: 'summer', shade_winter: 'winter', water: 'water' }
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

// Rows of the area: { kind, i, fit[], shade_summer[], shade_winter[], water[], today{summer, winter, water}, removes }
let rowsCache = { poly: null, all: null, rows: null }
function areaRows(A) {
  if (rowsCache.poly === A.poly && rowsCache.all === A.all) return rowsCache.rows
  rowsCache = { poly: A.poly, all: A.all, rows: buildRows(A) }
  return rowsCache.rows
}
function buildRows(A) {
  const pot = state.pot
  const rows = A.idx.map((i) => ({ kind: 'plane', i, fit: pot.fit[i], shade_summer: pot.shade_summer[i], shade_winter: pot.shade_winter[i],
    water: pot.water[i], today: planePot(i) }))
  if (A.all) {
    const t = state.trees.kept
    A.keptIdx.forEach((k) => {
      const q = pointPotentials(grid, state.meta, t.lon[k], t.lat[k])
      rows.push({ kind: 'kept', i: k, fit: withSizeRule(q.fit, t.size_class[k]), shade_summer: q.summer, shade_winter: q.winter,
        water: q.water, today: keptToday(k), removes: t.species[k] })
    })
  }
  return rows
}

// Metrics of "today's trees outside, new trees on the rows": newSums[k] = Σ potential of the new trees on the rows
function areaMetrics(rows, newSums) {
  const s0 = state.meta.scenarios.find((s) => s.id === 'S0_current').metrics
  const k = planeScales()
  const today = { shade_summer: 0, shade_winter: 0, water: 0 }
  rows.forEach((r) => {
    for (const key in today) today[key] += r.today[POT_KEY[key]]
  })
  return Object.fromEntries(Object.keys(s0).map((m) =>
    [m, PROXY[m] ? s0[m] + calibration.value[m].b * (newSums[PROXY[m]] - k[m] * today[PROXY[m]]) : null]))
}

// Room under the cap once the kept trees an area replaces are gone
function keptAfter(rows) {
  const kept = [...state.pot.kept]
  rows.forEach((r) => {
    const j = r.kind === 'kept' ? state.pot.species.indexOf(r.removes) : -1
    if (j >= 0) kept[j]--
  })
  return kept
}

// City rule on the rows: the expected value of the S1a draw (2026 mix weights among the fitting mix species; any
// fitting species if none of the mix fits), with capped species scaled down to their room, as the exact S1a draws
function areaCity(rows) {
  const pot = state.pot
  const cap = caps({ ...pot, kept: keptAfter(rows) }, state.share, state.exclude)
  let w = pot.species.map((s) => state.meta.s1a_mix?.[s] ?? 0)
  const probs = () => rows.map((r) => {
    let ww = pot.species.map((_, j) => (r.fit[j] ? w[j] : 0))
    if (!ww.some((v) => v > 0)) ww = pot.species.map((_, j) => r.fit[j])
    const tot = ww.reduce((a, b) => a + b, 0)
    return ww.map((v) => v / tot)
  })
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
  P.forEach((p, r) => p.forEach((v, j) => {
    if (!v) return
    for (const k in sums) sums[k] += v * rows[r][k][j]
    counts[pot.species[j]] += v
  }))
  const mostLikely = P.map((p) => p.indexOf(Math.max(...p))) // for drawing the kept trees the rule would replace
  return { metrics: areaMetrics(rows, sums), counts: Object.fromEntries(Object.entries(counts).map(([s, n]) => [s, Math.round(n)])),
    keptLayout: rows.map((r, n) => (r.kind === 'kept' ? mostLikely[n] : null)).filter((j) => j != null) }
}

export async function finishArea() {
  if (state.draft.length < 3) return void (state.addMsg = 'An area needs at least three corners.')
  await applyArea(state.draft)
}

// Set the project area to a polygon (drawn, or edited: keep its "replace all" choice and priorities)
async function applyArea(poly, keep = {}) {
  const p = state.trees.positions
  const t = state.trees.kept
  const idx = p.lon.map((lon, i) => (insidePoly(lon, p.lat[i], poly) ? i : -1)).filter((i) => i >= 0)
  const keptIdx = t.lon.map((lon, k) => (insidePoly(lon, t.lat[k], poly) ? k : -1)).filter((k) => k >= 0)
  const spotIdx = state.trees.spots.lon.map((lon, s) => (insidePoly(lon, state.trees.spots.lat[s], poly) ? s : -1)).filter((s) => s >= 0)
  if (!idx.length && !keptIdx.length) return void (state.addMsg = 'No street trees inside that area: draw it around some trees.')
  state.addMsg = 'Loading the site grid…'
  await ensureGrid()
  Object.assign(state, { drawing: false, editing: false, draft: [], addMsg: null })
  state.area = { poly, idx, keptIdx, spotIdx, all: !!keep.all || !idx.length, weights: keep.weights ?? weightsNow(), layout: [], keptLayout: [],
    metrics: null, counts: {}, edited: !!keep.weights }
  await runArea(state.area.weights)
}

// Edit the project area: drag corners, click a midpoint to add a corner, right-click a corner to remove it
export function startEditArea() {
  Object.assign(state, { editing: true, draft: state.area.poly.map((q) => [...q]), addMode: false,
    addMsg: 'Drag a corner to move it, click a midpoint to add one, right-click a corner to remove it. Enter or Done applies, Escape cancels.' })
}
export async function finishEditArea() {
  if (state.draft.length < 3) return void (state.addMsg = 'An area needs at least three corners.')
  await applyArea(state.draft, { all: state.area.all, weights: state.area.weights })
}
export function cancelEditArea() {
  Object.assign(state, { editing: false, draft: [], addMsg: null })
}

// "Replace all trees": the other street trees in the area become decision rows too
export async function setAreaAll(on) {
  state.area.all = on
  await runArea(state.area.weights)
}

// "Fill the free spots": every free planting spot in the area becomes an added tree (sizing rule of its sidewalk)
export async function fillAreaSpots() {
  const S = state.trees.spots
  const have = new Set(state.added.map((t) => t.spot))
  for (const s of state.area.spotIdx) {
    if (have.has(S.id[s])) continue
    const q = pointPotentials(grid, state.meta, S.lon[s], S.lat[s])
    const fit = withSizeRule(q.fit, S.size_class[s])
    state.added.push({ lon: S.lon[s], lat: S.lat[s], x: q.x, y: q.y, pot: { summer: q.summer, winter: q.winter, water: q.water, fit },
      warn: [], sun_summer: q.sun_summer, sun_winter: q.sun_winter, drains_to_hotspot: q.drains_to_hotspot, spot: S.id[s], auto: true,
      species: fit.indexOf(1) })
  }
  state.addedVersion++
  await runArea(state.area.weights)
}

export async function runArea(weights) {
  const A = state.area
  const rows = areaRows(A)
  const pot = state.pot
  const sub = { ...pot, kept: keptAfter(rows), fit: rows.map((r) => r.fit) }
  for (const k of ['shade_summer', 'shade_winter', 'water']) sub[k] = rows.map((r) => r[k])
  state.busy = true
  state.liveError = null
  const res = await optimise(sub, weights, { share: state.share, exclude: state.exclude, minEff: state.minEff, extra: state.added })
  state.busy = false
  if (res.error) return void (state.liveError = res.error)
  res.layout.slice(rows.length).forEach((j, k) => Object.assign(state.added[k], { species: j, auto: true }))
  const lay = res.layout.slice(0, rows.length)
  const sums = { shade_summer: 0, shade_winter: 0, water: 0 }
  lay.forEach((j, r) => {
    for (const key in sums) sums[key] += rows[r][key][j]
  })
  const counts = Object.fromEntries(pot.species.map((s, j) => [s, lay.filter((x) => x === j).length]))
  Object.assign(A, { weights, layout: lay.slice(0, A.idx.length), keptLayout: lay.slice(A.idx.length), metrics: areaMetrics(rows, sums),
    counts, city: areaCity(rows), ms: res.ms, version: (A.version ?? 0) + 1 })
  state.addedVersion++
  state.scenarioId = AREA
}

// ---- canopy cover against the tree master plan's 30% target ------------------------------------------------
// Today = measured cover (LiDAR CHM > 2 m). A precomputed layout adds the change of the crown-disc model (exact, with
// overlaps); live layouts, project areas and added trees add the change of their crown discs summed without overlaps
// (an estimate that runs high where new crowns overlap existing canopy).
export const cover = computed(() => {
  const C = state.meta?.cover
  if (!C || !state.trees) return null
  state.addedVersion // dependency
  state.area?.version
  const s = scenario.value
  const pal = state.meta.palette
  const disc = (d) => Math.PI * (d / 2) ** 2
  let d = 0
  let approx = false
  if (s?.metrics?.canopy_pct != null && s.group !== 'live' && s.group !== 'area') d = s.metrics.canopy_pct - C.s0_disc_pct
  else if (s && s.id !== 'S0_current') {
    const P = state.trees.positions
    const a = currentLayout().reduce((acc, j, i) => acc + (pal[j].in_palette ? disc(pal[j].crown_diam_m) - disc(P.s0_crown_diam_m[i]) : 0), 0)
    d = (100 * a) / C.area_m2
    approx = true
  }
  if (s?.id === AREA) {
    const t = state.trees.kept
    let a = 0
    keptReplaced().forEach((j, k) => (a += disc(pal[j].crown_diam_m) - disc(t.crown_diam_m[k])))
    d += (100 * a) / C.area_m2
  }
  const added = (100 * state.added.reduce((acc, t) => acc + (t.species >= 0 ? disc(pal[t.species].crown_diam_m) : 0), 0)) / C.area_m2
  if (state.added.length) approx = true
  const pct = C.measured_pct + d + added
  return { ...C, pct, vsToday: d + added, added, addedN: state.added.length, approx,
    gap: C.target_pct - pct, gapHa: ((C.target_pct - pct) / 100) * C.area_m2 / 1e4 }
})

// ---- side panels: width and open state, remembered in this browser ---------------------------------------------
export const MIN_W = 200
export const MAX_W = 520
const PANEL_KEY = 'shade-sponge-panels'
const savedPanels = (() => {
  try { return JSON.parse(localStorage.getItem(PANEL_KEY) ?? '{}') } catch { return {} }
})()
export const panels = reactive({ leftW: 270, rightW: 330, leftOpen: true, rightOpen: true, ...savedPanels })
watch(panels, (p) => {
  try { localStorage.setItem(PANEL_KEY, JSON.stringify(p)) } catch { /* private window or blocked storage: keep the defaults */ }
})

// ---- theme: 'auto' follows the system; the choice is remembered in this browser ---------------------------------
const THEME_KEY = 'shade-sponge-theme'
const mq = typeof matchMedia === 'function' ? matchMedia('(prefers-color-scheme: dark)') : null
export const ui = reactive({ theme: (() => { try { return localStorage.getItem(THEME_KEY) || 'auto' } catch { return 'auto' } })(),
  systemDark: !!mq?.matches })
mq?.addEventListener?.('change', (e) => (ui.systemDark = e.matches))
export const isDark = computed(() => ui.theme === 'dark' || (ui.theme === 'auto' && ui.systemDark))
watch(() => ui.theme, (t) => {
  try { localStorage.setItem(THEME_KEY, t) } catch { /* storage blocked: the choice lasts this visit */ }
  if (t === 'auto') document.documentElement.removeAttribute('data-theme')
  else document.documentElement.setAttribute('data-theme', t)
}, { immediate: true })
// Earth palette (as the slides) for deck.gl and ECharts, light and dark
export const themeColors = computed(() => (isDark.value
  ? { text: '#F2F0EA', muted: '#B3BAB9', grid: '#333A33', plane: '#E4DFD3', other: '#5E5B54', kept: [150, 150, 140, 150],
      building: [64, 70, 64, 235], buildingLine: [40, 44, 40], facade: [196, 140, 100, 230], kerb: [214, 220, 228, 235],
      spotLine: [230, 240, 220], ring: [242, 240, 234], ringOn: [157, 180, 222], area: [157, 180, 222], draft: [217, 184, 102],
      random: '#7A776E', city: '#D9B866', optimised: '#9DB4DE', current: '#E4DFD3', on: '#F2F0EA',
      basemap: 'https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json' }
  : { text: '#2A2622', muted: '#665E4F', grid: '#DCD8CE', plane: '#3A3630', other: '#C9C4B8', kept: [150, 155, 135, 150],
      building: [222, 218, 208, 235], buildingLine: [180, 176, 166], facade: [150, 95, 55, 220], kerb: [40, 48, 64, 235],
      spotLine: [20, 40, 10], ring: [255, 255, 255], ringOn: [40, 63, 102], area: [40, 63, 102], draft: [140, 106, 36],
      random: '#B4AE9F', city: '#8C6A24', optimised: '#5D7BAA', current: '#2A2622', on: '#283F66',
      basemap: 'https://tiles.openfreemap.org/styles/positron' }))
