<script setup>
// Canopy cover as an arc that fills up to the value, with a notch at the target (Giovanni's sketch, 27 Nov).
// The arc runs over half a circle; 0% at the left, `max`% at the right.
import { computed } from 'vue'
const p = defineProps({ value: Number, target: { type: Number, default: 30 }, max: { type: Number, default: 50 }, size: { type: Number, default: 46 } })
const R = 20, C = [24, 24]
const at = (v) => { const a = Math.PI * (1 - Math.min(Math.max(v, 0), p.max) / p.max); return [C[0] + R * Math.cos(a), C[1] - R * Math.sin(a)] }
const arc = (v) => { const [x, y] = at(v); return `M ${C[0] - R} ${C[1]} A ${R} ${R} 0 0 1 ${x.toFixed(2)} ${y.toFixed(2)}` }
const notch = computed(() => { const a = Math.PI * (1 - p.target / p.max); return [[C[0] + (R - 6) * Math.cos(a), C[1] - (R - 6) * Math.sin(a)], [C[0] + (R + 6) * Math.cos(a), C[1] - (R + 6) * Math.sin(a)]] })
</script>

<template>
  <svg :width="size" :height="size * 0.62" viewBox="0 0 48 30" role="img" :aria-label="`Canopy cover ${value?.toFixed(1)}% of a ${target}% target`">
    <path :d="arc(max)" class="track" />
    <path :d="arc(value ?? 0)" class="fill" />
    <line :x1="notch[0][0]" :y1="notch[0][1]" :x2="notch[1][0]" :y2="notch[1][1]" class="target" />
  </svg>
</template>

<style scoped>
path { fill: none; stroke-width: 6; stroke-linecap: round; }
.track { stroke: var(--line); }
.fill { stroke: var(--good); transition: d 0.7s ease; }
.target { stroke: var(--text); stroke-width: 1.6; }
</style>
