// Shared state: site data exported by `python -m shade_sponge.web_export`, plus what the user has selected.
import { reactive, computed } from 'vue'

export const MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
export const BALANCED = 'S4_s0.50_w0.25_r0.25'

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
})

export async function load(site = state.site) {
  const base = `./data/${site}/`
  try {
    const [meta, trees, pot] = await Promise.all(
      ['meta.json', 'trees.json', 'potentials.json'].map((f) => fetch(base + f).then((r) => r.json())),
    )
    Object.assign(state, { meta, trees, pot, site })
  } catch (e) {
    state.error = `Couldn't load the site data (${e.message}). Run python -m shade_sponge.web_export first.`
  }
}

export const dataUrl = (file) => `./data/${state.site}/${file}`

export const scenario = computed(() => state.meta?.scenarios.find((s) => s.id === state.scenarioId))

export function label(s) {
  if (!s) return ''
  if (s.id === 'S0_current') return 'Current trees (mature planes)'
  if (s.id.startsWith('S1')) return `Random palette #${s.id.split('_').pop()}`
  const [a, b, c] = s.weights
  return `Optimised: summer ${a}, winter ${b}, runoff ${c}`
}

// Mean of the 10 random-palette layouts: the reference for "what a trait-blind replacement gives"
export const randomMean = computed(() => {
  const r = state.meta?.scenarios.filter((s) => s.group === 'S1') ?? []
  if (!r.length) return null
  const keys = Object.keys(r[0].metrics)
  return Object.fromEntries(keys.map((k) => [k, r.reduce((a, s) => a + s.metrics[k], 0) / r.length]))
})

export const hexToRgb = (h) => [1, 3, 5].map((i) => parseInt(h.slice(i, i + 2), 16))
