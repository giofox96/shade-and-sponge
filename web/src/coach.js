// Short guided tour (v0.2.0, feedback 27 Nov): a pulsing ring around one element and a balloon that says what it does.
// Tours are lists of { sel, text }; a missing element is skipped. Each tour plays once per browser; "?" replays it.
import { reactive, nextTick } from 'vue'

const KEY = 'shade-sponge-coach'
const seen = (() => { try { return new Set(JSON.parse(localStorage.getItem(KEY)) ?? []) } catch { return new Set() } })()
export const coach = reactive({ name: null, steps: [], i: 0, rect: null })
// the welcome screen asks once: tips on or off (user 27 Nov); "?" still replays a step's tips
const TIPS = 'shade-sponge-tips'
export const tips = reactive({ on: (() => { try { return localStorage.getItem(TIPS) !== 'off' } catch { return true } })() })
export function setTips(on) {
  tips.on = on
  try { localStorage.setItem(TIPS, on ? 'on' : 'off') } catch { /* storage blocked */ }
}
let follow = null // re-measure the target while the tip shows: cards slide in and panels scroll (user 27 Nov: boxes off target)

export function place() {
  const el = coach.name && document.querySelector(coach.steps[coach.i]?.sel)
  if (!el && coach.name && coach.i < coach.steps.length) return void next() // nothing to point at: go on
  coach.rect = el ? el.getBoundingClientRect() : null
}
export async function startCoach(name, steps, force = false) {
  if (!force && (seen.has(name) || !tips.on)) return
  Object.assign(coach, { name, steps, i: 0, rect: null })
  await nextTick()
  setTimeout(place, 450) // after the step's slide-in
  clearInterval(follow)
  follow = setInterval(() => coach.name && coach.rect && place(), 200)
}
export function next() {
  coach.i++
  if (coach.i >= coach.steps.length) return stop()
  setTimeout(place, 50)
}
export function stop() {
  if (coach.name) seen.add(coach.name)
  try { localStorage.setItem(KEY, JSON.stringify([...seen])) } catch { /* storage blocked */ }
  clearInterval(follow)
  Object.assign(coach, { name: null, steps: [], i: 0, rect: null })
}
