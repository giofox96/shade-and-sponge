<script setup>
// Small line icons for the sidebar buttons (24 × 24, currentColor): swap = replace all trees, add = add trees,
// fill = fill the free spots, edit = edit the project area; map toolbar: sidewalk, building, sun, sunlow (winter sun), drop, alert,
// layers, more
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
    <template v-else-if="name === 'sidewalk'">
      <path d="M3 20L9 4M21 20L15 4" /><path d="M12 5v2M12 11v2M12 17v2" />
    </template>
    <template v-else-if="name === 'building'">
      <rect x="5" y="3" width="14" height="18" rx="1.5" /><path d="M9 7h1M14 7h1M9 11h1M14 11h1M9 15h1M14 15h1M11 21v-3h2v3" />
    </template>
    <template v-else-if="name === 'sun'">
      <circle cx="12" cy="12" r="4" /><path d="M12 2v2M12 20v2M2 12h2M20 12h2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4" />
    </template>
    <template v-else-if="name === 'sunlow'">
      <path d="M7 17a5 5 0 0 1 10 0" /><path d="M2 17h20M12 6v2M4.9 9.9l1.4 1.4M19.1 9.9l-1.4 1.4M6 21h12" />
    </template>
    <template v-else-if="name === 'drop'">
      <path d="M12 3c3.5 4.2 6 7.3 6 10.5a6 6 0 0 1-12 0C6 10.3 8.5 7.2 12 3z" />
    </template>
    <template v-else-if="name === 'alert'">
      <path d="M12 3.5L21.5 20h-19z" /><path d="M12 10v4.5M12 17.2v.3" />
    </template>
    <template v-else-if="name === 'layers'">
      <path d="M12 3l9 5-9 5-9-5z" /><path d="M3 12.5l9 5 9-5M3 17l9 5 9-5" />
    </template>
    <template v-else-if="name === 'more'">
      <circle v-for="x in [5, 12, 19]" :key="x" :cx="x" cy="12" r="1.3" fill="currentColor" />
    </template>
  </svg>
</template>

<style scoped>
.icon { flex: none; vertical-align: middle; }
</style>
