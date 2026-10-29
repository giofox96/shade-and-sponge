// The street trees of the layout on screen, for the Species tab: every plane position (today's plane or its new
// species), every other street tree (kept, or replaced by a "replace all" project area) and the added trees, limited
// to the project area when the scope is 'area'. Traits: the palette medians for new species, each tree's own LiDAR
// values for today's trees.
import { computed, watch } from 'vue'
import { state, currentLayout, keptReplaced, insidePoly, AREA } from './store.js'

// leaf habit class: palette text, or the leaf calendar (meta.leaf_by_species) for today's other species
export const HABITS = ['deciduous', 'semi-deciduous', 'evergreen']
const habitOf = (text, leaf) => {
  if (text) return text.startsWith('evergreen') ? 'evergreen' : text.includes('semi') ? 'semi-deciduous' : 'deciduous'
  if (!leaf) return 'unknown'
  const m = Math.min(...leaf)
  return m === 1 ? 'evergreen' : m === 0 ? 'deciduous' : 'semi-deciduous'
}
// crown classes as the Barcelona palette colours (shade_sponge/web_export.py: < 4.5 / 4.5–7 / > 7 m)
export const CROWNS = ['small', 'medium', 'large']
const crownOf = (d) => (d < 4.5 ? 'small' : d < 7 ? 'medium' : 'large')

export const scopeIsArea = computed(() => state.speciesScope === 'area' && !!state.area)

export const viewTrees = computed(() => {
  if (!state.meta || !state.trees) return []
  void state.addedVersion
  void state.live?.version
  const pal = state.meta.palette, P = state.trees.positions, K = state.trees.kept
  const palIdx = new Map(pal.map((p, j) => [p.species, j]))
  const habits = new Map(pal.map((p) => [p.species, habitOf(p.leaf_habit)]))
  const habit = (s) => habits.get(s) ?? habitOf(null, state.meta.leaf_by_species?.[s])
  const area = scopeIsArea.value ? state.area : null
  const lay = currentLayout()
  const repl = state.scenarioId === AREA && state.area ? keptReplaced() : new Map()
  const out = []
  const fromPalette = (j, kind) => {
    const p = pal[j]
    out.push({ species: p.species, j, kind, h: p.height_m, d: p.crown_diam_m, lai: p.lai, habit: habit(p.species), crown: crownOf(p.crown_diam_m) })
  }
  for (const i of area ? area.idx : P.lon.keys()) {
    const j = lay[i]
    if (pal[j].in_palette) fromPalette(j, 'new')
    else out.push({ species: pal[j].species, j, kind: 'today', h: P.s0_height_m[i], d: P.s0_crown_diam_m[i], lai: pal[j].lai,
      habit: habit(pal[j].species), crown: crownOf(P.s0_crown_diam_m[i]) })
  }
  for (const k of area ? area.keptIdx : K.lon.keys()) {
    if (repl.has(k)) fromPalette(repl.get(k), 'new')
    else out.push({ species: K.species[k], j: palIdx.get(K.species[k]) ?? -1, kind: 'today', h: K.height_m[k], d: K.crown_diam_m[k],
      lai: K.lai[k], habit: habit(K.species[k]), crown: crownOf(K.crown_diam_m[k]) })
  }
  for (const t of state.added) if (t.species >= 0 && (!area || insidePoly(t.lon, t.lat, area.poly))) fromPalette(t.species, 'added')
  return out
})

const mean = (xs) => xs.reduce((a, b) => a + b, 0) / (xs.length || 1)
const tally = (keys, xs) => keys.map((k) => ({ name: k, n: xs.filter((x) => x === k).length }))

export const summary = computed(() => {
  const T = viewTrees.value
  const bySp = new Map()
  for (const t of T) bySp.set(t.species, (bySp.get(t.species) ?? 0) + 1)
  const species = [...bySp.entries()].map(([name, n]) => ({ name, n, share: n / T.length })).sort((a, b) => b.n - a.n)
  const H = -species.reduce((a, s) => a + s.share * Math.log(s.share), 0)
  const habit = tally([...HABITS, 'unknown'], T.map((t) => t.habit)).filter((x) => x.n)
  return {
    n: T.length, species, nSpecies: species.length, eff: Math.exp(H),
    habit, crown: tally(CROWNS, T.map((t) => t.crown)), kind: tally(['today', 'new', 'added'], T.map((t) => t.kind)).filter((x) => x.n),
    h: mean(T.map((t) => t.h)), d: mean(T.map((t) => t.d)), lai: mean(T.map((t) => t.lai)),
    crownArea: T.reduce((a, t) => a + (Math.PI * t.d * t.d) / 4, 0),
    counts: T.reduce((c, t) => (t.j >= 0 && c.set(t.j, (c.get(t.j) ?? 0) + 1), c), new Map()),
  }
})

// a drawn project area switches the tab to it; clearing it goes back to the neighbourhood
watch(() => state.area?.poly, (p) => (state.speciesScope = p ? 'area' : 'site'))
