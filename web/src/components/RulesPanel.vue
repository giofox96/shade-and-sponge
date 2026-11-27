<script setup>
// Rules on the optimiser: max share per species, diversity floor, species on/off. Used in Expert mode and in the guided
// flow's "Advanced" (step 4); App.vue re-optimises when they change.
import { computed, ref } from 'vue'
import { state, layoutEff, habitOf } from '../store.js'

// species as cards (user 27 Nov): a dot (crown size) or an elevation (trunk, crown base, crown) at one scale for all
const look = ref('dots')
const species = computed(() => state.meta.palette.filter((p) => p.in_palette))
const maxCrown = computed(() => Math.max(...species.value.map((p) => p.crown_diam_m)))
const k = computed(() => 54 / Math.max(...species.value.map((p) => Math.max(p.height_m, p.crown_diam_m)))) // drawing units per metre
const HABIT = { deciduous: 'Deciduous, bare in winter', evergreen: 'Evergreen, green all year', 'semi-deciduous': 'Semi-deciduous' }
const toggle = (sp) => (state.exclude = state.exclude.includes(sp) ? state.exclude.filter((x) => x !== sp) : [...state.exclude, sp])

// diversity-floor benchmarks (notes/cobenefits_plan.md): the city's 2026 mix in Porta, and Santamour's 10% species cap
const DIV_PRESETS = [[9.4, 'City announced mix 9.4', "Effective species of the city's announced 2026 mix on Porta's plane positions"],
  [10, 'Santamour 10', 'No species above 10% (Santamour 1990) means at least 10 effective species']]
</script>

<template>
    <section>
      <h3>Max share per species <span class="muted">{{ Math.round(state.share * 100) }}%</span></h3>
      <input type="range" min="0.05" max="0.3" step="0.01" v-model.number="state.share" aria-label="Maximum share per species" />
      <p class="small muted">Of all {{ state.pot.n_total.toLocaleString('en') }} street trees; the city tree plan sets 15%.</p>
    </section>
    <section>
      <h3>Diversity floor <span class="muted">{{ state.minEff ? `≥ ${state.minEff.toFixed(1)} effective species` : 'off' }}</span></h3>
      <label class="check"><input type="checkbox" :checked="state.minEff > 0"
             @change="state.minEff = $event.target.checked ? Math.min(8, state.pot.species.length - state.exclude.length - 1) : 0" />
        Keep a minimum Shannon diversity</label>
      <input v-if="state.minEff" type="range" min="2" :max="state.pot.species.length - state.exclude.length" step="0.1" v-model.number="state.minEff"
             aria-label="Minimum effective number of species" />
      <!-- benchmarks (notes/cobenefits_plan.md): the city's 2026 mix in Porta = 9.4; Santamour's 10% species cap implies >= 10 -->
      <div class="btns">
        <button v-for="[v, name, why] in DIV_PRESETS"
                :key="v" :class="{ on: state.minEff === v }" :disabled="v > state.pot.species.length - state.exclude.length"
                :title="v > state.pot.species.length - state.exclude.length ? 'Needs more species than this palette allows: use the Barcelona palette' : why"
                @click="state.minEff = v">{{ name }}</button>
      </div>
      <p class="small muted">exp(Shannon H) of the replanted positions. This layout: {{ layoutEff?.toFixed(1) }}.</p>
    </section>
    <section>
      <h3>Species <span class="muted">click a card to leave a species out</span></h3>
      <span class="seg view" role="group" aria-label="How the species look">
        <button v-for="[v, l] in [['dots', 'Dots'], ['elev', 'Elevations']]" :key="v" :class="{ on: look === v }" :aria-pressed="look === v" @click="look = v">{{ l }}</button>
      </span>
      <ul class="cards">
        <li v-for="p in species" :key="p.species">
          <button class="card" :class="{ off: state.exclude.includes(p.species) }" :aria-pressed="!state.exclude.includes(p.species)"
                  :title="state.exclude.includes(p.species) ? 'Left out: click to allow it' : 'Allowed: click to leave it out'" @click="toggle(p.species)">
            <svg viewBox="0 0 60 60" class="pic" aria-hidden="true">
              <template v-if="look === 'dots'"><circle cx="30" cy="30" :r="4 + 22 * p.crown_diam_m / maxCrown" :fill="p.color" /></template>
              <template v-else>
                <line x1="2" y1="57" x2="58" y2="57" class="ground" />
                <rect :x="29" :y="57 - k * p.crown_base_m" width="2" :height="k * p.crown_base_m" class="trunk" />
                <ellipse cx="30" :cy="57 - k * (p.crown_base_m + p.height_m) / 2" :rx="(k * p.crown_diam_m) / 2"
                         :ry="Math.max(2, (k * (p.height_m - p.crown_base_m)) / 2)" :fill="p.color" />
              </template>
            </svg>
            <span class="tick" aria-hidden="true">{{ state.exclude.includes(p.species) ? '' : '✓' }}</span>
            <i class="nm">{{ p.species }}</i>
            <small>{{ HABIT[habitOf(p.species)] ?? 'Leaf habit not found' }}</small>
            <small class="muted">crown {{ p.crown_diam_m.toFixed(1) }} m, height {{ p.height_m.toFixed(1) }} m</small>
          </button>
        </li>
      </ul>
    </section>
</template>

<style scoped>
.view { margin: 4px 0 8px; display: inline-flex; }
.cards { list-style: none; padding: 0; margin: 0; display: grid; grid-template-columns: repeat(auto-fill, minmax(128px, 1fr)); gap: 8px; }
.card { position: relative; width: 100%; height: 100%; display: flex; flex-direction: column; align-items: flex-start; gap: 2px; text-align: left;
  padding: 8px 10px; border-radius: 12px; border: 1.5px solid var(--good); background: color-mix(in srgb, var(--good) 8%, var(--bg)); transition: opacity 0.2s, border-color 0.2s; }
.card.off { border: 1.5px dashed var(--line); background: transparent; opacity: 0.55; }
.card.off .pic { filter: grayscale(1); }
.pic { width: 52px; height: 52px; }
.ground { stroke: var(--line); stroke-width: 1; } .trunk { fill: #7a5a3a; }
.tick { position: absolute; top: 6px; right: 8px; width: 18px; height: 18px; border-radius: 50%; background: var(--good); color: #fff;
  font-size: 11px; display: grid; place-items: center; }
.card.off .tick { background: transparent; border: 1px dashed var(--muted); }
.nm { font-size: 13px; line-height: 1.2; }
.card small { font-size: 11px; line-height: 1.25; }
</style>
