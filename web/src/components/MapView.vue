<script setup>
// 3D map: MapLibre basemap + deck.gl layers (overlay raster, extruded buildings, tree crowns as ellipsoids).
// The map is flat: crown and building heights are metres above local ground.
import { onMounted, onBeforeUnmount, ref, watch } from 'vue'
import { Map as MapLibreMap, NavigationControl, setWorkerUrl } from 'maplibre-gl'
import workerUrl from 'maplibre-gl/dist/maplibre-gl-worker.mjs?url' // v6 looks for the worker next to its module; Vite moves it
import 'maplibre-gl/dist/maplibre-gl.css'
import { MapboxOverlay } from '@deck.gl/mapbox'
import { BitmapLayer, GeoJsonLayer, PathLayer, PolygonLayer, ScatterplotLayer } from '@deck.gl/layers'
import { SimpleMeshLayer } from '@deck.gl/mesh-layers'
import { SphereGeometry } from '@luma.gl/engine'
import { state, dataUrl, hexToRgb, currentLayout, addTreeAt, addVertex, keptReplaced, themeColors, isDark, AREA } from '../store.js'

setWorkerUrl(workerUrl)
const el = ref(null)
let map, overlay, ro
const sphere = new SphereGeometry({ nlat: 10, nlong: 16, radius: 1 })

function crowns() {
  const { trees, meta, scenarioId, month, selected } = state
  const p = trees.positions
  const lay = currentLayout()
  const pal = meta.palette
  const ids = [...p.lon.keys()]
  const dims = (i) => {
    // today's tree (S0, or outside a project area): its measured crown
    if (!pal[lay[i]].in_palette) return [p.s0_crown_diam_m[i], p.s0_height_m[i], p.s0_crown_base_m[i]]
    const s = pal[lay[i]]
    return [s.crown_diam_m, s.height_m, s.crown_base_m]
  }
  const add = [...state.added] // a new array: deck.gl only notices data changes by reference
  const aDims = (t) => {
    const s = pal[t.species]
    return [s.crown_diam_m, s.height_m, s.crown_base_m]
  }
  const k = state.trees.kept
  const repl = scenarioId === AREA ? keptReplaced() : new Map()
  return [
    new SimpleMeshLayer({
      id: 'kept-new',
      data: [...repl.keys()],
      mesh: sphere,
      getPosition: (i) => { const s = pal[repl.get(i)]; return [k.lon[i], k.lat[i], (s.height_m + s.crown_base_m) / 2] },
      getScale: (i) => { const s = pal[repl.get(i)]; return [s.crown_diam_m / 2, s.crown_diam_m / 2, Math.max(s.height_m - s.crown_base_m, 1) / 2] },
      getColor: (i) => { const s = pal[repl.get(i)]; return [...hexToRgb(s.color), Math.round(60 + 170 * s.leaf[month - 1])] },
      updateTriggers: { getPosition: state.area?.version, getScale: state.area?.version, getColor: [state.area?.version, month] },
    }),
    new SimpleMeshLayer({
      id: 'kept',
      data: [...k.lon.keys()].filter((i) => !repl.has(i)),
      mesh: sphere,
      getPosition: (i) => [k.lon[i], k.lat[i], (k.height_m[i] + k.crown_base_m[i]) / 2],
      getScale: (i) => [k.crown_diam_m[i] / 2, k.crown_diam_m[i] / 2, Math.max(k.height_m[i] - k.crown_base_m[i], 1) / 2],
      getColor: themeColors.value.kept,
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
      onClick: ({ index, coordinate }) => (state.drawing ? addVertex(...coordinate) : (state.selected = index)),
      updateTriggers: {
        getPosition: [scenarioId, state.live?.version, state.area?.version],
        getScale: [scenarioId, state.live?.version, state.area?.version],
        getColor: [scenarioId, state.live?.version, state.area?.version, month, selected],
      },
    }),
    new ScatterplotLayer({
      id: 'added-rings',
      data: add,
      getPosition: (t) => [t.lon, t.lat, 0.3],
      getRadius: (t) => aDims(t)[0] / 2 + 0.8,
      radiusUnits: 'meters',
      stroked: true,
      filled: false,
      getLineColor: (t, { index }) => (selected === `a${index}` ? themeColors.value.ringOn : themeColors.value.ring),
      lineWidthMinPixels: 2,
      updateTriggers: { getRadius: state.addedVersion, getLineColor: [selected, state.addedVersion] },
    }),
    new SimpleMeshLayer({
      id: 'added',
      data: add,
      mesh: sphere,
      pickable: true,
      getPosition: (t) => [t.lon, t.lat, (aDims(t)[1] + aDims(t)[2]) / 2],
      getScale: (t) => [aDims(t)[0] / 2, aDims(t)[0] / 2, Math.max(aDims(t)[1] - aDims(t)[2], 1) / 2],
      getColor: (t) => [...hexToRgb(pal[t.species].color), Math.round(60 + 170 * pal[t.species].leaf[month - 1])],
      onClick: ({ index, coordinate }) => (state.drawing ? addVertex(...coordinate) : (state.selected = `a${index}`)),
      updateTriggers: { getPosition: state.addedVersion, getScale: state.addedVersion, getColor: [state.addedVersion, month] },
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
      getFillColor: themeColors.value.building,
      getLineColor: themeColors.value.buildingLine,
      updateTriggers: { getFillColor: isDark.value, getLineColor: isDark.value },
      lineWidthMinPixels: 0,
    }),
    state.showStreets &&
      new GeoJsonLayer({ id: 'sidewalks', data: dataUrl('sidewalks.geojson'), stroked: true, filled: false,
        getLineColor: (f) => (f.properties.kind === 'facade' ? themeColors.value.facade : themeColors.value.kerb),
        updateTriggers: { getLineColor: isDark.value },
        getLineWidth: (f) => (f.properties.kind === 'facade' ? 0.5 : 0.8), lineWidthUnits: 'meters', lineWidthMinPixels: 1.5 }),
    state.showStreets &&
      new ScatterplotLayer({ id: 'spots', data: state.trees.spots.lon.map((lon, i) => i), radiusUnits: 'meters',
        getPosition: (i) => [state.trees.spots.lon[i], state.trees.spots.lat[i], 0.2],
        getRadius: (i) => ({ small: 1.6, medium: 2.2, large: 2.8 })[state.trees.spots.size_class[i]], radiusMinPixels: 3,
        getFillColor: (i) => ({ small: [168, 214, 110], medium: [92, 170, 50], large: [40, 110, 20] })[state.trees.spots.size_class[i]],
        stroked: true, getLineColor: themeColors.value.spotLine, lineWidthMinPixels: 1.5, pickable: true, updateTriggers: { getLineColor: isDark.value },
        onClick: ({ object, coordinate }) => { // a click on a free spot plants there in "Add trees" mode
          if (state.drawing) return addVertex(...coordinate)
          if (state.addMode) addTreeAt(state.trees.spots.lon[object], state.trees.spots.lat[object])
        } }),
    state.area &&
      new PolygonLayer({ id: 'area', data: [state.area.poly], getPolygon: (d) => d, stroked: true, filled: true,
        getFillColor: [...themeColors.value.area, 30], getLineColor: [...themeColors.value.area, 230], lineWidthMinPixels: 2 }),
    state.drawing && state.draft.length > 1 &&
      new PathLayer({ id: 'draft-path', data: [state.draft], getPath: (d) => d, getColor: themeColors.value.draft, widthMinPixels: 2 }),
    state.drawing &&
      new ScatterplotLayer({ id: 'draft-pts', data: [...state.draft], getPosition: (d) => d, getRadius: 4, radiusUnits: 'pixels',
        getFillColor: themeColors.value.draft }),
    ...crowns(),
  ].filter(Boolean)
}

onMounted(() => {
  map = new MapLibreMap({
    container: el.value,
    style: themeColors.value.basemap,
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
    getCursor: ({ isHovering }) => (state.addMode || state.drawing ? 'crosshair' : isHovering ? 'pointer' : 'grab'),
    onClick: (info) => {
      if (state.drawing && info.coordinate) return addVertex(info.coordinate[0], info.coordinate[1])
      if (state.addMode && !info.layer && info.coordinate) addTreeAt(info.coordinate[0], info.coordinate[1])
    },
    getTooltip: ({ layer, index, object }) => {
      if (layer?.id === 'added') return { text: `${state.meta.palette[object.species].species} (added)` }
      if (layer?.id === 'spots') { const S = state.trees.spots; return { text: `Free planting spot · ${S.size_class[object]} tree · sidewalk ${S.width_m[object]} m` } }
      if (layer?.id !== 'positions' || index < 0) return null
      return { text: state.meta.palette[currentLayout()[index]].species }
    },
  })
  map.addControl(overlay)
  map.on('load', () => overlay.setProps({ layers: layers() })) // redraw once the style and images are in
  ro = new ResizeObserver(() => map.resize())
  ro.observe(el.value)
})

watch(
  () => [state.scenarioId, state.live?.version, state.area?.version, state.area, state.drawing, state.draft, state.overlay, state.showStreets, isDark.value,
    state.month, state.selected, state.addedVersion],
  () => overlay?.setProps({ layers: layers() }),
)

// theme switch: swap the basemap (the deck.gl layers sit on their own canvas and stay)
watch(isDark, () => map?.setStyle(themeColors.value.basemap))

// a new project area: frame it (keeps the current pitch and bearing)
watch(() => state.area?.poly, (poly) => {
  if (!poly || !map) return
  const lons = poly.map((p) => p[0]), lats = poly.map((p) => p[1])
  map.fitBounds([[Math.min(...lons), Math.min(...lats)], [Math.max(...lons), Math.max(...lats)]],
    { padding: 60, pitch: map.getPitch(), bearing: map.getBearing(), duration: 800, maxZoom: 18.5 })
})

// while drawing a project area, double clicks place corners instead of zooming
watch(() => state.drawing, (on) => (on ? map?.doubleClickZoom.disable() : map?.doubleClickZoom.enable()))

onBeforeUnmount(() => {
  ro?.disconnect()
  map?.remove()
})
</script>

<template>
  <div ref="el" class="map" :class="{ crosshair: state.addMode || state.drawing }"></div>
</template>

<style scoped>
.map {
  position: absolute;
  inset: 0;
}
/* MapLibre sets its own grab cursor on the canvas; while drawing an area or adding trees, show a crosshair instead */
.map.crosshair :deep(.maplibregl-canvas-container.maplibregl-interactive),
.map.crosshair :deep(canvas) {
  cursor: crosshair !important;
}
</style>
