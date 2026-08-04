# Elden Ring — Vertical Streams · cut-list.md

**Standalone clip candidates, not a supercut.** Each row below is its own independently-postable
YouTube Short + Instagram Reel. Source video is native **1080x1920** — no facecam-corner reframe
needed. Timestamps are **cue-level exact** (pulled via `transcript.py window` on YouTube's real
`hi-orig` Hindi auto-caption track, not approximated from minute buckets). Tier: **S** = must-clip
standout · **A** = strong · **B** = optional/filler-ish. Quotes are the original Hindi ASR text
(phonetic Devanagari, code-switched English spelled out); `[bleep]` = YouTube's profanity filter.

**Two visual-verification passes so far.** Pass 1 sampled a fixed 4 frames per candidate regardless
of length and produced real false positives (a "died to a literal car" S-tier pick was pure
talking-to-chat). Pass 2 fixed that: **frame count now scales with duration**
(`clamp(ceil(duration/8), 4, 16)` via `candidate_preview.py --frames auto`), and every candidate that
survived pass 1 was re-checked end-to-end for two things pass 1 never asked: (a) does the **entire**
window hold up, not just some frames, and (b) does the **facecam reaction actually change** across
the window (a flat, static expression throughout is a warning sign even when the game-side frames
show real combat). This caught a second wave of problems pass 1 missed — including two more S-tier
picks that turned out to be filler-dominated once sampled densely.

**Marking key:** `✓` = confirmed across both passes, ready to cut as-is · `⟲` = core moment is real
but the pass-2 audit found dead material at the head/tail — **use the tightened in/out shown, not
the original span** · *(unverified)* = B-tier, never visually checked · dropped rows are removed
from the tables below entirely — see the Rejected appendix.

## Source VODs
Resolution was verified via `yt-dlp -F` (actual format list), **not** the title's "| Vertical" tag —
the tag is inconsistent (`jd9BmFyCIn8`, `hCbf17Aj9CI`, `y9ikYH3oECU`, `j8fuJ2xbVIg`, `2pIPs_ut25o`,
`AF_7niXth8g` have no tag but are still confirmed 1080x1920).

| Video ID | Title | Uploaded | Duration | Views |
|---|---|---|---|---|
| `NxOMr6_jzA4` | All Bosses Run \| Vertical | 2026-07-08 | 3:30:24 | 3 |
| `jd9BmFyCIn8` | ULTIMATE Elden Ring Playthrough | 2026-07-07 | 1:24:45 | 6 |
| `j39NRXGraXw` | The ULTIMATE Elden Ring Playthrough \| Vertical | 2026-07-05 | 2:16:09 | 5 |
| `hCbf17Aj9CI` | Elden Ring playthrough | 2026-07-04 | 2:25:22 | 7 |
| `vqya4IBji58` | The Max Bleed Run is Here \| Vertical | 2026-07-01 | 1:53:54 | 2 |
| `y9ikYH3oECU` | Best Player is here | 2026-06-30 | 1:14:50 | 14 |
| `j8fuJ2xbVIg` | Best Player is here | 2026-06-28 | 1:39:27 | 4 |
| `2pIPs_ut25o` | Elden Ring (mislabeled #shorts) | 2026-06-28 | 1:12:19 | 3 |
| `AF_7niXth8g` | Elden Ring (mislabeled #shorts) | 2026-06-27 | 2:39:18 | 1 |

Total ≈ **18.3 hours** across 9 streams. All essentially unwatched as VODs — high headroom for
repurposing.

---

## Quick-start: 12 fully-confirmed S-tier picks
Down from the original 20 → 15 (after pass 1) → **12 now** (after pass 2). Two more S-tier picks
that looked solid after pass 1 (`vqya4IBji58` Tree Sentinel "perfect run" and `2pIPs_ut25o`'s Patches
payoff) turned out on dense review to be dominated by dead time or menu/black/desktop frames and are
now fully dropped — see the Rejected appendix. **7 of these 12 need the tightened in/out below, not
the original span** (marked ⟲) — the moment is real, but part of the original window was filler.

**All 12 are now PRODUCED** — captioned, end-carded, and sitting in `~/Desktop/clips/` numbered
`01`–`12` to match this table's row order (for quick tracking of what's done). Production caught one
more filler tail during cutting: `jd9BmFyCIn8`'s Ancestor Spirit clip was re-tightened from
01:16:52→01:18:07 down to **01:16:52→01:17:15** after a from-scratch dense re-check found the last
~50s was calm Torrent traversal with no enemy on screen — the same failure pattern as the other ⟲
rows, just caught one stage later (during cutting instead of during the earlier audit passes).

| # | Stream | In → Out | Category | Label | Clip |
|---|---|---|---|---|---|
| 1 | ✓ `NxOMr6_jzA4` | 02:19:58 → 02:20:53 | BOSS | Calls the boss "cancer-shaped," dies the instant he says it, then repeats the irony — retimed to end right after the joke lands, before the reload/retry that followed in the original cut | `01-cancer-boss-instant-death.mp4` |
| 2 | ⟲ `NxOMr6_jzA4` | 03:17:56 → 03:18:58 | RAGE | "Hand" enemies flip him the middle finger — "I hate these hands" (was 03:17:56→03:19:10; trimmed a dead location-card + inventory-menu tail) | `02-hand-enemies-middle-finger.mp4` |
| 3 | ✓ `NxOMr6_jzA4` | 01:29:47 → 01:31:00 | RAGE | "Bhai bhai bhai bhai!" — panicked wipe vs Weapon-Bequeathed Harmonia, facecam breaks into a laugh right at the DEFEAT screen | `03-bhai-bhai-bhai-panicked-wipe.mp4` |
| 4 | ⟲ `jd9BmFyCIn8` | 01:16:52 → 01:17:15 | BOSS | Boss fight vs the Ancestor Spirit (Siofra River) — its glowing red spirit-form charges him across the misty plain, ends on the kill screen + genuine fist-pump reaction (was 01:16:52→01:18:07; production cut found ~50s of no-enemy Torrent traversal past the kill and tightened further) | `04-ancestor-spirit-chase.mp4` |
| 5 | ⟲ `hCbf17Aj9CI` | 00:59:39 → 01:00:50 | BOSS | Clutch win vs Deathbird — "chill chill chill, we got it" (was 00:59:39→01:01:08; trimmed a calm Torrent ride-away tail) | `05-deathbird-clutch-win.mp4` |
| 6 | ✓ `y9ikYH3oECU` | 01:13:52 → 01:14:44 | RAGE | A corrupted save forces a restart — quits out to the Windows desktop (visible taskbar confirms it) | `06-corrupted-save-quit.mp4` |
| 7 | ✓ `j8fuJ2xbVIg` | 00:23:10 → 00:24:45 | BOSS | Rennala boss intro cutscene — comedic "the Queen betrayed us" reveal | `07-rennala-queen-betrayed-us.mp4` |
| 8 | ✓ `j8fuJ2xbVIg` | 00:51:24 → 00:52:51 | BOSS | Rennala's boss transformation — comedic "she turned into Goku" reaction | `08-rennala-goku-transform.mp4` |
| 9 | ⟲ `j8fuJ2xbVIg` | 00:57:03 → 00:57:30 | BOSS | "I hate this boss!" rage quote mid-fight (was 00:57:03→00:57:53; the "comedic surrender" tail was actually calm unrelated walking, cut) | `09-i-hate-this-boss-rennala.mp4` |
| 10 | ⟲ `AF_7niXth8g` | 00:52:55 → 00:53:25 | RAGE | Meltdown — "I am dead" spam dying to a bat/fire swarm (was 00:52:55→00:53:52; trimmed a post-death respawn-run + location-card tail) | `10-i-am-dead-meltdown.mp4` |
| 11 | ⟲ `AF_7niXth8g` | 01:52:46 → 01:53:08 | BOSS | "I hate this boss" — Red Wolf of Radagon (was 01:52:46→01:53:29; trimmed a calm walk-away tail) | `11-red-wolf-hate.mp4` |
| 12 | ⟲ `AF_7niXth8g` | 01:56:30 → 01:56:45 | RAGE | Furious taunt finally killing the Red Wolf of Radagon (was 01:56:30→01:57:03; trimmed a calm aftermath tail) | `12-red-wolf-scream-kill.mp4` |

---

## Full sweep, by stream
Rows are marked ✓ (confirmed both passes), ⟲ (tightened — **use the new in/out shown**, original
span noted in the label), or left plain for *(unverified)* B-tier. Dropped rows are removed — see
the Rejected appendix for all of them with reasons.

### `NxOMr6_jzA4` — All Bosses Run \| Vertical (3:30:24)
| In → Out | Cat | Tier | Label | Quote |
|---|---|---|---|---|
| 00:20:04→00:20:56 | BOSS | B | *(unverified)* Risky sneak-up on the Death Rite Bird before the pull | "मैं बैठ के ट्रोल क्यों मार रहा हूं? ओए साली गेट हियर... दैट वाज़ रिस्की [bleep]" |
| ⟲ 00:31:39→00:32:19 | BOSS | A | "I walked right into this shit" vs the Bell-Bearing Hunter, ends on the "YOU DIED" screen (was 00:31:39→00:33:15; cut a respawn/rest/loading tail) | "आई वक्ड राइट इंटू दिस शिट भाई... एक बार और ट्राई मारता हूं।" |
| 00:52:45→00:53:25 | BOSS | B | *(unverified)* "Easy boss, noob boss" — Fire Star dies instantly | "चलो भाई ये तो ईजी ईजी बॉस है। ऐसे ही मर गया साला नबड़ा बॉस फायर स्टार।" |
| 00:57:08→00:58:00 | BOSS | B | *(unverified)* "Who is this? Oh no..." — quick silent boss kill | "कौन है? ओ नो... मार देता है इसको हो गया।" |
| ✓ 01:01:16→01:01:57 | RAGE | A | "Instant karma" — co-op Erdtree Avatar fight: dies while still laughing, then "LEVEL LOST" sobers him up — a real, visible reaction swing | "हाउ इट बिकम बैड रन फ्रॉम गुड रन इंस्टेंट लाइक इंस्टेंट कर्मा हो गया।" |
| ✓ 01:03:07→01:03:50 | RAGE | A | "These guys are some bullshit" vs Cariniblade / Divine Beast Warrior — a real, building frustration | "ये कौन है बे? बहुत ही जिंदा है। व्हाट दिस गाइस आर सम बुल शट।" |
| 01:31:30→01:32:00 | RAGE | B | *(unverified)* "Made Rakhi cry on Discord" — bragging about the beating he gave | "देख रहे हो 63 आवर्स ओ राखी को डीसी पर रुला दिया भाई।" |
| ✓ 01:29:47→01:31:00 | RAGE | S | "Bhai bhai bhai bhai!" — panicked wipe vs Weapon-Bequeathed Harmonia | "व्हाट द [bleep] भाई भाई भाई भाई बच गए ब्रो... मैं कितना रेप दूं भाई।" |
| 01:41:27→01:41:54 | BOSS | B | *(unverified)* "I'm a noob" — self-deprecating after the boss finally drops | "नूब है भाई। ज्यादा दिमाग लगा रहा था मैं... यह बंदा मर गया।" |
| ✓ 02:17:21→02:18:29 | RAGE | A | "India is not for beginners" — catacomb tension building to a boss reveal, facecam builds to a genuine laugh | "दैट वास सो [bleep] टाइमिंग भाई... इंडिया इज़ नॉट फॉर बिगिनर्स मैन।" |
| ✓ 02:19:58→02:20:53 | BOSS | S | Calls the boss "cancer-shaped," dies the instant he says it (retimed — see Quick-start) | "ये कैंसर की शक्ल का था... बोलते ही मर गया... जैसे ही बोला कैंसर का शक्ल का है मार दिया।" |
| 02:22:25→02:22:57 | BOSS | B | *(unverified)* Confirmed kill — "the cancer boss" is finally dead | "मार दिया भाई कैंसर बॉस है भाई एक्चुअल में कैंसर बॉस है।" |
| ✓ 02:43:20→02:43:38 | BOSS | A | "That was so f***ing close" — continuous close-quarters danger the entire 18s, no filler | "ब्रो दैट वास सो क्लोज दैट वास सो [bleep] क्लोज।" |
| 03:02:58→03:03:18 | RAGE | B | *(unverified)* "I should die to this guy, I'm perfect" — ironic overconfidence right before dying | "आई शुड डाई टू दिस गाय भाई आई एम परफेक्ट।" |
| ⟲ 03:17:56→03:18:58 | RAGE | S | "Hand" enemies flip him the middle finger — "I hate these hands" (was →03:19:10; cut a location-card + inventory-menu tail) | "मिडिल फिंगर दिखाता भाई ये बंदे... आई हेट दिस हाथ्स।" |
| ⟲ 03:27:25→03:28:24 | BOSS | A | "I hate this guy, round two" — final boss fight (was 03:26:54→03:28:24; cut a ~30s calm-walk/loading-card intro) | "आई हेट दिस गाय बेसिकली... असली हाथ तो इस बंदे के है भाई।" |

*Dropped from this stream (pass 1 + pass 2 combined): 01:33:44, 01:36:05, 01:52:30, 03:09:39 (the
original "died to a car" clip), 03:23:28 (was reacting to a YouTube video, not his own gameplay),
00:25:14 ("surprise instant kill" — 75% of the window is a frozen loot-pickup screen), 01:06:53
("chaotic meltdown" — mostly calm hillside walking either side of a brief effect), 01:37:02 ("3
deaths" — 78% of the window is Roundtable Hold hub/menu browsing), 01:39:12 ("range this big" —
mostly a checkpoint reload + weapon-menu screens), 03:20:01 ("hand grab + beast" — flat facecam the
entire 75s, likely two stitched incidents). See the Rejected appendix for detail.*

### `jd9BmFyCIn8` — ULTIMATE Elden Ring Playthrough (1:24:45)
| In → Out | Cat | Tier | Label | Quote |
|---|---|---|---|---|
| ✓ 00:07:10→00:07:52 | RAGE | A | Meltdown vs the Stonedagger Troll — fight → death → rant → cool-down, facecam tracks the whole arc | "शिट शिट ब्रो आई फक्ड अप आई [bleep] अप आई [bleep] अप आई [bleep] अप।" |
| 00:16:11→00:16:47 | BOSS | B | *(unverified)* Taunts the boss to "come get wrecked/tracked" before the fight | "आ जाओ भाई आ जाओ भाई तुम लोग भी क्या याद रखोगे इधर आओ गेट इट रेग्ड गेट ट्रैक्ड गेट ट्रैक्ड।" |
| 00:30:06→00:30:35 | RAGE | B | *(unverified)* Comes back visibly on-edge — "feeling tense today" rant to chat | "यो कैसे हो? अरे माल भगत मादर भगत रुक जा रुक जा भाई आज मैं टेंशन में लग रहा यार।" |
| ✓ 00:32:01→00:32:59 | RAGE | A | A dangerous bear closes in — facecam visibly tightens from relaxed to tense/yelling as it corners him | "खतरनाक भालू दिमाग गरम कर दिया था... तेरी गांड में दूंगा डंडा।" |
| 00:36:39→00:37:56 | BOSS | B | *(unverified)* Boss phase-2 transition — "he got shocked!", boss suddenly deals no damage | "फेस टू फेस टू... ब्रो ही गॉट शगर्ड वाओ ये बंदा कुछ डैमेज ही नहीं दे रहा है।" |
| 01:12:06→01:12:51 | RAGE | B | *(unverified)* Aggressive trash-talk at an enemy | "ठीक है भाई जल्दी जल्दी आगे आ... यू बॉय तेरे को इतना पीटूंगा।" |
| ⟲ 01:16:52→01:17:15 | BOSS | S | Boss fight vs the Ancestor Spirit (Siofra River) — chase/fight/kill/reaction (was 01:16:52→01:18:07; production cut found ~50s of no-enemy Torrent traversal past the kill screen and tightened further — PRODUCED as `04-ancestor-spirit-chase.mp4`) | "ओ नो साला नो हिट का प्लान लेफ्टेड हो गया... रेडान का पूरा सेट था बे।" |

*Dropped: 00:13:48 ("catacombs skirmish" — flat facecam throughout, low-threat enemy, no boss bar,
confirmed dead on dense review).*

### `j39NRXGraXw` — The ULTIMATE Elden Ring Playthrough \| Vertical (2:16:09)
| In → Out | Cat | Tier | Label | Quote |
|---|---|---|---|---|
| ⟲ 02:06:06→02:06:38 | BOSS | A | Godrick the Grafted boss fight and kill (was 02:06:06→02:06:45; cut a trailing equipment-menu frame) | "आई एम द लॉर्ड। हां भाई तू [bleep] है... दिस गाइस आई कैन ट्राई ईजी।" |
| ✓ 02:13:23→02:14:59 | BOSS | A | Flying Dragon Agheel killed in a dramatic finishing blow, facecam builds to a clear grin at the kill | "लोल ब्रो दैट इज लाइक द ग्रेटेस्ट किल एवर भाई व्हाट द [bleep]।" |
| 00:55:24→00:55:41 | RAGE | B | *(unverified)* Explosive mid-fight cursing/yelling at an enemy | "अरे ओए ओए साले... रुक जा।" |
| 00:49:02→00:52:00 | RAGE | B | *(unverified)* Taunts a swarming mob at a "dangerous tower," then a sudden scare | "इधर आ अंदर आओ तुम लोग... भाई इधर एक खतरनाक चीज होता था। वेट ओ [bleep]।" |
| 01:16:50→01:17:05 | RAGE | B | *(unverified)* Grumbles about a clunky in-game feature | "क्या है भाई क्या है ये कौन सा कचरा फीचर है भाई।" |
| 01:38:57→01:40:36 | RAGE | B | *(unverified)* Lever puzzle goes wrong — "oh no... shit bro" | "लीवर लीवर लीवर ये वाला... ओ नो... शिट ब्रो।" |
| 01:58:07→01:59:58 | BOSS | B | *(unverified)* Boss/NPC booms "Be Proud" — startled reaction | "बी प्राउड व्हाट द [bleep] ब्रो?" |
| 01:07:12→01:07:25 | RAGE | B | *(unverified)* Sudden shocked outburst at an unexpected turn | "हाउ यू [bleep] दैट हैपेंड ब्रो।" |

*Dropped (pass 1): 01:15:12, 00:21:14 (calm walking + map-browse, no pursuers/loot-result shown).*

### `hCbf17Aj9CI` — Elden Ring playthrough (2:25:22)
| In → Out | Cat | Tier | Label | Quote |
|---|---|---|---|---|
| ⟲ 00:14:02→00:14:32 | BOSS | A | Frantic mid-fight plea vs Margit, ends on "YOU DIED" (was 00:14:02→00:15:00; cut a respawn/walk tail) | "मार भाई मार ले प्लीज। रुक जा। मेरे को मेरा ऐशेस कलेक्ट करने दे फिर मार देना।" |
| ⟲ 00:23:25→00:24:14 | RAGE | A | Comedic tilt vs Margit: "like he's at someone's house party," facecam laughs at the reload screen (was 00:23:25→00:24:21; cut a post-respawn walk tail) | "साला इतना धीरे-धीरे खेल रहा है जैसे इसका घर पे पार्टी चल रहा है उसको डिले कराना है।" |
| ⟲ 00:59:39→01:00:50 | BOSS | S | Clutch win vs Deathbird — fight through kill through loot pickup (was →01:01:08; cut a calm Torrent ride-away) | "चिल चिल चिल वन एचपी वन एचपी वी गॉट इट भाई... तुम उसको मारना इतना इजी भी नहीं है।" |
| 01:19:20→01:19:40 | RAGE | B | *(unverified)* Ranting about the game's most irritating delayed-attack NPC ally | "साला मार्केट सबसे इरिटेटिंग लगता है... आधे घंटे के बाद मारता है अटैक।" |
| 01:30:23→01:30:38 | RAGE | B | *(unverified)* Constantly getting stuck in the terrain mid-fight | "मैं टेरेन में अटक जा रहा हूं। साला पिट जा रहा उसके टेरेन में।" |
| ⟲ 01:47:33→01:48:03 | BOSS | A | Real frost fight vs the Ancient Hero of Zamor, ends right before he dies (was 01:47:33→01:48:45; cut a death-menu/travel/grace tail) | "वाओ आई एम डेड एस [bleep] फ्रस्ट वाइट की वजह से।" |
| 02:18:07→02:18:32 | RAGE | B | *(unverified)* Annoyed at bleed-build trash mobs that "just won't die" | "हां माल सब लोग मार दो मेरे को। ये इरिटेट करते भाई... ब्लड लॉस डाल के रखे हैं इतना।" |
| 02:20:17→02:20:52 | RAGE | B | *(unverified)* Ganged up and instant-killed by four enemies at once | "भाई इंस्टेंट मुड़ा दिया मेरे को ये चार लोग मिलके।" |

*Dropped: 01:02:55 (riding on full health, no enemy), 01:20:54 (walking, no ally/combat visible),
01:42:29 (weapon menu + climbing, no boss), 00:56:47 ("hidden boss reveal" — 60% of the window is
loading/black/menu frames, flat facecam throughout).*

### `vqya4IBji58` — The Max Bleed Run is Here \| Vertical (1:53:54)
| In → Out | Cat | Tier | Label | Quote |
|---|---|---|---|---|
| 00:09:17→00:09:57 | RAGE | B | *(unverified)* Confused/frustrated reading a note item | "हाउ द हाउ द [bleep] ही रोट हियर... व्हाट द [bleep] इज दैट सपोज मी।" |
| 00:33:03→00:33:58 | RAGE | B | *(unverified)* Annoyed waiting on the day/night cycle before a fight | "पास्ट रात होने का वेट करना पड़ेगा इधर अबे रात क्यों नहीं हुआ?" |
| ✓ 00:36:10→00:36:48 | RAGE | A | Comedic non-combat "let me pass" chase alongside Night's Cavalry | "जाने देना भाई प्लीज मेरे भाई यार नहीं लड़ना है तेरे से अभी।" |
| ✓ 00:42:20→00:42:58 | BOSS | A | Vs Bloodhound Knight Darriwil — near-death then a real, visible relief smile at the kill | "भाई दैट वास क्लोज [bleep] आई वास गेटिंग ग्रीडी डेड मैन।" |
| 01:12:10→01:13:40 | BOSS | B | *(unverified)* Struggling attempt vs a ranged boss, "I'll try once more" | "आई थिंक इट्स पॉसिबल आई एम जस्ट रूफिंग ना ब्रो डिफिकल्ट।" |
| 01:14:03→01:14:22 | BOSS | B | *(unverified)* One-liner complaint about the boss's delayed attack timing | "भाई इतना डिलेड अटैक साला भगवान जाने इतना डीले अटैक क्यों मारता है।" |
| 01:16:35→01:17:53 | BOSS | B | *(unverified)* "That was close, we can do it" then "I'm making it difficult myself" | "वी कैन डू इट नॉट इमॉसिबल एट ऑल... इट्स नॉट डिफिकल्ट ब्रो।" |
| 01:18:25→01:18:50 | BOSS | B | *(unverified)* Quick mistake recap after a near-miss trade | "आई फॉरगॉट कि वो ऐसे करके ऐसा करेगा वो... ट्रेड हो गया थोड़ा।" |
| ✓ 01:22:30→01:24:00 | BOSS | A | Tree Sentinel fight → health bar drains to a sliver → relief stretch/release gesture → flees to a grace | "दैट वास सो क्लोज दैट वास सो फकी क्लोज लेट्स गो वी आर वी कैन डू नाउ इजी एस [bleep]।" |
| 01:48:58→01:49:32 | RAGE | B | *(unverified)* Resigned frustration muttering to self | "व्हाट द [bleep] आई नीड मोर टू यूज़ दैट फथ डल ओके ब्रो ओके ब्रो ठीक है बाय मार दो मेरे को नॉट हियर।" |
| 01:51:09→01:51:40 | RAGE | B | *(unverified)* "Kill me, beat me" spiral resolves into a comedic twist | "मार दो भाई मेरे को मार दो मारो को पीट दो तुम एनीवे आई वेंट फॉर दिस ओके दैट्स व्हाट वी नीडेड।" |

*Dropped: 00:28:10 ("startled by Fingers enemy" — flat facecam, dominated by calm walking + reading
notes), 01:19:20 (the S-tier "epic clutch win, euphoric disbelief" — facecam never changes across
88s, and the boss bar stays near-full with no visible finishing blow; the labeled emotional beat
just isn't on screen), 01:34:44 ("still grinding" — mostly menu/message/idle navigation).*

### `y9ikYH3oECU` — Best Player is here (1:14:50)
| In → Out | Cat | Tier | Label | Quote |
|---|---|---|---|---|
| 00:00:00→00:00:29 | RAGE | B | *(unverified)* Stream opens with a rant trashing Valorant | "वी वोंट प्ले वेलरेंट शिट गेम शिट गेम शिट प्लेयर्स द [bleep] शिट सर्वर।" |
| 00:51:10→00:51:58 | RAGE | B | *(unverified)* Tilted at a tanky mob dealing too much damage | "इतना डैमेज देता है ये बंदा इरिट लगता है मेरे को बहुत... ये ले ईगो हट कर दिया तूने।" |
| ⟲ 00:25:33→00:26:15 | BOSS | A | Real fight + kill vs a large antlered spirit/tree enemy, facecam laughs at the kill (relabeled — the "ledge-jump death" from the transcript isn't visible; was 00:25:33→00:26:52, cut a calm horseback-ride tail) | "वो देख भाई क्या कूद के मरा हुआ है... इंस्टा पे क्लिप डालूंगा।" |
| 00:56:29→00:56:53 | RAGE | B | *(unverified)* Game crashes twice mid-session; vents about a memory leak | "दो बार क्रैश हो गया मेरा गेम। कुछ तो मेमोरी लीक रहता है इनका।" |
| ✓ 01:04:35→01:05:08 | RAGE | A | Falls to his death off a ledge in the red battlefield — "YOU DIED" then a genuine deadpan reaction | "ऑफकोर्स वी डाई लाइक दिस ब्रो आफ्टर सर्वाइविंग ऑल दैट।" |
| 01:05:26→01:06:05 | RAGE | B | *(unverified)* Grumbles about the tough enemies guarding the boss door | "आई फॉरगॉट हाउ पेनफुल आर दिस दिस टू मदर फगस।" |
| ✓ 01:13:52→01:14:44 | RAGE | S | A corrupted save forces a restart — confirmed all the way to the visible Windows desktop | "आई एम नॉट प्लेइंग दिस गेम [bleep] इट [bleep] दिस गेम... आई क्विट [bleep] दिस गेम ब्रो।" |

*Dropped: 00:59:01 (plain traversal/ladder-climbing, no boss bar or kill visible), 00:08:12 (the
"Rennala battery-charge gag pays off with a kill" S-tier pick — this is the clip that triggered the
whole pass-2 re-audit: dense 10-frame review showed only the first ~35s of the 89s window is real
combat, the rest a level-up menu then calm exploring, with a flat facecam throughout).*

### `j8fuJ2xbVIg` — Best Player is here (1:39:27)
| In → Out | Cat | Tier | Label | Quote |
|---|---|---|---|---|
| ✓ 00:23:10→00:24:45 | BOSS | S | Rennala boss intro cutscene — comedic "the Queen betrayed us" reveal | "रानी ने हमको धोखा दे दिया यार... क्यूट था यार रेनाला... ओ नो नो नो नो।" |
| 00:18:10→00:19:24 | BOSS | B | *(unverified)* Hype walk-up to Rennala's arena | "लेट्स गो बॉयज हियर वी आर रेनालाइटस लेट्स गो।" |
| ✓ 00:51:24→00:52:51 | BOSS | S | Rennala's boss transformation — comedic "she turned into Goku" reaction | "भाई गोकू बन गई बहन की... ये भाई ये सांप बन गई।" |
| ✓ 00:53:03→00:53:45 | BOSS | A | Rennala phase-2 magic spam — animated, genuinely engaged facecam throughout | "गोकू का भाई है... थक गया भाई थक गया।" |
| ⟲ 00:57:03→00:57:30 | BOSS | S | "I hate this boss!" rage quote mid-fight (was 00:57:03→00:57:53; the "surrender" tail was unrelated calm walking, cut) | "आई हेट दिस बॉस ब्रो आई हेट दिस बॉस।" |
| 01:19:05→01:19:33 | BOSS | B | *(unverified)* Radahn hype: "Now let's go kill Radahn, he's a bit tougher" | "नाउ आई थिंक वी कैन गो एंड किल रडान।" |
| 01:21:13→01:21:33 | BOSS | B | *(unverified)* Radahn prep — summoning an army | "भाई कितना डैमेज देते हैं ये लोग। अपने को अपना आर्मी लाना पड़ेगा।" |
| 00:00:20→00:00:46 | RAGE | B | *(unverified)* "I've died here three times" — repeated-death frustration | "मैं तीन बार मर चुका हूं इधर मैं तीन बार मर चुका हूं तीन बार।" |
| 00:03:11→00:03:34 | RAGE | B | *(unverified)* "I ran all this way just to suicide-jump off a ledge" rant | "इतना दूर नीचे कूदने के लिए खुदकुशी करने के लिए... तंग आ चुका हूं भाई ये जगह से।" |
| 00:19:52→00:20:56 | RAGE | B | *(unverified)* Sorcerer-student mobs pelting him | "भाई बच्चे आई हिट बच्चे इन दिस गेम।" |
| ⟲ 00:21:34→00:22:29 | BOSS | A | Rennala's meteor/comet spell attack — genuinely startled facecam reaction (was 00:21:26→00:22:29; cut a leading equipment-menu frame) | "बाप रे बाप रे बाप रे बाप रे बाप ये क्या चकरी घूम रहा है।" |
| 00:25:27→00:25:56 | RAGE | B | *(unverified)* Post-Rennala-area magic spam — "why so much running" | "आई डोंट लाइक दिस प्लेस मैन इतना भागना क्यों पड़ता है।" |
| 00:34:39→00:35:05 | RAGE | B | *(unverified)* Comedic parry tutorial mid-frustration | "साला पेरी कर रहा है बहन का। हां अभी आएगा ना मजा।" |
| 00:36:20→00:36:59 | RAGE | B | *(unverified)* "What the hell kind of guy is this" | "साला कूद के मार रहा है। कितना बंदा है... व्हाट द इंटेलिजेंस चाहिए इसके लिए।" |
| 00:45:22→00:46:53 | RAGE | B | *(unverified)* Run-back rage rant | "दिस बॉस इज अ हेडेक बिकॉज़ आई हैव टू गो एंड कम कम बैक अगेन।" |
| ⟲ 01:15:41→01:16:04 | RAGE | A | "Get [bleep] regged!" trash-talk taunt vs Renna, Queen of the Full Moon (was →01:16:11; cut a trailing unrelated lore-text scene) | "गेट रेग्ड गेट रेग्ड इधर इधर इधर आंटी जी... नो मैजिक इन फ्रंट ऑफ माय।" |
| 01:33:45→01:34:20 | RAGE | B | *(unverified)* Comedic fall-death right after the big win | "साला नूब कूद के मर गया। वाह।" |

*Dropped: 00:03:46, 00:28:18, 00:44:01 (pass 1 — riding/menu, no enemy or tension shown), 01:31:45
("RADAHN DOWN" — already downgraded in pass 1, pass 2 confirms a completely flat facecam across a
status-effect skirmish with no death/victory screen visible; the actual Radahn kill moment never
surfaced in either pass).*

### `2pIPs_ut25o` — Elden Ring, mislabeled #shorts (1:12:19)
| In → Out | Cat | Tier | Label | Quote |
|---|---|---|---|---|
| 00:21:25→00:21:52 | BOSS | B | *(unverified — an earlier revision of this file mistakenly marked this row as checked; it wasn't, and pass 2 confirms it's dead: calm walk-up + flat facecam, no combat)* Jokes the tough NPC is basically "the boss that's in every Dark Souls game" | "इधर लेफ्ट में एक एनपीसी है उसको मारने का है। ये मतलब बॉस है।" |
| ✓ 00:22:04→00:23:03 | BOSS | A | Beats the NPC Patches to near-death, it fake-surrenders, they spare it — facecam shifts from relaxed to animated across the fight | "देख रहा है सरेंडर कर रहा है साला छोड़ दे... आके फिर से मैं कैसे आऊंगा।" |
| 00:42:29→00:42:46 | BOSS | B | *(unverified)* Sets up a "minor" boss fight, warns his co-op partner | "चिंगूमिंगू मत समझना इसको।" |
| 00:59:06→01:00:00 | BOSS | B | *(unverified)* Boss spawns and unleashes a ghost | "बाप रे बॉस यार भाई तो भूत छोड़ रहा है भूत।" |
| ⟲ 01:01:29→01:01:53 | BOSS | A | Huge Bell Bearing Hunter reveal, facecam's mouth snaps open in shock (was 01:01:29→01:02:32; cut a checkpoint/menu/second-encounter tail) | "बेल बियरिंग हंटर बड़े वाला ओ [bleep] ब्रो... बहुत मारता है भाई ये बहुत मारता है।" |
| ⟲ 01:03:17→01:03:26 | RAGE | A | Nearly one-shot by the Bell Bearing Hunter's spinning blade (was 01:03:17→01:03:47; cut a shack/merchant dialogue tail) | "क्या है भाई ये क्या डैमेज चाहिए? ...ब्लेड घुमाया मैं मर गया।" |

*Dropped: 00:25:37 (the S-tier "Patches payoff" — 4 of 6 frames are black/desktop/menu screens,
landing mid-window with no clean trim possible).*

### `AF_7niXth8g` — Elden Ring, mislabeled #shorts (2:39:18)
| In → Out | Cat | Tier | Label | Quote |
|---|---|---|---|---|
| ✓ 00:26:47→00:27:12 | BOSS | A | Clutch kill of the Bloody Finger Ravensworn Assassin invader — continuous real action, no filler | "यस यस यस ऐसे भी रहती है। फाइनली साला हमारा बग हो गया था लास्ट टाइम यार।" |
| 00:43:01→00:43:39 | RAGE | B | *(unverified)* Panic as enemies refuse to die and start using buff abilities | "व्हाट द [bleep] साले मरते ही नहीं है ये लोग। बाप रे बाप। एबिलिटीज छोड़ रहे हैं भाई।" |
| 00:45:20→00:46:37 | RAGE | B | *(unverified)* Poisoned by a mob swarm, screams, then decides to just flee | "इतना डैमेज देता है ये लोग मरते ही नहीं है। इग्नोर करके भागना पड़ेगा।" |
| 00:51:22→00:52:09 | RAGE | B | *(unverified)* Can't parry a ranged enemy's bolt in time | "साला साला मरते भी नहीं है, जाने भी नहीं देते।" |
| ⟲ 00:52:55→00:53:25 | RAGE | S | Meltdown — "I am dead" spam dying to a bat/fire swarm (was →00:53:52; cut a post-death respawn-run + location-card tail) | "रियली [bleep] x12 आई एम डेड आई एम डेड आई एम डेड आई एम डेड आई एम डेड।" |
| 00:54:04→00:54:32 | RAGE | B | *(unverified)* Bird swarm annoyance rant right after the bat meltdown | "चिड़िया गैंग मेरे पीछे है भाई। चिड़िया गैंग साले।" |
| 01:02:49→01:04:16 | BOSS | B | *(unverified)* "Fat boss" mini-boss shows up and gets cleared quickly | "साला एक मोटू बॉस आ गया है भाई... मारो मारो।" |
| ⟲ 01:52:46→01:53:08 | BOSS | S | "I hate this boss" — Red Wolf of Radagon (was 01:52:46→01:53:29; cut a calm walk-away tail) | "आई हेट दिस बॉय बॉस ब्रो ये पूरे गेम में मेरे को सबसे ज्यादा हेट ये बॉस पे ही आया था।" |
| 01:54:28→01:55:09 | RAGE | B | *(unverified)* More venting about the hated boss's unfair dual mechanic | "पास जाओ तो मुंह से तलवार निकाल के मारता है। दूर जाओ तो वो मैजिक पेन स्पॉन कर देता है।" |
| ⟲ 01:56:30→01:56:45 | RAGE | S | Furious taunt finally killing the Red Wolf of Radagon (was 01:56:30→01:57:03; cut a calm aftermath tail) | "मार जा मर जा मरा कुत्ता शट डाउन कुकर भाई बहुत दिमाग गरम करता है ये कुत्ता।" |
| 02:16:01→02:17:20 | BOSS | B | *(unverified)* Parrying-monkey boss finally goes down after a tense chase | "मर गया नबड़ा। बिट टफ बट ओके।" |
| 02:31:02→02:31:26 | RAGE | B | *(unverified)* Three zombies again, and no grace point nearby to retry from | "साला तीन-तीन ज़ॉम्बी वाला है। इतना फिर से भाग के आना पड़ेगा।" |
| 02:33:23→02:34:23 | RAGE | B | *(unverified)* Death spiral near the end of stream | "इनको मारना इतना डिफिकल्ट क्यों है?" |

*Dropped: 01:11:05 ("rat swarm rage-quit" — flat facecam, no rats or combat visible across the full
40s), plus the earlier-confirmed drop of the fabricated "Godrick grafts a dragon's arm" S-tier clip
and its mislabeled "get regged vs Godrick" companion (pass 1).*

---

## Rejected after visual check (32 of 69 originally S+A tier)
Kept for the record rather than silently deleted. 18 from pass 1 (transcript-only false positives —
no matching action at all) + 14 more from pass 2's denser re-audit (real action existed somewhere in
the window, but it was a minority of the runtime and the labeled emotional beat never actually
lands on screen). This second wave is exactly why the sparse 4-frame sampling wasn't trustworthy.

**Pass 1 drops** — `NxOMr6_jzA4`: 01:33:44 (menu/loading), 01:36:05 (settings menu + walking),
01:52:30 (map screen only, no fall shown), 03:09:39 ("died to a car" — the original catch, just
walking outdoors), 03:23:28 (watching a YouTube video, not his own gameplay). `j39NRXGraXw`:
01:15:12, 00:21:14 (calm walking, claimed pursuit/loot-search not visible). `hCbf17Aj9CI`: 01:02:55,
01:20:54, 01:42:29 (riding/menu/climbing, no enemy). `y9ikYH3oECU`: 00:59:01 (traversal, no boss).
`j8fuJ2xbVIg`: 00:03:46, 00:28:18, 00:44:01 (riding/menu, no enemy or tension). `2pIPs_ut25o`:
00:45:12 (player standing still, streamer absent from facecam for 2 of 4 frames). `AF_7niXth8g`:
00:07:22 (fabricated "Godrick dragon arm," S-tier), 00:24:12 ("Godrick temper flare" — wrong enemy,
flat facecam), 01:31:47 ("NPC kills NPC" — frames don't support the claim).

**Pass 2 drops (denser re-audit)** — `2pIPs_ut25o`: 00:21:25 (calm walk-up, no combat — also fixes a
mis-marked row from an earlier revision of this file), 00:25:37 (the S-tier Patches-payoff — 4 of 6
frames are black/desktop/menu, no clean trim possible). `AF_7niXth8g`: 01:11:05 (rat swarm claimed,
none visible; flat facecam). `NxOMr6_jzA4`: 00:25:14 (75% frozen loot screen), 01:06:53 (calm
walking either side of a brief effect, boss already dead by the only real frame), 01:37:02 (78%
Roundtable Hold hub/menu), 01:39:12 (checkpoint reload + weapon-menu screens dominate), 03:20:01
(flat facecam across the full 75s despite real game-side beats — likely two stitched incidents).
`jd9BmFyCIn8`: 00:13:48 (already downgraded in pass 1; confirmed dead — flat facecam, low-threat
skirmish, no boss). `hCbf17Aj9CI`: 00:56:47 (60% loading/black/menu frames). `vqya4IBji58`: 00:28:10
(flat facecam, calm walking + note-reading), 01:19:20 (the S-tier "epic clutch win, euphoric
disbelief" — facecam never changes across 88s and the boss bar stays near-full with no finishing
blow), 01:34:44 (mostly menu/message/idle navigation). `j8fuJ2xbVIg`: 01:31:45 (already downgraded
in pass 1; confirmed dead — flat facecam, no death/victory screen for the claimed "Radahn down").

**Confirmed bad by direct user review (the trigger for pass 2)** — `y9ikYH3oECU` 00:08:12 (the
"Rennala battery-charge gag" S-tier pick): only ~35s of the 89s window is real combat; the rest is a
level-up menu then calm exploring, flat facecam throughout. This is the clip that proved the pass-1
sparse-sampling method unreliable and triggered the full pass-2 re-audit.

## Hard cuts (never include)
- Dead air: silence, menu/inventory browsing beyond a few seconds, loading/death-recap screens,
  intro/outro stretches.
- Silent grinding / long backtracking runs with no commentary.
- Any stretch where the only content is navigating the map without reaction or commentary.
- Riding/traversal with a full, undamaged health bar and no enemy on screen.
- **A flat, unchanging facecam across the entire candidate window** — added after pass 2. Real
  payoff moments (a kill, a scare, a punchline) visibly move the streamer's face somewhere in the
  sequence; a static expression start-to-finish is now treated as a standalone warning sign, not
  just circumstantial.

## Cross-stream notes
**Recurring bosses/enemies across streams** (names corrected by the visual checks, not the ASR
transcript): Rennala/Renna, Queen of the Full Moon appears in two different sessions —
`y9ikYH3oECU`'s battery-charge-gag kill (now dropped, see rejected) and `j8fuJ2xbVIg`'s full "turned
into Goku" fight (confirmed, in the quick-start list). The **Red Wolf of Radagon** is the single
most-hated boss across the batch (`AF_7niXth8g`, two confirmed-but-tightened clips). Deathbird, the
Ancestor Spirit (Siofra River), Margit the Fell Omen, the Ancient Hero of Zamor, Bell Bearing
Hunter, and Godrick the Grafted (genuinely confirmed in `j39NRXGraXw`, unlike the fabricated
`AF_7niXth8g` "Godrick" clip) all stand out as real named-boss moments.

**Failure-mode pattern, updated after pass 2:** beyond the pass-1 pattern (traversal/riding with a
full health bar), pass 2 surfaced a second, subtler failure mode — **a real, confirmed action beat
sitting inside a much longer window whose remainder is dead** (a checkpoint reload, a menu screen, a
calm ride/walk away from the fight, or a second unrelated encounter). A fixed small sample size
reliably misses this because it only needs to land on the one real portion to read as "confirmed."
The fix: scale frame count with duration, and always ask whether the *entire* window holds up, not
just some of it.

## How to cut it (deferred — nothing downloaded/clipped yet)
1. Pull only the needed ranges per clip with the **`vod-clip-extraction`** skill — for any ⟲ row,
   cut the **new tightened in/out**, not the original span. Its `candidate_preview.py` can re-verify
   any B-tier candidate the same way (duration-scaled `--frames auto`) before cutting it.
   Store clips on **`/mnt/f`** (from the Windows/WSL side); verify cut points with a contact sheet.
2. No reframe pass needed — source is already 1080x1920. Straight cut → captions → post.
3. For exact wording/caption text, re-run `transcript.py window` on the relevant `.hi-orig.vtt` at
   cue-level before burning in captions (ASR still garbles some proper nouns — the boss *names* used
   above came from the visual checks, not the transcript).
4. Post BOSS and RAGE clips as separate framing (see `idea.md` packaging section) rather than mixed
   — each finds a different part of the audience.

## Stats
143 total candidates across 9 streams (~18.3h source). Of the original 69 S+A tier candidates that
went through visual verification: **20 confirmed as-is (including the retimed cancer-boss clip), 17
confirmed-but-tightened (use the new in/out shown), 32 dropped** (18 from pass 1's sparser check,
13 more from pass 2's duration-scaled re-audit, plus the Rennala clip confirmed bad by direct user
review). **12 S-tier candidates survive** as the quick-start list (down from an original 20).
**B-tier (74 candidates) remains transcript-only / unverified** — none of the B-tier rows have been
through either visual-verification pass except where noted inline.

**Production status: all 12 quick-start S-tier picks are now cut, captioned, and end-carded** —
numbered `01`–`12` in `~/Desktop/clips/` matching the quick-start table's row order. One more filler
tail was caught during cutting (the Ancestor Spirit clip, #4 — see its row above) and re-tightened,
following the same pattern as the other ⟲ rows. Remaining unproduced candidates: the ~25 other
confirmed/tightened A-tier picks from the full-sweep tables (never had a produced clip), plus the
full 74-candidate B-tier pool (still unverified).
