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
import { BitmapLayer, GeoJsonLayer, PathLayer, PointCloudLayer, PolygonLayer, ScatterplotLayer, TextLayer } from '@deck.gl/layers'
import { SimpleMeshLayer } from '@deck.gl/mesh-layers'
import { TileLayer } from '@deck.gl/geo-layers'
import { _TerrainExtension as TerrainExtension, PathStyleExtension } from '@deck.gl/extensions'
import { SphereGeometry } from '@luma.gl/engine'
import { state, dataUrl, hexToRgb, currentLayout, spotClass, addTreeAt, addVertex, keptReplaced, themeColors, isDark, AREA, addableMask, finishArea,
  cancelDrawing, finishEditArea, cancelEditArea, groundZ, HABIT_RGB, habits, habitOf, moveTargets, setMoveTarget, setGround3d, setLidar, setParks, setUtilities, spotWhy, keptKey, ORTO } from '../store.js'

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

// a crown as drawn: [height of its centre, half its depth]. Display only: no deeper than twice its width (ASSUMPTION, after the 0.5–2
// height:width range the i-Tree UFORE methods hold, notes/methodology.md): about 140 LiDAR crowns of ~2 m width under 10–29 m heights (small
// segments under a taller canopy) otherwise draw as needles. The crown top stays at the tree height; the trunk shows the rest.
const crownZ = (d, h, b) => { const depth = Math.max(Math.min(h - b, 2 * d), 1); return [h - depth / 2, depth / 2] }
const TRUNK_W = { SEGONA: 0.605 / Math.PI, TERCERA: 0.955 / Math.PI } // m, trunk class perimeter midpoints (SpeciesCards.vue)
const alpha = (leaf) => Math.round(60 + 170 * leaf) // crown (and trunk) opacity from the leaf-on share of the month

// metres east and north of the site centre, as deck.gl places METER_OFFSETS (Web Mercator sphere)
const M_DEG = 40075016.686 / 360
const local = () => ({ coordinateSystem: COORDINATE_SYSTEM.METER_OFFSETS, coordinateOrigin: [...state.meta.site.center, 0] })

// LiDAR points: on the flat map a point sits at its height above ground, on the relief at its true height
const LIDAR_RGB = [[150, 128, 104], [70, 140, 60], [196, 120, 92], [172, 172, 166]] // ground, vegetation, building, other
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

// 3D ground: sidewalk lines lifted onto the relief, a vertex every metre. Draped (TerrainExtension) they were drawn into a
// low-resolution ground texture and came out grainy.
let walks = null, walksOf = null
function sidewalks3d() {
  const key = state.site
  if (walksOf === key) return walks ?? []
  walksOf = key
  walks = null
  fetch(dataUrl('sidewalks.geojson')).then((r) => r.json()).then((fc) => {
    if (walksOf !== key) return
    const kx = M_DEG * Math.cos((state.meta.site.center[1] * Math.PI) / 180)
    const dense = (L) => L.flatMap((q, k) => {
      if (k === 0) return [q]
      const p = L[k - 1], n = Math.max(1, Math.ceil(Math.hypot((q[0] - p[0]) * kx, (q[1] - p[1]) * M_DEG))) // 1 m steps
      return Array.from({ length: n }, (_, j) => [p[0] + ((q[0] - p[0]) * (j + 1)) / n, p[1] + ((q[1] - p[1]) * (j + 1)) / n])
    }).map((q) => up(q, 0.15))
    walks = fc.features.map((f) => ({ ...f, geometry: f.geometry.type === 'LineString'
      ? { type: 'LineString', coordinates: dense(f.geometry.coordinates) }
      : { ...f.geometry, coordinates: f.geometry.coordinates.map(dense) } }))
    overlay?.setProps({ layers: layers() })
  })
  return []
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

// the crowns' data arrays are rebuilt only when what they show changes: deck.gl recomputes every attribute of a layer whose
// data is a new array, and rebuilding them on every redraw made drawing an area lag (user tests 27 Nov)
let crownMemo = { key: null, trees: null, data: null }
function crowns() {
  const { trees, meta, scenarioId, month, selected } = state
  const p = trees.positions
  const lay = currentLayout()
  const pal = meta.palette
  const memoKey = [scenarioId, state.live?.version, state.area?.version, state.addedVersion, month, selected, state.ground3d, isDark.value,
    Object.keys(habits.map).length].join('|')
  if (crownMemo.key !== memoKey || crownMemo.trees !== trees) crownMemo = { key: memoKey, trees, data: {} }
  const memo = (name, make) => (crownMemo.data[name] ??= make())
  const ids = memo('ids', () => [...p.lon.keys()])
  const dims = (i) => {
    // today's tree (S0, or outside a project area): its measured crown
    if (!pal[lay[i]].in_palette) return [p.s0_crown_diam_m[i], p.s0_height_m[i], p.s0_crown_base_m[i]]
    const s = pal[lay[i]]
    return [s.crown_diam_m, s.height_m, s.crown_base_m]
  }
  const add = memo('add', () => [...state.added]) // a new array when trees are added: deck.gl only notices data changes by reference
  const aDims = (t) => {
    const s = pal[t.species]
    return [s.crown_diam_m, s.height_m, s.crown_base_m]
  }
  const k = state.trees.kept
  const repl = scenarioId === AREA ? keptReplaced() : new Map()
  const g3 = state.ground3d, gz = groundZ
  const keptIds = memo('keptIds', () => [...k.lon.keys()].filter((i) => !repl.has(i)))
  const keptColor = (i) => [...HABIT_RGB[habitOf(k.species[i])], 150] // today's trees by leaf habit
  const sDims = (s) => [s.crown_diam_m, s.height_m, s.crown_base_m]
  const posColor = (i) => [...hexToRgb(pal[lay[i]].color), i === selected ? 255 : alpha(pal[lay[i]].leaf[month - 1])]
  const spColor = (s) => [...hexToRgb(s.color), alpha(s.leaf[month - 1])]
  // trunk width: the palette species' trunk class midpoint (2011 guide p. 18, perimeter / π, as the species cards); measured trees
  // have no trunk size in the data: 0.3 m stand-in (ASSUMPTION)
  const tw = (s) => (s?.in_palette && TRUNK_W[s.trunk_class]) || 0.3
  // every tree: [lon, lat, crown width, height, crown base, colour, trunk width]; trunk and ellipsoid share colour and opacity
  const all = memo('all', () => [
    ...[...repl.keys()].map((i) => { const s = pal[repl.get(i)]; return [k.lon[i], k.lat[i], ...sDims(s), spColor(s), tw(s)] }),
    ...keptIds.map((i) => [k.lon[i], k.lat[i], k.crown_diam_m[i], k.height_m[i], k.crown_base_m[i], keptColor(i), 0.3]),
    ...ids.map((i) => [p.lon[i], p.lat[i], ...dims(i), posColor(i), tw(pal[lay[i]])]),
    ...add.map((t) => [t.lon, t.lat, ...aDims(t), spColor(pal[t.species]), tw(pal[t.species])]),
  ])
  const ctr = (lon, lat, [d, h, b]) => [lon, lat, gz(lon, lat) + crownZ(d, h, b)[0]]
  const scale = ([d, h, b]) => [d / 2, d / 2, crownZ(d, h, b)[1]]
  return [
    // a trunk from the ground to the crown centre
    new PathLayer({
      id: 'trunks',
      data: all,
      getPath: (t) => [up(t), up(t, crownZ(t[2], t[3], t[4])[0])],
      getColor: (t) => t[5],
      getWidth: (t) => t[6],
      billboard: true, // a vertical path has no width in the ground plane: extrude it on screen
      widthMinPixels: 1,
      updateTriggers: { getPath: [scenarioId, state.live?.version, state.area?.version, state.addedVersion, g3], getWidth: [scenarioId, state.live?.version, state.area?.version, state.addedVersion],
        getColor: [scenarioId, state.live?.version, state.area?.version, state.addedVersion, month, selected, isDark.value] },
    }),
    new SimpleMeshLayer({
      id: 'kept-new',
      data: memo('repl', () => [...repl.keys()]),
      mesh: sphere,
      getPosition: (i) => ctr(k.lon[i], k.lat[i], sDims(pal[repl.get(i)])),
      getScale: (i) => scale(sDims(pal[repl.get(i)])),
      getColor: (i) => spColor(pal[repl.get(i)]),
      updateTriggers: { getPosition: [state.area?.version, g3], getScale: state.area?.version, getColor: [state.area?.version, month] },
    }),
    new SimpleMeshLayer({
      id: 'kept',
      data: keptIds,
      mesh: sphere,
      getPosition: (i) => ctr(k.lon[i], k.lat[i], [k.crown_diam_m[i], k.height_m[i], k.crown_base_m[i]]),
      updateTriggers: { getPosition: g3, getColor: habits.map },
      getScale: (i) => scale([k.crown_diam_m[i], k.height_m[i], k.crown_base_m[i]]),
      getColor: keptColor,
      pickable: true,
      onClick: (info) => (state.drawing ? addVertex(...at(info)) : (state.selected = keptKey(info.object))),
    }),
    state.showParks && state.parks?.site === state.site && new SimpleMeshLayer({
      id: 'parks',
      data: memo('parks', () => [...state.parks.lon.keys()]),
      mesh: sphere,
      pickable: true,
      getPosition: (i) => { const P = state.parks; return ctr(P.lon[i], P.lat[i], [P.crown_diam_m[i], P.height_m[i], P.crown_base_m[i]]) },
      getScale: (i) => { const P = state.parks; return scale([P.crown_diam_m[i], P.height_m[i], P.crown_base_m[i]]) },
      getColor: (i) => [...HABIT_RGB[habitOf(state.parks.species[i])], 110], // context: lighter than street trees
      updateTriggers: { getPosition: g3, getColor: [isDark.value, habits.map] },
    }),
    new SimpleMeshLayer({
      id: 'positions',
      data: ids,
      mesh: sphere,
      pickable: true,
      getPosition: (i) => ctr(p.lon[i], p.lat[i], dims(i)),
      getScale: (i) => scale(dims(i)),
      getColor: posColor,
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
      lineWidthMinPixels: 1,
      radiusMinPixels: 7, // young crowns are small: keep the ring findable at any zoom
      parameters: ON_TOP, // an added tree can sit inside an existing crown or behind a building: its ring stays visible
      updateTriggers: { getPosition: g3, getRadius: state.addedVersion, getLineColor: [selected, state.addedVersion] },
    }),
    new SimpleMeshLayer({
      id: 'added',
      data: add,
      mesh: sphere,
      pickable: true,
      getPosition: (t) => ctr(t.lon, t.lat, aDims(t)),
      getScale: (t) => scale(aDims(t)),
      getColor: (t) => spColor(pal[t.species]),
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

// trees marked Move: their crown at the new spot and a dashed line from the old pit (a plane keeps its measured crown)
function movedLayers() {
  const T = state.trees, S = T.spots, out = []
  for (const [spot, key] of moveTargets()) {
    const s = S.id.indexOf(spot)
    if (s < 0) continue
    const k = key.startsWith('k') ? Number(key.slice(1)) : T.positions.tree_id.indexOf(key)
    const d = key.startsWith('k') ? [T.kept.crown_diam_m[k], T.kept.height_m[k], T.kept.crown_base_m[k]]
      : [T.positions.s0_crown_diam_m[k], T.positions.s0_height_m[k], T.positions.s0_crown_base_m[k]]
    const from = key.startsWith('k') ? [T.kept.lon[k], T.kept.lat[k]] : [T.positions.lon[k], T.positions.lat[k]]
    out.push({ to: [S.lon[s], S.lat[s]], from, d })
  }
  if (!out.length) return []
  return [
    new PathLayer({ id: 'moved-path', data: out, getPath: (m) => [up(m.from, 0.5), up(m.to, 0.5)], getColor: themeColors.value.ringOn,
      getWidth: 2, widthUnits: 'pixels', getDashArray: [4, 3], extensions: [new PathStyleExtension({ dash: true })], parameters: ON_TOP }),
    new SimpleMeshLayer({ id: 'moved', data: out, mesh: sphere, getPosition: (m) => [m.to[0], m.to[1], groundZ(...m.to) + crownZ(...m.d)[0]],
      getScale: (m) => [m.d[0] / 2, m.d[0] / 2, crownZ(...m.d)[1]], getColor: [...themeColors.value.ringOn, 170] }),
  ]
}

// the selected tree or spot (map or schedule): a ring on the ground, drawn over everything
function selRing(sel) {
  if (sel == null) return null
  const T = state.trees, n = typeof sel === 'string' ? Number(sel.slice(1)) : sel, pal = state.meta.palette
  // the ring fits the crown drawn now: a replaced plane or kept tree, or an added tree, has its new species' crown (a ring sized
  // on today's small crown sat inside the new one and could not be seen)
  const now = (j) => (j != null && pal[j]?.in_palette ? pal[j].crown_diam_m : null)
  const [lon, lat, d] = typeof sel === 'number' ? [T.positions.lon[n], T.positions.lat[n], now(currentLayout()[n]) ?? T.positions.s0_crown_diam_m[n]]
    : sel[0] === 'k' ? [T.kept.lon[n], T.kept.lat[n], now(state.scenarioId === AREA ? keptReplaced().get(n) : null) ?? T.kept.crown_diam_m[n]]
    : sel[0] === 's' ? [T.spots.lon[n], T.spots.lat[n], 2 * SPOT_R[T.spots.size_class[n]]]
    : [state.added[n]?.lon, state.added[n]?.lat, now(state.added[n]?.species) ?? 4]
  if (lon == null) return null
  return new ScatterplotLayer({ id: 'sel-ring', data: [[lon, lat]], getPosition: (q) => up(q, 0.4), getRadius: Math.max(d || 4, 3) / 2 + 1,
    radiusUnits: 'meters', radiusMinPixels: 9, stroked: true, filled: false, getLineColor: themeColors.value.ringOn, lineWidthMinPixels: 3,
    parameters: ON_TOP })
}

// tree pits: the minimum pit of the 2011 street-tree guide p.25 (web_export pit_min_m2), a standard, not a measured pit.
// 1 m² is drawn 1 × 1 m, 1.5 m² as the guide prints it, 1.2 × 1.2 m. The square is turned to the kerb when the tree has a
// measuring ray (façade -> kerb), else it is north-up
function pitSquares() {
  const out = []
  for (const g of [state.trees.positions, state.trees.kept]) {
    if (!g.pit_min_m2) continue
    for (let i = 0; i < g.lon.length; i++) {
      const a = g.pit_min_m2[i]
      if (!a) continue
      const h = (a >= 1.5 ? 1.2 : 1.0) / 2, lat = g.lat[i], kx = M_DEG * Math.cos((lat * Math.PI) / 180), r = g.sw_ray?.[i]
      let [ux, uy] = r ? [(r[2] - r[0]) * kx, (r[3] - r[1]) * M_DEG] : [0, 1]
      const n = Math.hypot(ux, uy) || 1; [ux, uy] = [ux / n, uy / n]
      const pt = (s, t) => [g.lon[i] + (s * ux * h + t * uy * h) / kx, lat + (s * uy * h - t * ux * h) / M_DEG]
      out.push({ poly: [pt(1, 1), pt(1, -1), pt(-1, -1), pt(-1, 1)], basis: g.pit_basis[i] })
    }
  }
  return out
}
let pits = null, pitsOf = null
const pitData = () => (pitsOf !== state.trees ? ((pitsOf = state.trees), (pits = pitSquares())) : pits)

// free spots: footprint radius (m) per size class, and the spot lifted onto the highest ground under its footprint (a flat
// disc on a slope would otherwise sink into the relief)
const SPOT_R = { small: 1.6, medium: 2.2, large: 2.8 }
// synthetic utility lines by network (scripts/synthetic_utilities.py)
const UTIL_COLOR = { water: [60, 130, 200], gas: [220, 170, 40], electricity: [200, 70, 60], 'house connection': [140, 110, 160] }
function spotUp(i, dz) {
  const S = state.trees.spots, r = SPOT_R[S.size_class[i]], lon = S.lon[i], lat = S.lat[i]
  const dLon = r / (M_DEG * Math.cos((lat * Math.PI) / 180)), dLat = r / M_DEG
  const z = Math.max(groundZ(lon, lat), groundZ(lon + dLon, lat), groundZ(lon - dLon, lat), groundZ(lon, lat + dLat), groundZ(lon, lat - dLat))
  return [lon, lat, z + dz]
}

// façade and kerb lines of the site (sidewalks.geojson), kept for the dimension lines of trees the width script could not measure
let swLines = null, swOf = null
function sidewalkLines() {
  const url = dataUrl('sidewalks.geojson')
  if (swOf !== url) {
    swOf = url; swLines = null
    fetch(url).then((r) => r.json()).then((fc) => { if (swOf === url) { swLines = fc.features; overlay?.setProps({ layers: layers() }) } })
  }
  return swLines
}
const DIM_MAX_M = 25 // ASSUMPTION: farther than this, the nearest façade or kerb is not the tree's own sidewalk

// nearest point to t on the lines of one kind, in metres: { to, d } or null
function nearestOn(t, kind, kx) {
  let best = null
  for (const f of sidewalkLines() ?? []) {
    if (f.properties.kind !== kind) continue
    const L = f.geometry.coordinates
    for (let j = 1; j < L.length; j++) {
      const ax = (L[j - 1][0] - t[0]) * kx, ay = (L[j - 1][1] - t[1]) * M_DEG, bx = (L[j][0] - t[0]) * kx, by = (L[j][1] - t[1]) * M_DEG
      const vx = bx - ax, vy = by - ay, u = Math.max(0, Math.min(1, -(ax * vx + ay * vy) / (vx * vx + vy * vy || 1)))
      const px = ax + u * vx, py = ay + u * vy, d = Math.hypot(px, py)
      if (d <= DIM_MAX_M && (!best || d < best.d)) best = { to: [t[0] + px / kx, t[1] + py / M_DEG], d }
    }
  }
  return best
}

// the selected plane position: dimension lines tree -> façade foot and tree -> kerb, labelled in metres. Measured trees use the
// width script's ray; the others (no kerb, no façade, median) show whichever of the two is found nearby
function dimensions(i) {
  const p = state.trees.positions
  if (typeof i !== 'number' || p.lon[i] == null) return []
  const r = p.sw_ray?.[i]
  const t = [p.lon[i], p.lat[i]], kx = M_DEG * Math.cos((t[1] * Math.PI) / 180)
  const m = (q) => Math.hypot((q[0] - t[0]) * kx, (q[1] - t[1]) * M_DEG)
  const ends = r ? [[[r[0], r[1]], 'façade'], [[r[2], r[3]], 'kerb']]
    : ['facade', 'kerb'].map((k) => [nearestOn(t, k, kx)?.to, k === 'facade' ? 'façade' : 'kerb']).filter(([q]) => q)
  if (!ends.length) return []
  const dims = ends.map(([to, what]) => ({ to, text: `${m(to).toFixed(1)} m to ${what}` }))
  const col = themeColors.value.ringOn
  return [
    new PathLayer({ id: 'dim-lines', data: dims, getPath: (d) => [up(t, 0.3), up(d.to, 0.3)], getColor: col, getWidth: 1.5, widthUnits: 'pixels',
      parameters: ON_TOP }),
    // a dot at each end of the dimension: the trunk and the façade / kerb point
    new ScatterplotLayer({ id: 'dim-ends', data: [...dims.map((d) => d.to), t], getPosition: (q) => up(q, 0.3), getRadius: 3, radiusUnits: 'pixels',
      getFillColor: col, parameters: ON_TOP }),
    // one label above the tree, one line per distance: the kerb is often under a metre away, so labels at the two ends would collide
    new TextLayer({ id: 'dim-labels', data: [dims.map((d) => d.text).join('\n')], getPosition: () => up(t, 0.3), getText: (d) => d,
      getSize: 12, getPixelOffset: [0, -30], lineHeight: 1.3,
      characterSet: 'auto', background: true, getBackgroundColor: [255, 255, 255, 230], backgroundPadding: [4, 2], getColor: col,
      fontFamily: 'system-ui, sans-serif', parameters: ON_TOP }),
  ]
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
    // the street map has no keyless raster tiles (CARTO's carry an "API key required" watermark): plain ground colour instead
    g3 && state.basemap === 'satellite' &&
      new TileLayer({ id: 'ground-tiles', data: ORTO,
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
      new GeoJsonLayer({ id: 'sidewalks', data: state.ground3d ? sidewalks3d() : dataUrl('sidewalks.geojson'), stroked: true, filled: false,
        getLineColor: (f) => (f.properties.kind === 'facade' ? themeColors.value.facade : themeColors.value.kerb),
        updateTriggers: { getLineColor: isDark.value },
        getLineWidth: (f) => (f.properties.kind === 'facade' ? 0.5 : 1), lineWidthUnits: 'pixels' }),
    state.showStreets && state.trees.positions.pit_min_m2 &&
      new PolygonLayer({ id: 'pits', data: pitData(), getPolygon: (d) => d.poly, ...drape(), filled: true, stroked: true,
        getFillColor: themeColors.value.pit, getLineColor: themeColors.value.facade, lineWidthUnits: 'pixels', getLineWidth: 1,
        updateTriggers: { getFillColor: isDark.value, getLineColor: isDark.value } }),
    // free planting spots: the crown footprint of the spot's size class on the ground, a white dot at the planting point
    state.showSpots &&
      new ScatterplotLayer({ id: 'spots', data: state.trees.spots.lon.map((lon, i) => i), radiusUnits: 'meters',
        getPosition: (i) => spotUp(i, 0.15),
        getRadius: (i) => SPOT_R[state.trees.spots.size_class[i]], radiusMinPixels: 3,
        getFillColor: (i) => [...({ small: [168, 214, 110], medium: [92, 170, 50], large: [40, 110, 20] })[state.trees.spots.size_class[i]], 170],
        stroked: false, pickable: true, updateTriggers: { getPosition: g3 },
        onClick: (info) => { // a click on a free spot plants there in "Add trees" mode
          if (state.drawing) return addVertex(...at(info))
          if (spotClass(info.index) === 'blocked') return void (state.addMsg = `Blocked spot: ${state.trees.spots.reasons[info.index]?.replaceAll('_', ' ') || 'not plantable'}.`)
          if (state.movePick) return setMoveTarget(info.index) // the tree chosen for Move goes to this spot
          if (state.addMode) tryAdd(state.trees.spots.lon[info.index], state.trees.spots.lat[info.index], info)
          else state.selected = `s${info.index}` // the schedule's Spots tab follows
        } }),
    state.showSpots &&
      new ScatterplotLayer({ id: 'spot-centres', data: state.trees.spots.lon.map((lon, i) => i), getPosition: (i) => spotUp(i, 0.2),
        getRadius: 0.35, radiusUnits: 'meters', radiusMinPixels: 1.5, updateTriggers: { getPosition: g3 },
        // white = free; amber = conditional (an object a street project can move: field check first);
        // orange = the pit would sit on a buried service (scripts/utilities_conditional.py)
        getFillColor: (i) => (spotClass(i) === 'blocked' ? [178, 44, 34, 245] : state.trees.spots.utility_conditional?.[i] ? [230, 120, 20, 245]
          : spotClass(i) === 'conditional' ? [235, 150, 30, 245] : [255, 255, 255, 235]) }), // red centre = blocked
    // SYNTHETIC underground services (a mock from published rules): drawn on the ground, under the spots' rings
    state.showUtilities && state.utilities?.site === state.site &&
      new PathLayer({ id: 'utilities', data: state.utilities.features, getPath: (f) => f.geometry.coordinates, ...drape(),
        getColor: (f) => UTIL_COLOR[f.properties.network] ?? [150, 150, 150], getWidth: (f) => (f.properties.kind === 'connection' ? 1.2 : 2),
        widthUnits: 'pixels', pickable: true, parameters: ON_TOP }),
    state.area &&
      new PolygonLayer({ id: 'area', data: [state.area.poly], getPolygon: (d) => d, stroked: false, filled: true, ...drape(),
        getFillColor: [...themeColors.value.area, 30] }),
    ...crowns(),
    ...movedLayers(),
    ...dimensions(selected), // after the crowns: drawn over them
    state.showLidar && state.lidar &&
      new PointCloudLayer({ id: 'lidar', data: lidarData(), ...local(), pointSize: 2, sizeUnits: 'pixels', material: false }),
    // the project-area outline and the corners being drawn go over buildings and crowns (no depth test)
    state.area && !state.editing &&
      new PathLayer({ id: 'area-line', data: [[...state.area.poly, state.area.poly[0]]], getPath: (d) => d, parameters: ON_TOP, ...drape(),
        getColor: [...themeColors.value.area, 200], widthMinPixels: 1.5 }),
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
    selRing(selected), // last: always on top of crowns, rings and outlines (user 27 Nov)
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
  // gentler wheel and trackpad zoom (user tests 27 Nov: the map moved too fast); defaults are 1/450 and 1/100
  map.scrollZoom.setWheelZoomRate(1 / 900)
  map.scrollZoom.setZoomRate(1 / 250)
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
      if (layer?.id === 'spots') {
        const S = state.trees.spots, c = spotClass(index) === 'conditional'
        return { text: `${c ? 'Conditional' : 'Free'} planting spot · ${S.size_class[index]} tree · sidewalk ${S.width_m[index]} m` +
          (c ? `\nMove first: ${spotWhy(index)}` : '') +
          (S.utility_conditional?.[index] ? `\nThe pit would sit on a buried ${state.meta.utilities?.synthetic ? 'SYNTHETIC ' : ''}line (PTEV 2024 p. 31)` : '') }
      }
      if (layer?.id === 'utilities') return { text: `SYNTHETIC ${object.properties.network} line, not real data\n(mock from published layout rules)` }
      if (layer?.id === 'parks') { const P = state.parks; return { text: `${P.species[index]} (${P.kind[index]} tree, context only)${P.place[index] ? '\n' + P.place[index] : ''}` } }
      if (layer?.id === 'kept') return { text: `${state.trees.kept.species[object]} (existing)` }
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
  () => [state.scenarioId, state.live?.version, state.area?.version, state.area, state.drawing, state.draft, state.overlay, state.showStreets, state.showSpots, isDark.value,
    state.month, state.selected, state.addedVersion, state.showParks, state.showUtilities, state.buildingOpacity, state.addMode, state.editing, state.ground3d, state.basemap, state.meta, state.showLidar, habits.map, Object.values(state.schedule.trees).map((e) => e.to ?? "").join()],
  () => overlay?.setProps({ layers: layers() }),
)

// theme switch: swap the basemap (the deck.gl layers sit on their own canvas and stay)
watch(() => [isDark.value, state.basemap], () => map?.setStyle(style()))

// another site or palette: its own relief file
watch(() => state.meta, (m) => { if (m && state.ground3d) setGround3d(true); if (m && state.showLidar) setLidar(true); if (m && state.showParks) setParks(true); if (m && state.showUtilities) setUtilities(true) })

// a new project area: frame it (keeps the current pitch and bearing)
watch(() => state.area?.poly, (poly) => {
  if (!poly || !map || state.area.edited) return // an edited area stays where the view is
  const lons = poly.map((p) => p[0]), lats = poly.map((p) => p[1])
  map.fitBounds([[Math.min(...lons), Math.min(...lats)], [Math.max(...lons), Math.max(...lats)]],
    { padding: 60, pitch: map.getPitch(), bearing: map.getBearing(), duration: 800, maxZoom: 18.5 })
})

// while drawing a project area, double clicks place corners instead of zooming
// a schedule row was clicked: jump there, keeping the tree above the schedule panel
watch(() => state.focus, (f) => {
  if (!f || !map) return
  map.easeTo({ center: f, zoom: Math.max(map.getZoom(), 18), offset: [0, -0.2 * el.value.clientHeight], duration: 0 /* a jump: verified to land; an animated ease could not be checked here */ })
  state.focus = null
})
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
/* zoom and compass: the same pill, button size and line icons as the map toolbar below them (MapToolbar.vue) */
.map :deep(.maplibregl-ctrl-top-right .maplibregl-ctrl-group) {
  margin: 10px 10px 0 0; padding: 3px; display: flex; flex-direction: column; gap: 2px; border-radius: 10px; background: var(--panel);
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.18);
}
.map :deep(.maplibregl-ctrl-top-right .maplibregl-ctrl-group button) { width: 36px; height: 36px; border: 0; border-radius: 8px; background: transparent; }
.map :deep(.maplibregl-ctrl-top-right .maplibregl-ctrl-group button:hover) { background: var(--hover); }
.map :deep(.maplibregl-ctrl-top-right .maplibregl-ctrl-group .maplibregl-ctrl-icon) {
  background-image: none; background-color: var(--muted); -webkit-mask: var(--ico) center / 18px no-repeat; mask: var(--ico) center / 18px no-repeat;
}
.map :deep(.maplibregl-ctrl-top-right .maplibregl-ctrl-group button:hover .maplibregl-ctrl-icon) { background-color: var(--text); }
.map :deep(.maplibregl-ctrl-zoom-in .maplibregl-ctrl-icon) { --ico: url('data:image/svg+xml;utf8,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 24 24%22 fill=%22none%22 stroke=%22black%22 stroke-width=%221.6%22 stroke-linecap=%22round%22 stroke-linejoin=%22round%22><path d=%22M12 5v14M5 12h14%22/></svg>'); }
.map :deep(.maplibregl-ctrl-zoom-out .maplibregl-ctrl-icon) { --ico: url('data:image/svg+xml;utf8,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 24 24%22 fill=%22none%22 stroke=%22black%22 stroke-width=%221.6%22 stroke-linecap=%22round%22 stroke-linejoin=%22round%22><path d=%22M5 12h14%22/></svg>'); }
.map :deep(.maplibregl-ctrl-compass .maplibregl-ctrl-icon) { --ico: url('data:image/svg+xml;utf8,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 24 24%22 fill=%22none%22 stroke=%22black%22 stroke-width=%221.6%22 stroke-linecap=%22round%22 stroke-linejoin=%22round%22><path d=%22M12 3l5 17-5-3.5L7 20z%22/></svg>'); }
.tip {
  position: absolute; z-index: 5; max-width: 240px; pointer-events: none; padding: 5px 8px; border-radius: 6px;
  font-size: 12px; line-height: 1.35; background: var(--panel); color: var(--text); border: 1px solid var(--bad);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.18);
}
.tip.warn { border-color: var(--warn); }
</style>
