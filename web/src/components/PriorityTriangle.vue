<script setup>
// Priority triangle: each point is a weight set (summer shade, winter sun, runoff) that sums to 1.
// Dots = precomputed optimised layouts (exact scores); click anywhere else = live re-optimisation (estimate).
import { computed, ref } from 'vue'
import { state, runLive, LIVE } from '../store.js'

const V = { s: [120, 18], w: [16, 186], r: [224, 186] } // summer top, winter bottom-left, runoff bottom-right
const xy = ([s, w, r]) => [s * V.s[0] + w * V.w[0] + r * V.r[0], s * V.s[1] + w * V.w[1] + r * V.r[1]]
const svg = ref(null)

const points = computed(() =>
  (state.meta?.scenarios ?? [])
    .filter((s) => s.weights && s.in_layouts)
    .map((s) => ({ id: s.id, w: s.weights, p: xy(s.weights), pareto: s.pareto })),
)
const live = computed(() => (state.live ? xy(state.live.weights) : null))

function weightsAt(evt) {
  const pt = svg.value.createSVGPoint()
  Object.assign(pt, { x: evt.clientX, y: evt.clientY })
  const { x, y } = pt.matrixTransform(svg.value.getScreenCTM().inverse())
  const [S, W, R] = [V.s, V.w, V.r]
  const det = (W[1] - R[1]) * (S[0] - R[0]) + (R[0] - W[0]) * (S[1] - R[1])
  let s = ((W[1] - R[1]) * (x - R[0]) + (R[0] - W[0]) * (y - R[1])) / det
  let w = ((R[1] - S[1]) * (x - R[0]) + (S[0] - R[0]) * (y - R[1])) / det
  let r = 1 - s - w
  ;[s, w, r] = [s, w, r].map((v) => Math.max(0, v))
  const n = s + w + r
  const q = [s / n, w / n].map((v) => Math.round(v * 20) / 20) // 0.05 steps
  return [q[0], q[1], Math.max(0, +(1 - q[0] - q[1]).toFixed(2))]
}
</script>

<template>
  <svg ref="svg" viewBox="0 0 240 206" class="tri" role="img"
       aria-label="Priority triangle: pick the weights of summer shade, winter sun and runoff"
       @click="runLive(weightsAt($event))">
    <polygon :points="[V.s, V.w, V.r].map((p) => p.join(',')).join(' ')" class="edge" />
    <text :x="V.s[0]" :y="V.s[1] - 6" text-anchor="middle">summer shade</text>
    <text :x="V.w[0]" :y="V.w[1] + 16">winter sun</text>
    <text :x="V.r[0]" :y="V.r[1] + 16" text-anchor="end">runoff</text>
    <g v-for="pt in points" :key="pt.id" class="pt" @click.stop="state.scenarioId = pt.id">
      <title>summer {{ pt.w[0] }} · winter {{ pt.w[1] }} · runoff {{ pt.w[2] }} (exact)</title>
      <circle :cx="pt.p[0]" :cy="pt.p[1]" r="9" class="hit" />
      <circle :cx="pt.p[0]" :cy="pt.p[1]" :r="state.scenarioId === pt.id ? 7 : 4.5"
              :class="{ on: state.scenarioId === pt.id, front: pt.pareto }" />
    </g>
    <g v-if="live" class="live" @click.stop="state.scenarioId = LIVE">
      <title>live estimate: summer {{ state.live.weights[0] }} · winter {{ state.live.weights[1] }} · runoff {{ state.live.weights[2] }}</title>
      <polygon :points="`${live[0]},${live[1] - 8} ${live[0] - 7},${live[1] + 5} ${live[0] + 7},${live[1] + 5}`"
               :class="{ on: state.scenarioId === LIVE }" />
    </g>
  </svg>
</template>

<style scoped>
.tri { width: 100%; display: block; cursor: crosshair; }
.edge { fill: var(--hover); fill-opacity: 0.4; stroke: var(--muted); stroke-width: 1; }
text { font-size: 11px; fill: var(--muted); pointer-events: none; }
.pt { cursor: pointer; }
.hit { fill: transparent; }
.pt circle:not(.hit) { fill: var(--line); stroke: var(--bg); stroke-width: 1.5; }
.pt circle.front { fill: #85b7eb; }
.pt circle.on { fill: var(--accent); }
.pt:hover circle:not(.hit) { fill: var(--accent); }
.live polygon { fill: #f0997b; stroke: #993c1d; stroke-width: 1; cursor: pointer; }
.live polygon.on { fill: #d85a30; }
</style>
