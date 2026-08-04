---
name: faceless-explainer-build
description: Build a FULLY FACELESS long-form explainer for Amreet Talks — full-screen Remotion motion graphics covering 100% of the runtime (the creator's recording is VO ONLY, the face is never shown). Dense "takeover" hook clips + calmer "gap" explainer clips fill the whole timeline as straight V2 drops, word-synced to the VO captions, delivered with a one-import FCPXML assembly (all clips on the spine + every SFX hit on audio lanes). TRIGGER on "build the graphics for <video>", "make it faceless", "cover the whole timeline with motion graphics", "80%/100% graphics", or any ask for MORE visual density on an Amreet Talks long-form. Canonical build: remotion-all/src/AIKillSwitch/ (clips/gapKit.tsx + clips/Gap1..9.tsx) + scripts/killswitch_sfx_fcpxml.py.
metadata:
  tags: remotion, faceless, explainer, motion-graphics, takeover, gap-clips, fcpxml, davinci, sfx, hinglish
---

## When to use

An **Amreet Talks long-form** needs its visuals built (or needs more coverage). The creator's
recording — even if it's a talking-head take — is a **voice-over source only**. The deliverable
is full-screen motion graphics for the ENTIRE runtime + a drop-in assembly for Resolve.

- **NOT** overlays/PiP around a visible face. That was built once and rejected outright
  ("the whole timeline is without my face"). Never propose it again.
- **NOT** for Shorts (creator-shot-short — there the face IS the spine) or gameplay reels
  (remotion-highlight-reel).

## Core principle

> **Face never shown. Voice carries the argument; full-screen boards carry the eyes.
> Coverage target is 100% of the runtime — takeovers for the hooks, gap clips for the body.**

## The two clip registers

| | Takeovers (hooks) | Gap clips (explainer body) |
|---|---|---|
| Length | 8–14s | 12–45s (exact gap length) |
| Camera | ~1 station / 3–4s, showstopper set-pieces | ~1 station / **6–9s**, station–hold–drift |
| When | Cold open, section punches, showstoppers | Everything between takeovers |

Both use the same skeleton: `AbsoluteFill(bg)` → `SfxTrack` → `EnterExit` → [`Board`,
`MoStage(world)`, screen-fixed lockups, persistent `CaseTag`, `Vignette`] → `ImpactFlash*` →
`Letterbox`. Copy `GapClip` + `gapCam` from `remotion-all/src/AIKillSwitch/clips/gapKit.tsx`
(port per-video: palette/theme changes, grammar doesn't).

## Pipeline

1. **Cue map.** Pull the VO captions (SRT from the recording; `youtube-transcript-analysis`
   /whisper if needed). Extract per-line timestamps → every beat lands on a spoken word.
   Beats are clip-local frames: `f = (t_abs − clip_drop) × 30`. ±0.5s slip is fine.
2. **Coverage plan.** Table of clips with drop TC + duration where **every clip's end frame =
   the next clip's drop frame** (master @30fps, zero gaps, last clip ends exactly at runtime).
   If the VO outlasts the last clip, EXTEND that clip's `durationInFrames` (EnterExit's exit
   auto-moves to the new end) — never a Resolve freeze-frame. Safe only if the clip has no
   `<Sequence durationInFrames>` or duration-derived beats — check first.
3. **Beat sheets per gap clip.** VO order = station order. One camera station per beat
   cluster; during a hold a **new element must enter at least every ~5s** (sub-line, chip,
   dead-flip, unredact) — energy comes from the board, not the camera. Literal nameable
   devices only (stamps, docs, breakers, racks, clocks, tape); one red accent per frame.
4. **Build.** One file per clip on the gapKit scaffold; register in the video's `index.tsx`
   with EXACT gap durations. `npx tsc --noEmit` clean.
5. **Still QA (cheap loop).** `npx remotion bundle` ONCE, then
   `npx remotion still build <Comp> --frame=<busiest-beat> out.png` (no rebundle per still).
   Read every still. Check: letterbox band, world-y centering, drift-seam frames, text width.
   Fix → re-bundle → re-still only the affected frames.
6. **Render.** Default h264 config — `npx remotion render KS-<X> "/mnt/f/videoEditing/<video>/
   <takeovers|gaps>/<X>.mp4"` (no flags; DOM/canvas needs no --gl). Media on F:, never the
   repo. ffprobe every duration against the coverage table.
7. **SFX + assembly.** Sparse `SfxTrack` cues baked quiet (whoosh per flight, pop per chip,
   impact per stamp/strike, riser before big lands). Mirror every cue into the video's FCPXML
   generator (pattern: `scripts/killswitch_sfx_fcpxml.py` — CLIPS table of
   `(name, drop_at, dur, [(cue, local_f, vol)])`). Regenerate AFTER rendering (it asserts the
   MP4s exist). **The FCPXML is the deliverable**: all clips on the spine at their offsets +
   every hit on audio lanes = the user imports ONE file, adds VO + music, mutes baked audio.
   The summary line (`N clips, Mf ≈ Ss`) is the continuity check — must equal the runtime.
8. **Cut-sheet.** Rewrite `cut-sheet.md`: the one-import path first, then the full drop table
   (file, drop TC, dur, out TC, one-line description), music/grade notes, re-render recipes.

## Hard-won gotchas (each of these bit once)

- **`camAt()` lerps from the previous key's TARGET cam**, not the mid-flight position. A key
  starting before the previous key's `trans` completes = visible camera pop. `gapCam` fixes
  this by construction: after each station it emits a drift key (z +0.02–0.03, glide) whose
  trans ends EXACTLY at the next depart. Flights ~40f settle; arrive ≥2f before the beat
  (`depart = beatAt − trans − 2..6`).
- **Letterbox = 84px bars.** Screen-fixed lockups live in y 108–980 (bottom strips: flex-end
  + `paddingBottom: 132`). World content: the visible band center is the cam's `cy` (~880) —
  so a block's anchor `y ≈ 880 − blockHeight/2`. Anchoring tall blocks (server racks, stamps
  + subs) at y < ~500 clips them behind the top bar.
- **`Headline markWord` slabs exactly ONE word.** Multi-word red phrases → `RedSlab` under
  the headline or an `R` span in a BoardLine.
- **`MonoCounter` cannot tick backward** (by design). "Rewind" beats = a CCW-spinning clock
  device, not a down-counter.
- **`StrikeReplace` shows its `from` text from mount** — gate it (`StrikeBlock` wraps it in a
  `useEnter` + `frame >= at` guard).
- Punch lines that must survive a camera flight (final answers, REFUSED-style stamps mid-
  flight) are **screen-fixed**, not world content. For a coda pull-back with a screen-fixed
  lockup, aim the coda camera at an EMPTY patch of world so background text doesn't collide.
- Codas (z .33–.42 glide over the whole wall) only where the next takeover doesn't open wide;
  otherwise end on a slow push (drift) for a tension handoff.
- Straight cuts everywhere: every clip's `EnterExit` bakes the junction grammar. No dissolves.
- Alpha/ProRes flags are ONLY for the (archived) overlay track — never touch
  `remotion.config.ts`; takeover/gap MP4s use the default JPEG/h264 path.

## Canonical reference (copy from here)

- Scaffold + grammar: `remotion-all/src/AIKillSwitch/clips/gapKit.tsx`
- 9 worked examples (station maps, cascades, verdict boards, DotField blast, quote exhibit,
  strike finales): `remotion-all/src/AIKillSwitch/clips/Gap1.tsx … Gap9.tsx`
- Engine: `src/AIKillSwitch/mg/` (Stage/Cards/Kinetic/Board/motion) + `components/`
- Assembly generator: `scripts/killswitch_sfx_fcpxml.py`
- Delivered example: `channels/Amreet Talks/videos/AI Kill Switch/cut-sheet.md` (v3)

## Verification

- `tsc` clean → stills at every clip's busiest beats (Read them, actually look) → render →
  ffprobe durations vs the coverage table → FCPXML summary = exact runtime, zero `<gap>`s →
  cut-sheet table adds up (each Out = next Drop).
