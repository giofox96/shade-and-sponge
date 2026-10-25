<script setup>
// Trade-off chart: summer shade (benefit) vs winter shade (cost) for every scored layout; click a point to load it.
import { computed } from 'vue'
import VChart from 'vue-echarts'
import { use } from 'echarts/core'
import { ScatterChart } from 'echarts/charts'
import { GridComponent, TooltipComponent, LegendComponent } from 'echarts/components'
import { CanvasRenderer } from 'echarts/renderers'
import { state, label, scenario, LIVE } from '../store.js'

use([ScatterChart, GridComponent, TooltipComponent, LegendComponent, CanvasRenderer])

// Deck palette "Earth": ink = today, stone = random baseline, moss = optimised, ochre = live estimate
const INK = '#2a2622', MUTED = '#665e4f', LINE = '#dcd8ce', MOSS = '#3f663e', OCHRE = '#ba9546', OCHRE_TEXT = '#8c6a24'
const FONT = "'IBM Plex Sans', Arial, sans-serif"
const groups = [
  ['S0', 'Current trees', INK, 'rect'],
  ['S1', 'Random palette', '#b3bab9', 'circle'],
  ['S4', 'Optimised', '#7a9a6f', 'diamond'],
]
const axis = (name, gap) => ({
  name, nameLocation: 'middle', nameGap: gap, scale: true, nameTextStyle: { fontSize: 11, color: MUTED },
  axisLine: { lineStyle: { color: LINE } }, axisTick: { show: false }, splitLine: { lineStyle: { color: LINE, type: 'dashed' } },
  axisLabel: { color: MUTED, fontSize: 10, fontFamily: "'IBM Plex Mono', monospace" },
})

const option = computed(() => {
  const sc = state.meta?.scenarios ?? []
  const pt = (s) => ({
    value: [s.metrics.shade_summer_m2h / 1000, s.metrics.shade_winter_m2h / 1000],
    id: s.id,
    symbolSize: s.id === state.scenarioId ? 16 : 9,
    itemStyle: s.id === state.scenarioId ? { color: MOSS, borderColor: '#fff', borderWidth: 2 } : undefined,
  })
  return {
    animation: false,
    textStyle: { fontFamily: FONT, color: INK },
    grid: { left: 44, right: 10, top: state.live ? 48 : 28, bottom: 38 },
    legend: { top: 0, itemWidth: 10, itemHeight: 10, textStyle: { fontSize: 11, color: MUTED } },
    tooltip: {
      textStyle: { fontFamily: FONT, fontSize: 12, color: INK }, borderColor: LINE,
      formatter: (p) => {
        const s = p.data.id === LIVE ? scenario.value : sc.find((x) => x.id === p.data.id)
        return `${label(s)}<br>summer ${Math.round(p.value[0])}k · winter ${Math.round(p.value[1])}k m²·h`
      },
    },
    xAxis: axis('summer shade (k m²·h) →', 24),
    yAxis: axis('winter shade ↓', 32),
    series: [
      ...groups.map(([g, name, color, symbol]) => ({
        type: 'scatter', name, symbol, itemStyle: { color },
        data: sc.filter((s) => s.group === g).map(pt),
      })),
      ...(state.live ? [{ type: 'scatter', name: 'Live (estimate)', symbol: 'triangle', itemStyle: { color: OCHRE },
        data: [{ ...pt({ id: LIVE, metrics: state.live.metrics }), symbolSize: state.scenarioId === LIVE ? 16 : 11,
                 itemStyle: { color: OCHRE_TEXT, borderColor: '#fff', borderWidth: state.scenarioId === LIVE ? 2 : 0 } }] }] : []),
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
  <p class="note">Random palettes #1–9 are scored but have no saved layout, so only #0 opens on the map.</p>
</template>

<style scoped>
.chart { height: 220px; width: 100%; }
.note { font-size: 11px; color: var(--muted); margin: 2px 0 0; }
</style>
