<script setup>
// An "i" that opens a short explanation on click (user tests 27 Nov: long texts hidden until asked for; "?" is the tour).
import { ref } from 'vue'
defineProps({ label: { type: String, default: 'More information' } })
const open = ref(false)
</script>

<template>
  <span class="info">
    <button class="i" :aria-expanded="open" :aria-label="label" @click.stop="open = !open">i</button>
    <Transition name="pop"><span v-if="open" class="box" role="note" @click.stop><slot /></span></Transition>
  </span>
</template>

<style scoped>
.info { position: relative; display: inline-block; vertical-align: middle; margin-left: 6px; }
.i { width: 22px; height: 22px; padding: 0; border-radius: 50%; font: italic 600 13px/1 Georgia, serif; color: var(--accent); border-color: var(--accent); }
.box { position: absolute; left: 0; top: 28px; z-index: 20; width: 280px; background: var(--panel); color: var(--text); border: 0.5px solid var(--line);
  border-radius: 12px; padding: 10px 12px; font-size: 13px; font-weight: 400; line-height: 1.45; letter-spacing: 0; box-shadow: 0 8px 24px rgba(42, 38, 34, 0.18); }
.pop-enter-active, .pop-leave-active { transition: opacity 0.2s, transform 0.2s; }
.pop-enter-from, .pop-leave-to { opacity: 0; transform: translateY(-4px); }
</style>
