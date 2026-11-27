<script setup>
// Rules on the optimiser: max share per species, diversity floor, species on/off. Used in Expert mode and in the guided
// flow's "Advanced" (step 4); App.vue re-optimises when they change.
import { state, layoutEff } from '../store.js'

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
      <h3>Species <span class="muted">untick to exclude</span></h3>
      <p v-if="state.meta.palette_kind === 'barcelona'" class="small muted">Colour = leaf habit (ochre deciduous, green evergreen, olive semi-deciduous); darker = larger crown.</p>
      <ul class="legend">
        <li v-for="p in state.meta.palette" :key="p.species">
          <input v-if="p.in_palette" type="checkbox" :value="p.species" :checked="!state.exclude.includes(p.species)"
                 :aria-label="`Allow ${p.species}`"
                 @change="state.exclude = $event.target.checked ? state.exclude.filter((x) => x !== p.species) : [...state.exclude, p.species]" />
          <span class="dot" :style="{ background: p.color }"></span>{{ p.species }}
          <span class="muted">{{ p.in_palette ? p.leaf_habit.split(' ')[0] : 'current' }}</span>
        </li>
      </ul>
    </section>
</template>
