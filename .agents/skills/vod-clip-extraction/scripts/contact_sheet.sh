#!/usr/bin/env bash
# Build a labeled contact sheet of the IN + OUT frame of every .mp4 in a folder,
# so a batch of cut clips can be verified at a glance (ImageMagick `montage` is
# usually not installed, so this tiles with ffmpeg).
#
# Usage: contact_sheet.sh <clips_dir> [out.png]
set -euo pipefail
DIR="${1:?usage: contact_sheet.sh <clips_dir> [out.png]}"
OUT="${2:-/tmp/contact_sheet.png}"
FONT="$(fc-list 2>/dev/null | grep -iE 'DejaVuSans\.ttf' | head -1 | cut -d: -f1)"
TMP="$(mktemp -d)"
i=0
for f in "$DIR"/*.mp4; do
  [ -e "$f" ] || { echo "no .mp4 files in $DIR" >&2; exit 1; }
  n="$(basename "$f" .mp4)"
  dur="$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$f")"
  outt="$(python3 -c "print(max(0,$dur-3))")"
  idx="$(printf '%03d' "$i")"
  lab() { # <seek> <tag IN|OUT> <color>
    ffmpeg -y -ss "$1" -i "$f" -frames:v 1 \
      -vf "scale=640:-1,drawtext=fontfile='$FONT':text='$n $2':x=8:y=6:fontsize=30:fontcolor=$3:box=1:boxcolor=black@0.7" \
      "$TMP/${idx}_$2.jpg" 2>/dev/null
  }
  lab 1 IN yellow            # ~1s in (the cut's start)
  lab "$outt" OUT cyan       # ~3s before the end (the cut's tail)
  i=$((i + 1))
done
cnt=$(ls "$TMP"/*.jpg | wc -l)
rows=$(( (cnt + 3) / 4 ))
ffmpeg -y -pattern_type glob -i "$TMP/*.jpg" \
  -vf "tile=4x${rows}:margin=6:padding=4:color=white" "$OUT" 2>/dev/null
rm -rf "$TMP"
echo "wrote $OUT  ($cnt frames, 4x${rows} grid)"
