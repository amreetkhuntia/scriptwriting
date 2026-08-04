---
name: remotion-highlight-reel
description: Assemble cut gameplay clips into a connected highlight-reel composition in the remotion-all project — cold-open hook, manifest-driven hard-cut sequence, act lower-thirds, reaction callouts, render to /mnt/f. Use after vod-clip-extraction to build the reel.
metadata:
  tags: remotion, highlight-reel, offthreadvideo, series, gameplay, 2k
---

## When to use

To turn clips cut by [vod-clip-extraction] into a single connected reel in
`remotion-all/`. Read `docs/motion-graphics-guide.md` and the
`remotion-best-practices` skill for the general Remotion rules; this skill is the
reel-specific pattern. **Canonical implementation: `remotion-all/src/Bond007/`** —
copy it for a new video.

## Design principles (why it feels like one story)

- **Clean scene boundaries + merges** are done at the clip stage ([vod-clip-extraction]).
  The reel just plays complete scenes in order, so the game's own narration carries
  across cuts. This is the fix for "it looks like disconnected clips."
- **Cold-open hook**: a ~5 s dramatic teaser (e.g. the villain's "now you die")
  → hard cut → a punchy title slam → the story. Hooks first, explains after.
- **Hard cuts only.** Use `<Series>`, NOT `<TransitionSeries>` — leave fades/
  transitions to the NLE (the user finishes in DaVinci). Overlays (lower-thirds,
  callouts) are the only motion graphics baked in.

## Folder structure (mirror `src/Bond007/`)

```
remotion-all/src/<Video>/
  index.tsx          # registers one <Composition id="<Video>-Highlights"> (2560x1440 @ 30fps)
  clips.ts           # the manifest: clip files, frame counts, lower-thirds, callouts (single source of truth)
  Reel.tsx           # the assembly: <Series> of Teaser → ColdOpenTitle → clips → OutroCard
  theme.ts           # palette + fonts
  ColdOpenTitle.tsx  # the title slam
  LowerThird.tsx     # gold act-label, bottom-left
  ReactionCallout.tsx# spring-pop streamer reaction
```
Register in `src/Root.tsx`: `import { <Video>Compositions } from "./<Video>"` and render it.

## The manifest (`clips.ts`) drives everything

```ts
export const CLIPS: ReelClip[] = [
  { file: "02_briefing.mp4", frames: 5189, beat: "...", src: "16:07-19:00",
    lowerThird: { label: "The Mission", sub: "Find Agent 009" } },
  { file: "06_auction_coup.mp4", frames: 7169, beat: "...", src: "...",
    callout: { text: "We sold Greenway 😅", at: 2520 } }, // `at` = clip-local frame
  // ...
];
export const TEASER_FILE = "00_teaser.mp4";
export const TEASER_FRAMES = 160; export const TITLE_FRAMES = 80; export const OUTRO_FRAMES = 120;
// hard cuts → total is a plain sum (no transition overlap to subtract):
export const reelDurationInFrames = () =>
  TEASER_FRAMES + TITLE_FRAMES + OUTRO_FRAMES + CLIPS.reduce((s, c) => s + c.frames, 0);
```
`frames` come from `vod-clip-extraction` step 5 (`floor(sec*30)-1`).

## Reel.tsx essentials

```tsx
<Series>
  <Series.Sequence durationInFrames={TEASER_FRAMES}><Teaser /></Series.Sequence>
  <Series.Sequence durationInFrames={TITLE_FRAMES}><ColdOpenTitle /></Series.Sequence>
  {CLIPS.map((clip) => (
    <Series.Sequence key={clip.file} durationInFrames={clip.frames}>
      <AbsoluteFill>
        <OffthreadVideo src={staticFile(`<proj>clips/${clip.file}`)}
          style={{ width: "100%", height: "100%", objectFit: "cover" }} />
        {clip.lowerThird && (
          <Sequence durationInFrames={Math.min(110, clip.frames)} layout="none"><LowerThird .../></Sequence>
        )}
        {clip.callout && (
          <Sequence from={clip.callout.at} durationInFrames={80} layout="none"><ReactionCallout .../></Sequence>
        )}
      </AbsoluteFill>
    </Series.Sequence>
  ))}
  <Series.Sequence durationInFrames={OUTRO_FRAMES}><OutroCard /></Series.Sequence>
</Series>
```
`staticFile("<proj>clips/...")` resolves through the public→/mnt/f symlink ([vod-clip-extraction] step 2). `objectFit: cover` fills the 2K canvas exactly.

## Gotchas (hard-won)

- **`<OffthreadVideo>` has NO audio in Studio preview** (audio is muxed only on
  render). To sanity-check sync, temporarily swap to `<Video>`, then revert.
- This is usually the project's **first video-playback composition** — `<Video>`/
  `<OffthreadVideo>` weren't used before; the graphics-only clips use `<Sequence>`.
- **Animate with `useCurrentFrame` + `interpolate`/`spring` only** (no CSS
  transitions — they don't render). Delayed `<Sequence from={N}>` defaults to
  top-left layout; add `layout="none"` (overlays are `AbsoluteFill` so it's safe).
- If you DO add transitions later: `<TransitionSeries>`'s `presentation` prop is
  invariant in its generic — mixing `fade()`/`wipe()`/`slide()` needs a cast to
  `TransitionPresentation<Record<string, unknown>>`. (But default to hard cuts.)
- Removing a `clips.ts` export while Studio is open throws a transient hot-reload
  WARNING until the importing file reloads — harmless, clears itself.

## Verify + render

```bash
cd remotion-all
npm run dev                              # Studio → scrub <Video>-Highlights
npx remotion still <Video>-Highlights --frame=<N> --scale=0.5 --output=/tmp/s.png  # spot-check a frame
npm run lint                             # eslint + tsc (ignore unrelated other-video errors)
npx remotion render <Video>-Highlights --output "/mnt/f/recordings/<proj>/<name>_highlights.mp4"
```
Render to /mnt/f (keep the big mp4 out of the repo). The output is the source
assembly with graphics + hard cuts — final trims/transitions happen in DaVinci.
