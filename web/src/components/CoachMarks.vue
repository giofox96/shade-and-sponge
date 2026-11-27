<script setup>
// The tour's ring and balloon (state and steps in coach.js)
import { computed, watch, nextTick, onBeforeUnmount } from 'vue'
import { coach, next, stop, place } from '../coach.js'

const onResize = () => coach.name && place()
window.addEventListener('resize', onResize)
onBeforeUnmount(() => window.removeEventListener('resize', onResize))
watch(() => coach.i, () => nextTick(place))

const ring = computed(() => {
  const r = coach.rect
  return r && { left: `${r.left - 6}px`, top: `${r.top - 6}px`, width: `${r.width + 12}px`, height: `${r.height + 12}px` }
})
// the balloon goes on the side of the element with more room
const balloon = computed(() => {
  const r = coach.rect
  if (!r) return { left: '50%', top: '40%', transform: 'translate(-50%, -50%)' }
  const right = r.right + 300 < window.innerWidth
  const top = Math.min(Math.max(12, r.top), window.innerHeight - 170)
  return right ? { left: `${r.right + 18}px`, top: `${top}px` } : { left: `${Math.max(12, r.left - 300)}px`, top: `${Math.max(12, r.top - 150)}px` }
})
</script>

<template>
  <Teleport to="body">
    <div v-if="coach.name" class="coach" role="dialog" aria-live="polite" :aria-label="`Tip ${coach.i + 1} of ${coach.steps.length}`">
      <div v-if="ring" class="ring" :style="ring"></div>
      <div class="balloon" :style="balloon">
        <p>{{ coach.steps[coach.i]?.text }}</p>
        <div class="row">
          <span class="muted">{{ coach.i + 1 }} / {{ coach.steps.length }}</span>
          <button class="ghost" @click="stop">Skip</button>
          <button class="primary" @click="next">{{ coach.i + 1 < coach.steps.length ? 'Next tip' : 'Got it' }}</button>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<style scoped>
.coach { position: fixed; inset: 0; z-index: 50; pointer-events: none; }
.ring { position: fixed; border-radius: 14px; border: 3px solid var(--good); box-shadow: 0 0 0 9999px rgba(42, 38, 34, 0.28);
  animation: pulse 1.4s ease-in-out infinite; transition: all 0.35s cubic-bezier(.2, .8, .2, 1); }
.balloon { position: fixed; width: 280px; background: var(--panel); color: var(--text); border-radius: 16px; padding: 14px 16px;
  box-shadow: 0 12px 30px rgba(42, 38, 34, 0.25); pointer-events: auto; animation: rise 0.35s ease both; transition: all 0.35s cubic-bezier(.2, .8, .2, 1); }
.balloon p { font-size: 16px; line-height: 1.4; margin: 0 0 10px; }
.row { display: flex; gap: 8px; align-items: center; } .row .muted { margin-right: auto; font-size: 12px; }
.primary { background: var(--accent); color: var(--bg); border-color: var(--accent); font-weight: 600; border-radius: 999px; padding: 6px 14px; }
.ghost { background: transparent; border-radius: 999px; }
@keyframes pulse { 50% { border-color: color-mix(in srgb, var(--good) 40%, transparent); } }
@keyframes rise { from { transform: translateY(8px); opacity: 0; } to { transform: none; opacity: 1; } }
@media (prefers-reduced-motion: reduce) { .ring, .balloon { animation: none; transition: none; } }
</style>
