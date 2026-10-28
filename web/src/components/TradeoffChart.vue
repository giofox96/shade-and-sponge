<script setup>
// Trade-off chart: summer shade (benefit) vs winter shade (cost) for every scored layout; click a point to load it.
import { computed } from 'vue'
import VChart from 'vue-echarts'
import { use } from 'echarts/core'
import { ScatterChart } from 'echarts/charts'
import { GridComponent, TooltipComponent, LegendComponent } from 'echarts/components'
import { CanvasRenderer } from 'echarts/renderers'
import { state, label, scenario, themeColors, LIVE } from '../store.js'

use([ScatterChart, GridComponent, TooltipComponent, LegendComponent, CanvasRenderer])

const groups = computed(() => {
  const C = themeColors.value
  return [['S0', 'Current trees', C.current, 'rect'], ['S1', 'Random palette', C.random, 'circle'],
    ['S1a', 'City rule', C.city, 'circle'], ['S4', 'Optimised', C.optimised, 'diamond']]
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
    grid: { left: 44, right: 10, top: state.live ? 48 : 28, bottom: 38 },
    legend: { top: 0, itemWidth: 10, itemHeight: 10, textStyle: { fontSize: 11, color: C.text } },
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
      })),
      ...(state.live ? [{ type: 'scatter', name: 'Live (estimate)', symbol: 'triangle', itemStyle: { color: themeColors.value.city },
        data: [{ ...pt({ id: LIVE, metrics: state.live.metrics }), symbolSize: state.scenarioId === LIVE ? 16 : 11,
                 itemStyle: { color: themeColors.value.city, borderColor: themeColors.value.text, borderWidth: state.scenarioId === LIVE ? 2 : 0 } }] }] : []),
    ],
  }
})

function onClick(p) {
  if (p.data?.id === LIVE) return void (state.scenarioId = LIVE)
  const s = state.meta.scenarios.find((x) => x.id === p.data?.id)
  if (s && (s.in_layouts || s.id === 'S0_current')) state.scenarioId = s.id
}
</script>

<template>
  <v-chart class="chart" :option="option" autoresize @click="onClick" />
  <p class="note">Random palettes and city-rule layouts #1–9 are scored but have no saved layout, so only #0 of each opens on the map.</p>
</template>

<style scoped>
.chart { height: 220px; width: 100%; }
.note { font-size: 11px; color: var(--muted); margin: 2px 0 0; }
</style>
