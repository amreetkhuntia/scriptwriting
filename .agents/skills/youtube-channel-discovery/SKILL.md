---
name: youtube-channel-discovery
description: Find a YouTube channel's own recent videos/streams/shorts by handle or channel ID — no API key, no MCP server, just yt-dlp against the channel's /videos, /streams, or /shorts tab. Use when the user asks to check their channel, find recent uploads/live streams, or wants candidates before a video ID is known. Also confirms actual video resolution (don't trust title tags like "| Vertical") and whether real captions exist before handing off to transcript analysis.
metadata:
  tags: yt-dlp, youtube, channel, discovery, streams, resolution, captions
---

## When to use

Every other `youtube-*` / `vod-*` skill in this repo assumes you already have a
video URL or ID. This one is the step *before* that — "check my channel", "find
my recent live streams", "what have I uploaded lately" — when you're starting
from a channel, not a link.

Once you have a shortlist of video IDs, hand off to
[youtube-transcript-analysis] (pull + analyze the transcript) and from there
[vod-clip-extraction] / [remotion-highlight-reel] (cut + assemble clips).

There is no working MCP tool for this in this repo — `mcp-youtube` in
`.mcp.json` was a dead stub (the published package body was literally
`{status: 'coming-soon'}`, no real server) and has been removed. Plain `yt-dlp`
against the channel's own tabs does the job for free.

## 1. List the channel's videos/streams/shorts

```bash
.Codex/skills/youtube-channel-discovery/scripts/list_channel_videos.sh <handle-or-channelID> streams 30
```

`TAB` is `videos` (default), `streams` (past live streams — this is what you
want for "find my live streams"), or `shorts`. Raw equivalent, for
transparency:

```bash
yt-dlp --flat-playlist --playlist-end 30 \
  --print "%(id)s | %(duration_string)s | %(title)s" \
  "https://www.youtube.com/@<handle>/streams"
```

This is fast and anonymous, but **`upload_date` comes back `NA`** in flat mode —
it only gives you id/duration/title cheaply to build a shortlist.

## 2. Get real dates once you have a shortlist

Per-video metadata (not flat-playlist) does return the date:

```bash
yt-dlp --skip-download --print "%(id)s | %(upload_date)s | %(duration_string)s | %(view_count)s views | %(title)s" \
  "https://www.youtube.com/watch?v=<ID>"
```

This occasionally hits YouTube's bot-check ("Sign in to confirm you're not a
bot") even on public videos — it's usually transient, just retry. `-F` (step 3)
and `--flat-playlist` (step 1) don't seem to trigger it.

## 3. Check ACTUAL resolution — don't trust the title

Channels sometimes tag a title `"| Vertical"` inconsistently — some vertical
(9:16) uploads have no tag at all, and it's not safe to assume an untagged
video is horizontal. Always verify with the real format list:

```bash
yt-dlp -F "https://www.youtube.com/watch?v=<ID>" | grep -E "1080x1920|1920x1080|1440x2560|2560x1440"
```

`1080x1920` / `1440x2560` = vertical (9:16); `1920x1080` / `2560x1440` =
horizontal (16:9). This is cheap (no download) — check every candidate before
filtering by orientation.

## 4. Check for real captions BEFORE assuming you need Whisper

`yt-dlp --list-subs <url>` prints two sections: "Available automatic
captions" (100+ entries, one per translation target, alphabetical) and
"Available subtitles" (manually uploaded, usually empty). **Do not truncate
this output** (e.g. with `tail`) — the alphabetical translation list can push
the video's *actual* original ASR track off the visible tail, making it look
like no captions exist when they do. This was a real mistake in this repo's
history: assuming Hindi/Hinglish streams had no captions and planning to fall
back to local Whisper transcription, when the real Hindi track was there all
along — just hidden above a truncated `tail -15`.

Look for a `<lang>-orig` entry (e.g. `hi-orig`, `en-orig`) — that's the real
original ASR track, not a translation. Grep for it directly instead of eyeballing:

```bash
yt-dlp --list-subs "https://www.youtube.com/watch?v=<ID>" | grep -i orig
```

If a `-orig` track exists, fetch it and hand off to
[youtube-transcript-analysis] (its `--sub-langs` example uses `en.*` — swap in
whatever language code you found here, e.g. `hi-orig`). Only consider a local
Whisper fallback if this genuinely comes back empty.

## Notes / Gotchas

- Channel URL forms all work: `@handle`, `UC...` channel ID, or a full URL —
  the script normalizes any of them.
- The `impersonation … no impersonate target` WARNING yt-dlp prints is harmless.
- Very low view counts on a channel's own past streams (single digits) usually
  just mean nobody watched live — the VOD itself is still fine to mine for clips.
