// Shared state: site data exported by `python -m shade_sponge.web_export`, plus what the user has selected.
import { reactive, computed, watch, markRaw } from 'vue'
import { optimise, proxySums, fitLine, effSpecies, caps } from './optimize.js'
import { loadGrid, pointPotentials, crownPotential } from './pointpot.js'

export const MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
export const BALANCED = 'S4_s0.50_w0.25_r0.25'
export const LIVE = 'live'
export const AREA = 'area'

export const state = reactive({
  site: 'porta-barcelona', // one palette only: the Barcelona shortlist of 30 species (user 27 Nov)
  barri: 'Porta', // neighbourhood picked in BarriPicker (only barris with exported data change `site`)
  meta: null,
  trees: null,
  pot: null,
  scenarioId: 'S0_current', // the tool always opens on today's trees (user 27 Nov)
  view: 'map', // 'map' | 'compare' (side-by-side columns: today | city practice | optimised) | 'species' (botanical cards)
  speciesScope: 'site', // Species tab: 'site' (whole neighbourhood) or 'area' (the project area, when one is drawn)
  // project area: only the plane positions inside a drawn polygon are replaced; outside, today's trees stay
  drawing: false,
  editing: false, // moving the corners of the project area (draft holds the polygon being edited)
  draft: [], // [lon, lat] vertices while drawing
  area: null, // { poly, idx, keptIdx, spotIdx, all, weights, layout, keptLayout, metrics, counts, city, ms }
  buildingOpacity: 0.9, // Map display slider: 1 = solid, lower = see-through; 0.9 so trees behind buildings show (user 27 Nov)
  showStreets: true, // sidewalk edges (facades, kerbs) and minimum pits on the map
  showSpots: true, // free planting spots, on their own switch (user 27 Nov)
  overlay: '', // none by default: sidewalks and free spots read better (the sun / water layers are in Map display)
  basemap: 'map', // 'map' (street map) | 'satellite' (ICGC orthophoto)
  ground3d: false, // relief from the site DTM (meta.terrain); trees, buildings and lines then sit on it
  terrain: null, // { w, h, z (Float32Array, m above the site's lowest point), bounds: [west, south, east, north] } once loaded
  showParks: true, // park and zone trees (meta.parks): context only, never scored; always drawn (user 27 Nov)
  parks: null, // { site, id, kind, place, species, lon, lat, height_m, crown_diam_m, crown_base_m } once loaded
  showUtilities: false, // SYNTHETIC underground services (meta.utilities, scripts/synthetic_utilities.py): a mock, not real plans
  utilities: null, // { site, features } once loaded
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
  useConditional: false, // "Fill spots" also plants conditional spots (a sign, crossing, lamp, bollard or bus stop to move)
  // tree schedule (designer's decisions): trees by key (plane tree_id, 'k<index>' for other street trees), spots by id
  schedule: { trees: {}, spots: {} },
  showSchedule: false,
  focus: null, // [lon, lat]: the map jumps there (a schedule row was clicked)
  loadingConfig: false,
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
export async function switchSite(site, keep = true) {
  // the designer's work (project area, schedule, added trees, rules) carries over to the other palette or tree size
  const oldName = state.meta?.site.name // only within the same neighbourhood: another barri's trees are elsewhere
  const carry = keep && state.meta && (state.area || state.added.length || Object.keys(state.schedule.trees).length || Object.keys(state.schedule.spots).length)
    ? JSON.parse(configJson()) : null
  Object.assign(state, { scenarioId: 'S0_current', live: null, selected: null, exclude: [], minEff: 0, liveError: null, meta: null, added: [], addMsg: null, area: null, drawing: false, editing: false, draft: [], addMode: false, schedule: { trees: {}, spots: {} } }) // the new site's grid loads with the next Add trees
  grid = null
  planePotCache.clear()
  planeScale = null
  await load(site)
  if (!carry || state.error || state.meta.site.name !== oldName) return
  const names = state.meta.palette.map((p) => p.species)
  carry.rules.exclude = carry.rules.exclude.filter((x) => names.includes(x)) // species the new palette lacks drop out
  await loadConfig({ ...carry, site })
}

// Leaf habit of every species drawn (web/public/data/leaf_habit.json, scripts/web_leaf_habit.py): colour code of today's
// trees and park trees, as the palette's (ochre deciduous, green evergreen, olive semi-deciduous; grey unknown)
export const HABIT_RGB = { deciduous: [176, 138, 46], evergreen: [94, 143, 85], 'semi-deciduous': [163, 163, 90], unknown: [150, 150, 140] }
export const habits = reactive({ map: {} })
fetch('./data/leaf_habit.json').then((r) => r.json()).then((m) => (habits.map = m)).catch(() => {})
// a cultivar falls back to its species (first two words, without the cultivar name)
export function habitOf(sp) {
  const m = habits.map
  return m[sp] ?? m[(sp ?? '').replace(/['‘’].*/, '').replace(/[×�]/g, 'x').split(/\s+/).slice(0, 2).join(' ')] ?? 'unknown'
}

// Whole-city view (scripts/make_city_web.py): every barri's numbers and the method's new trees, one light file
export const city = reactive({ data: null })
fetch('./data/city.json').then((r) => r.json()).then((d) => (city.data = markRaw(d))).catch(() => {})
const CITY_RGB = [[63, 102, 62], [40, 63, 102], [102, 56, 37], [140, 106, 36], [157, 181, 150], [120, 90, 140],
  [60, 130, 140], [170, 90, 60], [110, 120, 50], [168, 162, 147]]
export const cityColor = (k) => CITY_RGB[k % CITY_RGB.length]

export const dataUrl = (file) => `./data/${state.site}/${file}`

// Relief: terrain.png (python scripts/web_export_terrain.py) holds the site DTM on a lon/lat grid, as metres above the
// site's lowest point: red × 25.6 + green × 0.1. Decoded once for groundZ(); deck.gl's TerrainLayer reads the same file.
export async function loadTerrain() {
  const T = state.meta?.terrain
  if (!T || state.terrain?.site === state.site) return
  const img = new Image()
  img.src = dataUrl(T.file)
  await img.decode()
  const c = Object.assign(document.createElement('canvas'), { width: img.width, height: img.height })
  const g = c.getContext('2d', { willReadFrequently: true })
  g.drawImage(img, 0, 0)
  const px = g.getImageData(0, 0, img.width, img.height).data
  const z = new Float32Array(img.width * img.height)
  for (let i = 0; i < z.length; i++) z[i] = px[4 * i] * 25.6 + px[4 * i + 1] * 0.1
  state.terrain = markRaw({ site: state.site, w: img.width, h: img.height, z, bounds: T.bounds })
}
// Ground height (m above the site's lowest point) at a lon/lat, bilinear; 0 on the flat map and outside the DTM
export function groundZ(lon, lat) {
  const T = state.ground3d && state.terrain
  if (!T) return 0
  const [w, s, e, n] = T.bounds
  const fx = ((lon - w) / (e - w)) * T.w - 0.5, fy = ((n - lat) / (n - s)) * T.h - 0.5
  if (fx < -0.5 || fy < -0.5 || fx > T.w - 0.5 || fy > T.h - 0.5) return 0
  const x0 = Math.min(Math.max(Math.floor(fx), 0), T.w - 2), y0 = Math.min(Math.max(Math.floor(fy), 0), T.h - 2)
  const ax = Math.min(Math.max(fx - x0, 0), 1), ay = Math.min(Math.max(fy - y0, 0), 1), k = y0 * T.w + x0
  return (T.z[k] * (1 - ax) + T.z[k + 1] * ax) * (1 - ay) + (T.z[k + T.w] * (1 - ax) + T.z[k + T.w + 1] * ax) * ay
}
// Park and zone trees (python scripts/web_export_parks.py): drawn for context only; their canopy is already fixed background
export async function setParks(on) {
  if (on && state.meta?.parks && state.parks?.site !== state.site)
    state.parks = markRaw({ site: state.site, ...(await (await fetch(dataUrl(state.meta.parks.file))).json()) })
  state.showParks = on && !!state.parks
}
// Synthetic underground services (python scripts/synthetic_utilities.py): random lines drawn from the real networks' statistics, not real plans
// one colour per synthetic network (map lines and the legend); a service line to a building takes its network's colour, thinner
export const UTIL_NETS = [['water', 'Water', [40, 110, 210]], ['gas', 'Gas', [230, 170, 20]], ['electricity (LV)', 'Electricity, low voltage', [210, 50, 50]],
  ['electricity (MV)', 'Electricity, medium voltage', [130, 20, 40]], ['telecom', 'Telecom (Telefónica)', [140, 80, 190]],
  ['telecom (ONO)', 'Telecom (Vodafone-ONO)', [40, 150, 70]], ['lighting', 'Street lighting', [240, 120, 20]]]
export const UTIL_COLOR = Object.fromEntries([...UTIL_NETS.map(([k, , c]) => [k, c]),
  ['gas service', [230, 170, 20]], ['water service', [40, 110, 210]], ['electricity service', [210, 50, 50]]])
export async function setUtilities(on) {
  if (on && state.meta?.utilities && state.utilities?.site !== state.site)
    state.utilities = markRaw({ site: state.site, features: (await (await fetch(dataUrl(state.meta.utilities.file))).json()).features })
  state.showUtilities = on && !!state.utilities
}
export async function setGround3d(on) {
  if (on) await loadTerrain()
  state.ground3d = on && !!state.terrain
}

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
  if (s.id.startsWith('S1b')) return `City practice (observed) #${s.id.split('_').pop()}`
  if (s.id.startsWith('S1a')) return `City announced mix (2026) #${s.id.split('_').pop()}`
  if (s.id.startsWith('S1')) return `Random palette #${s.id.split('_').pop()}`
  const [a, b, c] = s.weights.map((w) => +w.toFixed(2))
  return `${s.id === LIVE ? 'Live estimate' : 'Optimised'}: summer ${a}, winter ${b}, runoff ${c}`
}

// Mean of the 10 city-practice layouts (S1b, the mix the city actually planted in place of planes 2018–2026, within the sizing
// rule): the thesis baseline. S1a (the announced 2026 mix) is shown as "City announced mix"
export const cityMean = computed(() => {
  const r = state.meta?.scenarios.filter((s) => s.group === 'S1b') ?? []
  if (!r.length) return null
  const keys = Object.keys(r[0].metrics)
  return Object.fromEntries(keys.map((k) => [k, r.reduce((a, s) => a + s.metrics[k], 0) / r.length]))
})

// "vs city practice" reference: the whole-site S1b mean, or the city practice inside the project area (estimate)
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
    img.data.set(near[k] || facade[k] < 20 ? [230, 160, 30, 170] : [70, 190, 80, 170], 4 * k) // strong enough to see where a click counts
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
  if (tree.species < 0) { // no sidewalk size class here (a courtyard, a square): best species without the sizing rule
    tree.species = recommend({ ...tree.pot, fit: tree.pot.fit.map(() => 1) })
    warn.push('no sidewalk sizing rule here: check the species')
  }
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
  if (!A?.keptRows?.length) return new Map()
  const src = useCity ? A.city.keptLayout : A.keptLayout
  return new Map(A.keptRows.map((k, r) => [k, src?.[r]]).filter(([, j]) => j != null))
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
  if (rowsCache.idx === A.idx && rowsCache.keptRows === A.keptRows) return rowsCache.rows
  rowsCache = { idx: A.idx, keptRows: A.keptRows, rows: buildRows(A) }
  return rowsCache.rows
}
function buildRows(A) {
  const pot = state.pot
  const rows = A.idx.map((i) => ({ kind: 'plane', i, fit: pot.fit[i], shade_summer: pot.shade_summer[i], shade_winter: pot.shade_winter[i],
    water: pot.water[i], today: planePot(i) }))
  if (A.keptRows.length) {
    const t = state.trees.kept
    A.keptRows.forEach((k) => {
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

// The area on its own (Angelos's street-segment scale): today's contribution of the trees it replaces and the change, in
// absolute units. Today = the calibrated share of those trees (b × scale × potential); change = the site metric minus today.
function areaLocal(rows, metrics) {
  const s0 = state.meta.scenarios.find((s) => s.id === 'S0_current').metrics
  const k = planeScales()
  const today = { shade_summer: 0, shade_winter: 0, water: 0 }
  rows.forEach((r) => {
    for (const key in today) today[key] += r.today[POT_KEY[key]]
  })
  return Object.fromEntries(Object.keys(PROXY).filter((m) => s0[m] != null)
    .map((m) => [m, { today: calibration.value[m].b * k[m] * today[PROXY[m]], delta: metrics[m] - s0[m] }]))
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

// City practice on the rows: the expected value of an S1b-like draw (mix weights among the fitting mix species; any fitting
// species if none of the mix fits), with capped species scaled down to their room, as the exact draws. Weights = the species
// counts summed over the site's 10 S1b layouts (the observed mix as the palette and the sizing rule let it land; an
// approximation of layout.s1b_mix); S1a's announced mix if the data has no S1b
function areaCity(rows) {
  const pot = state.pot
  const cap = caps({ ...pot, kept: keptAfter(rows) }, state.share, state.exclude)
  const s1b = state.meta.scenarios.filter((s) => s.group === 'S1b')
  let w = pot.species.map((s) => (s1b.length ? s1b.reduce((a, x) => a + (x.counts?.[s] ?? 0), 0) : state.meta.s1a_mix?.[s] ?? 0))
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
    keptLayout: rows.map((r, n) => (r.kind === 'kept' ? mostLikely[n] : null)).filter((j) => j != null),
    planeLayout: rows.map((r, n) => (r.kind === 'plane' ? mostLikely[n] : null)).filter((j) => j != null) } // A.idx order, for the report
}

export async function finishArea() {
  if (state.draft.length < 3) return void (state.addMsg = 'An area needs at least three corners.')
  await applyArea(state.draft)
}

// Set the project area to a polygon (drawn, or edited: keep its "replace all" choice and priorities)
async function applyArea(poly, keep = {}) {
  const p = state.trees.positions
  const t = state.trees.kept
  const inPlanes = p.lon.map((lon, i) => (insidePoly(lon, p.lat[i], poly) ? i : -1)).filter((i) => i >= 0)
  const keptIdx = t.lon.map((lon, k) => (insidePoly(lon, t.lat[k], poly) ? k : -1)).filter((k) => k >= 0)
  const spotIdx = state.trees.spots.lon.map((lon, s) => (insidePoly(lon, state.trees.spots.lat[s], poly) ? s : -1)).filter((s) => s >= 0)
  if (!inPlanes.length && !keptIdx.length) return void (state.addMsg = 'No street trees inside that area: draw it around some trees.')
  state.addMsg = 'Loading the site grid…'
  await ensureGrid()
  Object.assign(state, { drawing: false, editing: false, draft: [], addMsg: null })
  state.area = { poly, inPlanes, keptIdx, spotIdx, all: !!keep.all || !inPlanes.length, weights: keep.weights ?? weightsNow(), layout: [],
    keptLayout: [], metrics: null, counts: {}, edited: !!keep.weights }
  areaSets(state.area)
  await runArea(state.area.weights)
}

// The area's decision rows, after the schedule: planes unless marked Keep; other street trees when "replace all" (unless Keep)
// or when marked Replace or Move. A moved tree is scored as replaced at its position (where it goes is not modelled).
function areaSets(A) {
  const act = (key) => state.schedule.trees[key]?.action
  A.idx = A.inPlanes.filter((i) => act(state.trees.positions.tree_id[i]) !== 'keep')
  A.keptRows = A.keptIdx.filter((k) => (A.all ? act(`k${k}`) !== 'keep' : ['replace', 'move'].includes(act(`k${k}`))))
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
  areaSets(state.area)
  await runArea(state.area.weights)
}

// Spot class (scripts/porta_spot_classes.py, user decision 18 Nov): 'free' or 'conditional'; data without classes = free.
// A free spot whose pit would sit on a buried line (synthetic in the public app) is conditional too (PTEV 2024 p. 31)
export const spotClass = (s) => (state.trees.spots.utility_conditional?.[s] ? 'conditional' : state.trees.spots.spot_class?.[s] ?? 'free')
// what has to move first at a conditional spot: surface objects, and the buried line under the pit
export const spotWhy = (s) => {
  const S = state.trees.spots
  return [S.reasons[s] && S.reasons[s].replaceAll('_', ' ').replaceAll(';', ', '),
    S.utility_conditional?.[s] && `buried service${state.meta?.utilities?.synthetic ? ' (synthetic)' : ''}`].filter(Boolean).join(', ')
}
// the area's spots that "Fill" plants: free ones, plus conditional ones when the switch is on
// Move (user tests 27 Nov): a tree marked Move goes to an empty spot the designer picks on the map. Its old pit is replaced
// like any other row; at the new spot the tree is drawn with its own crown and its transplant is costed, but its shade and
// water there are not scored (ASSUMPTION: a moved tree's effect at the spot is left out of the estimates).
export const moveTargets = () => {
  const m = new Map()
  for (const [key, e] of Object.entries(state.schedule.trees)) if (e.action === 'move' && e.to) m.set(e.to, key)
  return m
}
export function pickMoveTarget(key) { state.movePick = key; state.addMsg = 'Click an empty spot on the map for this tree.' }
export async function setMoveTarget(spotIdx) {
  const key = state.movePick, id = state.trees.spots.id[spotIdx]
  state.movePick = null
  state.addMsg = null
  if (!key || moveTargets().has(id)) return
  await setTreeEntry(key, { action: 'move', to: id })
}
export const fillableSpots = () => state.area.spotIdx.filter((s) => (spotClass(s) === 'free' || state.useConditional) &&
  !moveTargets().has(state.trees.spots.id[s])) // a spot that receives a moved tree is taken

// "Fill the free spots": every free planting spot in the area becomes an added tree (sizing rule of its sidewalk)
export async function fillAreaSpots() {
  const S = state.trees.spots
  const have = new Set(state.added.map((t) => t.spot))
  for (const s of fillableSpots()) {
    if (have.has(S.id[s]) || state.schedule.spots[S.id[s]]?.action === 'empty') continue
    pushSpotTree(s)
  }
  state.addedVersion++
  await runArea(state.area.weights)
}

function pushSpotTree(s) {
  const S = state.trees.spots
  const q = pointPotentials(grid, state.meta, S.lon[s], S.lat[s])
  const fit = withSizeRule(q.fit, S.size_class[s])
  const t = { lon: S.lon[s], lat: S.lat[s], x: q.x, y: q.y, pot: { summer: q.summer, winter: q.winter, water: q.water, fit },
    warn: spotClass(s) === 'conditional' ? [`conditional spot: move ${spotWhy(s)} first`] : [],
    sun_summer: q.sun_summer, sun_winter: q.sun_winter, drains_to_hotspot: q.drains_to_hotspot, spot: S.id[s], auto: true,
    species: fit.indexOf(1) }
  if (!state.area) t.species = recommend(t.pot) // no optimiser run follows: the best fitting species for the priorities on screen
  state.added.push(t)
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
  const metrics = areaMetrics(rows, sums)
  Object.assign(A, { weights, layout: lay.slice(0, A.idx.length), keptLayout: lay.slice(A.idx.length), metrics, local: areaLocal(rows, metrics),
    counts, city: areaCity(rows), ms: res.ms, version: (A.version ?? 0) + 1 })
  state.addedVersion++
  state.scenarioId = AREA
}

// ---- tree schedule: the designer's decision per tree and per spot (Action, Reason, Field check), linked to the map --------
// Tree actions: keep / move / replace ('' = the tool decides). Inside a project area they change what is optimised (areaSets);
// on the whole site they are recorded only. Spot actions: add (plants it, as "Fill spots") / empty ('' = the tool decides).
export const TREE_ACTIONS = [['', '–'], ['keep', 'Keep'], ['move', 'Move'], ['replace', 'Replace']]
export const SPOT_ACTIONS = [['', '–'], ['add', 'Add'], ['empty', 'Leave empty']]
export const REASONS = [['', '–'], ['dead', 'Dead'], ['diseased', 'Diseased'], ['pests', 'Pests'], ['dangerous', 'Dangerous'],
  ['roots', 'Roots damage paving'], ['works', 'Works'], ['other', 'Other']]
export const CHECKS = [['', 'To do'], ['ok', 'OK'], ['no', 'Not possible']]
export const keptKey = (k) => `k${k}`

export async function setTreeEntry(key, patch) {
  const prev = state.schedule.trees[key] ?? {}
  state.schedule.trees[key] = { ...prev, ...patch }
  if ('action' in patch && patch.action !== prev.action && state.area) {
    areaSets(state.area)
    await runArea(state.area.weights)
  }
}

export async function setSpotEntry(s, patch) {
  const S = state.trees.spots, id = S.id[s]
  const prev = state.schedule.spots[id] ?? {}
  state.schedule.spots[id] = { ...prev, ...patch }
  if (!('action' in patch) || patch.action === prev.action) return
  const k = state.added.findIndex((t) => t.spot === id)
  if (patch.action === 'add' && k < 0) {
    if (spotClass(s) === 'blocked') return void (state.addMsg = 'A blocked spot cannot take a tree.')
    await ensureGrid()
    pushSpotTree(s)
  } else if (patch.action !== 'add' && k >= 0) state.added.splice(k, 1)
  else return
  state.selected = null
  state.addedVersion++
  if (state.area) await runArea(state.area.weights)
}

// select a schedule row: the map highlights it and flies there
export function focusOn(sel, lon, lat) {
  state.selected = sel
  state.focus = [lon, lat]
}

// Save / load: the whole configuration as a JSON file (actions, reasons, checks, area, added trees, rules, priorities)
export function configJson() {
  const A = state.area
  return JSON.stringify({ tool: 'shade-and-sponge', version: 1, site: state.site, saved: new Date().toISOString(),
    schedule: state.schedule, rules: { share: state.share, exclude: state.exclude, minEff: state.minEff },
    weights: scenario.value?.weights ?? null, scenarioId: state.scenarioId,
    area: A ? { poly: A.poly, all: A.all, weights: A.weights } : null,
    added: state.added.map((t) => ({ lon: t.lon, lat: t.lat, spot: t.spot ?? null, species: state.meta.palette[t.species]?.species ?? null, auto: t.auto })),
  }, null, 1)
}

// Autosave (v0.2.0, no login): the configuration goes to this browser's storage when it changes; the guided flow offers
// to resume it. Download "Save project" to keep it elsewhere.
const AUTO_KEY = 'shade-sponge-autosave'
export function savedProject() {
  try { const j = JSON.parse(localStorage.getItem(AUTO_KEY)); return j?.tool === 'shade-and-sponge' ? j : null } catch { return null }
}
let autoTimer
watch(() => [state.area?.version, state.area?.poly, state.addedVersion, state.schedule, state.share, state.minEff, state.exclude.length], () => {
  if (!state.meta || state.loadingConfig || !(state.area || state.added.length)) return
  clearTimeout(autoTimer)
  autoTimer = setTimeout(() => { try { localStorage.setItem(AUTO_KEY, configJson()) } catch { /* storage blocked or full */ } }, 1000)
}, { deep: true })

export async function loadConfig(cfg) {
  if (cfg?.tool !== 'shade-and-sponge') throw new Error('not a Shade and sponge configuration file')
  state.loadingConfig = true
  try {
    if (cfg.site !== state.site) await switchSite(cfg.site, false)
    Object.assign(state, { area: null, added: [], selected: null, ...cfg.rules, schedule: { trees: {}, spots: {}, ...cfg.schedule } })
    await ensureGrid()
    const S = state.trees.spots
    const names = state.meta.palette.map((p) => p.species)
    for (const a of cfg.added ?? []) {
      const s = a.spot ? S.id.indexOf(a.spot) : -1
      if (s >= 0) pushSpotTree(s)
      else addTreeAt(a.lon, a.lat)
      const t = state.added.at(-1)
      if (t && !a.auto && names.includes(a.species)) Object.assign(t, { species: names.indexOf(a.species), auto: false })
    }
    state.addedVersion++
    state.selected = null
    if (cfg.area) await applyArea(cfg.area.poly, { all: cfg.area.all, weights: cfg.area.weights })
    else if (cfg.scenarioId === LIVE && cfg.weights) await runLive(cfg.weights)
    else if (state.trees.layouts[cfg.scenarioId]) state.scenarioId = cfg.scenarioId
  } finally {
    state.loadingConfig = false
  }
}

// The schedule as CSV: one row per tree (existing and new) and per spot, in the project area or the whole site
export function scheduleCsv(rows) {
  const q = (v) => (v == null ? '' : /[",\n]/.test(String(v)) ? `"${String(v).replaceAll('"', '""')}"` : v)
  const head = 'tab,id,lon,lat,species_today,species_new,sidewalk_m,size_class,status,in_the_way,action,reason,reason_text,field_check'
  return [head, ...rows.map((r) => [r.tab, r.id, r.lon.toFixed(6), r.lat.toFixed(6), r.today, r.next, r.width?.toFixed?.(2), r.size, r.status,
    r.inWay, r.action, r.reason, r.note, r.check].map(q).join(','))].join(String.fromCharCode(10))
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

// The project area's own canopy cover: today = canopy cells inside the polygon (grid bit 3: LiDAR canopy + street crown
// discs), then the crown-disc change of its replaced and added trees (summed without overlaps, as the site estimate).
export const areaCover = computed(() => {
  const A = state.area
  state.addedVersion // dependency
  if (!A?.layout?.length && !A?.keptLayout?.length || !grid) return null
  A.version
  const { W, H, res, x0, y1, flags } = grid
  const xy = A.poly.map(([lon, lat]) => grid.toXY(lon, lat))
  const area = Math.abs(xy.reduce((a, [x, y], i) => { const [u, v] = xy[(i + 1) % xy.length]; return a + x * v - u * y }, 0)) / 2
  const xs = xy.map((q) => q[0]), ys = xy.map((q) => q[1])
  let can = 0
  for (let r = Math.max(0, Math.floor((y1 - Math.max(...ys)) / res)); r <= Math.min(H - 1, Math.ceil((y1 - Math.min(...ys)) / res)); r++)
    for (let c = Math.max(0, Math.floor((Math.min(...xs) - x0) / res)); c <= Math.min(W - 1, Math.ceil((Math.max(...xs) - x0) / res)); c++)
      if (flags[r * W + c] & 8 && insidePoly(x0 + (c + 0.5) * res, y1 - (r + 0.5) * res, xy)) can++
  const pal = state.meta.palette, P = state.trees.positions, t = state.trees.kept
  const disc = (d) => Math.PI * (d / 2) ** 2
  let d = 0
  A.layout.forEach((j, n) => (d += disc(pal[j].crown_diam_m) - disc(P.s0_crown_diam_m[A.idx[n]])))
  A.keptLayout.forEach((j, n) => (d += disc(pal[j].crown_diam_m) - disc(t.crown_diam_m[A.keptRows[n]])))
  state.added.forEach((a) => { if (a.species >= 0 && insidePoly(a.lon, a.lat, A.poly)) d += disc(pal[a.species].crown_diam_m) })
  const today = (100 * can * res * res) / area
  return { area_m2: area, today, now: today + (100 * d) / area, crowns_m2: d }
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

// ---- cost of the project area (v0.2.0, notes/tutor_feedback_24nov.md §3c): unit costs are the designer's own (the tool has no
// sourced prices), remembered in this browser; shown beside heat and runoff, never optimised
const COST_KEY = 'shade-sponge-costs'
// default unit prices = direct costs (no overhead, profit or VAT), notes/costs_stakeholders.md §1: new pit on a free spot ~260 €
// (a replaced small tree ~190 €, a large one with its stump ~1,070 €), young-tree transplant ~700 € (CYPE JSP020),
// dismantling and re-installing a traffic sign ~80 € without the post (CYPE DTM030, TSV050). Watering is not priced.
const COST_DEFAULTS = { tree: 260, move: 700, object: 80 }
export const costs = reactive((() => { try { return JSON.parse(localStorage.getItem(COST_KEY)) ?? { ...COST_DEFAULTS } } catch { return { ...COST_DEFAULTS } } })())
watch(costs, (c) => { try { localStorage.setItem(COST_KEY, JSON.stringify(c)) } catch { /* storage blocked */ } }, { deep: true })
export const projectCost = computed(() => {
  const A = state.area
  if (!A?.idx) return null
  const act = (key) => state.schedule.trees[key]?.action
  const keys = [...A.idx.map((i) => state.trees.positions.tree_id[i]), ...A.keptRows.map((k) => `k${k}`)]
  const moves = keys.filter((k) => act(k) === 'move').length
  const added = state.added.filter((t) => insidePoly(t.lon, t.lat, A.poly))
  const S = state.trees.spots
  const objects = added.filter((t) => t.spot && spotClass(S.id.indexOf(t.spot)) === 'conditional').length
  const n = { replace: keys.length - moves, move: moves, add: added.length, object: objects }
  const unit = { replace: costs.tree, move: costs.move, add: costs.tree, object: costs.object }
  const known = Object.keys(n).every((k) => !n[k] || unit[k] > 0)
  const total = Object.keys(n).reduce((a, k) => a + n[k] * (unit[k] || 0), 0)
  const trees = n.replace + n.move + n.add
  const shade = A.local?.shade_summer_m2h?.delta
  return { n, total, known, perTree: trees ? total / trees : null, perShade: shade > 0 ? (1000 * total) / shade : null }
})

// ---- theme: 'auto' follows the system; the choice is remembered in this browser ---------------------------------
const THEME_KEY = 'shade-sponge-theme'
const mq = typeof matchMedia === 'function' ? matchMedia('(prefers-color-scheme: dark)') : null
export const ui = reactive({ theme: (() => { try { return localStorage.getItem(THEME_KEY) || 'auto' } catch { return 'auto' } })(),
  systemDark: !!mq?.matches })
mq?.addEventListener?.('change', (e) => (ui.systemDark = e.matches))
// v0.2.0: guided flow (one step at a time) or expert mode (every setting at once, as v0.1.0); remembered in this browser
const MODE_KEY = 'shade-sponge-mode'
Object.assign(ui, { mode: (() => { try { return localStorage.getItem(MODE_KEY) || 'guided' } catch { return 'guided' } })(), step: 0 })
watch(() => ui.mode, (m) => { try { localStorage.setItem(MODE_KEY, m) } catch { /* storage blocked */ } })
export const isDark = computed(() => ui.theme === 'dark' || (ui.theme === 'auto' && ui.systemDark))
watch(() => ui.theme, (t) => {
  try { localStorage.setItem(THEME_KEY, t) } catch { /* storage blocked: the choice lasts this visit */ }
  if (t === 'auto') document.documentElement.removeAttribute('data-theme')
  else document.documentElement.setAttribute('data-theme', t)
}, { immediate: true })
// Earth palette (as the slides) for deck.gl and ECharts, light and dark
export const themeColors = computed(() => (isDark.value
  ? { text: '#F2F0EA', muted: '#B3BAB9', grid: '#333A33', plane: '#E4DFD3', other: '#5E5B54', kept: [150, 150, 140, 150], park: [110, 140, 105, 140],
      building: [64, 70, 64, 235], buildingLine: [40, 44, 40], facade: [120, 120, 115, 170], kerb: [170, 176, 184, 150], pit: [176, 120, 88, 170],
      ring: [242, 240, 234], ringOn: [157, 180, 222], area: [157, 180, 222], draft: [217, 184, 102],
      random: '#7A776E', city: '#D9B866', announced: '#8F8460', optimised: '#9DB4DE', current: '#E4DFD3', on: '#F2F0EA',
      ground: [44, 48, 44], basemap: 'https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json' }
  : { text: '#2A2622', muted: '#665E4F', grid: '#DCD8CE', plane: '#3A3630', other: '#C9C4B8', kept: [150, 155, 135, 150], park: [120, 150, 110, 140],
      building: [228, 226, 219, 235], buildingLine: [180, 176, 166], facade: [195, 195, 190, 210], kerb: [110, 116, 128, 210], pit: [102, 56, 37, 150],
      ring: [255, 255, 255], ringOn: [40, 63, 102], area: [40, 63, 102], draft: [140, 106, 36],
      random: '#B4AE9F', city: '#8C6A24', announced: '#CDB98A', optimised: '#5D7BAA', current: '#2A2622', on: '#283F66',
      ground: [242, 243, 240], basemap: 'https://tiles.openfreemap.org/styles/positron' }))
// Orthophoto of Catalonia, ICGC base-map service (CC BY 4.0)
export const ORTO = 'https://geoserveis.icgc.cat/servei/catalunya/mapa-base/wmts/orto/MON3857NW/{z}/{x}/{y}.png'
