// Shared state: site data exported by `python -m shade_sponge.web_export`, plus what the user has selected.
import { reactive, computed } from 'vue'
import { optimise, proxySums, fitLine } from './optimize.js'

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
})

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
  const res = await optimise(state.pot, weights, { share: state.share, exclude: state.exclude })
  state.busy = false
  if (res.error) {
    state.liveError = res.error
    return
  }
  const sums = proxySums(state.pot, res.layout)
  const metrics = Object.fromEntries(Object.entries(calibration.value).map(([m, c]) => [m, c.a + c.b * sums[PROXY[m]]]))
  const counts = Object.fromEntries(state.pot.species.map((s, j) => [s, res.layout.filter((x) => x === j).length]))
  state.live = { weights, layout: res.layout, metrics, counts, ms: res.ms, version: (state.live?.version ?? 0) + 1 }
  state.scenarioId = LIVE
}

export const hexToRgb = (h) => [1, 3, 5].map((i) => parseInt(h.slice(i, i + 2), 16))
