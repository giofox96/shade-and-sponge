// Short guided tour (v0.2.0, feedback 27 Nov): a pulsing ring around one element and a balloon that says what it does.
// Tours are lists of { sel, text }; a missing element is skipped. Each tour plays once per browser; "?" replays it.
import { reactive, nextTick } from 'vue'

const KEY = 'shade-sponge-coach'
const seen = (() => { try { return new Set(JSON.parse(localStorage.getItem(KEY)) ?? []) } catch { return new Set() } })()
export const coach = reactive({ name: null, steps: [], i: 0, rect: null })

export function place() {
  const el = coach.name && document.querySelector(coach.steps[coach.i]?.sel)
  if (!el && coach.name && coach.i < coach.steps.length) return void next() // nothing to point at: go on
  coach.rect = el ? el.getBoundingClientRect() : null
}
export async function startCoach(name, steps, force = false) {
  if (!force && seen.has(name)) return
  Object.assign(coach, { name, steps, i: 0, rect: null })
  await nextTick()
  setTimeout(place, 450) // after the step's slide-in
}
export function next() {
  coach.i++
  if (coach.i >= coach.steps.length) return stop()
  setTimeout(place, 50)
}
export function stop() {
  if (coach.name) seen.add(coach.name)
  try { localStorage.setItem(KEY, JSON.stringify([...seen])) } catch { /* storage blocked */ }
  Object.assign(coach, { name: null, steps: [], i: 0, rect: null })
}
