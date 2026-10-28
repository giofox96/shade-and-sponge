<script setup>
// Drag handle on the inner edge of a side panel: drag (or arrow keys) to resize, the button to collapse / reopen.
import { panels, MIN_W, MAX_W } from '../store.js'

const props = defineProps({ side: { type: String, required: true } }) // 'left' | 'right'
const key = props.side === 'left' ? 'leftW' : 'rightW'
const open = props.side === 'left' ? 'leftOpen' : 'rightOpen'
const clamp = (w) => Math.max(MIN_W, Math.min(MAX_W, Math.round(w)))

function drag(e) {
  if (!panels[open] || e.button !== 0) return
  const x0 = e.clientX, w0 = panels[key], sign = props.side === 'left' ? 1 : -1
  const move = (ev) => (panels[key] = clamp(w0 + sign * (ev.clientX - x0)))
  const up = () => {
    window.removeEventListener('pointermove', move)
    window.removeEventListener('pointerup', up)
    document.body.classList.remove('resizing')
  }
  document.body.classList.add('resizing')
  window.addEventListener('pointermove', move)
  window.addEventListener('pointerup', up)
}
function key_(e) {
  const step = e.shiftKey ? 50 : 10, sign = props.side === 'left' ? 1 : -1
  if (e.key === 'ArrowRight') panels[key] = clamp(panels[key] + sign * step)
  else if (e.key === 'ArrowLeft') panels[key] = clamp(panels[key] - sign * step)
  else return
  e.preventDefault()
}
</script>

<template>
  <div class="handle" :class="side">
    <div v-if="panels[open]" class="grip" role="separator" tabindex="0" aria-orientation="vertical"
         :aria-label="`Resize the ${side} panel (arrow keys)`" :aria-valuenow="panels[key]" :aria-valuemin="MIN_W" :aria-valuemax="MAX_W"
         @pointerdown.prevent="drag" @keydown="key_"></div>
    <button class="fold" :aria-label="`${panels[open] ? 'Hide' : 'Show'} the ${side} panel`" :title="`${panels[open] ? 'Hide' : 'Show'} the ${side} panel`"
            @click="panels[open] = !panels[open]">{{ (side === 'left') === panels[open] ? '‹' : '›' }}</button>
  </div>
</template>

<style scoped>
.handle { position: absolute; top: 0; bottom: 0; width: 0; z-index: 6; }
.handle.left { left: 0; }
.handle.right { right: 0; }
.grip { position: absolute; top: 0; bottom: 0; width: 8px; cursor: col-resize; }
.left .grip { left: -4px; }
.right .grip { right: -4px; }
.grip:hover, .grip:focus-visible { background: color-mix(in srgb, var(--accent) 30%, transparent); outline: none; }
.fold { position: absolute; top: 50%; transform: translateY(-50%); width: 18px; height: 44px; padding: 0; font-size: 14px; line-height: 1;
  border-radius: 0 6px 6px 0; background: var(--panel); box-shadow: 0 1px 3px rgba(0, 0, 0, 0.15); }
.left .fold { left: 0; }
.right .fold { right: 0; border-radius: 6px 0 0 6px; }
</style>
