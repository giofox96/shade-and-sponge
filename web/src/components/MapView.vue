<script setup>
// 3D map: MapLibre basemap + deck.gl layers (overlay raster, extruded buildings, tree crowns as ellipsoids).
// The map is flat by default: crown and building heights are metres above local ground. With "3D ground" on, the site DTM
// becomes a relief (TerrainLayer, metres above the site's lowest point): flat layers are draped on it, and trees, spots and
// buildings get the ground height under them (groundZ). The basemap is then drawn on the relief as raster tiles.
import { onMounted, onBeforeUnmount, ref, watch } from 'vue'
import { Map as MapLibreMap, NavigationControl, setWorkerUrl } from 'maplibre-gl'
import workerUrl from 'maplibre-gl/dist/maplibre-gl-worker.mjs?url' // v6 looks for the worker next to its module; Vite moves it
import 'maplibre-gl/dist/maplibre-gl.css'
import { MapboxOverlay } from '@deck.gl/mapbox'
import { COORDINATE_SYSTEM } from '@deck.gl/core'
import { BitmapLayer, GeoJsonLayer, PathLayer, PointCloudLayer, PolygonLayer, ScatterplotLayer } from '@deck.gl/layers'
import { SimpleMeshLayer } from '@deck.gl/mesh-layers'
import { TileLayer } from '@deck.gl/geo-layers'
import { _TerrainExtension as TerrainExtension } from '@deck.gl/extensions'
import { SphereGeometry } from '@luma.gl/engine'
import { state, dataUrl, hexToRgb, currentLayout, addTreeAt, addVertex, keptReplaced, themeColors, isDark, AREA, addableMask, finishArea,
  cancelDrawing, finishEditArea, cancelEditArea, groundZ, setGround3d, setLidar, ORTO } from '../store.js'

setWorkerUrl(workerUrl)
const el = ref(null)
let map, overlay, ro
const sphere = new SphereGeometry({ nlat: 10, nlong: 16, radius: 1 })
const ON_TOP = { depthCompare: 'always', depthWriteEnabled: false }
const mid = (a, b) => [(a[0] + b[0]) / 2, (a[1] + b[1]) / 2]
const DRAPE = [new TerrainExtension()]
const drape = () => (state.ground3d ? { extensions: DRAPE, terrainDrawMode: 'drape' } : {})
const up = (q, dz = 0) => [q[0], q[1], groundZ(q[0], q[1]) + dz] // a lon/lat point lifted onto the ground
// where a click or drag meets the ground: on the relief the flat-map coordinate would be off by height × tan(pitch)
const at = (info) => (state.ground3d && overlay?.pickObject({ x: info.x, y: info.y, unproject3D: true, layerIds: ['terrain'] })?.coordinate) || info.coordinate

// metres east and north of the site centre, as deck.gl places METER_OFFSETS (Web Mercator sphere)
const M_DEG = 40075016.686 / 360
const local = () => ({ coordinateSystem: COORDINATE_SYSTEM.METER_OFFSETS, coordinateOrigin: [...state.meta.site.center, 0] })

// LiDAR points: on the flat map a point sits at its height above ground, on the relief at its true height
const LIDAR_RGB = [[150, 128, 104], [70, 140, 60], [196, 120, 92], [120, 120, 120]] // ground, vegetation, building, other
let cloud = null, cloudOf = null
function lidarData() {
  const L = state.lidar, key = `${L.site}:${state.ground3d}`
  if (cloudOf !== key) {
    const pos = new Float32Array(L.pos), col = new Uint8Array(3 * L.n), h = state.ground3d ? L.z : L.hag
    for (let i = 0; i < L.n; i++) { pos[3 * i + 2] = h[i]; col.set(LIDAR_RGB[L.cls[i]], 3 * i) }
    cloud = { length: L.n, attributes: { getPosition: { value: pos, size: 3 }, getColor: { value: col, size: 3 } } }
    cloudOf = key
  }
  return cloud
}

// 3D ground: the DTM grid as one mesh (a vertex per cell: metres east, north, up), with normals so the slopes are shaded
let relief = null, reliefOf = null
function reliefMesh() {
  const T = state.terrain
  if (reliefOf === T) return relief
  const { w, h, z } = T, [W, S, E, N] = T.bounds, [lon0, lat0] = state.meta.site.center, kx = M_DEG * Math.cos((lat0 * Math.PI) / 180)
  const dx = ((E - W) / w) * kx, dy = ((N - S) / h) * M_DEG // cell size, m
  const pos = new Float32Array(w * h * 3), nor = new Float32Array(w * h * 3), idx = new Uint32Array((w - 1) * (h - 1) * 6)
  for (let j = 0, k = 0; j < h; j++) for (let i = 0; i < w; i++, k++) {
    pos.set([(W + ((i + 0.5) / w) * (E - W) - lon0) * kx, (N - ((j + 0.5) / h) * (N - S) - lat0) * M_DEG, z[k]], 3 * k)
    const gx = (z[k + (i < w - 1)] - z[k - (i > 0)]) / dx, gy = (z[k - (j > 0) * w] - z[k + (j < h - 1) * w]) / dy // twice the slope, east and north
    const l = Math.hypot(gx / 2, gy / 2, 1)
    nor.set([-gx / 2 / l, -gy / 2 / l, 1 / l], 3 * k)
  }
  for (let j = 0, q = 0; j < h - 1; j++) for (let i = 0; i < w - 1; i++, q += 6) {
    const a = j * w + i
    idx.set([a, a + w, a + 1, a + 1, a + w, a + w + 1], q)
  }
  // a skirt down to the flat map around the block, so its raised edges do not float
  const rim = [...Array(w).keys(), ...Array.from({ length: h - 1 }, (_, j) => (j + 1) * w + w - 1),
    ...Array.from({ length: w - 1 }, (_, i) => (h - 1) * w + w - 2 - i), ...Array.from({ length: h - 2 }, (_, j) => (h - 2 - j) * w)]
  const n = w * h, m = rim.length
  const P = new Float32Array((n + m) * 3), Nn = new Float32Array((n + m) * 3), I = new Uint32Array(idx.length + m * 6)
  P.set(pos); Nn.set(nor); I.set(idx)
  rim.forEach((v, r) => {
    P.set([pos[3 * v], pos[3 * v + 1], 0], 3 * (n + r))
    Nn[3 * (n + r) + 2] = 1
    const v2 = rim[(r + 1) % m], b = n + r, b2 = n + ((r + 1) % m)
    I.set([v, b, v2, v2, b, b2], idx.length + 6 * r)
  })
  reliefOf = T
  return (relief = { attributes: { POSITION: { value: P, size: 3 }, NORMAL: { value: Nn, size: 3 } }, indices: { value: I, size: 1 } })
}

// 3D ground: building footprints with their base on the lowest ground under them
let lifted = null, liftedOf = null
function buildings3d() {
  const key = state.site
  if (liftedOf === key) return lifted ?? []
  liftedOf = key
  lifted = null
  fetch(dataUrl('buildings.geojson')).then((r) => r.json()).then((fc) => {
    if (liftedOf !== key) return
    lifted = fc.features.map((f) => {
      const polys = f.geometry.type === 'Polygon' ? [f.geometry.coordinates] : f.geometry.coordinates
      const z = Math.min(...polys.flatMap((P) => (P[0] ?? []).map((q) => groundZ(q[0], q[1]))), 1e9) % 1e9 // no outline: 0
      return { ...f, geometry: { type: 'MultiPolygon', coordinates: polys.map((P) => P.map((R) => R.map((q) => [q[0], q[1], z]))) } }
    })
    overlay?.setProps({ layers: layers() })
  })
  return []
}

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
  const g3 = state.ground3d, gz = groundZ
  return [
    new SimpleMeshLayer({
      id: 'kept-new',
      data: [...repl.keys()],
      mesh: sphere,
      getPosition: (i) => { const s = pal[repl.get(i)]; return [k.lon[i], k.lat[i], gz(k.lon[i], k.lat[i]) + (s.height_m + s.crown_base_m) / 2] },
      getScale: (i) => { const s = pal[repl.get(i)]; return [s.crown_diam_m / 2, s.crown_diam_m / 2, Math.max(s.height_m - s.crown_base_m, 1) / 2] },
      getColor: (i) => { const s = pal[repl.get(i)]; return [...hexToRgb(s.color), Math.round(60 + 170 * s.leaf[month - 1])] },
      updateTriggers: { getPosition: [state.area?.version, g3], getScale: state.area?.version, getColor: [state.area?.version, month] },
    }),
    new SimpleMeshLayer({
      id: 'kept',
      data: [...k.lon.keys()].filter((i) => !repl.has(i)),
      mesh: sphere,
      getPosition: (i) => [k.lon[i], k.lat[i], gz(k.lon[i], k.lat[i]) + (k.height_m[i] + k.crown_base_m[i]) / 2],
      updateTriggers: { getPosition: g3 },
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
        return [p.lon[i], p.lat[i], gz(p.lon[i], p.lat[i]) + (h + b) / 2]
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
      onClick: (info) => (state.drawing ? addVertex(...at(info)) : (state.selected = info.index)),
      updateTriggers: {
        getPosition: [scenarioId, state.live?.version, state.area?.version, g3],
        getScale: [scenarioId, state.live?.version, state.area?.version],
        getColor: [scenarioId, state.live?.version, state.area?.version, month, selected],
      },
    }),
    new ScatterplotLayer({
      id: 'added-rings',
      data: add,
      getPosition: (t) => up([t.lon, t.lat], 0.3),
      getRadius: (t) => aDims(t)[0] / 2 + 0.8,
      radiusUnits: 'meters',
      stroked: true,
      filled: false,
      getLineColor: (t, { index }) => (selected === `a${index}` ? themeColors.value.ringOn : themeColors.value.ring),
      lineWidthMinPixels: 2,
      radiusMinPixels: 7, // young crowns are small: keep the ring findable at any zoom
      parameters: ON_TOP, // an added tree can sit inside an existing crown or behind a building: its ring stays visible
      updateTriggers: { getPosition: g3, getRadius: state.addedVersion, getLineColor: [selected, state.addedVersion] },
    }),
    // a trunk up to the crown, so a small or young added tree is easy to spot next to the bigger crowns
    new PathLayer({
      id: 'added-trunks',
      data: add,
      getPath: (t) => [up([t.lon, t.lat]), up([t.lon, t.lat], (aDims(t)[1] + aDims(t)[2]) / 2)],
      getColor: [90, 70, 50, 230],
      getWidth: 0.35,
      widthMinPixels: 2,
      updateTriggers: { getPath: [state.addedVersion, g3] },
    }),
    new SimpleMeshLayer({
      id: 'added',
      data: add,
      mesh: sphere,
      pickable: true,
      getPosition: (t) => up([t.lon, t.lat], (aDims(t)[1] + aDims(t)[2]) / 2),
      getScale: (t) => [aDims(t)[0] / 2, aDims(t)[0] / 2, Math.max(aDims(t)[1] - aDims(t)[2], 1) / 2],
      getColor: (t) => [...hexToRgb(pal[t.species].color), Math.round(60 + 170 * pal[t.species].leaf[month - 1])],
      onClick: (info) => (state.drawing ? addVertex(...at(info)) : (state.selected = `a${info.index}`)),
      updateTriggers: { getPosition: [state.addedVersion, g3], getScale: state.addedVersion, getColor: [state.addedVersion, month] },
    }),
  ]
}


// "Add trees": a short note next to the cursor when a click is refused, or accepted with a warning
const tip = ref(null)
let tipTimer
function tryAdd(lon, lat, { x, y }) {
  const n = state.added.length
  addTreeAt(lon, lat)
  const t = state.added.length > n ? state.added.at(-1) : null
  const text = t ? (t.warn.length ? `Added, but ${t.warn.join(' and ')}` : null) : state.addMsg
  clearTimeout(tipTimer)
  tip.value = text ? { x, y, text, ok: !!t } : null
  if (text) tipTimer = setTimeout(() => (tip.value = null), 3000)
}

// "Add trees": where a click is accepted, rebuilt when trees are added (the spacing ring moves)
let mask = null, maskKey = null, maskPoly = null
function addMask() {
  const key = `${state.site}:${state.addedVersion}`
  if (key !== maskKey || state.area?.poly !== maskPoly || !mask) // no grid yet: try again on the next redraw
    [mask, maskKey, maskPoly] = [addableMask(), key, state.area?.poly]
  return mask
}

// sidewalk measuring rays (façade foot -> kerb) of the measured positions (i = position index) and kept trees
let rays = null, raysOf = null
function swRays() {
  if (raysOf !== state.trees) {
    const seg = (r) => [[r[0], r[1]], [r[2], r[3]]]
    const p = state.trees.positions.sw_ray ?? [], k = state.trees.kept.sw_ray ?? []
    rays = [...p.flatMap((r, i) => (r ? [{ i, path: seg(r) }] : [])), ...k.flatMap((r) => (r ? [{ i: -1, path: seg(r) }] : []))]
    raysOf = state.trees
  }
  return rays
}

function layers() {
  if (!state.meta) return []
  const { selected } = state
  const ov = state.meta.overlays.find((o) => o.id === state.overlay)
  const c = state.meta.site.corners
  const g3 = state.ground3d, T = state.meta.terrain
  return [
    // 3D ground: the relief, then the basemap drawn on it (the MapLibre basemap below stays flat, outside the site)
    g3 &&
      new SimpleMeshLayer({ id: 'terrain', data: [0], mesh: reliefMesh(), _instanced: false, getPosition: [0, 0, 0], pickable: true, ...local(),
        getColor: themeColors.value.ground, updateTriggers: { getColor: isDark.value }, operation: 'terrain+draw' }),
    g3 &&
      new TileLayer({ id: 'ground-tiles-' + state.basemap + isDark.value, data: state.basemap === 'satellite' ? ORTO : themeColors.value.raster,
        extent: T.bounds, minZoom: 12, maxZoom: 19, tileSize: 256, ...drape(),
        renderSubLayers: (props) => { const [[w, s], [e, n]] = props.tile.boundingBox
          return new BitmapLayer(props, { data: null, image: props.data, bounds: [w, s, e, n] }) } }),
    ov &&
      new BitmapLayer({ id: 'overlay-' + ov.id, image: dataUrl(ov.file), bounds: c, opacity: 0.55, ...drape() }),
    state.addMode && addMask() &&
      new BitmapLayer({ id: 'addable-' + maskKey + (maskPoly ? ':area' + maskPoly.length + maskPoly[0] : ''), image: mask, bounds: c, textureParameters: { minFilter: 'nearest', magFilter: 'nearest' }, ...drape() }),
    new GeoJsonLayer({
      id: 'buildings',
      data: g3 ? buildings3d() : dataUrl('buildings.geojson'),
      extruded: true,
      getElevation: (f) => f.properties.height_m,
      getFillColor: themeColors.value.building,
      getLineColor: themeColors.value.buildingLine,
      updateTriggers: { getFillColor: isDark.value, getLineColor: isDark.value },
      lineWidthMinPixels: 0,
      opacity: state.buildingOpacity,
      // see-through buildings must not hide the crowns behind them
      parameters: { depthWriteEnabled: state.buildingOpacity >= 1 },
    }),
    state.showStreets &&
      new GeoJsonLayer({ id: 'sidewalks', data: dataUrl('sidewalks.geojson'), stroked: true, filled: false, ...drape(),
        getLineColor: (f) => (f.properties.kind === 'facade' ? themeColors.value.facade : themeColors.value.kerb),
        updateTriggers: { getLineColor: isDark.value },
        getLineWidth: (f) => (f.properties.kind === 'facade' ? 0.5 : 0.8), lineWidthUnits: 'meters', lineWidthMinPixels: 1.5 }),
    // where each sidewalk width was measured: façade foot -> kerb, through the tree (scripts/porta_sidewalk_width.py)
    state.showStreets &&
      new PathLayer({ id: 'sidewalk-rays', data: swRays(), getPath: (d) => d.path.map((q) => up(q, 0.3)), widthUnits: 'pixels', parameters: ON_TOP,
        getWidth: (d) => (d.i === selected ? 3 : 1),
        getColor: (d) => (d.i === selected ? themeColors.value.ringOn : [...hexToRgb(themeColors.value.muted), 150]),
        updateTriggers: { getPath: g3, getWidth: selected, getColor: [selected, isDark.value] } }),
    state.showStreets &&
      new ScatterplotLayer({ id: 'spots', data: state.trees.spots.lon.map((lon, i) => i), radiusUnits: 'meters',
        getPosition: (i) => up([state.trees.spots.lon[i], state.trees.spots.lat[i]], 0.2),
        getRadius: (i) => ({ small: 1.6, medium: 2.2, large: 2.8 })[state.trees.spots.size_class[i]], radiusMinPixels: 3,
        getFillColor: (i) => ({ small: [168, 214, 110], medium: [92, 170, 50], large: [40, 110, 20] })[state.trees.spots.size_class[i]],
        stroked: true, getLineColor: themeColors.value.spotLine, lineWidthMinPixels: 1.5, pickable: true, updateTriggers: { getPosition: g3, getLineColor: isDark.value },
        onClick: (info) => { // a click on a free spot plants there in "Add trees" mode
          if (state.drawing) return addVertex(...at(info))
          if (state.addMode) tryAdd(state.trees.spots.lon[info.index], state.trees.spots.lat[info.index], info)
        } }),
    state.area &&
      new PolygonLayer({ id: 'area', data: [state.area.poly], getPolygon: (d) => d, stroked: false, filled: true, ...drape(),
        getFillColor: [...themeColors.value.area, 30] }),
    ...crowns(),
    state.showLidar && state.lidar &&
      new PointCloudLayer({ id: 'lidar', data: lidarData(), ...local(), pointSize: 2, sizeUnits: 'pixels', material: false }),
    // the project-area outline and the corners being drawn go over buildings and crowns (no depth test)
    state.area && !state.editing &&
      new PathLayer({ id: 'area-line', data: [[...state.area.poly, state.area.poly[0]]], getPath: (d) => d, parameters: ON_TOP, ...drape(),
        getColor: [...themeColors.value.area, 240], widthMinPixels: 2.5 }),
    state.drawing && state.draft.length > 1 &&
      new PathLayer({ id: 'draft-path', data: [state.draft], getPath: (d) => d, getColor: themeColors.value.draft, widthMinPixels: 2.5,
        parameters: ON_TOP, ...drape() }),
    state.drawing &&
      new ScatterplotLayer({ id: 'draft-pts', data: [...state.draft], getPosition: (d) => up(d), getRadius: 4, radiusUnits: 'pixels',
        getFillColor: themeColors.value.draft, parameters: ON_TOP }),
    // editing the area: the polygon, its corners (drag, right-click removes) and midpoints (click adds a corner)
    state.editing &&
      new PathLayer({ id: 'edit-path', data: [[...state.draft, state.draft[0]]], getPath: (d) => d, getColor: themeColors.value.draft,
        widthMinPixels: 2.5, parameters: ON_TOP, ...drape() }),
    state.editing &&
      new ScatterplotLayer({ id: 'edit-mid', data: state.draft.map((q, i) => mid(q, state.draft[(i + 1) % state.draft.length])),
        getPosition: (d) => up(d), getRadius: 4, radiusUnits: 'pixels', stroked: true, filled: true, getFillColor: [255, 255, 255, 200],
        getLineColor: themeColors.value.draft, lineWidthMinPixels: 1.5, pickable: true, parameters: ON_TOP }),
    state.editing &&
      new ScatterplotLayer({ id: 'edit-pts', data: [...state.draft], getPosition: (d) => up(d), getRadius: 6, radiusUnits: 'pixels',
        getFillColor: themeColors.value.draft, stroked: true, getLineColor: [255, 255, 255], lineWidthMinPixels: 1.5, pickable: true,
        parameters: ON_TOP }),
  ].filter(Boolean)
}

// basemap: the street map of the theme, or the ICGC orthophoto
const style = () => (state.basemap === 'satellite'
  ? { version: 8, sources: { orto: { type: 'raster', tiles: [ORTO], tileSize: 256, maxzoom: 20, attribution: 'Orthophoto © ICGC (CC BY 4.0)' } },
      layers: [{ id: 'orto', type: 'raster', source: 'orto' }] }
  : themeColors.value.basemap)
let overTerrain = false // the relief is pickable (clicks need its height) but must not turn the cursor into a pointer

onMounted(() => {
  map = new MapLibreMap({
    container: el.value,
    style: style(),
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
    onHover: (info) => (overTerrain = info.layer?.id === 'terrain'),
    getCursor: ({ isHovering: h }) => { const isHovering = h && !overTerrain; return state.editing ? (isHovering ? 'move' : 'grab') : state.addMode || state.drawing ? 'crosshair' : isHovering ? 'pointer' : 'grab' },
    onClick: (info) => {
      if (state.editing) return
      const q = info.coordinate && at(info)
      if (state.drawing && q) return addVertex(q[0], q[1])
      if (state.addMode && (!info.layer || info.layer.id === 'terrain') && q) tryAdd(q[0], q[1], info)
    },
    getTooltip: ({ layer, index, object }) => {
      if (layer?.id === 'added') return { text: `${state.meta.palette[object.species].species} (added)` }
      if (layer?.id === 'spots') { const S = state.trees.spots; return { text: `Free planting spot · ${S.size_class[index]} tree · sidewalk ${S.width_m[index]} m` } }
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
    state.month, state.selected, state.addedVersion, state.buildingOpacity, state.addMode, state.editing, state.ground3d, state.basemap, state.meta, state.showLidar],
  () => overlay?.setProps({ layers: layers() }),
)

// theme switch: swap the basemap (the deck.gl layers sit on their own canvas and stay)
watch(() => [isDark.value, state.basemap], () => map?.setStyle(style()))

// another site or palette: its own relief file
watch(() => state.meta, (m) => { if (m && state.ground3d) setGround3d(true); if (m && state.showLidar) setLidar(true) })

// a new project area: frame it (keeps the current pitch and bearing)
watch(() => state.area?.poly, (poly) => {
  if (!poly || !map || state.area.edited) return // an edited area stays where the view is
  const lons = poly.map((p) => p[0]), lats = poly.map((p) => p[1])
  map.fitBounds([[Math.min(...lons), Math.min(...lats)], [Math.max(...lons), Math.max(...lats)]],
    { padding: 60, pitch: map.getPitch(), bearing: map.getBearing(), duration: 800, maxZoom: 18.5 })
})

// while drawing a project area, double clicks place corners instead of zooming
watch(() => state.drawing, (on) => (on ? map?.doubleClickZoom.disable() : map?.doubleClickZoom.enable()))

// while drawing, a right click (without dragging the view), Enter or Space closes the area; Escape cancels it.
// While editing, a corner or midpoint under the mouse is dragged instead of the map, and a right click on a corner removes it.
let rightDown = null
let dragging = null // index of the corner being moved
const px = (e) => { const r = el.value.getBoundingClientRect(); return [e.clientX - r.left, e.clientY - r.top] }
const pickEdit = (e) => { const [x, y] = px(e); return overlay?.pickObject({ x, y, radius: 6, layerIds: ['edit-pts', 'edit-mid'] }) }
const onMouseDown = (e) => {
  rightDown = e.button === 2 ? [e.clientX, e.clientY] : null
  if (!state.editing || e.button !== 0) return
  const hit = pickEdit(e)
  if (!hit) return
  e.stopPropagation() // keep MapLibre from panning
  e.preventDefault()
  if (hit.layer.id === 'edit-mid') state.draft = [...state.draft.slice(0, hit.index + 1), hit.object, ...state.draft.slice(hit.index + 1)]
  dragging = hit.layer.id === 'edit-mid' ? hit.index + 1 : hit.index
  window.addEventListener('mousemove', onDrag)
  window.addEventListener('mouseup', onDrop, { once: true })
}
const onDrag = (e) => {
  const [x, y] = px(e), { lng, lat } = map.unproject([x, y])
  const [lon, la] = at({ x, y, coordinate: [lng, lat] })
  state.draft = state.draft.map((q, i) => (i === dragging ? [lon, la] : q))
}
const onDrop = () => {
  dragging = null
  window.removeEventListener('mousemove', onDrag)
}
const onContextMenu = (e) => {
  if (state.editing) {
    e.preventDefault()
    const hit = pickEdit(e)
    if (hit?.layer.id !== 'edit-pts') return
    if (state.draft.length <= 3) return void (state.addMsg = 'An area needs at least three corners.')
    state.draft = state.draft.filter((_, i) => i !== hit.index)
    return
  }
  if (!state.drawing) return
  e.preventDefault()
  if (rightDown && Math.hypot(e.clientX - rightDown[0], e.clientY - rightDown[1]) < 5 && state.draft.length >= 3) finishArea()
}
const onKey = (e) => {
  if (!(state.drawing || state.editing) || e.target.closest?.('input, select, textarea')) return
  if (e.key === 'Escape') return state.editing ? cancelEditArea() : cancelDrawing()
  if (e.key !== 'Enter' && e.key !== ' ') return
  e.preventDefault() // Space would otherwise press the focused button
  if (state.draft.length >= 3) state.editing ? finishEditArea() : finishArea()
}
onMounted(() => {
  el.value.addEventListener('mousedown', onMouseDown, true)
  el.value.addEventListener('contextmenu', onContextMenu, true)
  window.addEventListener('keydown', onKey)
})
onBeforeUnmount(() => window.removeEventListener('keydown', onKey))

onBeforeUnmount(() => {
  ro?.disconnect()
  map?.remove()
})
</script>

<template>
  <div ref="el" class="map" :class="{ crosshair: state.addMode || state.drawing }"></div>
  <div v-if="tip" class="tip" :class="{ warn: tip.ok }" :style="{ left: tip.x + 14 + 'px', top: tip.y + 14 + 'px' }" role="status">{{ tip.text }}</div>
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
.tip {
  position: absolute; z-index: 5; max-width: 240px; pointer-events: none; padding: 5px 8px; border-radius: 6px;
  font-size: 12px; line-height: 1.35; background: var(--panel); color: var(--text); border: 1px solid var(--bad);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.18);
}
.tip.warn { border-color: var(--warn); }
</style>
