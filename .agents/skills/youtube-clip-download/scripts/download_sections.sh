#!/usr/bin/env bash
# Download only specific time ranges from a YouTube video — no full download.
# Each range is fetched on its own with `yt-dlp --download-sections` and saved as
# a separately-named mp4, so you can ask for several disjoint clips at once.
#
# Usage: download_sections.sh [-o OUTDIR] [-q MAXHEIGHT] [-x] URL RANGE [RANGE ...]
#   URL        a YouTube watch/live/youtu.be/shorts URL (or a bare 11-char ID)
#   RANGE      START-END, where START/END are HH:MM:SS, MM:SS, or raw seconds
#              e.g.  12:30-13:05   41:20-42:00   90-135
#   -o OUTDIR  output directory (default: ./clips)
#   -q MAXH    max video height, e.g. 1080 / 1440 / 2160 (default: 1080)
#   -x         frame-exact cut (--force-keyframes-at-cuts; re-encodes, slower).
#              Default is a fast keyframe cut: output may start a few seconds
#              early at the nearest keyframe; length is ~ the requested length.
set -euo pipefail

OUTDIR="./clips"
MAXH="1080"
EXACT=""

while getopts ":o:q:xh" opt; do
  case "$opt" in
    o) OUTDIR="$OPTARG" ;;
    q) MAXH="$OPTARG" ;;
    x) EXACT="--force-keyframes-at-cuts" ;;
    h) grep '^#' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    :) echo "error: -$OPTARG needs an argument" >&2; exit 2 ;;
    \?) echo "error: unknown option -$OPTARG" >&2; exit 2 ;;
  esac
done
shift $((OPTIND - 1))

URL="${1:?usage: download_sections.sh [-o OUTDIR] [-q MAXHEIGHT] [-x] URL RANGE [RANGE ...]}"
shift
[ "$#" -ge 1 ] || { echo "error: give at least one START-END range" >&2; exit 2; }

mkdir -p "$OUTDIR"
i=1
for RANGE in "$@"; do
  case "$RANGE" in
    *-*) : ;;
    *) echo "error: '$RANGE' is not START-END (e.g. 12:30-13:05)" >&2; exit 2 ;;
  esac
  # filesystem-safe label: 12:30-13:05 -> 12-30-13-05
  LABEL="$(printf '%s' "$RANGE" | tr ':' '-')"
  IDX="$(printf '%02d' "$i")"
  echo ">> [$IDX] downloading section *$RANGE" >&2
  yt-dlp -f "bestvideo[height<=$MAXH]+bestaudio/best[height<=$MAXH]/best" \
    --download-sections "*$RANGE" --merge-output-format mp4 --no-part \
    ${EXACT:+$EXACT} \
    -o "$OUTDIR/${IDX}_${LABEL}.%(ext)s" "$URL"
  i=$((i + 1))
done

echo "wrote ${OUTDIR%/}/ :" >&2
ls -1 "$OUTDIR"/*.mp4 2>/dev/null || echo "  (no .mp4 produced — check the warnings above)" >&2
