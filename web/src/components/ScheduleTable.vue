<script setup>
// Tree schedule (like a Revit schedule): the trees and the free spots of the project area (or the whole site) in two tabs,
// linked to the map both ways. The designer records an Action, a Reason and a field check per row; inside a project area
// the actions change what the optimiser replaces or plants (store.js, areaSets / setSpotEntry).
import { computed, ref, reactive, watch, nextTick, onMounted, onBeforeUnmount } from 'vue'
import { state, currentLayout, keptReplaced, spotClass, spotWhy, AREA, TREE_ACTIONS, SPOT_ACTIONS, REASONS, CHECKS, keptKey,
  setTreeEntry, setSpotEntry, pickMoveTarget, focusOn, scheduleCsv, configJson, loadConfig, removeAdded, ui } from '../store.js'

const tab = ref('trees') // trees | spots | both
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
    ...state.added.map((t, k) => ({ key: `a${k}`, sel: `a${k}`, id: t.spot ? `New tree · spot ${t.spot}` : `New tree ${k + 1}`, lon: t.lon, lat: t.lat,
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
  state.addedVersion // dependency
  const planted = new Map(state.added.map((t, k) => [t.spot, k]).filter(([id]) => id))
  return idx.map((s) => {
    const e = state.schedule.spots[S.id[s]] ?? {}, a = planted.get(S.id[s])
    return { key: S.id[s], sel: `s${s}`, s, id: S.id[s], lon: S.lon[s], lat: S.lat[s], width: S.width_m[s], size: S.size_class[s],
      status: a == null ? spotClass(s) : 'planted', inWay: spotWhy(s), planted: a, ...e }
  })
})
// columns; f = an Excel-like filter on its values (user 27 Nov), num = right-aligned
const TREE_COLS = [['id', 'Id'], ['today', 'Today', 'f'], ['crown', 'Crown', 'num'], ['width', 'Sidewalk', 'num'], ['size', 'Size', 'f'],
  ['action', 'Action', 'f'], ['reason', 'Reason', 'f'], ['next', 'New species', 'f']]
const SPOT_COLS = [['id', 'Id'], ['width', 'Sidewalk', 'num'], ['size', 'Size', 'f'], ['status', 'Status', 'f'], ['inWay', 'In the way', 'f'],
  ['action', 'Action', 'f'], ['check', 'Field check', 'f']]
const LABEL = Object.fromEntries([...TREE_ACTIONS, ...SPOT_ACTIONS, ...REASONS].filter(([v]) => v))
const cell = (r, k) => (k === 'action' && r.isNew ? 'Add' : k === 'size' && r.size === 'check' ? '' : k === 'check' ? (CHECKS.find(([v]) => v === (r.check ?? ''))?.[1]) : LABEL[r[k]] ?? r[k]) || '(empty)'
const out = reactive({ trees: {}, spots: {} }) // per tab: column -> Set of values left out
const openCol = ref(null) // 'trees.today'
function filterRows(r, t) {
  const f = filter.value.trim().toLowerCase(), o = Object.entries(out[t]).filter(([, v]) => v.size)
  return r.filter((x) => (!f || [x.id, x.today, x.next, x.status, x.inWay, x.action, x.reason, x.note].some((v) => v && String(v).toLowerCase().includes(f)))
    && o.every(([k, v]) => !v.has(cell(x, k))))
}
function values(t, k) { // distinct values of a column with their counts
  const n = new Map()
  for (const r of t === 'trees' ? treeRows.value : spotRows.value) n.set(cell(r, k), (n.get(cell(r, k)) ?? 0) + 1)
  return [...n].sort((a, b) => b[1] - a[1])
}
function toggleVal(t, k, v) {
  const set = (out[t][k] ??= new Set())
  set.has(v) ? set.delete(v) : set.add(v)
}
const onlyVal = (t, k, v) => (out[t][k] = new Set(values(t, k).map(([x]) => x).filter((x) => x !== v)))
const closeCol = () => (openCol.value = null)
onMounted(() => document.addEventListener('click', closeCol))
onBeforeUnmount(() => document.removeEventListener('click', closeCol))
const treeRowsF = computed(() => filterRows(treeRows.value, 'trees'))
const spotRowsF = computed(() => filterRows(spotRows.value, 'spots'))
const rows = computed(() => (tab.value === 'spots' ? spotRowsF.value : tab.value === 'trees' ? treeRowsF.value : [...treeRowsF.value, ...spotRowsF.value]))
const treeShown = computed(() => (tab.value === 'spots' ? [] : treeRowsF.value.slice(0, limit.value)))
const spotShown = computed(() => (tab.value === 'trees' ? [] : spotRowsF.value.slice(0, Math.max(0, limit.value - treeShown.value.length))))
const shownN = computed(() => treeShown.value.length + spotShown.value.length)

// docked next to the guide, or detached: a floating window you drag by its bar and resize from its corner, remembered here
const DOCK = 'shade-sponge-schedule'
const DOCK0 = { docked: true, x: 80, y: 80, w: 900, h: 360 }
const dock = reactive((() => { try { return { ...DOCK0, ...JSON.parse(localStorage.getItem(DOCK)) } } catch { return { ...DOCK0 } } })())
watch(dock, () => { try { localStorage.setItem(DOCK, JSON.stringify(dock)) } catch { /* storage blocked */ } })
const box = ref(null)
// guided and docked: the table's top follows the guide card's top, its bottom the step bar's (user 27 Nov sketch)
const guideTop = ref(null)
const floatStyle = computed(() => (!dock.docked ? { left: `${dock.x}px`, top: `${dock.y}px`, width: `${dock.w}px`, height: `${dock.h}px` }
  : ui.mode === 'guided' && guideTop.value != null ? { top: `${guideTop.value}px`, height: 'auto' } : {}))
let gro = null
function measureGuide() {
  const g = document.querySelector('.guide'), m = box.value?.offsetParent
  guideTop.value = g && m && innerWidth > 1000 ? Math.max(12, g.firstElementChild.getBoundingClientRect().top - m.getBoundingClientRect().top) : null
}
onMounted(() => {
  gro = new ResizeObserver(measureGuide)
  const g = document.querySelector('.guide')
  if (g) { gro.observe(g); [...g.children].forEach((c) => gro.observe(c)) }
  addEventListener('resize', measureGuide)
  setTimeout(measureGuide, 500) // after the card's slide-in
})
onBeforeUnmount(() => { gro?.disconnect(); removeEventListener('resize', measureGuide) })
watch(() => ui.step, () => setTimeout(measureGuide, 500))
function drag(e) {
  if (dock.docked || e.target.closest('button, input, select')) return
  const x0 = e.clientX - dock.x, y0 = e.clientY - dock.y
  const move = (m) => Object.assign(dock, { x: Math.max(0, m.clientX - x0), y: Math.max(0, m.clientY - y0) })
  const up = () => { removeEventListener('pointermove', move); removeEventListener('pointerup', up) }
  addEventListener('pointermove', move)
  addEventListener('pointerup', up)
}
let ro = null
onMounted(() => {
  ro = new ResizeObserver(() => { const el = box.value; if (!dock.docked && el) Object.assign(dock, { w: el.offsetWidth, h: el.offsetHeight }) })
  ro.observe(box.value)
})
onBeforeUnmount(() => ro?.disconnect())
const decided = computed(() => {
  const n = (r) => r.filter((x) => x.action && !x.auto).length
  return { trees: n(treeRows.value), spots: n(spotRows.value) }
})
watch([tab, filter, () => state.area, out], () => (limit.value = LIMIT), { deep: true })

// a selection made on the map: switch tab, make sure the row is drawn, scroll to it
const body = ref(null)
watch(() => state.selected, async (sel) => {
  if (sel == null) return
  const inSpots = typeof sel === 'string' && sel[0] === 's'
  if (tab.value !== 'both' && inSpots !== (tab.value === 'spots')) tab.value = inSpots ? 'spots' : 'trees'
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
  <div ref="box" class="schedule" :class="{ docked: dock.docked, floating: !dock.docked, guided: ui.mode === 'guided' }" :style="floatStyle">
    <div class="bar" @pointerdown="drag">
      <span class="seg" role="tablist" aria-label="Schedule tab">
        <button v-for="[v, l, n] in [['trees', 'Trees', treeRows.length], ['spots', 'Spots', spotRows.length], ['both', 'Both', treeRows.length + spotRows.length]]"
                :key="v" role="tab" :aria-selected="tab === v" :class="{ on: tab === v }" @click="tab = v">{{ l }} <span class="muted">{{ n }}</span></button>
      </span>
      <span class="muted small">{{ state.area ? 'Project area' : 'Whole site' }}: {{ decided.trees }} trees and {{ decided.spots }} spots decided</span>
      <input v-model="filter" class="find" type="search" placeholder="Search (id, species, reason…)" aria-label="Search rows" />
      <span class="spacer"></span>
      <button title="Schedule as CSV (both tabs)" @click="csv">CSV</button>
      <button title="Save actions, reasons, checks, project area, added trees, rules and priorities" @click="saveCfg">Save</button>
      <button title="Load a saved configuration" @click="fileIn.click()">Load</button>
      <span v-if="msg" class="small accent">{{ msg }}</span>
      <input ref="fileIn" type="file" accept=".json,application/json" hidden @change="openCfg" />
      <button :title="dock.docked ? 'Detach: a window you can move and resize' : 'Dock it back at the bottom'" @click="dock.docked = !dock.docked">
        {{ dock.docked ? 'Detach' : 'Dock' }}</button>
      <button class="close" aria-label="Close the schedule" @click="state.showSchedule = false">×</button>
    </div>
    <div ref="body" class="scroll">
      <template v-for="t in tab === 'both' ? ['trees', 'spots'] : [tab]" :key="t">
        <p v-if="tab === 'both'" class="cap">{{ t === 'trees' ? 'Trees' : 'Planting spots' }}</p>
        <table>
          <thead><tr>
            <th v-for="[k, l, f] in t === 'trees' ? TREE_COLS : SPOT_COLS" :key="k" :class="{ num: f === 'num' }">{{ l }}
              <button v-if="f === 'f'" class="fbtn" :class="{ active: out[t][k]?.size }" :aria-label="`Filter ${l}`"
                      @click.stop="openCol = openCol === `${t}.${k}` ? null : `${t}.${k}`">▾</button>
              <div v-if="openCol === `${t}.${k}`" class="fpop" @click.stop>
                <label v-for="[v, n] in values(t, k)" :key="v"><input type="checkbox" :checked="!out[t][k]?.has(v)" @change="toggleVal(t, k, v)" />
                  <span>{{ v }}</span><button class="only" @click.prevent="onlyVal(t, k, v)">only</button><span class="muted">{{ n }}</span></label>
                <button class="clear" @click="out[t][k] = new Set()">Show all</button>
              </div>
            </th>
          </tr></thead>
          <tbody v-if="t === 'trees'">
            <tr v-for="r in treeShown" :key="r.key" :data-k="r.sel" :class="{ on: state.selected === r.sel, isnew: r.isNew }" @click="focusOn(r.sel, r.lon, r.lat)">
              <td>{{ r.id }}</td>
              <td><i>{{ r.today }}</i></td>
              <td class="num">{{ r.crown ? r.crown.toFixed(1) + ' m' : '' }}</td>
              <td class="num">{{ r.width ? r.width.toFixed(1) + ' m' : '' }}</td>
              <td>{{ r.size === 'check' ? '' : r.size }}</td>
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
          <tbody v-else>
            <tr v-for="r in spotShown" :key="r.key" :data-k="r.sel" :class="{ on: state.selected === r.sel }" @click="focusOn(r.sel, r.lon, r.lat)">
              <td>{{ r.id }}</td>
              <td class="num">{{ r.width?.toFixed(1) }} m</td>
              <td>{{ r.size }}</td>
              <td :class="r.status">{{ r.status }}</td>
              <td class="muted">
                <button v-if="r.planted != null" class="to" title="Show the new tree on this spot"
                        @click.stop="focusOn(`a${r.planted}`, state.added[r.planted].lon, state.added[r.planted].lat)">planted →</button>
                <template v-else>{{ r.inWay }}</template></td>
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
      </template>
      <p v-if="rows.length > shownN" class="small more">
        {{ shownN }} of {{ rows.length }} rows · <button @click="limit = rows.length">Show all</button>
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
.schedule.docked { left: 12px; right: 12px; bottom: 12px; height: 42%; }
/* guided mode: docked to the right of the guide card (user 27 Nov); on a narrow screen it goes under it */
.schedule.docked.guided { left: calc(min(460px, 100% - 40px) + 32px); right: 60px; bottom: 20px; } /* clear of the layer column */
@media (max-width: 1000px) { .schedule.docked.guided { left: 12px; } }
.schedule.floating { position: fixed; z-index: 9; resize: both; min-width: 420px; min-height: 160px; }
.floating .bar { cursor: move; }
.schedule { position: absolute; z-index: 6; display: flex; flex-direction: column;
  background: var(--panel); border: 0.5px solid var(--line); border-radius: 16px; overflow: hidden; box-shadow: 0 10px 30px rgba(42, 38, 34, 0.16); }
.bar { display: flex; align-items: center; gap: 8px; padding: 6px 10px; flex-wrap: wrap; border-bottom: 0.5px solid var(--line); }
.spacer { flex: 1; }
.find { font: inherit; font-size: 12px; padding: 3px 6px; border: 0.5px solid var(--line); border-radius: 4px; background: var(--bg); color: var(--text); min-width: 160px; }
.close { font-size: 16px; line-height: 1; padding: 2px 8px; }
.scroll { overflow: auto; flex: 1; min-height: 0; }
table { width: 100%; border-collapse: collapse; font-size: 12px; }
th { position: sticky; top: 0; background: var(--panel); font-weight: 500; color: var(--muted); text-align: left; padding: 4px 8px; border-bottom: 0.5px solid var(--line); }
td { padding: 2px 8px; vertical-align: middle; border-bottom: 0.5px solid var(--line); white-space: nowrap; }
td.num, th.num { text-align: right; font-variant-numeric: tabular-nums; }
th { white-space: nowrap; }
.fbtn { font-size: 10px; padding: 0 4px; margin-left: 2px; border-radius: 3px; color: var(--muted); }
.fbtn.active { background: var(--accent); color: var(--bg); border-color: var(--accent); }
.fpop { position: absolute; top: 100%; left: 0; z-index: 3; min-width: 190px; max-height: 240px; overflow: auto; background: var(--panel);
  border: 0.5px solid var(--line); border-radius: 10px; padding: 6px; box-shadow: 0 8px 24px rgba(42, 38, 34, 0.18); color: var(--text); font-weight: 400; }
.fpop label { display: grid; grid-template-columns: auto 1fr auto auto; gap: 6px; align-items: center; padding: 2px 4px; text-align: left; }
.fpop .only { font-size: 10px; padding: 0 4px; opacity: 0; } .fpop label:hover .only { opacity: 1; }
.fpop .clear { width: 100%; margin-top: 4px; font-size: 11px; }
.cap { margin: 8px 10px 2px; font-size: 12px; font-weight: 600; }
td.planted { color: var(--good); }
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
