#!/usr/bin/env python3
"""Clean a YouTube .vtt subtitle file and slice it by time.

Two subcommands:

  clean   Dedupe rolling auto-caption repeats and group into minute buckets.
          Good for scanning a long video to find interesting sections.

  window  Print fine-grained, cue-level lines (with HH:MM:SS timestamps) for a
          given time range. Use after `clean` to pull verbatim quotes for a clip.

Timestamps for `window` accept either seconds (e.g. 1830) or HH:MM:SS / MM:SS.

Examples:
  python3 transcript.py clean  vid.en.vtt --out vid_clean.txt
  python3 transcript.py window vid.en.vtt 03:01:00 03:12:30
"""
import argparse
import re
import sys

TS_RE = re.compile(r"(\d{2}):(\d{2}):(\d{2})\.\d{3} --> ")
TAG_RE = re.compile(r"<[^>]+>")


def parse_cues(path):
    """Return [(seconds, text)] from a VTT file, one entry per caption line."""
    cues = []
    cur = None
    for raw in open(path, encoding="utf-8").read().splitlines():
        m = TS_RE.match(raw)
        if m:
            h, mm, s = int(m.group(1)), int(m.group(2)), int(m.group(3))
            cur = h * 3600 + mm * 60 + s
            continue
        if cur is None or "align:" in raw or "-->" in raw:
            continue
        txt = TAG_RE.sub("", raw).strip()
        txt = (txt.replace("&gt;", "").replace("&lt;", "").replace("&amp;", "&")
                  .replace("&nbsp;", " ").replace("__", "[bleep]").strip())
        if txt:
            cues.append((cur, txt))
    return cues


def dedupe(cues, lookback=8):
    """Drop rolling-caption repeats: skip a line already seen in the recent window."""
    seen, out = [], []
    for ts, txt in cues:
        if txt in seen:
            continue
        seen.append(txt)
        if len(seen) > lookback:
            seen.pop(0)
        out.append((ts, txt))
    return out


def fmt(sec):
    return f"{sec // 3600:02d}:{(sec % 3600) // 60:02d}:{sec % 60:02d}"


def to_seconds(val):
    if ":" not in val:
        return int(val)
    parts = [int(p) for p in val.split(":")]
    while len(parts) < 3:
        parts.insert(0, 0)
    h, m, s = parts[-3], parts[-2], parts[-1]
    return h * 3600 + m * 60 + s


def cmd_clean(args):
    cues = dedupe(parse_cues(args.vtt))
    buckets = {}
    for ts, txt in cues:
        buckets.setdefault(ts // 60, []).append(txt)
    lines = [f"[{fmt(b * 60)}] {' '.join(txts)}" for b, txts in sorted(buckets.items())]
    body = "\n\n".join(lines) + "\n"
    if args.out:
        open(args.out, "w", encoding="utf-8").write(body)
        total = cues[-1][0] if cues else 0
        print(f"wrote {args.out}  |  duration {fmt(total)}  |  "
              f"{len(cues)} cues  |  {len(buckets)} minute-buckets")
    else:
        sys.stdout.write(body)


def cmd_window(args):
    start, end = to_seconds(args.start), to_seconds(args.end)
    cues = dedupe(parse_cues(args.vtt))
    for ts, txt in cues:
        if start <= ts <= end:
            print(f"[{fmt(ts)}] {txt}")


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    c = sub.add_parser("clean", help="dedupe + minute-bucket the whole file")
    c.add_argument("vtt")
    c.add_argument("--out", help="write to file instead of stdout")
    c.set_defaults(func=cmd_clean)

    w = sub.add_parser("window", help="fine-grained cues for a time range")
    w.add_argument("vtt")
    w.add_argument("start", help="HH:MM:SS, MM:SS, or seconds")
    w.add_argument("end", help="HH:MM:SS, MM:SS, or seconds")
    w.set_defaults(func=cmd_window)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
