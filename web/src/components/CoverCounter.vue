<script setup>
// Canopy cover of the layout on screen against the tree master plan's 30% target, with the added trees counted in.
import { computed } from 'vue'
import { cover } from '../store.js'

const c = computed(() => cover.value)
const sign = (v) => `${v > 0 ? '+' : v < 0 ? '−' : '±'}${Math.abs(v).toFixed(2)}`
const width = (v) => `${Math.max(0, Math.min(100, (100 * v) / c.value.target_pct))}%`
</script>

<template>
  <div v-if="c" class="cover">
    <div class="row">
      <span class="big">{{ c.approx ? '≈ ' : '' }}{{ c.pct.toFixed(1) }}%</span>
      <span class="muted small">canopy cover · plan target {{ c.target_pct }}%</span>
    </div>
    <div class="bar" role="meter" :aria-valuenow="c.pct.toFixed(1)" aria-valuemin="0" :aria-valuemax="c.target_pct"
         :aria-label="`Canopy cover ${c.pct.toFixed(1)} percent of a ${c.target_pct} percent target`">
      <span class="today" :style="{ width: width(c.measured_pct) }"></span>
      <span class="now" :class="{ up: c.vsToday > 0 }" :style="{ width: width(c.pct) }"></span>
    </div>
    <p class="small">
      <b :class="c.vsToday > 0.005 ? 'good' : c.vsToday < -0.005 ? 'bad' : ''">{{ sign(c.vsToday) }} pts</b> vs today ({{ c.measured_pct.toFixed(1) }}%)
      <template v-if="c.addedN"> · {{ c.addedN }} added tree{{ c.addedN > 1 ? 's' : '' }}: {{ sign(c.added) }} pts</template>
      <br>{{ c.gap > 0 ? `${c.gap.toFixed(1)} pts to the target, about ${c.gapHa.toFixed(1)} ha of crowns` : 'Target reached' }}
    </p>
    <p v-if="c.additions" class="muted small">
      For scale: planting all {{ c.additions.spots }} free street spots (an upper bound), with the optimised species, adds
      {{ sign(c.additions.opt_pts) }} pts ({{ sign(c.additions.city_pts) }} with the city's mix).
    </p>
    <p class="muted small note">Today = LiDAR canopy over 2 m (2021). Changes come from the crown discs<template v-if="c.approx">,
      summed without overlaps (an estimate that runs high where new crowns overlap existing ones)</template>.
      The 30% is the plan's city-wide target for 2037.</p>
  </div>
</template>

<style scoped>
.cover { margin-bottom: 4px; }
.row { display: flex; align-items: baseline; gap: 8px; }
.big { font-size: 24px; font-weight: 700; }
.bar { position: relative; height: 10px; border-radius: 5px; background: var(--line, #e4e2dc); overflow: hidden; margin: 6px 0; }
.bar span { position: absolute; left: 0; top: 0; bottom: 0; }
.bar .today { background: var(--kept); }
.bar .now { background: var(--bad); opacity: 0.8; }
.bar .now.up { background: var(--good); }
p { margin: 4px 0; }
.note { font-size: 10.5px; }
</style>
