#!/usr/bin/env python3
"""Find the horizontal seam between a facecam feed (top) and gameplay footage
(bottom) in a stacked-layout vertical clip (Amreet Aint's format: facecam
baked into the corner... for these gameplay VODs specifically, facecam sits
in its own band on top, gameplay fills the rest).

Works by grabbing one frame and finding the sharpest row-to-row average-
brightness discontinuity in the upper-middle band of the frame (facecam
bands are typically vivid/lit, gameplay footage below often starts darker
or just visually distinct) — a hard seam between two independent video feeds
shows up as a much bigger jump than normal in-scene gradients.

Usage:
  python3 detect_seam.py CLIP.mp4 [--time T]
  python3 detect_seam.py FRAME.png

Prints a single integer: the pixel row (y) of the seam. Sanity-check it once
per clip layout by cropping +-50px around the printed row (this repo's ffmpeg
has no drawtext, so eyeballing via Read on a cropped PNG is the fast path).
"""
import argparse
import os
import subprocess
import tempfile

import numpy as np
from PIL import Image


def get_frame(path, t):
    if path.lower().endswith((".png", ".jpg", ".jpeg")):
        return Image.open(path).convert("RGB")
    fd, tmp = tempfile.mkstemp(suffix=".png")
    os.close(fd)
    subprocess.run(
        ["ffmpeg", "-y", "-ss", str(t), "-i", path, "-frames:v", "1", tmp],
        check=True, capture_output=True,
    )
    img = Image.open(tmp).convert("RGB")
    os.remove(tmp)
    return img


def find_seam(img, lo_frac=0.25, hi_frac=0.65):
    arr = np.array(img)
    row_means = arr.mean(axis=(1, 2))
    diffs = np.abs(np.diff(row_means))
    h = len(diffs)
    lo, hi = int(h * lo_frac), int(h * hi_frac)
    window = diffs[lo:hi]
    return lo + int(np.argmax(window))


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("path", help="video file or a single extracted frame (png/jpg)")
    p.add_argument("--time", type=float, default=5.0, help="timestamp to sample if PATH is a video (default 5s)")
    args = p.parse_args()
    img = get_frame(args.path, args.time)
    print(find_seam(img))


if __name__ == "__main__":
    main()
