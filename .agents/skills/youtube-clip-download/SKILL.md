---
name: youtube-clip-download
description: Download only specific time ranges from a YouTube video with yt-dlp --download-sections — give a URL and one or more start–end timestamps and get just those clips, no full download. Use when you already know the segment(s) you want (a:b), not when scanning a transcript or cutting a full highlight reel.
metadata:
  tags: yt-dlp, youtube, download-sections, clips, ffmpeg
---

## When to use

You already know the exact range(s) you want — "from this video, grab
12:30–13:05" — and you just want the bytes for that span without pulling the
whole video. This is the quick "grab a:b" path.

Pick the right sibling instead when:
- you *don't* know where the moment is yet → [youtube-transcript-analysis]
  finds it from the transcript first (then come back here with the timestamps);
- you need scene-boundary cuts, a uniform 2K re-encode, `/mnt/f` storage and
  Remotion-ready frame counts → [vod-clip-extraction] is the full highlight-reel
  pipeline. This skill is the lightweight counterpart — it does not re-encode,
  organize, or assemble anything.

## Workflow

### 1. Normalize the URL (and optionally check resolutions)

Every YouTube URL form (`/watch?v=`, `/live/`, `youtu.be/`, `/shorts/`) carries
an 11-char video ID; `https://www.youtube.com/watch?v=<ID>` is the safe form.
To see what qualities exist before choosing `-q`:

```bash
yt-dlp -F "https://www.youtube.com/watch?v=<ID>" | grep -E "1080|1440|2160"
```

### 2. Download the range(s) with the bundled helper

One or more `START-END` ranges in a single call — each lands as its own
`NN_<start>-<end>.mp4`:

```bash
.Codex/skills/youtube-clip-download/scripts/download_sections.sh \
  -o /tmp/clips "https://www.youtube.com/watch?v=<ID>" 12:30-13:05 41:20-42:00
```

`START`/`END` accept `HH:MM:SS`, `MM:SS`, or raw seconds. Flags: `-o OUTDIR`
(default `./clips`), `-q MAXHEIGHT` (default `1080`), `-x` (frame-exact, see
step 3). The equivalent raw one-liner per range, for transparency:

```bash
yt-dlp -f "bestvideo[height<=1080]+bestaudio/best[height<=1080]/best" \
  --download-sections "*12:30-13:05" --merge-output-format mp4 --no-part \
  -o "/tmp/clips/01_12-30-13-05.%(ext)s" "https://www.youtube.com/watch?v=<ID>"
```

### 3. Precision: fast keyframe cut vs. frame-exact

By default yt-dlp stream-copies and cuts at the nearest **keyframe** — fast, no
re-encode, but the clip can start a few seconds early and its length is only
*approximately* what you asked for. Two ways to get exact edges:

- Pass `-x` to the helper (adds `--force-keyframes-at-cuts`) — frame-accurate but
  re-encodes the whole span, so it's slow (especially on AV1 2K sources).
- Or download with ~3 s of pad each side (default mode) and trim precisely with
  ffmpeg `-ss <pad> -t <dur>` — see [vod-clip-extraction] step 3 for the
  re-encode recipe. Cheaper than `-x` when you only need one or two clips exact.

## Notes / Gotchas

- Scratch clips go to `/tmp`; for durable media point `-o` at `/mnt/f/...` per
  the repo's media-on-F-drive rule — never commit the bytes to the repo.
- The `impersonation … no impersonate target` WARNING from yt-dlp is harmless.
- **zsh:** an unmatched glob aborts the whole command — keep ranges quoted and
  output names unique (the helper already does this via the `NN_` prefix).
- **Private / age-gated videos:** a bare `--download-sections` call may fail
  without auth — add `--cookies-from-browser <browser>` to the yt-dlp call (the
  same limitation `video-clipper` hits, since it strips cookies on its segment
  path). The helper passes through whatever auth your yt-dlp config already has.
