// Potentials of a new tree position, computed in the browser with the formulas of shade_sponge (layout.shade_potential,
// layout.water_potential, layout.fits, heat.shadow_xy_area, heat.opacity, season.factor) on the site grid exported by
// web_export.py (grid.bin.gz: per-hour sun bits for the summer and winter design days, ground flags, façade distance).

export async function loadGrid(url, g) {
  let buf = await (await fetch(url)).arrayBuffer()
  const head = new Uint8Array(buf, 0, 2)
  if (head[0] === 0x1f && head[1] === 0x8b) // still gzipped (static hosts); dev servers may already have decoded it
    buf = await new Response(new Blob([buf]).stream().pipeThrough(new DecompressionStream('gzip'))).arrayBuffer()
  const n = g.W * g.H
  const u8 = new Uint8Array(buf)
  // lon/lat -> grid metres: affine through three corners (bl, tl, br); over 1 km the UTM grid is affine to < 0.1 m
  const [bl, tl, , br] = g.corners
  const X0 = g.x0, Y0 = g.y1 - g.H * g.res, X1 = g.x0 + g.W * g.res, Y1 = g.y1
  const det = (tl[0] - bl[0]) * (br[1] - bl[1]) - (br[0] - bl[0]) * (tl[1] - bl[1])
  const toXY = (lon, lat) => {
    const u = ((lon - bl[0]) * (br[1] - bl[1]) - (br[0] - bl[0]) * (lat - bl[1])) / det // along bl->tl
    const v = ((tl[0] - bl[0]) * (lat - bl[1]) - (lon - bl[0]) * (tl[1] - bl[1])) / det // along bl->br
    return [X0 + v * (X1 - X0), Y0 + u * (Y1 - Y0)]
  }
  return {
    ...g,
    summer: u8.subarray(0, n),
    winter: u8.subarray(n, 2 * n),
    flags: u8.subarray(2 * n, 3 * n), // bit 0 open ground in the site, bit 1 drains to a hotspot, bit 2 roof
    facade: new Uint16Array(buf.slice(3 * n, 5 * n)), // distance to the nearest building, decimetres
    toXY,
  }
}

const rc = (G, x, y) => [
  Math.min(G.H - 1, Math.max(0, Math.floor((G.y1 - y) / G.res))),
  Math.min(G.W - 1, Math.max(0, Math.floor((x - G.x0) / G.res))),
]

// Mean of a per-cell 0/1 value over an n x n window around (r, c), as scipy.ndimage.uniform_filter (reflect at edges)
function boxMean(G, r, c, n, value) {
  const s = Math.floor(n / 2)
  const refl = (i, N) => (i < 0 ? -i - 1 : i >= N ? 2 * N - i - 1 : i)
  let sum = 0
  for (let i = r - s; i < r - s + n; i++) {
    const ri = refl(i, G.H) * G.W
    for (let j = c - s; j < c - s + n; j++) sum += value(ri + refl(j, G.W))
  }
  return sum / (n * n)
}

export function opacity(sp, month, K, OP_BARE) {
  const f = sp.leaf[month - 1]
  return f * (1 - Math.exp(-K * sp.lai)) + (1 - f) * OP_BARE
}

// Potentials of every palette species at (lon, lat): { x, y, inSite, onRoof, facade_m, fit[], summer[], winter[], water[] }
export function pointPotentials(G, M, lon, lat) {
  const [x, y] = G.toXY(lon, lat)
  const [r, c] = rc(G, x, y)
  const k = r * G.W + c
  const P = M.model
  const facade = G.facade[k] / 10
  const species = M.palette.filter((s) => s.in_palette)
  const out = { x, y, inSite: (G.flags[k] & 1) === 1, onRoof: (G.flags[k] & 4) === 4, facade_m: facade,
    fit: [], summer: [], winter: [], water: [] }
  for (const sp of species) {
    const a = sp.crown_diam_m / 2
    const b = Math.max(sp.height_m - sp.crown_base_m, 1) / 2
    const zc = (sp.height_m + sp.crown_base_m) / 2
    for (const season of ['summer', 'winter']) {
      const op = opacity(sp, P.months[season], P.K, P.OP_BARE)
      let tot = 0
      P.suns[season].forEach(([alt, az], h) => {
        const along = Math.sqrt(a * a * Math.sin(alt) ** 2 + b * b * Math.cos(alt) ** 2) / Math.sin(alt)
        const off = Math.max(zc - P.Z_PED, 0) / Math.tan(alt)
        const area = Math.PI * a * along
        const [r2, c2] = rc(G, x - off * Math.sin(az), y - off * Math.cos(az))
        const n = Math.max(1, Math.round(Math.sqrt(area) / G.res))
        tot += boxMean(G, r2, c2, n, (q) => (G[season][q] >> h) & 1 & G.flags[q]) * area * op
      })
      out[season].push(tot)
    }
    const stor = P.storms.reduce((acc, [m, w]) => {
      const g = P.R_OFF + (1 - P.R_OFF) * sp.leaf[m - 1]
      return acc + w * Math.min(P.p_mm, P.s_mm_per_lai * sp.lai * g)
    }, 0) / P.storms.reduce((acc, [, w]) => acc + w, 0)
    const n = Math.max(1, Math.round(sp.crown_diam_m / G.res))
    out.water.push(boxMean(G, r, c, n, (q) => (G.flags[q] & 3) === 3 ? 1 : 0) * Math.PI * a * a * stor / 1000)
    out.fit.push(facade >= a ? 1 : 0)
  }
  const share = (season) => P.suns[season].reduce((acc, _, h) => acc + ((G[season][k] >> h) & 1), 0) / P.suns[season].length
  out.sun_summer = share('summer')
  out.sun_winter = share('winter')
  out.drains_to_hotspot = boxMean(G, r, c, 6, (q) => ((G.flags[q] & 2) && !(G.flags[q] & 4) ? 1 : 0)) // as web_export / positions file
  if (!out.fit.some(Boolean)) out.fit[species.reduce((m, s, j) => (s.crown_diam_m < species[m].crown_diam_m ? j : m), 0)] = 1
  return out
}
