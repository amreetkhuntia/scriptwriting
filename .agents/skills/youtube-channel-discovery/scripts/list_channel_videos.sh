#!/usr/bin/env bash
# List a YouTube channel's own videos/streams/shorts via yt-dlp --flat-playlist —
# no API key, no MCP server, works anonymously. This is the "find the video in
# the first place" step for a channel you don't have a URL for yet.
#
# Usage: list_channel_videos.sh CHANNEL [TAB] [LIMIT]
#   CHANNEL  a handle (@name), a channel ID (UC...), or a full channel URL
#   TAB      videos | streams | shorts   (default: videos)
#   LIMIT    max entries to list (default: 30)
#
# NOTE: upload_date comes back "NA" in flat-playlist mode — this only lists
# id/duration/title cheaply. Get real dates for your shortlisted candidates
# with a per-video call (see SKILL.md step 2).
set -euo pipefail

CHANNEL="${1:?usage: list_channel_videos.sh CHANNEL [TAB] [LIMIT]}"
TAB="${2:-videos}"
LIMIT="${3:-30}"

case "$CHANNEL" in
  http*) URL="$CHANNEL" ;;
  @*) URL="https://www.youtube.com/$CHANNEL" ;;
  UC*) URL="https://www.youtube.com/channel/$CHANNEL" ;;
  *) URL="https://www.youtube.com/@$CHANNEL" ;;
esac

# strip a trailing tab the caller may have already included
URL="${URL%/videos}"
URL="${URL%/streams}"
URL="${URL%/shorts}"

yt-dlp --flat-playlist --playlist-end "$LIMIT" \
  --print "%(id)s | %(duration_string)s | %(title)s" \
  "$URL/$TAB"
