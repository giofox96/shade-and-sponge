<script setup>
// Icon column on the right edge of the map: one button per map layer, grouped in pills. A dot marks a layer that is on;
// the tooltip gives name, state and action. "More" opens the month (leaf calendar) and building-opacity tools.
import { ref } from 'vue'
import { state, MONTHS } from '../store.js'
import Icon from './Icon.vue'

const more = ref(false)
let lastOpacity = 1 // building opacity to restore when the layer is switched back on
function toggleBuildings() {
  if (state.buildingOpacity > 0) { lastOpacity = state.buildingOpacity; state.buildingOpacity = 0 } else state.buildingOpacity = lastOpacity
}
const OVERLAY_ICON = { sun_summer: 'sun', sun_winter: 'sunlow', water: 'drop', hotspots: 'alert' }
const hint = (on) => (on ? 'Visible on map · click to hide' : 'Hidden · click to show')
</script>

<template>
  <div class="toolbar" role="toolbar" aria-label="Map layers" aria-orientation="vertical">
    <div class="pill">
      <button class="tb" :aria-pressed="state.showStreets" aria-label="Sidewalks and free spots" @click="state.showStreets = !state.showStreets">
        <Icon name="sidewalk" /><i v-if="state.showStreets" class="dot"></i>
        <span class="tt"><b>Sidewalks and free spots</b>{{ hint(state.showStreets) }}
          <em>Brown = façade, dark = kerb. Green dots = free spots, light to dark = small / medium / large tree.</em></span>
      </button>
      <button class="tb" :aria-pressed="state.buildingOpacity > 0" aria-label="Buildings" @click="toggleBuildings">
        <Icon name="building" /><i v-if="state.buildingOpacity > 0" class="dot"></i>
        <span class="tt"><b>Buildings</b>{{ state.buildingOpacity > 0 ? `${Math.round(state.buildingOpacity * 100)}% opaque · click to hide` : 'Hidden · click to show' }}</span>
      </button>
    </div>
    <div class="pill">
      <button v-for="o in state.meta.overlays" :key="o.id" class="tb" :aria-pressed="state.overlay === o.id" :aria-label="o.label"
              @click="state.overlay = state.overlay === o.id ? '' : o.id">
        <Icon :name="OVERLAY_ICON[o.id] || 'layers'" /><i v-if="state.overlay === o.id" class="dot"></i>
        <span class="tt"><b>{{ o.label }}</b>{{ hint(state.overlay === o.id) }}<em>One overlay at a time.</em></span>
      </button>
    </div>
    <div class="pill">
      <button class="tb" :class="{ open: more }" :aria-expanded="more" aria-label="More map tools" @click="more = !more">
        <Icon name="more" />
        <span v-if="!more" class="tt"><b>More map tools</b>Month and building opacity</span>
      </button>
      <div v-if="more" class="row">
        <div class="tool">
          <span class="lbl">Month <span class="muted">{{ MONTHS[state.month - 1] }} · crowns follow each species' leaf calendar</span></span>
          <span class="months" role="group" aria-label="Month">
            <button v-for="(m, i) in MONTHS" :key="m" :class="{ on: state.month === i + 1 }" :aria-pressed="state.month === i + 1"
                    :aria-label="m" :title="m" @click="state.month = i + 1">{{ m[0] }}</button>
          </span>
        </div>
        <div class="tool">
          <span class="lbl">Buildings <span class="muted">{{ Math.round(state.buildingOpacity * 100) }}% opaque</span></span>
          <input type="range" min="0" max="1" step="0.05" v-model.number="state.buildingOpacity" aria-label="Building opacity" />
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.toolbar { position: absolute; top: 118px; right: 10px; z-index: 5; display: flex; flex-direction: column; gap: 8px; } /* below the zoom control */
.pill { position: relative; display: flex; flex-direction: column; gap: 2px; padding: 3px; border-radius: 10px; background: var(--panel);
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.18); }
.tb { position: relative; width: 36px; height: 36px; padding: 0; display: grid; place-items: center; border: 0; border-radius: 8px;
  background: transparent; color: var(--muted); }
.tb:hover, .tb.open { background: var(--hover); color: var(--text); }
.tb[aria-pressed='true'] { color: var(--text); }
.dot { position: absolute; right: 5px; bottom: 5px; width: 6px; height: 6px; border-radius: 50%; background: var(--accent); }
.tt { display: none; position: absolute; right: 44px; top: 50%; transform: translateY(-50%); width: max-content; max-width: 230px; padding: 6px 9px;
  border-radius: 8px; background: var(--panel); color: var(--muted); box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2); font-size: 11.5px;
  line-height: 1.35; text-align: left; pointer-events: none; }
.tt b { display: block; color: var(--text); font-weight: 600; }
.tt em { display: block; font-style: normal; margin-top: 3px; }
.tb:hover .tt, .tb:focus-visible .tt { display: block; }
.row { position: absolute; right: 46px; top: 0; display: flex; gap: 14px; padding: 8px 10px; border-radius: 10px; background: var(--panel);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2); white-space: nowrap; }
.tool { display: flex; flex-direction: column; gap: 5px; font-size: 12px; }
.lbl { font-weight: 500; }
.lbl .muted { font-weight: 400; }
.months { display: flex; gap: 1px; }
.months button { width: 20px; height: 22px; padding: 0; border: 0; border-radius: 5px; background: transparent; font-size: 11px; color: var(--muted); }
.months button:hover { background: var(--hover); }
.months button.on { background: var(--accent); color: var(--panel); }
.tool input[type='range'] { width: 150px; }
</style>
