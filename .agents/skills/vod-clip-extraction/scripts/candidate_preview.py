#!/usr/bin/env python3
"""Build a reviewable contact sheet for PRE-cut clip candidates.

Given a local video file and a JSON list of candidates (start/end timestamps
plus their label/category/tier), grabs a few evenly-spaced frames per
candidate and tiles them into one composite image, with a text header per
candidate. This is the sibling of contact_sheet.sh for a step *earlier* in
the pipeline: verifying a transcript-derived candidate is visually what it
claims to be, before you commit to actually cutting it.

Uses Pillow for frame labeling/tiling instead of ffmpeg's `drawtext`/`tile`
filters — some ffmpeg builds (this one included) aren't compiled with
libfreetype, so `drawtext` isn't available. ffmpeg is still used to grab the
raw frames (-ss seek + -frames:v 1); everything after that is Python/PIL.

Usage:
  python3 candidate_preview.py VIDEO CANDIDATES.json OUT.jpg [--frames N|auto] [--start-index I]

CANDIDATES.json: a list of objects with at least start, end (HH:MM:SS or
seconds), label, category, tier. Extra keys are ignored.

--frames auto (the default) scales sample count with each candidate's own
duration: frames = clamp(ceil(duration_sec / 8), 4, 16). A fixed low count
(e.g. 4) is fine for a 20s clip but dangerously sparse for anything upwards of
a minute — a real 30s action beat inside a 90s window can fool a 4-frame
sample into a false CONFIRMED while missing that the other 60s is menu
navigation or dead walking. Pass an integer to force the same frame count for
every candidate instead.

Each candidate may optionally set its own "video" path (e.g. a small
per-candidate section pulled with --download-sections instead of a full
stream download) — when present, frames are sampled evenly across that
file's own duration instead of seeking into the shared VIDEO argument at
absolute start/end. start/end are still shown in the header for reference.
"""
import argparse
import json
import math
import subprocess
import sys
import tempfile
import os

from PIL import Image, ImageDraw, ImageFont

FONT_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
FONT_REGULAR = "/System/Library/Fonts/Supplemental/Arial.ttf"
THUMB_W = 320
HEADER_H = 90
PAD = 10
MIN_FRAMES = 4
MAX_FRAMES = 16
SECONDS_PER_FRAME = 8


def auto_frame_count(duration_s):
    return max(MIN_FRAMES, min(MAX_FRAMES, math.ceil(duration_s / SECONDS_PER_FRAME)))


def to_seconds(val):
    if isinstance(val, (int, float)):
        return float(val)
    parts = [float(p) for p in str(val).split(":")]
    while len(parts) < 3:
        parts.insert(0, 0)
    h, m, s = parts[-3], parts[-2], parts[-1]
    return h * 3600 + m * 60 + s


def grab_frame(video, t, out_path):
    subprocess.run(
        ["ffmpeg", "-y", "-ss", str(t), "-i", video, "-frames:v", "1",
         "-vf", f"scale={THUMB_W}:-1", "-q:v", "4", out_path],
        check=True, capture_output=True,
    )


def probe_duration(video):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", video],
        check=True, capture_output=True, text=True,
    )
    return float(out.stdout.strip())


def build_sheet(video, candidates, out_path, n_frames: "str | int" = "auto", start_index=1):
    font_bold = ImageFont.truetype(FONT_BOLD, 26)
    font_small = ImageFont.truetype(FONT_REGULAR, 20)

    sections = []  # (header_lines, [PIL.Image, ...])
    frame_counts = []
    with tempfile.TemporaryDirectory() as tmp:
        for idx, c in enumerate(candidates, start=start_index):
            src = c.get("video", video)
            if "video" in c:
                # per-candidate section file: sample across its own duration
                start_s = 0.0
                end_s = probe_duration(src)
            else:
                start_s = to_seconds(c["start"])
                end_s = to_seconds(c["end"])
            span = max(end_s - start_s, 0.1)
            this_n = auto_frame_count(span) if n_frames == "auto" else int(n_frames)
            frame_counts.append(this_n)
            times = [start_s + span * (k / (this_n - 1)) for k in range(this_n)]
            frames = []
            for k, t in enumerate(times):
                fp = os.path.join(tmp, f"{idx}_{k}.jpg")
                try:
                    grab_frame(src, t, fp)
                    frames.append(Image.open(fp).convert("RGB"))
                except subprocess.CalledProcessError:
                    frames.append(Image.new("RGB", (THUMB_W, int(THUMB_W * 16 / 9)), "black"))
            header = (
                f"#{idx}  [{c.get('category','?')}/{c.get('tier','?')}]  "
                f"{c['start']} -> {c['end']}  ({span:.0f}s, {this_n} frames)",
                c.get("label", ""),
            )
            sections.append((header, frames))

    max_frames = max(frame_counts) if frame_counts else 4
    thumb_h = sections[0][1][0].height if sections else int(THUMB_W * 16 / 9)
    row_w = max_frames * THUMB_W + (max_frames + 1) * PAD
    row_h = thumb_h + HEADER_H + PAD
    total_h = row_h * len(sections) + PAD

    sheet = Image.new("RGB", (row_w, total_h), "white")
    draw = ImageDraw.Draw(sheet)

    y = PAD
    for (title, subtitle), frames in sections:
        draw.rectangle([0, y, row_w, y + HEADER_H], fill=(20, 20, 20))
        draw.text((PAD, y + 8), title, font=font_bold, fill="yellow")
        # wrap subtitle crudely if too long
        max_chars = int(row_w / 11)
        sub = subtitle if len(subtitle) <= max_chars else subtitle[: max_chars - 1] + "…"
        draw.text((PAD, y + 44), sub, font=font_small, fill="white")
        y += HEADER_H
        x = PAD
        for f in frames:
            sheet.paste(f, (x, y))
            x += THUMB_W + PAD
        y += thumb_h + PAD

    sheet.save(out_path, quality=90)
    counts_desc = f"{min(frame_counts)}-{max(frame_counts)}" if frame_counts else "0"
    print(f"wrote {out_path}  ({len(sections)} candidates, {counts_desc} frames each)", file=sys.stderr)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("video", help="shared video file, or '-' if every candidate sets its own 'video'")
    p.add_argument("candidates_json")
    p.add_argument("out")
    p.add_argument("--frames", default="auto", help="'auto' (default, duration-scaled) or a fixed integer")
    p.add_argument("--start-index", type=int, default=1)
    args = p.parse_args()

    video = None if args.video == "-" else args.video
    candidates = json.load(open(args.candidates_json, encoding="utf-8"))
    n_frames = "auto" if args.frames == "auto" else int(args.frames)
    build_sheet(video, candidates, args.out, n_frames=n_frames, start_index=args.start_index)


if __name__ == "__main__":
    main()
