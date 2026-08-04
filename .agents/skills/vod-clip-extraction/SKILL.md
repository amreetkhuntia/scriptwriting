---
name: vod-clip-extraction
description: Download a YouTube gameplay/stream VOD (or just the needed time ranges) and cut clean-boundary clips for a highlight reel — store on /mnt/f, verify cut points with a contact sheet. Use after youtube-transcript-analysis when turning a long VOD into editable clips.
metadata:
  tags: yt-dlp, ffmpeg, clips, highlight-reel, 2k, davinci
---

## When to use

After picking the beats for a highlight reel (see [youtube-transcript-analysis]),
to pull the source video and cut it into clips. Pairs with
[remotion-highlight-reel], which assembles the clips. The guiding principle for
*where* to cut is in memory — `feedback-highlight-clip-boundaries`.

## Core principle: cut on COMPLETE scene boundaries

The game's own cutscene dialogue is the narration. Cut each clip as a complete
unit — **start at the first line of the scene, end AFTER the final thought /
payoff line.** Caption-anchor timestamps cut mid-sentence and make the reel feel
like disconnected fragments. Find exact edges from the cue-level transcript
(`transcript.py window` in the transcript skill). **Merge** consecutive beats
whose gap is ≤ ~1:30 into one continuous clip (truly end-to-end). Verify before
committing (step 4).

## 1. Get the source — full VOD vs. just the sections

Check available resolutions first (2K = `1440p`, often VP9 `308` / AV1 `400`):
```bash
yt-dlp -F "https://www.youtube.com/watch?v=<ID>" | grep -E "1440|2160|1080"
```

**Sections only (fast, less disk)** — download just the ranges you need. Without
`--force-keyframes-at-cuts` it stream-copies (fast) and the output is the exact
requested length; pad ~3 s each side for trim headroom:
```bash
yt-dlp -f "400+251/308+251/bestvideo[height<=1440]+bestaudio" \
  --download-sections "*00:16:04-00:19:03" --merge-output-format mp4 --no-part \
  -o "/tmp/raw/02_briefing.%(ext)s" "https://www.youtube.com/watch?v=<ID>"
```
`--force-keyframes-at-cuts` makes it frame-exact but re-encodes (slow on AV1) — avoid; pad + trim in step 3 instead.

**Full VOD (when you'll iterate on boundaries a lot, or want the archive)** — one
download, then cut locally any number of times:
```bash
yt-dlp -f "400+251/308+251/bestvideo[height<=1440]+bestaudio" \
  --merge-output-format mp4 --no-part -o "007_day3_full.mp4" \
  "https://www.youtube.com/watch?v=<ID>"
```
2K VODs are ~6 GB and merge AV1+opus into the mp4 container.

## 2. Store media on /mnt/f, not the repo

Per `feedback-media-on-f-drive`: cut clips to a folder on the external drive and
symlink the Remotion public subfolder to it, so `staticFile()` still resolves
while the bytes stay off-repo:
```bash
ln -s "/mnt/f/recordings/<proj>/clips" remotion-all/public/<proj>clips
# add `remotion-all/public/<proj>clips` (no trailing slash) to .gitignore
```

## 3. Cut + re-encode to a uniform spec

Re-encode every clip to identical codec/fps/dims so Remotion `OffthreadVideo`
plays them predictably (2K source is AV1 60fps → normalize to h264 30fps). Put
`-ss` before `-i` (fast accurate seek in ffmpeg ≥ 5) and `-t` after for duration:
```bash
ffmpeg -y -ss 00:16:07 -i "$SRC" -t 173 \
  -vf "scale=2560:1440:force_original_aspect_ratio=decrease,pad=2560:1440:-1:-1,fps=30" \
  -c:v libx264 -crf 18 -preset veryfast -pix_fmt yuv420p \
  -c:a aac -ar 48000 -ac 2 "$OUT/02_briefing.mp4"
```
- From padded section files (step 1), trim the pad with `-ss <pad> -t <dur>`.
- `veryfast` is fine — the clips get re-encoded again by the final Remotion render.
- Long AV1 clips decode slowly; run the batch with `run_in_background: true`.

## 4. Verify cut points before assembling

Caption timing drifts — confirm each cut visually:
```bash
.Codex/skills/vod-clip-extraction/scripts/contact_sheet.sh "/mnt/f/recordings/<proj>/clips" /tmp/sheet.png
```
Read the sheet image; it shows a labeled IN + OUT frame per clip. Nudge any
boundary that clips a line or lands on the wrong scene, then re-cut that one clip.

## 5. Durations → frames (for the Remotion manifest)

```bash
for f in "$OUT"/*.mp4; do d=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$f");
  printf "%-22s %5d frames\n" "$(basename "$f")" "$(python3 -c "import math;print(math.floor($d*30)-1)")"; done
```
`floor(seconds*30)-1` so a clip never freezes on its last frame in a Sequence.
Hand these to [remotion-highlight-reel] (`clips.ts`).

## Gotchas
- **zsh** doesn't word-split unquoted vars (`set -- $r` fails) — use `${=r}`; and
  an unmatched glob (`rm foo.*`) aborts the whole command — guard or use unique names.
- yt-dlp's `impersonation … no impersonate target` WARNING is harmless.
- Auto-captions garble proper nouns — verify names against the video if they matter.
