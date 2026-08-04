---
name: creator-shot-short
description: Build a ≤20s vertical "creator-shot" YouTube Short where the creator's OWN recording is the spine (their real voice + face carry the video) and motion-graphics only SUPPORT it — a short voiced hook (~3–4s) → the facecam clip with captions + on-beat supporting overlays (search/stat/tease) → CTA. Channel-agnostic pipeline that reads a per-channel brand pack (palette, fonts, component library, hook-VO voice). TRIGGER when turning a raw talking-head take into a funnel short, or phrases like "make a creator short", "cut a short from my recording", "talking-head short", "put my face in the reel", "short with my clip + graphics". Canonical build: remotion-all/src/AIJobs/clips/AIJobsReel1Talk.tsx.
metadata:
  tags: shorts, talking-head, remotion, offthreadvideo, captions, ffmpeg, vertical, 9x16, funnel
---

## When to use

Turn a **raw talking-head recording** (the creator on camera) into a **≤20s vertical Short** that funnels to a parent long-form. Use this when the creator wants *themselves* in the reel, not a faceless graphics explainer.

- **NOT** for pure-graphics reels (build those directly in the channel's `remotion-all` folder).
- **NOT** for gameplay highlight reels (that's [remotion-highlight-reel]).
- Pairs with a channel's existing `remotion-all/src/<Channel>/` component library for on-brand graphics.

## Core principle (this is the whole point)

> **The creator's recording is the spine. Their voice carries the argument. Graphics NEVER explain — they only support.**

This was learned the hard way. Rejected approaches:
- Pure graphics + full TTS VO → generic, no creator in it.
- Graphics tell the whole story, then a face clip is bolted on → **"two parallel explanations"** — the reel repeats itself in two voices. **Avoid.**
- A **silent** graphics hook → dead air; viewers scroll. **Every second needs audio.**

**One narrative — the creator's.** Overlays back up *what they say*, on their beats, and never bury their face.

## Locked structure (~18–20s, 1080×1920 @30fps)

| Seg | ~time | Content | Audio |
|---|---|---|---|
| **Hook** | 0–3.5s | Bold graphics (2 beats, e.g. "AI ISN'T COMING FOR YOUR JOB" → "BUT THIS IS"), **with a 3–4s voiceover** — never silent — then a whoosh | **hook VO** + whoosh |
| **Spine** | 3.5–~17s | The facecam clip (cropped vertical). Captions (channel's caption language). Supporting overlays pop on beats, kept in the **upper area** so the face stays visible: a search/news receipt, a stat, a cliffhanger tease | **creator's own voice** |
| **CTA** | last ~2s | End card: "▶ Watch the full video / <PARENT TITLE> / Subscribe" | (tail) |

## Pipeline

### 1. Source the raw take
Raw facecam takes live on the media drive, not the repo — `<mediaRoot>/<video>/*.mkv` (+ often a `.srt`). The published video's pre-cut `src/` clips are usually mostly graphics; the **raw `.mkv` is the real footage**. Confirm it's clean facecam (`ffmpeg -ss <t> -i take.mkv -frames:v 1 f.png` → Read it).

### 2. Choose the clip window on BREATH boundaries
Don't trust the `.srt` timing (it was offset ~+3s in testing). Find real pauses:
```
ffmpeg -t <scan_secs> -i take.mkv -af "silencedetect=noise=-32dB:duration=0.22" -f null - 2>&1 | grep silence_
```
Pick a **self-contained ~13s arc** (setup → payoff → cliffhanger) and cut **only inside pauses** so audio is clean. Jump-cuts are fine if both cut points land in silence.

### 3. Crop 16:9 → 9:16 (ffmpeg — Remotion has no reframe helper)
Gentle subject-centered cover crop (head-and-shoulders, "not totally cropped"). Tune the crop-x for where the subject sits (`(iw-ih*9/16)/2` = center ≈ 656 for 1920w; nudge left/right):
```
ffmpeg -ss <in> -i take.mkv -t <dur> \
  -vf "crop=608:1080:580:0,scale=1080:1920,fps=30" \
  -c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p -c:a aac -b:a 192k \
  <mediaRoot>/<slug>/src/recording-vert.mp4
```
For a jump-cut spine, trim+crop each window and `concat` them in one `filter_complex` (see git history of `recording-vert.mp4`).

### 4. Hook VO (3–4s, never silent)
Reuse an existing channel VO trimmed to the hook line (zero cost):
```
ffmpeg -i <existing-vo>.mp3 -t 2.95 -af "afade=t=out:st=2.6:d=0.35" <slug>/vo/<slug>-hook.mp3
```
…or generate fresh with the channel's hook voice via `vidiq_voiceover_generate` (see the brand pack for the `voiceId`). Make the graphics hook words **match the VO words**. (Optional: creator records their own 3–4s hook line instead.)

### 5. Build the Remotion composition
Copy the canonical build **`remotion-all/src/AIJobs/clips/AIJobsReel1Talk.tsx`** into `remotion-all/src/<Channel>/clips/<Name>Talk.tsx`, register it in that channel's `index.tsx` as a `1080×1920 @30fps` `<Composition>`, and swap in the brand pack's components/colors. Key patterns:
- **Spine:** `<OffthreadVideo src={staticFile("<publicSymlink>/<slug>/src/recording-vert.mp4")} style={{width:"100%",height:"100%",objectFit:"cover"}} />`. OffthreadVideo **carries its audio on render only** — silent in Studio preview, that's normal.
- **Captions:** timed as `clipStartFrame + clipTime*30`. Each caption is its own `<Sequence from={f} durationInFrames={n}>` with fade in/out; keyword pop in the accent color. Lower-third with a dark scrim pill.
- **Hook text:** each beat in its **own `<Sequence>` with fade in/out** so line 1 exits before line 2 (else they overlap).
- **Supporting overlays:** in an **upper-area holder** so the face stays visible; pop on the matching beat. Reuse the channel's stat component; add small in-file `SearchCard`/`HeadlineChip` for receipts.
- **Numbers must be real** — source from the channel's graphics/research, NOT the ASR captions (they're garbled). Cite (e.g. 300M = Goldman 2023; "no measurable impact" = Yale Budget Lab + Brookings 2025).
- Global fade the outer `AbsoluteFill` over the last ~14f.

### 6. Render
```
cd remotion-all && rm -rf node_modules/.cache && \
  npx remotion render <Channel>-<Name>Talk "<mediaRoot>/<slug>/out/<slug>.mp4" --gl=swangle
```

### 7. Verify + document
ffprobe (1080×1920, ≤20s), check hook audio is **non-silent** (`ffmpeg -ss 0 -t 3 -i out.mp4 -af volumedetect -f null -`), grab frames of each beat and Read them. Note the build in the channel's shorts plan + F-drive README.

## Brand packs (per-channel branding)

The pipeline is identical across channels; only the *look/voice* changes. Each channel has a brand pack in `brand-packs/`:
- **`brand-packs/amreet-talks.md`** — filled in (dark-cyan AIJobs style, Liam hook VO).
- **`brand-packs/_template.md`** — copy this to add a channel (e.g. Amreet Aint gaming/horror).

A brand pack specifies: media root, `remotion-all/src/<Channel>/` component library + `theme.ts` palette/fonts, which components map to hook-slam / stat / caption-accent, the hook-VO voice (or "record own"), caption language, CTA style, and the `public/` symlink.

## Gotchas (each cost a re-render)

- **Overlapping text** → every text beat needs its **own `<Sequence>` with fade in/out**.
- **A card balloons to full-frame** → an `alignItems:"stretch"` AbsoluteFill (Remotion's default) or a bare nested `<Sequence>` stretches a child; wrap overlays in `alignItems:"center"` containers (or use `layout="none"`).
- **Webpack crash on render** → `rm -rf node_modules/.cache` first.
- **WSL render** → needs `--gl=swangle`.
- **Silent hook** → dead air; always put a VO (or the creator's voice) on the first 3–4s.
- **SRT timing is unreliable** → align beats to `silencedetect`, not the `.srt` timestamps.
- **`.mkv` is 60fps** → `fps=30` in the crop; the comp is 30fps.

## Verification checklist

- [ ] Hook is **voiced** (not silent), lands by 0:03.
- [ ] Creator's voice carries the body; graphics only support (no second narration).
- [ ] Overlays pop on the right beats and **don't bury the face**; captions synced; keyword pops hit.
- [ ] Audio jump-cuts clean (cut on pauses); numbers on screen are real + sourced.
- [ ] Runtime ≤20s; end card + parent title correct; 1080×1920.
- [ ] Watch end-to-end before posting; parent link in description + pinned comment.
