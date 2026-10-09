// Live re-optimisation in the browser: the same transportation LP as shade_sponge/layout.py (assign + sweep scoring),
// solved with HiGHS compiled to WebAssembly, on the per-position potentials exported by web_export.py.
// The resulting metrics are estimates: potentials ignore crown overlaps, so they are calibrated on the saved layouts.
import loadHighs from 'highs'
import wasmUrl from 'highs/runtime?url'

let highs
const solver = () => (highs ??= loadHighs({ locateFile: () => wasmUrl }))

const OBJS = [['shade_summer', 1], ['shade_winter', -1], ['water', 1]] // weights order: summer, winter, runoff

export function caps(pot, share, exclude) {
  return pot.species.map((s, j) => (exclude.includes(s) ? 0 : Math.max(0, Math.floor(share * pot.n_total) - pot.kept[j])))
}

// extra: designer-added trees ({ pot: { summer, winter, water, fit }, species, auto }); a species the designer fixed is kept
export async function optimise(pot, weights, { share = pot.max_share, exclude = [], extra = [] } = {}) {
  const P = pot.fit.length + extra.length
  const val = (k, i, j) => (i < pot.fit.length ? pot[k][i][j] : extra[i - pot.fit.length].pot[{ shade_summer: 'summer', shade_winter: 'winter', water: 'water' }[k]][j])
  const fits = (i, j) => (i < pot.fit.length ? pot.fit[i][j] : extra[i - pot.fit.length].auto ? extra[i - pot.fit.length].pot.fit[j] : +(extra[i - pot.fit.length].species === j))
  const S = pot.species.length
  const mx = OBJS.map(([k]) => Math.max(...pot[k].flat()))
  const norm = (i, j) => OBJS.map(([k, sign], n) => (sign * val(k, i, j)) / mx[n])
  const cap = caps({ ...pot, n_total: pot.n_total + extra.length }, share, exclude)
  const obj = []
  const rows = []
  const col = Array.from({ length: S }, () => [])
  for (let i = 0; i < P; i++) {
    const r = []
    for (let j = 0; j < S; j++) {
      if (!fits(i, j) || !cap[j]) continue
      const z = norm(i, j)
      const sc = weights.reduce((a, w, n) => a + w * z[n], 0) + 1e-3 * z.reduce((a, b) => a + b, 0)
      obj.push(`${sc < 0 ? '-' : '+'} ${Math.abs(sc).toFixed(9)} x${i}_${j}`)
      r.push(`x${i}_${j}`)
      col[j].push(`x${i}_${j}`)
    }
    if (!r.length) return { error: 'Some positions have no species that both fits and has room under the cap. Raise the max share or allow more species.' }
    rows.push(` p${i}: ${r.join(' + ')} = 1`)
  }
  col.forEach((c, j) => c.length && rows.push(` s${j}: ${c.join(' + ')} <= ${cap[j]}`))
  const lp = `Maximize\n obj: ${obj.join('\n  ')}\nSubject To\n${rows.join('\n')}\nEnd`

  const t0 = performance.now()
  const res = (await solver()).solve(lp, { output_flag: false })
  if (res.Status !== 'Optimal') return { error: `No layout satisfies the caps (${res.Status}). Raise the max share or allow more species.` }
  const layout = Array.from({ length: P }, (_, i) => {
    let best = -1
    let bv = -1
    for (let j = 0; j < S; j++) {
      const v = res.Columns[`x${i}_${j}`]?.Primal ?? -1
      if (v > bv) [best, bv] = [j, v]
    }
    return best
  })
  return { layout, ms: Math.round(performance.now() - t0) }
}

// Sum of the single-tree potentials of a layout (palette indices; indices beyond the palette, e.g. planes, add 0)
export function proxySums(pot, layout) {
  const s = { shade_summer: 0, shade_winter: 0, water: 0 }
  layout.forEach((j, i) => {
    if (j < pot.species.length) for (const k in s) s[k] += pot[k][i][j]
  })
  return s
}

// Least-squares line exact = a + b * proxy over the saved layouts, with R²
export function fitLine(xs, ys) {
  const n = xs.length
  const mx = xs.reduce((a, b) => a + b, 0) / n
  const my = ys.reduce((a, b) => a + b, 0) / n
  let sxy = 0
  let sxx = 0
  let syy = 0
  xs.forEach((x, k) => {
    sxy += (x - mx) * (ys[k] - my)
    sxx += (x - mx) ** 2
    syy += (ys[k] - my) ** 2
  })
  const b = sxx ? sxy / sxx : 0
  return { a: my - b * mx, b, r2: sxx && syy ? (sxy * sxy) / (sxx * syy) : 0 }
}
