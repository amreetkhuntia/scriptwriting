---
name: gaming-clip-captions
description: Finish a cut gameplay short — burn in dynamic word-synced captions (with emoji on reaction beats) plus a "CHECK FULL VIDEO AND SUBSCRIBE" end-card. Includes a dense fixed-rate (2-3fps) frame-burst tool for pinpointing exact moments (caption sync, cut boundaries, reaction frames) — finer-grained than vod-clip-extraction's whole-candidate contact sheets. Built for Amreet Aint's facecam-on-top / gameplay-below vertical layout. Use after a clip has been cut (from vod-clip-extraction or a direct yt-dlp --download-sections pull) and is ready to post to Shorts/Reels.
metadata:
  tags: captions, emoji, ffmpeg, pillow, shorts, reels, amreet-aint, gaming, frame-extraction
---

## When to use

You already have a cut, trimmed gameplay clip (see [vod-clip-extraction] and
`channels/Amreet Aint/videos/<game>/cut-list.md` for picking + cutting the
moment) and want to finish it for posting: captions that pop in synced to
the actual dialogue, emoji on the punchlines, and a subscribe end-card. This
is the "editing" pass, not the "which moment to clip" pass.

Designed around Amreet Aint's recording layout: facecam band on top,
gameplay footage below, both baked into one 1080x1920 vertical frame — no
separate reframe/crop needed for that layout, captions just get positioned
at the seam between the two.

## Workflow

### 1. Get word-level caption timing

Pull the video's real auto-caption track the same way
[youtube-transcript-analysis] does (`yt-dlp --write-auto-subs`), but don't
use the cleaned/bucketed output for this — go straight to the raw `.vtt`.
YouTube's auto-captions are word-by-word "growing" cues:
```
01:29:56.080 --> 01:29:58.310 align:start position:0%
भाई<01:29:56.400><c> नहीं</c><01:29:56.639><c> रहे</c>...
```
Each `<HH:MM:SS.mmm><c>word</c>` tag is that word's exact on-screen moment —
this is the ground truth for syncing captions, far more precise than the
minute-bucketed `transcript.py clean` output (which is for *finding* beats,
not for word-level sync). Grep the raw VTT for your clip's time range.

**If your clip is a jump-cut** (spliced from multiple non-contiguous source
segments — see the `bhai-bhai-bhai` clip for a worked example), convert each
segment's word timestamps to `(word_time - segment_start)`, then add that
segment's **cumulative offset** in the final concatenated video (segment 2's
offset = segment 1's duration; segment 3's offset = segment 1 + segment 2's
duration; etc.). Add the offset **once** — a doubled offset is the most
likely bug here and will silently push cards past the clip's actual end
(ffmpeg just fails or the tail cards never show).

### 2. Group words into caption cards

Break the word timeline into ~2-6 word phrases at natural speech pauses
(the auto-caption cue boundaries are a good default breakpoint; punctuation
and repeated-word bursts like "bhai bhai bhai bhai" work well as their own
card). Write a JSON manifest:

```json
[
  {"text": "Oh what the [bleep]", "start": 11.3, "end": 12.6, "emoji": "💀"},
  {"text": "BHAI BHAI BHAI BHAI", "start": 12.6, "end": 15.6, "emoji": "😭"},
  {"text": "Bach gaye", "start": 15.6, "end": 16.8, "emoji": null}
]
```

**Caption text rules** (learned the hard way — see Gotchas):
- Write in **Hinglish** (Roman-script transliteration), not Devanagari —
  Impact is a Latin-only font. Match how the streamer actually talks;
  don't formally translate.
- **Verify each line against what's actually meant, not the literal ASR
  text.** Hindi auto-captions transliterate *phonetically* — real words get
  swapped for similar-sounding ones. Confirmed mistakes so far: "रेप" is
  usually **"revive"** (co-op revive callout), not "rep"; "एडिट" can
  actually be **"addict"** (streamer banter), not "edit". When a word looks
  out of place for the context, say so before locking in the caption.
- **Emoji only on the beats that land** — reaction/punchline words, not
  every card. Rough mapping that's worked so far: swearing/bleep → 💀 or
  🤬, panic/exclamation → 😭 or 😱, pain sounds ("aay aay aay") → 😵,
  a joke/aside → 😂. Don't force one onto a flat narration line.

### 3. Verify exact moments with a dense frame burst

Whenever you need to pin down an exact second — where a caption word should
really land, the exact "YOU DIED" frame, an exact cut boundary — don't rely
on a single frame grab or a coarse sample. Pull a dense, fixed-rate burst:

```bash
python3 .Codex/skills/gaming-clip-captions/scripts/dense_frames.py \
  your_clip.mp4 12 16 review.png --fps 2.5
```
Tiles 2-3 labeled frames per second across the given window into one
contact sheet (splits into `review_1.png`, `review_2.png`, ... past
`--max-per-sheet`, default 30). This is the sibling of
[vod-clip-extraction]'s `candidate_preview.py` — that one scales frame count
to a whole 30-90s candidate window for broad "does this hold up" checks
(~1 frame per 8s); this one is for zooming into a few seconds you already
suspect matter, at real precision. Use it before locking in caption
timestamps, not just after something looks off.

### 4. Find the facecam/gameplay seam

```bash
python3 .Codex/skills/gaming-clip-captions/scripts/detect_seam.py your_clip.mp4
```
Prints the y-pixel row. This is stable across clips from the same recording
setup, so you only need to (re)run it if the facecam position changes.

### 5. Burn in the captions

```bash
python3 .Codex/skills/gaming-clip-captions/scripts/caption_overlay.py \
  your_clip.mp4 manifest.json <SEAM_Y> your_clip_captioned.mp4
```
Renders every card as its own transparent PNG (Pillow — **not** ffmpeg
`drawtext`, this repo's ffmpeg build has no libfreetype) and composites them
with a chained `overlay=...:enable='between(t,start,end)'` filter graph so
each card only shows during its own window.

### 6. Add the subscribe end-card

```bash
python3 .Codex/skills/gaming-clip-captions/scripts/subscribe_endcard.py \
  your_clip_captioned.mp4 final.mp4 --handle @AmreetAint
```
Freezes + darkens the last frame, burns in "CHECK FULL VIDEO / AND
SUBSCRIBE" + the handle (override with `--line1`/`--line2`/`--handle`, hold
duration with `--hold`), and concats it onto the clip.

## Gotchas

- **No ffmpeg `drawtext`/`tile` on this machine** — no libfreetype in the
  build. Every text/emoji render in this pipeline goes through Pillow, then
  gets composited as an image via ffmpeg's `overlay` filter. If a future
  environment *does* have drawtext, it's still simpler to keep using this
  Pillow path for consistency (font metrics, emoji, outline style all match).
- **Apple Color Emoji only renders at fixed bitmap-strike sizes**: 20, 32,
  40, 48, 64, 96, 160px. Any other size throws `invalid pixel size`. Render
  at 160 (the largest/crispest) and let Pillow's `.resize()` scale it down
  to whatever you actually need.
- **Jump-cut offset math** — see step 1. Sanity-check by spot-reading a
  frame right at each card's start time before trusting the whole render.
- Devanagari text will not render in Impact — if a caption looks like tofu
  boxes, you forgot to transliterate it.

## Reference example

The `bhai-bhai-bhai-panicked-wipe` short (`NxOMr6_jzA4`, cut-list entry
01:29:47→01:31:00, tightened + jump-cut to 47s) is the worked example this
skill was built from — 15 caption cards, 5 with emoji, seam detected at
y≈735 for that recording's layout.
