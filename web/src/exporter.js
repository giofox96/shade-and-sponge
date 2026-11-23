// Export of the layout on screen (or of the drawn project area) for CAD (DXF) and GIS (GeoPackage), in EPSG:25831
// metres. Utility plans are never part of the export.
import { state, dataUrl, currentLayout, keptReplaced, insidePoly, AREA } from './store.js'
import { makeToXY } from './pointpot.js'

export const CONTEXT_M = 20 // ASSUMPTION: buildings and sidewalk edges within 20 m of the project area go out as context

const r2 = (v) => Math.round(v * 100) / 100
const fetchJson = (f) => fetch(dataUrl(f)).then((r) => r.json())

// Everything to export, as plain records with [x, y] in EPSG:25831
export async function collect() {
  const { trees, meta, area, scenarioId } = state
  const toXY = makeToXY(meta.grid)
  const pal = meta.palette
  const poly = area?.poly
  const inside = (lon, lat) => !poly || insidePoly(lon, lat, poly)
  const out = { trees: [], spots: [], buildings: [], edges: [], area: poly ? poly.map(([lon, lat]) => toXY(lon, lat)) : null }
  const tree = (id, lon, lat, species, status, d, h, b) =>
    inside(lon, lat) && out.trees.push({ id, xy: toXY(lon, lat), species, status, crown_diam_m: r2(d), height_m: r2(h), crown_base_m: r2(b) })

  // plane positions: today's plane (measured crown) or the new species (palette crown)
  const p = trees.positions, lay = currentLayout()
  p.lon.forEach((lon, i) => {
    const s = pal[lay[i]]
    if (s.in_palette) tree(p.tree_id[i], lon, p.lat[i], s.species, 'new_replacement', s.crown_diam_m, s.height_m, s.crown_base_m)
    else tree(p.tree_id[i], lon, p.lat[i], s.species, 'existing', p.s0_crown_diam_m[i], p.s0_height_m[i], p.s0_crown_base_m[i])
  })
  // other street trees: kept, or replaced when the project area replaces all trees
  const k = trees.kept, repl = scenarioId === AREA ? keptReplaced() : new Map()
  k.lon.forEach((lon, i) => {
    const s = repl.has(i) && pal[repl.get(i)]
    if (s) tree(`kept_${i}`, lon, k.lat[i], s.species, 'new_replacement', s.crown_diam_m, s.height_m, s.crown_base_m)
    else tree(`kept_${i}`, lon, k.lat[i], k.species[i], 'existing', k.crown_diam_m[i], k.height_m[i], k.crown_base_m[i])
  })
  // added trees (designer clicks or filled free spots)
  state.added.forEach((t, n) => {
    const s = pal[t.species]
    if (s) tree(t.spot ?? `new_${n + 1}`, t.lon, t.lat, s.species, 'new_added', s.crown_diam_m, s.height_m, s.crown_base_m)
  })
  // free planting spots not used by an added tree
  const used = new Set(state.added.map((t) => t.spot))
  const S = trees.spots
  S.lon.forEach((lon, s) => {
    if (!used.has(S.id[s]) && inside(lon, S.lat[s]))
      out.spots.push({ id: S.id[s], xy: toXY(lon, S.lat[s]), size_class: S.size_class[s], width_m: S.width_m[s] })
  })

  // context: buildings and sidewalk edges near the area (all of them without an area)
  let box = null
  if (out.area) {
    const xs = out.area.map((v) => v[0]), ys = out.area.map((v) => v[1])
    box = [Math.min(...xs) - CONTEXT_M, Math.min(...ys) - CONTEXT_M, Math.max(...xs) + CONTEXT_M, Math.max(...ys) + CONTEXT_M]
  }
  const near = (pts) => !box || pts.some(([x, y]) => x >= box[0] && x <= box[2] && y >= box[1] && y <= box[3])
  const [bld, sw] = await Promise.all([fetchJson('buildings.geojson'), fetchJson('sidewalks.geojson')])
  for (const f of bld.features) {
    const rings = f.geometry.coordinates.map((r) => r.map(([lon, lat]) => toXY(lon, lat))) // outer ring, then courtyards
    if (rings.length && near(rings[0])) out.buildings.push({ rings, height_m: f.properties.height_m })
  }
  for (const f of sw.features) {
    const line = f.geometry.coordinates.map(([lon, lat]) => toXY(lon, lat))
    if (near(line)) out.edges.push({ line, kind: f.properties.kind })
  }
  return out
}

// ---- DXF (AutoCAD R12 ASCII: opens in AutoCAD, Rhino, QGIS, BricsCAD, LibreCAD) ---------------------------------
const LAYERS = { TREES_EXISTING: 3, TREES_NEW: 1, TREE_LABELS: 8, FREE_SPOTS: 30, BUILDINGS: 9, FACADES: 8, KERBS: 252, PROJECT_AREA: 5 }

export function toDxf(d) {
  const o = []
  const g = (...kv) => { for (let i = 0; i < kv.length; i += 2) o.push(kv[i], typeof kv[i + 1] === 'number' ? kv[i + 1].toFixed(3) : kv[i + 1]) }
  const f = (n) => +n.toFixed(3)
  g(0, 'SECTION', 2, 'HEADER', 9, '$INSUNITS', 70, '6', 0, 'ENDSEC') // 6 = metres
  g(0, 'SECTION', 2, 'TABLES', 0, 'TABLE', 2, 'LAYER', 70, String(Object.keys(LAYERS).length))
  for (const [name, col] of Object.entries(LAYERS)) g(0, 'LAYER', 2, name, 70, '0', 62, String(col), 6, 'CONTINUOUS')
  g(0, 'ENDTAB', 0, 'ENDSEC', 0, 'SECTION', 2, 'ENTITIES')
  const poly = (layer, pts, closed, thick = 0) => {
    g(0, 'POLYLINE', 8, layer, 66, '1', 70, closed ? '1' : '0')
    if (thick) g(39, f(thick)) // extrusion height: buildings come out as 3D blocks in CAD
    for (const [x, y] of pts) g(0, 'VERTEX', 8, layer, 10, f(x), 20, f(y), 30, 0)
    g(0, 'SEQEND', 8, layer)
  }
  for (const t of d.trees) {
    const layer = t.status === 'existing' ? 'TREES_EXISTING' : 'TREES_NEW'
    const [x, y] = t.xy
    g(0, 'CIRCLE', 8, layer, 10, f(x), 20, f(y), 30, 0, 40, f(t.crown_diam_m / 2))
    g(0, 'POINT', 8, layer, 10, f(x), 20, f(y), 30, 0)
    g(0, 'TEXT', 8, 'TREE_LABELS', 10, f(x + 0.4), 20, f(y + 0.4), 30, 0, 40, 0.6, 1, t.species)
  }
  for (const s of d.spots) {
    g(0, 'POINT', 8, 'FREE_SPOTS', 10, f(s.xy[0]), 20, f(s.xy[1]), 30, 0)
    g(0, 'CIRCLE', 8, 'FREE_SPOTS', 10, f(s.xy[0]), 20, f(s.xy[1]), 30, 0, 40, 0.5)
  }
  for (const b of d.buildings) for (const r of b.rings) poly('BUILDINGS', r.slice(0, -1), true, b.height_m)
  for (const e of d.edges) poly(e.kind === 'facade' ? 'FACADES' : 'KERBS', e.line, false)
  if (d.area) poly('PROJECT_AREA', d.area, true)
  g(0, 'ENDSEC', 0, 'EOF')
  return o.join('\n') + '\n'
}

// ---- GeoPackage (OGC GeoPackage 1.2, SQLite via sql.js, loaded only when used) ----------------------------------
// Geometries: GeoPackage binary header + little-endian WKB (point 1, line 2, polygon 3), srs_id 25831.
function gpkgGeom(type, coords) {
  const n = type === 1 ? 1 : type === 2 ? coords.length : coords.reduce((a, r) => a + r.length, 0)
  const size = 8 + 5 + (type === 1 ? 16 : type === 2 ? 4 + 16 * n : 4 + coords.length * 4 + 16 * n)
  const dv = new DataView(new ArrayBuffer(size))
  let o = 0
  dv.setUint8(o++, 0x47); dv.setUint8(o++, 0x50); dv.setUint8(o++, 0); dv.setUint8(o++, 1) // 'GP', v0, LE, no envelope
  dv.setInt32(o, 25831, true); o += 4
  dv.setUint8(o++, 1); dv.setUint32(o, type, true); o += 4
  const pt = ([x, y]) => { dv.setFloat64(o, x, true); dv.setFloat64(o + 8, y, true); o += 16 }
  if (type === 1) pt(coords)
  else if (type === 2) { dv.setUint32(o, coords.length, true); o += 4; coords.forEach(pt) }
  else { dv.setUint32(o, coords.length, true); o += 4; for (const r of coords) { dv.setUint32(o, r.length, true); o += 4; r.forEach(pt) } }
  return new Uint8Array(dv.buffer)
}

const UTM31N = 'PROJCS["ETRS89 / UTM zone 31N",GEOGCS["ETRS89",DATUM["European_Terrestrial_Reference_System_1989",SPHEROID["GRS 1980",6378137,298.257222101]],PRIMEM["Greenwich",0],UNIT["degree",0.0174532925199433]],PROJECTION["Transverse_Mercator"],PARAMETER["latitude_of_origin",0],PARAMETER["central_meridian",3],PARAMETER["scale_factor",0.9996],PARAMETER["false_easting",500000],PARAMETER["false_northing",0],UNIT["metre",1],AUTHORITY["EPSG","25831"]]'

export async function toGpkg(d) {
  const [{ default: initSqlJs }, { default: wasmUrl }] = await Promise.all([import('sql.js'), import('sql.js/dist/sql-wasm.wasm?url')])
  const SQL = await initSqlJs({ locateFile: () => wasmUrl })
  const db = new SQL.Database()
  db.run(`PRAGMA application_id = 1196444487; PRAGMA user_version = 10200;
    CREATE TABLE gpkg_spatial_ref_sys (srs_name TEXT NOT NULL, srs_id INTEGER PRIMARY KEY, organization TEXT NOT NULL,
      organization_coordsys_id INTEGER NOT NULL, definition TEXT NOT NULL, description TEXT);
    CREATE TABLE gpkg_contents (table_name TEXT PRIMARY KEY, data_type TEXT NOT NULL, identifier TEXT UNIQUE, description TEXT DEFAULT '',
      last_change DATETIME NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now')), min_x DOUBLE, min_y DOUBLE, max_x DOUBLE, max_y DOUBLE, srs_id INTEGER);
    CREATE TABLE gpkg_geometry_columns (table_name TEXT NOT NULL, column_name TEXT NOT NULL, geometry_type_name TEXT NOT NULL,
      srs_id INTEGER NOT NULL, z TINYINT NOT NULL, m TINYINT NOT NULL, PRIMARY KEY (table_name, column_name));`)
  db.run('INSERT INTO gpkg_spatial_ref_sys VALUES (?,?,?,?,?,?)', ['Undefined cartesian SRS', -1, 'NONE', -1, 'undefined', null])
  db.run('INSERT INTO gpkg_spatial_ref_sys VALUES (?,?,?,?,?,?)', ['Undefined geographic SRS', 0, 'NONE', 0, 'undefined', null])
  db.run('INSERT INTO gpkg_spatial_ref_sys VALUES (?,?,?,?,?,?)', ['WGS 84 geodetic', 4326, 'EPSG', 4326,
    'GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563]],PRIMEM["Greenwich",0],UNIT["degree",0.0174532925199433]]', null])
  db.run('INSERT INTO gpkg_spatial_ref_sys VALUES (?,?,?,?,?,?)', ['ETRS89 / UTM zone 31N', 25831, 'EPSG', 25831, UTM31N, null])

  const table = (name, gtype, cols, rows) => {
    if (!rows.length) return
    db.run(`CREATE TABLE "${name}" (fid INTEGER PRIMARY KEY AUTOINCREMENT, geom ${gtype}, ${cols.map(([c, t]) => `"${c}" ${t}`).join(', ')})`)
    const st = db.prepare(`INSERT INTO "${name}" (geom, ${cols.map(([c]) => `"${c}"`).join(', ')}) VALUES (${['?', ...cols.map(() => '?')].join(',')})`)
    let [x0, y0, x1, y1] = [Infinity, Infinity, -Infinity, -Infinity]
    for (const [geom, vals, pts] of rows) {
      st.run([geom, ...vals])
      for (const [x, y] of pts) { x0 = Math.min(x0, x); y0 = Math.min(y0, y); x1 = Math.max(x1, x); y1 = Math.max(y1, y) }
    }
    st.free()
    db.run('INSERT INTO gpkg_contents (table_name, data_type, identifier, min_x, min_y, max_x, max_y, srs_id) VALUES (?,?,?,?,?,?,?,?)',
      [name, 'features', name, x0, y0, x1, y1, 25831])
    db.run('INSERT INTO gpkg_geometry_columns VALUES (?,?,?,?,?,?)', [name, 'geom', gtype, 25831, 0, 0])
  }
  table('trees', 'POINT', [['tree_id', 'TEXT'], ['species', 'TEXT'], ['status', 'TEXT'], ['crown_diam_m', 'REAL'], ['height_m', 'REAL'], ['crown_base_m', 'REAL']],
    d.trees.map((t) => [gpkgGeom(1, t.xy), [t.id, t.species, t.status, t.crown_diam_m, t.height_m, t.crown_base_m], [t.xy]]))
  table('free_spots', 'POINT', [['spot_id', 'TEXT'], ['size_class', 'TEXT'], ['sidewalk_width_m', 'REAL']],
    d.spots.map((s) => [gpkgGeom(1, s.xy), [s.id, s.size_class, s.width_m], [s.xy]]))
  table('buildings', 'POLYGON', [['height_m', 'REAL']], d.buildings.map((b) => [gpkgGeom(3, b.rings), [b.height_m], b.rings[0]]))
  table('sidewalk_edges', 'LINESTRING', [['kind', 'TEXT']], d.edges.map((e) => [gpkgGeom(2, e.line), [e.kind], e.line]))
  if (d.area) {
    const ring = [...d.area, d.area[0]]
    table('project_area', 'POLYGON', [['name', 'TEXT']], [[gpkgGeom(3, [ring]), ['project area'], ring]])
  }
  const bytes = db.export()
  db.close()
  return bytes
}

export async function download(format) {
  const d = await collect()
  const name = `${state.site}_${state.area ? 'project_area' : 'site'}`
  const [data, type, ext] = format === 'dxf' ? [toDxf(d), 'application/dxf', 'dxf'] : [await toGpkg(d), 'application/geopackage+sqlite3', 'gpkg']
  const a = Object.assign(document.createElement('a'), { download: `${name}.${ext}`, href: URL.createObjectURL(new Blob([data], { type })) })
  a.click()
  URL.revokeObjectURL(a.href)
  return { trees: d.trees.length, spots: d.spots.length, buildings: d.buildings.length }
}
