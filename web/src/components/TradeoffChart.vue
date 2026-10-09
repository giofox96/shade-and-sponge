<script setup>
// Trade-off chart: summer shade (benefit) vs winter shade (cost) for every scored layout; click a point to load it.
import { computed } from 'vue'
import VChart from 'vue-echarts'
import { use } from 'echarts/core'
import { ScatterChart } from 'echarts/charts'
import { GridComponent, TooltipComponent, LegendComponent } from 'echarts/components'
import { CanvasRenderer } from 'echarts/renderers'
import { state, label } from '../store.js'

use([ScatterChart, GridComponent, TooltipComponent, LegendComponent, CanvasRenderer])

const groups = [
  ['S0', 'Current trees', '#444441', 'rect'],
  ['S1', 'Random palette', '#b4b2a9', 'circle'],
  ['S4', 'Optimised', '#85b7eb', 'diamond'],
]

const option = computed(() => {
  const sc = state.meta?.scenarios ?? []
  const pt = (s) => ({
    value: [s.metrics.shade_summer_m2h / 1000, s.metrics.shade_winter_m2h / 1000],
    id: s.id,
    symbolSize: s.id === state.scenarioId ? 16 : 9,
    itemStyle: s.id === state.scenarioId ? { color: '#185fa5', borderColor: '#fff', borderWidth: 2 } : undefined,
  })
  return {
    animation: false,
    grid: { left: 44, right: 10, top: 28, bottom: 38 },
    legend: { top: 0, itemWidth: 10, itemHeight: 10, textStyle: { fontSize: 11 } },
    tooltip: {
      formatter: (p) => {
        const s = sc.find((x) => x.id === p.data.id)
        return `${label(s)}<br>summer ${Math.round(p.value[0])}k · winter ${Math.round(p.value[1])}k m²·h`
      },
    },
    xAxis: { name: 'summer shade (k m²·h) →', nameLocation: 'middle', nameGap: 24, scale: true, nameTextStyle: { fontSize: 11 } },
    yAxis: { name: 'winter shade ↓', nameLocation: 'middle', nameGap: 32, scale: true, nameTextStyle: { fontSize: 11 } },
    series: groups.map(([g, name, color, symbol]) => ({
      type: 'scatter', name, symbol, itemStyle: { color },
      data: sc.filter((s) => s.group === g).map(pt),
    })),
  }
})

function onClick(p) {
  const s = state.meta.scenarios.find((x) => x.id === p.data?.id)
  if (s && (s.in_layouts || s.id === 'S0_current')) state.scenarioId = s.id
}
</script>

<template>
  <v-chart class="chart" :option="option" autoresize @click="onClick" />
  <p class="note">Random palettes #1–9 are scored but have no saved layout, so only #0 opens on the map.</p>
</template>

<style scoped>
.chart { height: 220px; width: 100%; }
.note { font-size: 11px; color: var(--muted); margin: 2px 0 0; }
</style>
