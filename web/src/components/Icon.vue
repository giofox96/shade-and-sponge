<script setup>
// Small line icons for the sidebar buttons (24 × 24, currentColor): swap = replace all trees, add = add trees,
// fill = fill the free spots, edit = edit the project area
defineProps({ name: { type: String, required: true } })
</script>

<template>
  <svg class="icon" viewBox="0 0 24 24" width="18" height="18" aria-hidden="true" fill="none" stroke="currentColor"
       stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">
    <template v-if="name === 'swap'">
      <ellipse cx="7" cy="8" rx="5" ry="4.5" fill="currentColor" fill-opacity="0.25" />
      <path d="M7 12.5V21" />
      <ellipse cx="18.5" cy="14.5" rx="3.3" ry="2.8" fill="currentColor" fill-opacity="0.25" />
      <path d="M18.5 17.3V21" />
      <path d="M12.5 3.5c3 -0.3 5.5 1.5 6 5" /><path d="M16.5 7.5l2 1.5 1.3 -2.2" />
      <path d="M15 21.5c-2.5 0.4 -4.5 -0.5 -5.3 -2.5" /><path d="M11.8 18.6l-2.1 0.4 -0.3 2.3" />
    </template>
    <template v-else-if="name === 'add'">
      <path d="M2 12h8M6 8v8" />
      <ellipse cx="16.5" cy="9" rx="5.5" ry="5" fill="currentColor" fill-opacity="0.25" />
      <path d="M16.5 14V21" />
    </template>
    <template v-else-if="name === 'edit'">
      <path d="M4 18L7 5l12 3 1 9z" stroke-dasharray="2.5 2" />
      <rect v-for="[x, y] in [[4, 18], [7, 5], [19, 8], [20, 17]]" :key="x" :x="x - 1.8" :y="y - 1.8" width="3.6" height="3.6"
            fill="currentColor" stroke="none" />
    </template>
    <template v-else-if="name === 'fill'">
      <rect x="2" y="3" width="20" height="18" rx="2" stroke-dasharray="2.5 2" />
      <circle v-for="x in [7, 12, 17]" :key="x" :cx="x" cy="10" r="2.6" fill="currentColor" fill-opacity="0.25" />
      <path d="M7 12.6V17M12 12.6V17M17 12.6V17" />
    </template>
  </svg>
</template>

<style scoped>
.icon { flex: none; vertical-align: middle; }
</style>
