<script setup>
// Tree schedule (like a Revit schedule): the trees and the free spots of the project area (or the whole site) in two tabs,
// linked to the map both ways. The designer records an Action, a Reason and a field check per row; inside a project area
// the actions change what the optimiser replaces or plants (store.js, areaSets / setSpotEntry).
import { computed, ref, watch, nextTick } from 'vue'
import { state, currentLayout, keptReplaced, spotClass, spotWhy, AREA, TREE_ACTIONS, SPOT_ACTIONS, REASONS, CHECKS, keptKey,
  setTreeEntry, setSpotEntry, pickMoveTarget, focusOn, scheduleCsv, configJson, loadConfig, removeAdded } from '../store.js'

const tab = ref('trees')
const filter = ref('')
const LIMIT = 300 // rows drawn at once (the whole site has about 2,900 trees): "Show all" draws the rest
const limit = ref(LIMIT)
const msg = ref('')
const fileIn = ref(null)

// a tree the layout on screen already replaces shows Replace until the designer picks an action (not stored, so it
// follows the layout and does not change the optimisation)
const auto = (e, replaced) => (!e.action && replaced ? { action: 'replace', auto: true } : {})
const treeRows = computed(() => {
  state.addedVersion // dependency
  state.area?.version
  const T = state.trees, P = T.positions, K = T.kept, pal = state.meta.palette
  const lay = currentLayout()
  const plane = pal.find((s) => !s.in_palette)?.species ?? 'Platanus'
  const A = state.area
  const repl = state.scenarioId === AREA ? keptReplaced() : new Map()
  const planes = A ? A.inPlanes : [...P.lon.keys()]
  const kept = A ? A.keptIdx : [...K.lon.keys()]
  const sched = state.schedule.trees
  return [ // new trees first: the whole site has more rows than are drawn
    ...state.added.map((t, k) => ({ key: `a${k}`, sel: `a${k}`, id: t.spot ? `new · ${t.spot}` : `new ${k + 1}`, lon: t.lon, lat: t.lat,
      today: '', next: pal[t.species]?.species ?? '', size: t.spot ? T.spots.size_class[T.spots.id.indexOf(t.spot)] : '', isNew: true, added: k })),
    ...planes.map((i) => {
      const id = P.tree_id[i], e = sched[id] ?? {}, s = pal[lay[i]]
      return { key: id, sel: i, id, lon: P.lon[i], lat: P.lat[i], today: plane, next: s.in_palette ? s.species : '', width: P.sw_width_m?.[i],
        size: P.sw_size_class?.[i], crown: P.s0_crown_diam_m[i], ...e, ...auto(e, s.in_palette) }
    }),
    ...kept.map((k) => {
      const key = keptKey(k), e = sched[key] ?? {}
      return { key, sel: key, id: K.tree_id?.[k] ?? `other ${k + 1}`, lon: K.lon[k], lat: K.lat[k], today: K.species[k], next: pal[repl.get(k)]?.species ?? '',
        width: K.sw_width_m?.[k], size: K.size_class?.[k], crown: K.crown_diam_m[k], ...e, ...auto(e, repl.has(k)) }
    }),
  ]
})
const spotRows = computed(() => {
  const S = state.trees.spots
  const idx = state.area ? state.area.spotIdx : [...S.lon.keys()]
  return idx.map((s) => {
    const e = state.schedule.spots[S.id[s]] ?? {}
    return { key: S.id[s], sel: `s${s}`, s, id: S.id[s], lon: S.lon[s], lat: S.lat[s], width: S.width_m[s], size: S.size_class[s],
      status: spotClass(s), inWay: spotWhy(s), ...e }
  })
})
const rows = computed(() => {
  const r = tab.value === 'trees' ? treeRows.value : spotRows.value
  const f = filter.value.trim().toLowerCase()
  return f ? r.filter((x) => [x.id, x.today, x.next, x.status, x.inWay, x.action, x.reason, x.note].some((v) => v && String(v).toLowerCase().includes(f))) : r
})
const shown = computed(() => rows.value.slice(0, limit.value))
const decided = computed(() => {
  const n = (r) => r.filter((x) => x.action && !x.auto).length
  return { trees: n(treeRows.value), spots: n(spotRows.value) }
})
watch([tab, filter, () => state.area], () => (limit.value = LIMIT))

// a selection made on the map: switch tab, make sure the row is drawn, scroll to it
const body = ref(null)
watch(() => state.selected, async (sel) => {
  if (sel == null) return
  const inSpots = typeof sel === 'string' && sel[0] === 's'
  if (inSpots !== (tab.value === 'spots')) tab.value = inSpots ? 'spots' : 'trees'
  await nextTick()
  const at = rows.value.findIndex((r) => r.sel === sel)
  if (at < 0) return
  if (at >= limit.value) limit.value = at + 50
  await nextTick()
  body.value?.querySelector(`tr[data-k="${CSS.escape(String(sel))}"]`)?.scrollIntoView({ block: 'nearest' })
})

function save(name, text, type) {
  const a = Object.assign(document.createElement('a'), { download: name, href: URL.createObjectURL(new Blob([text], { type })) })
  a.click()
  URL.revokeObjectURL(a.href)
}
const scope = () => (state.area ? 'area' : 'site')
const csv = () => save(`schedule_${state.site}_${scope()}.csv`, scheduleCsv([
  ...treeRows.value.map((r) => ({ tab: 'tree', ...r, action: r.isNew ? 'add' : r.action })),
  ...spotRows.value.map((r) => ({ tab: 'spot', ...r })),
]), 'text/csv')
const saveCfg = () => save(`shade_sponge_${state.site}_config.json`, configJson(), 'application/json')
async function openCfg(ev) {
  const f = ev.target.files?.[0]
  ev.target.value = ''
  if (!f) return
  msg.value = 'Loading…'
  try {
    await loadConfig(JSON.parse(await f.text()))
    msg.value = `Loaded ${f.name}.`
  } catch (e) {
    msg.value = `Could not load ${f.name}: ${e.message}`
  }
}
</script>

<template>
  <div class="schedule">
    <div class="bar">
      <span class="seg" role="tablist" aria-label="Schedule tab">
        <button role="tab" :aria-selected="tab === 'trees'" :class="{ on: tab === 'trees' }" @click="tab = 'trees'">
          Trees <span class="muted">{{ treeRows.length }}</span></button>
        <button role="tab" :aria-selected="tab === 'spots'" :class="{ on: tab === 'spots' }" @click="tab = 'spots'">
          Spots <span class="muted">{{ spotRows.length }}</span></button>
      </span>
      <span class="muted small">{{ state.area ? 'Project area' : 'Whole site' }} · {{ decided.trees }} trees and {{ decided.spots }} spots decided</span>
      <input v-model="filter" class="find" type="search" placeholder="Filter (id, species, reason…)" aria-label="Filter rows" />
      <span class="spacer"></span>
      <button title="Schedule as CSV (both tabs)" @click="csv">CSV</button>
      <button title="Save actions, reasons, checks, project area, added trees, rules and priorities" @click="saveCfg">Save</button>
      <button title="Load a saved configuration" @click="fileIn.click()">Load</button>
      <span v-if="msg" class="small accent">{{ msg }}</span>
      <input ref="fileIn" type="file" accept=".json,application/json" hidden @change="openCfg" />
      <button class="close" aria-label="Close the schedule" @click="state.showSchedule = false">×</button>
    </div>
    <div ref="body" class="scroll">
      <table v-if="tab === 'trees'">
        <thead><tr><th>Id</th><th>Today</th><th>Crown</th><th>Sidewalk</th><th>Action</th><th>Reason</th><th>New species</th></tr></thead>
        <tbody>
          <tr v-for="r in shown" :key="r.key" :data-k="r.sel" :class="{ on: state.selected === r.sel, isnew: r.isNew }" @click="focusOn(r.sel, r.lon, r.lat)">
            <td>{{ r.id }}</td>
            <td><i>{{ r.today }}</i></td>
            <td class="num">{{ r.crown ? r.crown.toFixed(1) + ' m' : '' }}</td>
            <td class="num">{{ r.width ? r.width.toFixed(1) + ' m' : '' }} <span class="muted">{{ r.size === 'check' ? '' : r.size }}</span></td>
            <td @click.stop>
              <template v-if="r.isNew"><span class="accent">Add</span> <button class="x" title="Remove this new tree" @click="removeAdded(r.added)">×</button></template>
              <select v-else :value="r.action ?? ''" :class="{ auto: r.auto }" :title="r.auto ? 'Replaced by the layout on screen: pick an action to fix it' : ''"
                      :aria-label="`Action for ${r.id}`" @change="setTreeEntry(r.key, { action: $event.target.value })">
                <option v-for="[v, l] in TREE_ACTIONS" :key="v" :value="v">{{ l }}</option>
              </select>
              <button v-if="r.action === 'move' && !r.isNew" class="to" :class="{ on: state.movePick === r.key }"
                      :title="r.to ? `Moving to spot ${r.to}: click to choose another` : 'Choose the empty spot this tree goes to'"
                      @click="pickMoveTarget(r.key)">{{ r.to ? `→ ${r.to}` : 'choose spot' }}</button>
            </td>
            <td @click.stop>
              <template v-if="!r.isNew">
                <select :value="r.reason ?? ''" :aria-label="`Reason for ${r.id}`" @change="setTreeEntry(r.key, { reason: $event.target.value })">
                  <option v-for="[v, l] in REASONS" :key="v" :value="v">{{ l }}</option>
                </select>
                <input v-if="r.reason === 'other'" class="note" :value="r.note ?? ''" placeholder="why" :aria-label="`Reason text for ${r.id}`"
                       @change="setTreeEntry(r.key, { note: $event.target.value })" />
              </template>
            </td>
            <td><i>{{ r.next }}</i></td>
          </tr>
        </tbody>
      </table>
      <table v-else>
        <thead><tr><th>Id</th><th>Sidewalk</th><th>Status</th><th>In the way</th><th>Action</th><th>Field check</th></tr></thead>
        <tbody>
          <tr v-for="r in shown" :key="r.key" :data-k="r.sel" :class="{ on: state.selected === r.sel }" @click="focusOn(r.sel, r.lon, r.lat)">
            <td>{{ r.id }}</td>
            <td class="num">{{ r.width?.toFixed(1) }} m <span class="muted">{{ r.size }}</span></td>
            <td :class="r.status">{{ r.status }}</td>
            <td class="muted">{{ r.inWay }}</td>
            <td @click.stop>
              <select :value="r.action ?? ''" :aria-label="`Action for ${r.id}`" @change="setSpotEntry(r.s, { action: $event.target.value })">
                <option v-for="[v, l] in SPOT_ACTIONS" :key="v" :value="v">{{ l }}</option>
              </select>
            </td>
            <td @click.stop>
              <select :value="r.check ?? ''" :aria-label="`Field check for ${r.id}`" @change="setSpotEntry(r.s, { check: $event.target.value })">
                <option v-for="[v, l] in CHECKS" :key="v" :value="v">{{ l }}</option>
              </select>
            </td>
          </tr>
        </tbody>
      </table>
      <p v-if="rows.length > shown.length" class="small more">
        {{ shown.length }} of {{ rows.length }} rows · <button @click="limit = rows.length">Show all</button>
        <span class="muted"> or draw a project area</span></p>
      <p class="small muted foot">{{ state.area
        ? 'Inside the project area the actions change the result: Keep leaves a tree out of the optimisation, Replace or Move puts it in (a moved tree is scored as replaced at its position; where it goes is not modelled), Add plants a spot and Leave empty keeps "Fill spots" off it.'
        : 'On the whole site the actions are recorded only (they go into the CSV and the saved file); draw a project area to let them change the result. Add on a spot plants it.' }}</p>
    </div>
  </div>
</template>

<style scoped>
.to { font-size: 11px; padding: 1px 6px; border-radius: 999px; margin-left: 4px; }
.to.on { background: var(--accent); color: var(--bg); }
select.auto { font-style: italic; color: var(--muted); }
.schedule { position: absolute; left: 12px; right: 12px; bottom: 12px; height: 42%; z-index: 6; display: flex; flex-direction: column;
  background: var(--panel); border: 0.5px solid var(--line); border-radius: 16px; overflow: hidden; box-shadow: 0 10px 30px rgba(42, 38, 34, 0.16); }
.bar { display: flex; align-items: center; gap: 8px; padding: 6px 10px; flex-wrap: wrap; border-bottom: 0.5px solid var(--line); }
.spacer { flex: 1; }
.find { font: inherit; font-size: 12px; padding: 3px 6px; border: 0.5px solid var(--line); border-radius: 4px; background: var(--bg); color: var(--text); min-width: 160px; }
.close { font-size: 16px; line-height: 1; padding: 2px 8px; }
.scroll { overflow: auto; flex: 1; min-height: 0; }
table { width: 100%; border-collapse: collapse; font-size: 12px; }
th { position: sticky; top: 0; background: var(--panel); font-weight: 500; color: var(--muted); text-align: left; padding: 4px 8px; border-bottom: 0.5px solid var(--line); }
td { padding: 2px 8px; vertical-align: middle; border-bottom: 0.5px solid var(--line); white-space: nowrap; }
td.num { text-align: right; }
tr { cursor: pointer; }
tr:hover td { background: var(--hover); }
tr.on td { background: var(--hover); box-shadow: inset 0 0 0 9999px color-mix(in srgb, var(--accent) 12%, transparent); }
tr.isnew td:first-child { color: var(--accent); }
td.conditional { color: var(--warn); }
td.blocked { color: var(--bad); }
select { width: auto; max-width: 170px; }
select, .note { font: inherit; font-size: 12px; padding: 1px 2px; border: 0.5px solid var(--line); border-radius: 3px; background: var(--bg); color: var(--text); }
.note { width: 110px; margin-left: 4px; }
.x { padding: 0 6px; font-size: 12px; }
.more, .foot { padding: 6px 10px; margin: 0; }
.small { font-size: 11px; line-height: 1.45; }
.muted { color: var(--muted); }
.accent { color: var(--accent); }
</style>
