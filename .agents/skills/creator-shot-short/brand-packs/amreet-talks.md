# Brand pack — Amreet Talks (AI/tech explainers)

Faceless-leaning AI/business explainers; the creator-shot short adds his face as the funnel spine. Dark, high-contrast, cyan-accent motion-graphics.

| Field | Value |
|---|---|
| **Media root** | `/mnt/f/recordings/ai talks/` — shorts under `/mnt/f/recordings/ai talks/shorts/<NN-slug>/` (`src/`, `vo/`, `out/`). Raw takes at `/mnt/f/recordings/ai talks/<video>/*.mkv` (+ `.srt`). |
| **public symlink** | `remotion-all/public/aitalks-shorts` → `/mnt/f/recordings/ai talks/shorts` — so `staticFile("aitalks-shorts/<slug>/src/…mp4")` resolves. |
| **Component library** | `remotion-all/src/AIJobs/` (per-video folders exist: `AIJobs/`, `Fable5/`, `China/`, `AIBubble/`). `theme.ts` per folder. |
| **Palette** (`AIJobs/theme.ts`) | dark navy scene; accents `colors.skyLight="#6EE7F9"` (cyan = win), `signal.bad="#FB7185"` (rose = fear/predicted), `signal.good="#34D399"` (emerald). |
| **Fonts** | `fonts.impact` = Anton (hook slams), `fonts.display` = Bebas (section titles), `fonts.body` = Montserrat (captions/labels). |
| **Background** | `SceneBackground` (noise drift + cyan glow + vignette, deterministic). |
| **Hook-slam component** | local `ImpactLine` (Anton, damped-spring pop + glow) — copy from `AIJobsReel1Talk.tsx`. |
| **Stat component** | `AIJobs/components/StatCounter` (count-up; `to/suffix/lead/label/color/accent/entrance/fontSize`). |
| **Caption / receipts** | in-file `Caption` (lower-third pill, keyword pops cyan), `SearchCard` (search-bar + result snippet), `HeadlineChip` (news-source + headline) — all in `AIJobsReel1Talk.tsx`. |
| **Hook VO voice** | ElevenLabs **Liam** via vidIQ, `voiceId TX3LPaxmHKxFdv7VOQHJ` (energetic male). Reuse/trim an existing reel VO for the hook (zero cost) when the words match. |
| **Caption language** | **English captions over his Hindi/Hinglish audio** (matches his published style; works on mute; broadens reach). |
| **CTA end card** | cyan "▶ WATCH THE FULL VIDEO" eyebrow + big white/cyan parent title + "Link in description · Subscribe". |
| **Canonical build** | `remotion-all/src/AIJobs/clips/AIJobsReel1Talk.tsx` (comp id `AIJobs-Reel1-Talk`, 555f). Output `01-aijobs-person/out/r1-talk.mp4`. |

**Parent long-forms + IDs:** AI Jobs `V2-_0JBnP2w`, China `wLSqttwg0JU`, AI Bubble `Nv0W9K-cDQ4`, Fable 5 `9hNiFmOZCw0`. Full 12-reel plan: `channels/Amreet Talks/shorts/shorts-plan.md`.

**Notes:** Fable5 has a *cream editorial* sub-theme (`Fable5/theme.ts`, Fraunces serif, clay accent) — if a creator short is cut from the Fable5 parent, use that palette/components instead of the dark AIJobs one.
