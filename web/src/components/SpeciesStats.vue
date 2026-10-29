<script setup>
// Summary of the street trees in view (whole neighbourhood or project area): headline numbers, the species mix as
// ranked bars against the plan's 15% cap, and three donuts (leaf habit, crown size, today's vs new trees).
import { computed } from 'vue'
import VChart from 'vue-echarts'
import { use } from 'echarts/core'
import { PieChart } from 'echarts/charts'
import { TooltipComponent } from 'echarts/components'
import { CanvasRenderer } from 'echarts/renderers'
import { state, themeColors } from '../store.js'
import { summary, scopeIsArea } from '../speciesview.js'

use([PieChart, TooltipComponent, CanvasRenderer])

const CAP = 0.15 // the tree master plan's city-wide cap per species (notes/tree_master_plan.md)
const TOP = 10
// fixed categorical order, from the validated palette slots (web_export.COLORS; dataviz check light + dark, 29 Oct)
const HABIT_C = { deciduous: '#b07a12', 'semi-deciduous': '#2f5fa8', evergreen: '#3e8a3a' }
const CROWN_C = { small: '#a9c79a', medium: '#5e8f55', large: '#2f5a2b' } // one hue, light to dark = magnitude
const LABEL = { today: "today's trees", new: 'new (replanted)', added: 'added', 'semi-deciduous': 'semi-deciduous',
  small: '< 4.5 m', medium: '4.5–7 m', large: '> 7 m' }

const S = computed(() => summary.value)
const colorOf = computed(() => {
  const m = new Map(state.meta.palette.map((p) => [p.species, p.color]))
  return (s) => m.get(s) ?? themeColors.value.other
})
const bars = computed(() => {
  const sp = S.value.species
  const top = sp.slice(0, TOP).map((s) => ({ ...s, color: colorOf.value(s.name) }))
  const rest = sp.slice(TOP)
  if (rest.length) top.push({ name: `${rest.length} other species`, n: rest.reduce((a, s) => a + s.n, 0),
    share: rest.reduce((a, s) => a + s.share, 0), color: themeColors.value.other, other: true })
  return top
})
const maxShare = computed(() => Math.max(CAP * 1.15, ...bars.value.map((b) => b.share)))
const pct = (v) => `${(100 * v).toFixed(v < 0.1 ? 1 : 0)}%`

function donut(title, rows, colors) {
  const C = themeColors.value
  return {
    title,
    rows: rows.map((r) => ({ ...r, color: colors[r.name] ?? C.other })),
    option: {
      tooltip: { trigger: 'item', formatter: (p) => `${p.name}<br/><b>${p.value.toLocaleString('en')}</b> trees · ${p.percent}%` },
      series: [{
        type: 'pie', radius: ['52%', '82%'], center: ['50%', '50%'], label: { show: false }, avoidLabelOverlap: true,
        itemStyle: { borderColor: getComputedStyle(document.documentElement).getPropertyValue('--panel').trim() || '#fff', borderWidth: 2, borderRadius: 3 },
        emphasis: { scale: true, scaleSize: 4 },
        data: rows.filter((r) => r.n).map((r) => ({ name: LABEL[r.name] ?? r.name, value: r.n, itemStyle: { color: colors[r.name] ?? C.other } })),
      }],
    },
  }
}
const donuts = computed(() => {
  const C = themeColors.value
  return [
    donut('Leaf habit', S.value.habit, { ...HABIT_C, unknown: C.other }),
    donut('Crown width', S.value.crown, CROWN_C),
    donut("Today's and new trees", S.value.kind, { today: C.other, new: C.optimised, added: '#3e8a3a' }),
  ]
})
const missing = computed(() => state.pot.n_total - state.trees.positions.lon.length - state.trees.kept.lon.length)
const share = (rows, k) => (S.value.n ? (rows.find((r) => r.name === k)?.n ?? 0) / S.value.n : 0)
</script>

<template>
  <div v-if="S.n" class="stats">
    <div class="tiles">
      <div><b>{{ S.n.toLocaleString('en') }}</b><small>street trees</small></div>
      <div><b>{{ S.nSpecies }}</b><small>species</small></div>
      <div :title="'exp(Shannon H): the number of equally common species with the same diversity'"><b>{{ S.eff.toFixed(1) }}</b><small>effective species</small></div>
      <div><b :class="{ bad: !scopeIsArea && S.species[0].share > CAP }">{{ pct(S.species[0].share) }}</b><small>largest: {{ S.species[0].name.split(' ')[0] }}</small></div>
      <div><b>{{ pct(share(S.habit, 'evergreen')) }}</b><small>evergreen</small></div>
      <div><b>{{ S.h.toFixed(1) }} m</b><small>mean height</small></div>
      <div><b>{{ S.d.toFixed(1) }} m</b><small>mean crown width</small></div>
      <div><b>{{ S.lai.toFixed(2) }}</b><small>mean LAI</small></div>
      <div :title="'Sum of the crown discs, overlaps counted twice'"><b>{{ (S.crownArea / 1e4).toFixed(2) }} ha</b><small>crown area (discs)</small></div>
    </div>

    <div class="row">
      <section class="mix">
        <h4>Species mix <span class="muted">dashed line = 15% cap</span></h4>
        <ul class="bars">
          <li v-for="b in bars" :key="b.name" :title="`${b.name}: ${b.n.toLocaleString('en')} trees, ${pct(b.share)}`">
            <span class="name"><span class="dot" :style="{ background: b.color }"></span><i v-if="!b.other">{{ b.name }}</i><template v-else>{{ b.name }}</template></span>
            <span class="track">
              <span class="fill" :style="{ width: (100 * b.share) / maxShare + '%', background: b.color }"></span>
              <span class="cap" :style="{ left: (100 * CAP) / maxShare + '%' }"></span>
            </span>
            <span class="val">{{ pct(b.share) }}</span>
          </li>
        </ul>
      </section>
      <section v-for="d in donuts" :key="d.title" class="donut">
        <h4>{{ d.title }}</h4>
        <VChart class="pie" :option="d.option" autoresize :aria-label="`${d.title} donut chart`" />
        <ul class="legend">
          <li v-for="r in d.rows" :key="r.name"><span class="dot" :style="{ background: r.color }"></span>{{ LABEL[r.name] ?? r.name }}
            <span class="muted">{{ pct(r.n / S.n) }}</span></li>
        </ul>
      </section>
    </div>
    <p class="small muted">Today's trees carry their own LiDAR crown, height and LAI; new and added trees the palette medians. Habit of
      today's other species from their leaf calendar ("unknown" when there is none). The 15% cap is the plan's city-wide rule:
      inside a small area it is only a reference.<template v-if="missing > 0"> Street trees without a matched LiDAR crown
      ({{ missing.toLocaleString('en') }} of {{ state.pot.n_total.toLocaleString('en') }}) are not counted.</template></p>
  </div>
</template>

<style scoped>
.stats { background: var(--panel); border: 0.5px solid var(--line); border-radius: 8px; padding: 12px; margin-bottom: 14px; }
.tiles { display: grid; grid-template-columns: repeat(auto-fill, minmax(104px, 1fr)); gap: 8px; margin-bottom: 12px; }
.tiles div { border-left: 2px solid var(--line); padding-left: 8px; }
.tiles b { display: block; font-size: 17px; font-weight: 500; font-variant-numeric: tabular-nums; }
.tiles b.bad { color: var(--bad); }
.tiles small { display: block; font-size: 10px; color: var(--muted); }
.row { display: grid; grid-template-columns: minmax(240px, 2fr) repeat(3, minmax(140px, 1fr)); gap: 14px; }
@media (max-width: 1100px) { .row { grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); } .mix { grid-column: 1 / -1; } }
h4 { font-size: 12px; font-weight: 500; margin: 0 0 6px; display: flex; justify-content: space-between; gap: 6px; }
h4 .muted { font-weight: 400; font-size: 10px; }
.bars { list-style: none; padding: 0; margin: 0; font-size: 11px; }
.bars li { display: grid; grid-template-columns: minmax(90px, 40%) 1fr 38px; gap: 6px; align-items: center; padding: 1px 0; }
.bars .name { overflow: hidden; white-space: nowrap; text-overflow: ellipsis; }
.track { position: relative; height: 8px; }
.fill { position: absolute; left: 0; top: 0; bottom: 0; border-radius: 0 4px 4px 0; min-width: 2px; }
.cap { position: absolute; top: -3px; bottom: -3px; border-left: 1px dashed var(--muted); }
.val { text-align: right; font-variant-numeric: tabular-nums; color: var(--muted); }
.pie { height: 120px; width: 100%; }
.legend { list-style: none; padding: 0; margin: 4px 0 0; font-size: 11px; }
.legend li { display: flex; align-items: center; gap: 5px; }
.legend .muted { margin-left: auto; font-variant-numeric: tabular-nums; }
.dot { display: inline-block; width: 8px; height: 8px; border-radius: 50%; flex: none; margin-right: 4px; }
.small { font-size: 11px; line-height: 1.45; margin: 10px 0 0; }
.muted { color: var(--muted); }
section { padding: 0; border: 0; }
</style>
