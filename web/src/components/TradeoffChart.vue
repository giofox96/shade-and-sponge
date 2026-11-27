<script setup>
// Trade-off chart: summer shade (benefit) vs winter shade (cost) for every scored layout; click a point to load it.
import { computed } from 'vue'
import VChart from 'vue-echarts'
import { use } from 'echarts/core'
import { ScatterChart } from 'echarts/charts'
import { GridComponent, TooltipComponent, MarkLineComponent } from 'echarts/components'
import { CanvasRenderer } from 'echarts/renderers'
import { state, label, scenario, themeColors, LIVE } from '../store.js'

use([ScatterChart, GridComponent, TooltipComponent, MarkLineComponent, CanvasRenderer])

const groups = computed(() => {
  const C = themeColors.value
  return [['S0', 'Current trees', C.current, 'rect'], ['S1', 'Random palette', C.random, 'circle'],
    ['S1a', 'City announced mix', C.announced, 'circle'], ['S1b', 'City practice', C.city, 'circle'], ['S4', 'Optimised', C.optimised, 'diamond']]
})

const option = computed(() => {
  const sc = state.meta?.scenarios ?? []
  const pt = (s) => ({
    value: [s.metrics.shade_summer_m2h / 1000, s.metrics.shade_winter_m2h / 1000],
    id: s.id,
    symbolSize: s.id === state.scenarioId ? 16 : 9,
    itemStyle: s.id === state.scenarioId ? { color: themeColors.value.on, borderColor: themeColors.value.text, borderWidth: 2 } : undefined,
  })
  const C = themeColors.value
  const axis = { axisLine: { lineStyle: { color: C.muted } }, axisLabel: { color: C.muted }, splitLine: { lineStyle: { color: C.grid } },
    nameTextStyle: { fontSize: 11, color: C.muted } }
  return {
    animation: false,
    textStyle: { fontFamily: "'IBM Plex Sans', system-ui, sans-serif", color: C.text },
    // the legend is an HTML row above the chart (it wraps in a narrow panel instead of overlapping the plot)
    grid: { left: 44, right: 10, top: 10, bottom: 38 },
    tooltip: {
      formatter: (p) => {
        const s = p.data.id === LIVE ? scenario.value : sc.find((x) => x.id === p.data.id)
        return `${label(s)}<br>summer ${Math.round(p.value[0])}k · winter ${Math.round(p.value[1])}k m²·h`
      },
    },
    xAxis: { name: 'summer shade (k m²·h) →', nameLocation: 'middle', nameGap: 24, scale: true, ...axis },
    yAxis: { name: 'winter shade ↓', nameLocation: 'middle', nameGap: 32, scale: true, ...axis },
    series: [
      ...groups.value.map(([g, name, color, symbol]) => ({
        type: 'scatter', name, symbol, itemStyle: { color },
        data: sc.filter((s) => s.group === g).map(pt),
        // dashed lines through today's trees: a layout right of and below them gains summer shade and loses winter shade
        ...(g === 'S0' && today.value ? { markLine: { silent: true, symbol: 'none', label: { show: false },
          lineStyle: { color: C.current, type: 'dashed', width: 1 }, data: [{ xAxis: today.value[0] }, { yAxis: today.value[1] }] } } : {}),
      })),
      ...(state.live ? [{ type: 'scatter', name: 'Live (estimate)', symbol: 'triangle', itemStyle: { color: themeColors.value.city },
        data: [{ ...pt({ id: LIVE, metrics: state.live.metrics }), symbolSize: state.scenarioId === LIVE ? 16 : 11,
                 itemStyle: { color: themeColors.value.city, borderColor: themeColors.value.text, borderWidth: state.scenarioId === LIVE ? 2 : 0 } }] }] : []),
    ],
  }
})

const today = computed(() => {
  const s = state.meta?.scenarios?.find((x) => x.group === 'S0')
  return s ? [s.metrics.shade_summer_m2h / 1000, s.metrics.shade_winter_m2h / 1000] : null
})

const legend = computed(() => [
  ...groups.value.map(([, name, color, symbol]) => ({ name, color, symbol })),
  ...(state.live ? [{ name: 'Live (estimate)', color: themeColors.value.city, symbol: 'triangle' }] : []),
])

function onClick(p) {
  if (p.data?.id === LIVE) return void (state.scenarioId = LIVE)
  const s = state.meta.scenarios.find((x) => x.id === p.data?.id)
  if (s && (s.in_layouts || s.id === 'S0_current')) state.scenarioId = s.id
}
</script>

<template>
  <p class="hint">Better is <b>right</b> (more summer shade) and <b>down</b> (less winter shade) of today's trees. Click a point to open it.</p>
  <ul class="legend">
    <li v-for="l in legend" :key="l.name"><span :class="['mark', l.symbol]" :style="{ background: l.color }" />{{ l.name }}</li>
  </ul>
  <v-chart class="chart" :option="option" autoresize @click="onClick" />
  <p class="note">Random palettes and city-practice layouts #1–9 are scored but have no saved layout, so only #0 of each opens on the map.</p>
</template>

<style scoped>
.chart { height: 300px; width: 100%; }
.hint { font-size: 12px; margin: 0 0 6px; }
.legend { display: flex; flex-wrap: wrap; gap: 4px 12px; list-style: none; margin: 0; padding: 0; font-size: 11px; }
.legend li { display: flex; align-items: center; gap: 5px; }
.mark { width: 9px; height: 9px; border-radius: 50%; }
.mark.rect { border-radius: 1px; }
.mark.diamond { border-radius: 1px; transform: rotate(45deg) scale(0.85); }
.mark.triangle { border-radius: 0; clip-path: polygon(50% 0, 100% 100%, 0 100%); }
.note { font-size: 11px; color: var(--muted); margin: 2px 0 0; }
</style>
