#!/usr/bin/env python3
"""Burn dynamic, word-synced captions (with optional emoji) onto a cut clip.

Renders each caption as its own transparent PNG via Pillow (this repo's
ffmpeg has no drawtext/libfreetype — do not try ffmpeg's text filters) then
composites them onto the video with a chained ffmpeg overlay filter, each
one only visible during its own time window (`enable='between(t,start,end)'`).

Usage:
  python3 caption_overlay.py VIDEO.mp4 MANIFEST.json SEAM_Y OUT.mp4

MANIFEST.json: a JSON list of caption cards, each
  {"text": "...", "start": 12.3, "end": 15.6, "emoji": "💀" | null}
`start`/`end` are seconds, ABSOLUTE within VIDEO.mp4 (already-trimmed clip,
so time 0 = the clip's own start). If your clip is a jump-cut spliced from
multiple source segments, remember to offset each segment's word timestamps
by the CUMULATIVE duration of the segments before it — add the offset once,
not per-segment-again (easy bug: doubling an offset by re-adding it).

SEAM_Y: the y-pixel row to center each caption band on — get it from
`detect_seam.py`, or hardcode once per channel/layout since it doesn't
change between clips from the same recording setup.

Caption text conventions (matches what shipped well for Amreet Aint):
- Devanagari doesn't render in Impact (Latin-only font) — write captions in
  Hinglish (Roman-script transliteration), colloquial, matching how the
  streamer actually talks, not a formal translation.
- Verify each line against what's actually being said, not just the literal
  ASR transliteration — Hindi ASR auto-captions phonetically mishear real
  words as similar-sounding ones (e.g. "revive" transcribed as "rep", "addict"
  transcribed as "edit"). Read the raw quote and sanity-check odd words
  before locking in the caption text.
- 2-6 words per card, broken at natural speech pauses (the auto-caption
  cue boundaries are a good default breakpoint).
- Add an emoji on reaction/punchline words (bleep/curses -> \U0001F480 or
  \U0001F92C, panic exclamations -> \U0001F62D/\U0001F631, pain sounds ->
  \U0001F635, jokes -> \U0001F602) — not on every card, just the beats that
  land.
"""
import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

FONT_BOLD = "/System/Library/Fonts/Supplemental/Impact.ttf"
EMOJI_FONT = "/System/Library/Fonts/Apple Color Emoji.ttc"
# Apple Color Emoji only has bitmap strikes at these exact sizes — anything
# else throws "invalid pixel size". Render at the largest (160) and resize
# down with Pillow for whatever target size you actually want.
EMOJI_STRIKE_SIZE = 160
W = 1080
CARD_H = 130
FONT_SIZE = 58
EMOJI_SIZE = 90


def get_emoji_img(emoji, size):
    img = Image.new("RGBA", (EMOJI_STRIKE_SIZE, EMOJI_STRIKE_SIZE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(EMOJI_FONT, EMOJI_STRIKE_SIZE)
    draw.text((0, 0), emoji, font=font, embedded_color=True)
    bbox = img.getbbox()
    if bbox:
        img = img.crop(bbox)
    return img.resize((size, max(1, int(size * img.height / img.width))))


def make_card(text, emoji, out_path, width=W, height=CARD_H, font_size=FONT_SIZE, emoji_size=EMOJI_SIZE):
    canvas = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(canvas)
    font = ImageFont.truetype(FONT_BOLD, font_size)

    emoji_img = get_emoji_img(emoji, emoji_size) if emoji else None
    emoji_w = emoji_img.width + 20 if emoji_img else 0

    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    total_w = tw + emoji_w
    x = (width - total_w) / 2
    y = (height - th) / 2 - bbox[1]

    for dx, dy in [(-3, -3), (-3, 3), (3, -3), (3, 3), (0, -3), (0, 3), (-3, 0), (3, 0)]:
        draw.text((x + dx, y + dy), text, font=font, fill=(0, 0, 0, 255))
    draw.text((x, y), text, font=font, fill=(255, 255, 255, 255))

    if emoji_img:
        ey = (height - emoji_img.height) // 2
        canvas.paste(emoji_img, (int(x + tw + 20), ey), emoji_img)

    canvas.save(out_path)


def build_overlay_chain(video_in, cards, tmpdir, seam_y, out_path):
    inputs = ["-i", video_in]
    for i, _ in enumerate(cards):
        inputs += ["-i", str(Path(tmpdir) / f"card_{i:02d}.png")]

    filter_parts = []
    prev = "0:v"
    for i, card in enumerate(cards):
        idx = i + 1
        out_label = f"v{i}" if i < len(cards) - 1 else "vout"
        filter_parts.append(
            f"[{prev}][{idx}:v]overlay=0:{seam_y}:"
            f"enable='between(t,{card['start']},{card['end']})'[{out_label}]"
        )
        prev = out_label

    cmd = ["ffmpeg", "-y"] + inputs + [
        "-filter_complex", ";".join(filter_parts),
        "-map", "[vout]", "-map", "0:a",
        "-c:v", "libx264", "-crf", "18", "-preset", "veryfast", "-pix_fmt", "yuv420p",
        "-c:a", "copy",
        out_path,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(result.stderr[-3000:], file=sys.stderr)
        raise SystemExit(f"ffmpeg failed (exit {result.returncode})")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("video")
    p.add_argument("manifest_json")
    p.add_argument("seam_y", type=int)
    p.add_argument("out")
    args = p.parse_args()

    cards = json.load(open(args.manifest_json, encoding="utf-8"))
    if not cards:
        raise SystemExit("manifest has no cards")

    with tempfile.TemporaryDirectory() as tmpdir:
        for i, c in enumerate(cards):
            make_card(c["text"], c.get("emoji"), Path(tmpdir) / f"card_{i:02d}.png")
        build_overlay_chain(args.video, cards, tmpdir, args.seam_y, args.out)

    print(f"wrote {args.out}  ({len(cards)} caption cards)", file=sys.stderr)


if __name__ == "__main__":
    main()
