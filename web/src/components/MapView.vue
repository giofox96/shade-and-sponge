<script setup>
// 3D map: MapLibre basemap + deck.gl layers (overlay raster, extruded buildings, tree crowns as ellipsoids).
// The map is flat: crown and building heights are metres above local ground.
import { onMounted, onBeforeUnmount, ref, watch } from 'vue'
import { Map as MapLibreMap, NavigationControl, setWorkerUrl } from 'maplibre-gl'
import workerUrl from 'maplibre-gl/dist/maplibre-gl-worker.mjs?url' // v6 looks for the worker next to its module; Vite moves it
import 'maplibre-gl/dist/maplibre-gl.css'
import { MapboxOverlay } from '@deck.gl/mapbox'
import { BitmapLayer, GeoJsonLayer } from '@deck.gl/layers'
import { SimpleMeshLayer } from '@deck.gl/mesh-layers'
import { SphereGeometry } from '@luma.gl/engine'
import { state, dataUrl, hexToRgb, currentLayout } from '../store.js'

setWorkerUrl(workerUrl)
const el = ref(null)
let map, overlay
const sphere = new SphereGeometry({ nlat: 10, nlong: 16, radius: 1 })

function crowns() {
  const { trees, meta, scenarioId, month, selected } = state
  const p = trees.positions
  const lay = currentLayout()
  const isS0 = scenarioId === 'S0_current'
  const pal = meta.palette
  const ids = [...p.lon.keys()]
  const dims = (i) => {
    if (isS0) return [p.s0_crown_diam_m[i], p.s0_height_m[i], p.s0_crown_base_m[i]]
    const s = pal[lay[i]]
    return [s.crown_diam_m, s.height_m, s.crown_base_m]
  }
  const k = state.trees.kept
  return [
    new SimpleMeshLayer({
      id: 'kept',
      data: [...k.lon.keys()],
      mesh: sphere,
      getPosition: (i) => [k.lon[i], k.lat[i], (k.height_m[i] + k.crown_base_m[i]) / 2],
      getScale: (i) => [k.crown_diam_m[i] / 2, k.crown_diam_m[i] / 2, Math.max(k.height_m[i] - k.crown_base_m[i], 1) / 2],
      getColor: [150, 160, 140, 150],
    }),
    new SimpleMeshLayer({
      id: 'positions',
      data: ids,
      mesh: sphere,
      pickable: true,
      getPosition: (i) => {
        const [, h, b] = dims(i)
        return [p.lon[i], p.lat[i], (h + b) / 2]
      },
      getScale: (i) => {
        const [d, h, b] = dims(i)
        return [d / 2, d / 2, Math.max(h - b, 1) / 2]
      },
      getColor: (i) => {
        const s = pal[lay[i]]
        const leaf = s.leaf[month - 1]
        return [...hexToRgb(s.color), i === selected ? 255 : Math.round(60 + 170 * leaf)]
      },
      onClick: ({ index }) => (state.selected = index),
      updateTriggers: {
        getPosition: [scenarioId, state.live?.version],
        getScale: [scenarioId, state.live?.version],
        getColor: [scenarioId, state.live?.version, month, selected],
      },
    }),
  ]
}

function layers() {
  if (!state.meta) return []
  const ov = state.meta.overlays.find((o) => o.id === state.overlay)
  const c = state.meta.site.corners
  return [
    ov &&
      new BitmapLayer({ id: 'overlay-' + ov.id, image: dataUrl(ov.file), bounds: c, opacity: 0.55 }),
    new GeoJsonLayer({
      id: 'buildings',
      data: dataUrl('buildings.geojson'),
      extruded: true,
      getElevation: (f) => f.properties.height_m,
      getFillColor: [222, 218, 208, 235],
      getLineColor: [180, 176, 166],
      lineWidthMinPixels: 0,
    }),
    ...crowns(),
  ].filter(Boolean)
}

onMounted(() => {
  map = new MapLibreMap({
    container: el.value,
    style: 'https://tiles.openfreemap.org/styles/positron',
    center: state.meta.site.center,
    zoom: 15.4,
    pitch: 50,
    bearing: -35,
    attributionControl: { compact: true },
  })
  map.addControl(new NavigationControl({ visualizePitch: true }), 'top-right')
  overlay = new MapboxOverlay({
    interleaved: false,
    layers: layers(),
    getTooltip: ({ layer, index }) => {
      if (layer?.id !== 'positions' || index < 0) return null
      return { text: state.meta.palette[currentLayout()[index]].species }
    },
  })
  map.addControl(overlay)
  map.on('load', () => overlay.setProps({ layers: layers() })) // redraw once the style and images are in
})

watch(
  () => [state.scenarioId, state.live?.version, state.overlay, state.month, state.selected],
  () => overlay?.setProps({ layers: layers() }),
)

onBeforeUnmount(() => map?.remove())
</script>

<template>
  <div ref="el" class="map"></div>
</template>

<style scoped>
.map {
  position: absolute;
  inset: 0;
}
</style>
