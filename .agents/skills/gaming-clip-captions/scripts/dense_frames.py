#!/usr/bin/env python3
"""Pull a dense, fixed-rate burst of frames (2-3 per second by default) from
a short window of a video, tiled into one labeled contact sheet — for
PRECISE review, not broad verification.

This is the sibling of vod-clip-extraction's `candidate_preview.py` (which
scales frame count to a whole candidate's duration, ~1 frame per 8s, meant
for "does this 30-90s window hold up at all"). This tool is for the opposite
situation: you already know roughly *where* something is and need to pin
down the exact second — the exact frame a caption word lands on, the exact
"YOU DIED" frame, the exact reaction peak, an exact cut boundary. A coarse
sample can straddle the moment and miss it; 2-3 fps over a 2-5s window
rarely does.

Usage:
  python3 dense_frames.py VIDEO.mp4 START END OUT.png [--fps 2.5] [--cols 5]

START/END accept seconds, MM:SS, or HH:MM:SS. Splits into OUT_1.png,
OUT_2.png, ... if the burst would produce more than --max-per-sheet frames
(default 30) so no single sheet gets unreadably long.
"""
import argparse
import math
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

FONT_REGULAR = "/System/Library/Fonts/Supplemental/Arial.ttf"
THUMB_W = 260
LABEL_H = 24
PAD = 6


def to_seconds(val):
    if isinstance(val, (int, float)):
        return float(val)
    parts = [float(p) for p in str(val).split(":")]
    while len(parts) < 3:
        parts.insert(0, 0)
    h, m, s = parts[-3], parts[-2], parts[-1]
    return h * 3600 + m * 60 + s


def fmt(sec):
    return f"{int(sec // 60):02d}:{sec % 60:05.2f}"


def extract_burst(video, start, end, fps, tmpdir):
    duration = max(end - start, 0.05)
    pattern = str(Path(tmpdir) / "frame_%04d.jpg")
    subprocess.run(
        ["ffmpeg", "-y", "-ss", str(start), "-i", video, "-t", str(duration),
         "-vf", f"fps={fps},scale={THUMB_W}:-1", "-q:v", "4", pattern],
        check=True, capture_output=True,
    )
    files = sorted(Path(tmpdir).glob("frame_*.jpg"))
    return [(start + i / fps, f) for i, f in enumerate(files)]


def build_sheet(frames, cols, out_path):
    font = ImageFont.truetype(FONT_REGULAR, 18)
    imgs = [Image.open(f).convert("RGB") for _, f in frames]
    thumb_h = imgs[0].height if imgs else 100
    rows = math.ceil(len(imgs) / cols)
    cell_w, cell_h = THUMB_W + PAD, thumb_h + LABEL_H + PAD
    sheet = Image.new("RGB", (cols * cell_w + PAD, rows * cell_h + PAD), "white")
    draw = ImageDraw.Draw(sheet)
    for i, ((t, _), img) in enumerate(zip(frames, imgs)):
        r, c = divmod(i, cols)
        x, y = PAD + c * cell_w, PAD + r * cell_h
        draw.rectangle([x, y, x + THUMB_W, y + LABEL_H], fill=(20, 20, 20))
        draw.text((x + 4, y + 3), fmt(t), font=font, fill="yellow")
        sheet.paste(img, (x, y + LABEL_H))
    sheet.save(out_path, quality=90)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("video")
    p.add_argument("start")
    p.add_argument("end")
    p.add_argument("out", help="e.g. review.png -> review_1.png, review_2.png, ... if split")
    p.add_argument("--fps", type=float, default=2.5)
    p.add_argument("--cols", type=int, default=5)
    p.add_argument("--max-per-sheet", type=int, default=30)
    args = p.parse_args()

    start, end = to_seconds(args.start), to_seconds(args.end)
    if end <= start:
        raise SystemExit("end must be after start")

    with tempfile.TemporaryDirectory() as tmpdir:
        frames = extract_burst(args.video, start, end, args.fps, tmpdir)
        if not frames:
            raise SystemExit("no frames extracted — check the time range")

        stem, _, suffix = args.out.rpartition(".")
        suffix = suffix or "png"
        chunks = [frames[i:i + args.max_per_sheet] for i in range(0, len(frames), args.max_per_sheet)]
        for i, chunk in enumerate(chunks, start=1):
            out_path = f"{stem}_{i}.{suffix}" if len(chunks) > 1 else args.out
            build_sheet(chunk, args.cols, out_path)
            print(f"wrote {out_path}  ({len(chunk)} frames, {args.fps} fps)", file=sys.stderr)


if __name__ == "__main__":
    main()
