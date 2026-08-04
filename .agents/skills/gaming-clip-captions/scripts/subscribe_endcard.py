#!/usr/bin/env python3
"""Append a "CHECK FULL VIDEO / AND SUBSCRIBE" end-card to a cut clip.

Freezes the clip's last frame, darkens it, burns in the CTA text + a handle
via Pillow (ffmpeg here has no drawtext), holds it for a few seconds, then
concats it onto the end of the main clip. Same recipe used for every Amreet
Aint Elden Ring short so far.

Usage:
  python3 subscribe_endcard.py VIDEO.mp4 OUT.mp4 [--handle @AmreetAint]
    [--line1 "CHECK FULL VIDEO"] [--line2 "AND SUBSCRIBE"] [--hold 3]
"""
import argparse
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFont

FONT_BOLD = "/System/Library/Fonts/Supplemental/Impact.ttf"
W, H = 1080, 1920


def grab_last_frame(video, out_path):
    subprocess.run(
        ["ffmpeg", "-y", "-sseof", "-0.5", "-i", video, "-update", "1", "-q:v", "2", out_path],
        check=True, capture_output=True,
    )


def get_fps(video):
    # The end-card's own fps must match the source clip's, or concat -c copy
    # fails/desyncs on fps mismatch (e.g. a 60fps clip + a hardcoded-30fps card).
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0",
         "-show_entries", "stream=r_frame_rate", "-of", "csv=p=0", video],
        check=True, capture_output=True, text=True,
    )
    num, _, den = result.stdout.strip().partition("/")
    return float(num) / float(den or 1)


def build_endcard_image(src, out_path, line1, line2, handle):
    img = Image.open(src).convert("RGB").resize((W, H))
    img = ImageEnhance.Brightness(img).enhance(0.55)
    draw = ImageDraw.Draw(img)
    font_big = ImageFont.truetype(FONT_BOLD, 90)
    font_small = ImageFont.truetype(FONT_BOLD, 55)

    def centered(y, text, font, fill="white"):
        bbox = draw.textbbox((0, 0), text, font=font)
        w = bbox[2] - bbox[0]
        x = (W - w) / 2
        for dx, dy in [(-3, -3), (-3, 3), (3, -3), (3, 3), (0, -3), (0, 3), (-3, 0), (3, 0)]:
            draw.text((x + dx, y + dy), text, font=font, fill="black")
        draw.text((x, y), text, font=font, fill=fill)

    centered(820, line1, font_big)
    centered(940, line2, font_big)
    if handle:
        centered(1080, handle, font_small, fill="yellow")
    img.save(out_path, quality=95)


def build_endcard_video(image_path, out_path, hold_s, fps):
    subprocess.run(
        ["ffmpeg", "-y", "-loop", "1", "-i", image_path,
         "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo", "-t", str(hold_s),
         "-vf", f"fps={fps},format=yuv420p",
         "-c:v", "libx264", "-crf", "18", "-preset", "veryfast", "-pix_fmt", "yuv420p",
         "-c:a", "aac", "-ar", "48000", "-ac", "2", "-shortest", out_path],
        check=True, capture_output=True,
    )


def concat(main_video, endcard_video, out_path, tmpdir):
    # concat demuxer resolves relative paths against the list file's own
    # directory (tmpdir here), not the caller's cwd -- always write
    # absolute paths or a relative main_video silently fails to resolve.
    list_path = Path(tmpdir) / "concat.txt"
    main_video_abs = str(Path(main_video).resolve())
    endcard_video_abs = str(Path(endcard_video).resolve())
    list_path.write_text(f"file '{main_video_abs}'\nfile '{endcard_video_abs}'\n")
    subprocess.run(
        ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(list_path), "-c", "copy", out_path],
        check=True, capture_output=True,
    )


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("video")
    p.add_argument("out")
    p.add_argument("--handle", default="@AmreetAint")
    p.add_argument("--line1", default="CHECK FULL VIDEO")
    p.add_argument("--line2", default="AND SUBSCRIBE")
    p.add_argument("--hold", type=float, default=3.0)
    args = p.parse_args()

    with tempfile.TemporaryDirectory() as tmpdir:
        last_frame = Path(tmpdir) / "last.jpg"
        endcard_img = Path(tmpdir) / "endcard.jpg"
        endcard_vid = Path(tmpdir) / "endcard.mp4"

        grab_last_frame(args.video, str(last_frame))
        build_endcard_image(str(last_frame), str(endcard_img), args.line1, args.line2, args.handle)
        build_endcard_video(str(endcard_img), str(endcard_vid), args.hold, get_fps(args.video))
        concat(args.video, str(endcard_vid), args.out, tmpdir)

    print(f"wrote {args.out}", file=sys.stderr)


if __name__ == "__main__":
    main()
