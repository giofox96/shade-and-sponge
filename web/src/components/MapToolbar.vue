<script setup>
// Icon column on the right edge of the map: one button per map layer, grouped in pills. A dot marks a layer that is on;
// the tooltip gives name, state and action. "More" opens the month (leaf calendar) and building-opacity tools.
import { ref } from 'vue'
import { state, MONTHS, setGround3d, setLidar, setParks, setUtilities } from '../store.js'
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
      <button v-if="state.meta.terrain" class="tb" :aria-pressed="state.ground3d" aria-label="3D ground" @click="setGround3d(!state.ground3d)">
        <Icon name="terrain" /><i v-if="state.ground3d" class="dot"></i>
        <span class="tt"><b>3D ground</b>{{ state.ground3d ? 'Relief on · click for the flat map' : 'Flat map · click for the relief' }}
          <em>The ground model from the LiDAR flight (ICGC), true scale: the same one that routes the storm water. Trees and buildings sit on it.</em></span>
      </button>
      <button class="tb" :aria-pressed="state.basemap === 'satellite'" aria-label="Aerial photo"
              @click="state.basemap = state.basemap === 'satellite' ? 'map' : 'satellite'">
        <Icon name="satellite" /><i v-if="state.basemap === 'satellite'" class="dot"></i>
        <span class="tt"><b>Aerial photo</b>{{ state.basemap === 'satellite' ? 'On · click for the street map' : 'Street map · click for the aerial photo' }}
          <em>Orthophoto of Catalonia, ICGC.</em></span>
      </button>
      <button v-if="state.meta.lidar" class="tb" :aria-pressed="state.showLidar" aria-label="LiDAR points" @click="setLidar(!state.showLidar)">
        <Icon name="points" /><i v-if="state.showLidar" class="dot"></i>
        <span class="tt"><b>LiDAR points</b>{{ state.showLidar ? 'Visible on map · click to hide' : 'Hidden · click to show' }}
          <em>The laser scan behind the crowns, building heights and ground (ICGC, flown 26 Sept 2021), thinned to one point per {{ state.meta.lidar.voxel_m }} m cube: {{ state.meta.lidar.n.toLocaleString('en') }} points. Brown = ground, green = vegetation, red = buildings, grey = unclassified.</em></span>
      </button>
    </div>
    <div class="pill">
      <button class="tb" :aria-pressed="state.showStreets" aria-label="Sidewalk lines" @click="state.showStreets = !state.showStreets">
        <Icon name="sidewalk" /><i v-if="state.showStreets" class="dot"></i>
        <span class="tt"><b>Sidewalk lines</b>{{ hint(state.showStreets) }}
          <em>Grey = façade, dark = kerb, both from the city's 1:1000 map; a tree's sidewalk width is measured along a line through it: 1,545 of Porta's 2,825 street trees. Squares at the trunks = the minimum tree pit of the 2011 guide (1 × 1 or 1.2 × 1.2 m), not a measured pit.</em></span>
      </button>
      <button class="tb" :aria-pressed="state.showSpots" aria-label="Free planting spots" @click="state.showSpots = !state.showSpots">
        <Icon name="fill" /><i v-if="state.showSpots" class="dot"></i>
        <span class="tt"><b>Free planting spots</b>{{ hint(state.showSpots) }}
          <em>Green discs = free spots, light to dark = small / medium / large tree; an amber centre = a field check first, orange = a buried service.</em></span>
      </button>
      <button v-if="state.meta.parks" class="tb" :aria-pressed="state.showParks" aria-label="Park trees" @click="setParks(!state.showParks)">
        <Icon name="park" /><i v-if="state.showParks" class="dot"></i>
        <span class="tt"><b>Park trees</b>{{ hint(state.showParks) }}
          <em>{{ state.meta.parks.n.toLocaleString('en') }} trees of parks and squares (city inventories, Open Data BCN), sized from the LiDAR. Context only: the tool does not change or score them; their shade is already in the model as fixed canopy.</em></span>
      </button>
      <button v-if="state.meta.utilities" class="tb" :aria-pressed="state.showUtilities" aria-label="Underground services (synthetic)"
              @click="setUtilities(!state.showUtilities)">
        <Icon name="pipe" /><i v-if="state.showUtilities" class="dot"></i>
        <span class="tt"><b>Underground services · SYNTHETIC</b>{{ hint(state.showUtilities) }}
          <em>A mock layer, not Porta's real services (those plans cannot be published). Built from published layout rules: house
            connections cross the sidewalk from each building, water, gas and electricity run along it. Blue = water, yellow = gas,
            red = electricity, purple = house connections. {{ state.meta.utilities.free_spots_flagged }} free spots would sit on a line
            and count as conditional.</em></span>
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
.toolbar { position: absolute; top: 136px; right: 10px; z-index: 5; display: flex; flex-direction: column; gap: 8px; } /* below the zoom control */
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
