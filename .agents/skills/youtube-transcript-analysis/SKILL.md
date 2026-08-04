---
name: youtube-transcript-analysis
description: Pull a YouTube video's transcript with yt-dlp and analyze it for interesting/clip-worthy parts — works for long streams, interviews, talks, and documentaries. Use when the user gives a YouTube URL and asks what's in it, what parts are interesting, for a clip list, or to source quotes for research.
metadata:
  tags: youtube, transcript, yt-dlp, vtt, research, clips, scriptwriting
---

## When to use

Any time the user drops a YouTube URL and wants to know what's *in* it without
watching — "pull the transcript", "what parts are interesting", "find the X
moment", "make me a clip list", or sourcing quotes for a `research.md`. Works on
long live streams (4h+), interviews, talks, and documentaries.

Don't have a video ID yet — just "check my channel" or "find my recent
streams"? Start with [youtube-channel-discovery] instead, then come back here
with the shortlisted IDs.

Prefer this `yt-dlp` flow over the MCP transcript tools: it returns **real
timestamps** (the MCP transcript returns one undifferentiated blob), it's free,
and it handles videos the MCP tool can't reach.

## Workflow

### 1. Get the video ID and download subtitles

Every YouTube URL form (`/watch?v=`, `/live/`, `youtu.be/`, `/shorts/`) contains
an 11-char video ID. `yt-dlp` accepts the full URL, but normalizing to
`https://www.youtube.com/watch?v=<ID>` is the safe path.

Download into `/tmp` (these files are scratch, not repo content):

```bash
yt-dlp --skip-download --write-auto-subs --write-subs \
  --sub-langs "en.*" --sub-format vtt \
  -o "/tmp/yt_<ID>.%(ext)s" "https://www.youtube.com/watch?v=<ID>"
```

- For another language swap `en.*` for the real language code (e.g. `"hi.*"`
  for Hindi/Hinglish streams, `"es.*"` for Spanish).
- **Before assuming a non-English video has no captions**, run
  `yt-dlp --list-subs <url> | grep -i orig` first — don't guess from a
  truncated `--list-subs` glance. The original ASR track is named `<lang>-orig`
  (e.g. `hi-orig`), not necessarily `en-orig`, and it's easy to miss it inside
  the long alphabetical auto-translate list if you eyeball/truncate the output.
  See [youtube-channel-discovery] step 4 for the full gotcha — this exact
  mistake once led to planning a whole local-Whisper fallback for streams that
  had working Hindi captions all along.
- This usually writes two files: `...en.vtt` (manual) and `...en-orig.vtt`
  (auto). Use whichever exists; they're often identical. Auto-captions only →
  expect garbled words (timestamps stay accurate).
- The `impersonation ... no impersonate target` WARNING is harmless — ignore it.
- **zsh gotcha:** don't `rm /tmp/yt_<ID>.*` — an unmatched glob errors out in
  zsh. Use a unique `<ID>` per video and skip the cleanup, or `setopt
  null_glob`.

Grab metadata too (title/duration tell you what kind of video this is and how
hard to dedupe) — the `vidiq_get_videos_by_ids` MCP tool or `yt-dlp --print
"%(title)s | %(duration_string)s"` both work.

### 2. Clean it into a scannable transcript

The bundled script lives next to this file at `scripts/transcript.py`.

```bash
python3 scripts/transcript.py clean /tmp/yt_<ID>.en.vtt --out /tmp/yt_<ID>_clean.txt
```

This strips VTT markup, dedupes rolling auto-caption repeats, and groups lines
into **one block per minute** with an `[HH:MM:SS]` header — readable in a single
pass. Read the output file and scan for the beats below.

### 3. Analyze — find the interesting parts

Read with the content type in mind. What counts as "interesting" differs:

- **Gameplay / live streams** — boss fights and clutch moments; emotional or
  story cutscene beats; *funny or opinionated streamer commentary* (this is the
  channel's personality, separate it out); and **dead air to trim** (intro/outro
  music, repetitive death-loops that read as "heal / behind you / groaning").
- **Interviews / podcasts** — surprising claims, strong quotable lines, the
  guest's core thesis, disagreements, story anecdotes.
- **Talks / documentaries** — key stats, the central argument, vivid examples,
  anything citable for a script's research notes.

Report back as a **timestamped, categorized rundown**, not a summary. For each
moment give `[HH:MM:SS]`, a one-line label, and a short quote. Lead with the 2–3
strongest. If the goal is an edit, add concrete clip in/out points and call out
sections to cut. Then offer to pull verbatim lines for any moment.

### 4. Pull verbatim lines for a chosen moment

Minute-buckets are for scanning; for an exact quote or precise clip in/out,
slice the original VTT at cue-level resolution:

```bash
python3 scripts/transcript.py window /tmp/yt_<ID>.en.vtt 03:01:00 03:12:30
```

Accepts `HH:MM:SS`, `MM:SS`, or raw seconds. Use this to confirm exact wording
and timing before handing off a clip list.

## Notes

- Auto-captions garble proper nouns and uncommon words — don't trust exact
  spellings of names; verify against the video or a web search if it matters.
- The clean step's minute-bucketing is lossy by design (good for scanning, not
  quoting). Always go back to `window` on the raw VTT for verbatim text.
- For sourcing a script, drop the relevant findings into the project's
  `research.md` with the video link + timestamp, per `docs/research-framework.md`.
- To turn the chosen beats into an edited highlight reel, continue with the
  **vod-clip-extraction** skill (download + cut clean-boundary clips) then
  **remotion-highlight-reel** skill (assemble the reel).
