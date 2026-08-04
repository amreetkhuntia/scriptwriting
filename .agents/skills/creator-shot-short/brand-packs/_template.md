# Brand pack — <CHANNEL NAME>  (copy this file, fill it in, drop the leading _)

One-line vibe of the channel's look (e.g. "gaming/horror, warm-grunge, red accent, facecam-in-corner").

| Field | Value |
|---|---|
| **Media root** | `/mnt/f/recordings/<…>/` — shorts under `…/shorts/<NN-slug>/` (`src/`, `vo/`, `out/`). Raw takes at `…/<video>/*.mkv` (+ `.srt` if any). |
| **public symlink** | `remotion-all/public/<name>` → `<media shorts folder>` (mirror the `007clips` / `aitalks-shorts` pattern). |
| **Component library** | `remotion-all/src/<Channel>/` + `theme.ts`. If none exists, scaffold one (palette + `SceneBackground` equivalent + a hook-slam + a stat component). |
| **Palette** | scene/bg + 2–3 accent colors (win / alert / neutral). |
| **Fonts** | impact (hook slams) / display (titles) / body (captions). |
| **Background** | the deterministic full-screen ground component. |
| **Hook-slam component** | the big one-liner reveal. |
| **Stat component** | count-up / number-punch. |
| **Caption / receipts** | caption style + any receipt cards (search / headline / quote). |
| **Hook VO voice** | vidIQ `voiceId` **or** "creator records own 3–4s hook". |
| **Caption language** | e.g. "English captions over Hindi audio" / "Hinglish" / "English". |
| **CTA end card** | eyebrow + parent-title + subscribe styling. |
| **Canonical build** | fill after the first reel is built (the `…Talk.tsx` file + comp id). |

**Parent long-forms + IDs:** …

**Notes / sub-themes:** …

---
### How to use
1. Fill this in for the new channel.
2. Follow `../SKILL.md` — the pipeline is identical; only these values change.
3. First build: copy `remotion-all/src/AIJobs/clips/AIJobsReel1Talk.tsx` → `remotion-all/src/<Channel>/clips/<Name>Talk.tsx`, swap the components/colors listed above, register in that channel's `index.tsx`.
