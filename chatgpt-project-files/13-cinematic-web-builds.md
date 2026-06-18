# Brandon's Kung Fu — Cinematic & Interactive Web Builds

> **Status:** v0.3.0. Optional / advanced. Generic routing and supervision
> doctrine for motion-led, 3D, and interactive web work — no proprietary names, no
> business goals, no private paths, no third-party skill bodies. Vendor-neutral:
> "the engine" is whatever rendering or animation library the build uses. Upload
> this file only while cinematic / interactive web work is active.

This file teaches the conductor how to scope, lane, route, and verify a
**cinematic or interactive web build** — the visual, motion-heavy, or 3D work that
a standard CRUD-UI task template under-specifies. It adds the extra discipline this
class of work needs; it does not replace `03-driving-coding-agents.md` or
`06-skills-and-routing.md`, it sits on top of them.

## What counts as a cinematic / interactive build

This file applies when the *experience* is the deliverable, not just the data.
Signals:

- **3D / WebGL / GPU** — a scene, model, or rendered surface (3D engines, WebGL,
  shaders, generative visuals).
- **Motion-led** — the value is in animation, transitions, or choreography, not a
  static layout.
- **Scroll- or pointer-driven** — the page reacts continuously to scroll, cursor,
  gesture, or device motion.
- **Immersive surface** — a landing hero, product showcase, or interactive story
  where polish and feel are the point.

If the work is ordinary forms, tables, and CRUD screens, use the normal coding-
standards and driving-agents files — not this one. Mixed builds: apply this file
only to the cinematic surface, the standard files to the rest.

## Lane the work first

Most *bounded* cinematic work (one component, one scene, behind a flag) is **Green
Lane**. It turns **Red** the moment it touches anything below — treat these as
Red until proven otherwise:

- **Heavy new dependencies** — a 3D engine, physics, or large animation runtime is
  a bundle-size and supply-chain decision, not a casual import (see
  `07-safety-and-scrub.md` and `02-coding-standards.md`).
- **Build / bundle config** — loaders, asset pipelines, code-splitting, or
  shader/GLSL build steps.
- **Performance-critical paths** — anything on the first-paint or main-thread
  budget of a shipping page.
- **Asset rights** — models, textures, fonts, audio, or capture with unclear
  licensing or provenance.

Lane the *spectacle* conservatively: a demo that regresses load time or locks out a
low-power device is a real defect, not a polish note.

## Route by capability, not by name

There is **no cinematic skill cluster in this kit's catalog** (`../skills/SKILLS.md`
covers core workflow, RAG/CAG, QA, and security only). So route by the **dominant
axis** of the work, to whatever skill **actually exists in your pack** — never
invent a `/slash` name, never link an unresolved one (`06-skills-and-routing.md`).

Name the axis first, then pick the capability:

- **3D / WebGL scene** → a 3D/WebGL capability (scene graph, camera, lighting,
  loaders).
- **Shader / generative** → a shader/GLSL capability.
- **Motion / animation** → a timeline or animation capability.
- **Scroll / pointer choreography** → a scroll-experience capability.
- **Visual direction / design polish** → a frontend-design or UI-direction
  capability.
- **Performance** → a web-performance / profiling capability.
- **Accessibility / motion safety** → an accessibility-audit capability.

If your pack has a skill for the axis, route to it by its **real name**; if it does
not, treat the technique as a **distilled prose pattern** and drive the agent
directly. Most cinematic builds span several axes — pick the **one** that dominates
the current slice and route that, rather than chaining four skills at once.

## The cinematic task box

The six-part task template (`03-driving-coding-agents.md`) still applies, plus four
extra fields this work fails without:

- **Target & budget** — the device floor (e.g. mid-tier laptop / phone) and the
  perf budget it must hold (frame time, bundle weight, load metric).
- **Motion behavior** — what `prefers-reduced-motion` does, and that no content is
  *only* reachable through animation.
- **Fallback** — what a no-WebGL, low-power, or reduced-motion visitor sees. There
  is always a fallback; "it just breaks" is not one.
- **Visual acceptance** — what *done* looks like, concretely enough to check
  (reference, states, the feel in one sentence) — not "make it cinematic."

A cinematic task with no budget, no fallback, and no acceptance picture is where
the agent burns hours and the result still misses.

## Verify with eyes and numbers, not vibes

"Looks cool" is not verification. Require evidence, the same as any other build:

- **Visual evidence** — a screenshot or short capture of the actual running build,
  not a description (`05-qa-and-debug.md`). Browser-driving / capture commands are
  **RED** — gate them per `06-skills-and-routing.md`.
- **Performance numbers** — frame budget held, bundle size, and the load metric,
  measured on the target device floor, not the dev machine.
- **Fallback proven** — the no-WebGL / reduced-motion path actually rendered and
  was checked, not assumed.
- **Re-verify yourself** — re-run or re-measure; do not accept "it's smooth" on
  faith.

## Performance is a gate, not a polish step

Frame rate and weight are acceptance criteria, decided before the build, not
tuned after it ships:

- **Budget first** — set the frame and bundle budget in the task; the build is
  judged against it.
- **Split the heavy engine** — lazy-load and code-split the renderer so a non-
  cinematic visitor never pays for it.
- **Watch the obvious costs** — draw calls, oversized textures, uncompressed
  assets, layout thrash, and animation on non-composited properties.
- **Measure on the floor device** — a desktop GPU hides the regression a mid-tier
  phone will feel.

## Accessibility and motion safety

Spectacle never overrides access. Non-negotiable:

- **Honor `prefers-reduced-motion`** — a calm, equivalent experience, not a broken
  one.
- **No seizure risk** — avoid high-frequency flashing and harsh strobing.
- **Keyboard and focus survive** — interactive scenes stay operable without a
  pointer; focus is never trapped in a canvas.
- **Content is not animation-gated** — text and actions are reachable even if the
  motion never runs.

Accessibility regressions in cinematic work are common and easy to miss — make them
an explicit verification line, not an afterthought.

## Asset and dependency discipline

Cinematic builds pull in the heaviest, least-vetted third-party material in the
stack. Apply the kit's safety posture (`07-safety-and-scrub.md`):

- **License every asset** — models, textures, fonts, audio, and captured media
  carry rights; unverified provenance is a Red-Lane stop, not a default-yes.
- **Weigh every dependency** — a multi-megabyte engine is a deliberate decision
  with a bundle-size cost, audited, not slipped in.
- **No vendored proprietary assets** — never commit private or unlicensed media,
  and never bake a private path or remote into a loader.
- **Third-party stays referenced** — engines and packs are installed from upstream,
  not copied into the repo wholesale.

## Scope-box the spectacle

Cinematic scope creeps faster than any other kind. Hold the line:

- **Smallest impressive slice first** — ship one scene or one transition that
  lands, then iterate; do not build the whole experience before anything is seen.
- **Keep the plain path working** — the non-cinematic version stays shippable, so a
  stalled effect never blocks the release.
- **HALT on drift** — if the agent gilds beyond the boxed slice, stop and re-scope
  (`03-driving-coding-agents.md`).

## Related project files

- `02-coding-standards.md` — the quality bar, including dependency and bundle
  discipline.
- `03-driving-coding-agents.md` — the six-part task template and supervision rules.
- `05-qa-and-debug.md` — verification and browser-evidence discipline.
- `06-skills-and-routing.md` — routing rules and the never-invent-a-name rule.
- `07-safety-and-scrub.md` — asset rights, dependency vetting, and the public
  boundary.
