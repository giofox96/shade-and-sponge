<script setup>
// Priority triangle: each point is a weight set (summer shade, winter sun, runoff) that sums to 1.
// Read-only mode: the points are the precomputed optimised layouts; clicking one loads it.
import { computed } from 'vue'
import { state } from '../store.js'

const V = { s: [120, 18], w: [16, 186], r: [224, 186] } // summer top, winter bottom-left, runoff bottom-right
const xy = ([s, w, r]) => [s * V.s[0] + w * V.w[0] + r * V.r[0], s * V.s[1] + w * V.w[1] + r * V.r[1]]

const points = computed(() =>
  (state.meta?.scenarios ?? [])
    .filter((s) => s.weights && s.in_layouts)
    .map((s) => ({ id: s.id, w: s.weights, p: xy(s.weights), pareto: s.pareto })),
)
</script>

<template>
  <svg viewBox="0 0 240 206" class="tri" role="img" aria-label="Priority triangle: pick the weights of summer shade, winter sun and runoff">
    <polygon :points="[V.s, V.w, V.r].map((p) => p.join(',')).join(' ')" class="edge" />
    <text :x="V.s[0]" :y="V.s[1] - 6" text-anchor="middle">summer shade</text>
    <text :x="V.w[0]" :y="V.w[1] + 16">winter sun</text>
    <text :x="V.r[0]" :y="V.r[1] + 16" text-anchor="end">runoff</text>
    <g v-for="pt in points" :key="pt.id" class="pt" @click="state.scenarioId = pt.id">
      <title>summer {{ pt.w[0] }} · winter {{ pt.w[1] }} · runoff {{ pt.w[2] }}</title>
      <circle :cx="pt.p[0]" :cy="pt.p[1]" r="11" class="hit" />
      <circle :cx="pt.p[0]" :cy="pt.p[1]" :r="state.scenarioId === pt.id ? 7 : 4.5"
              :class="{ on: state.scenarioId === pt.id, front: pt.pareto }" />
    </g>
  </svg>
</template>

<style scoped>
.tri { width: 100%; display: block; }
.edge { fill: none; stroke: var(--muted); stroke-width: 1; }
text { font-size: 11px; fill: var(--muted); }
.pt { cursor: pointer; }
.hit { fill: transparent; }
.pt circle:not(.hit) { fill: var(--line); stroke: var(--bg); stroke-width: 1.5; }
.pt circle.front { fill: #85b7eb; }
.pt circle.on { fill: var(--accent); }
.pt:hover circle:not(.hit) { fill: var(--accent); }
</style>
