# Sound test scenario 1.33.0 (ChatGPT Work)

Owner test of generative sound and music design, released in 1.33.0. Written 2026-10-08 for the owner's occasional larger ChatGPT Work test; Codex can run the same prompts. The prompts are in Polish because the owner tests in Polish; they are exact test inputs and stay in their original language. About 15 to 20 minutes.

## Preparation

1. Update the hosted plugin in ChatGPT Work to 1.33.0 ([release v1.33.0](https://github.com/FrameCoreWorks/framecore-works-creative-studio/releases/tag/v1.33.0)).
2. Open a new ChatGPT Work chat and note the reasoning setting.
3. Unknown in advance: whether the Work environment has `ffmpeg`. Without it no MP4 with sound can be written; step 1 shows it.

## Step 1: a video with sound (calm, product)

```text
Użyj FrameCore Works Creative Studio. Zrób krótką rolkę motion graphics 9:16, około 10 sekund, w stylu Meadow, dla aplikacji do planowania domowego budżetu „Spokojny Portfel”. Przekaz: „Twoje wydatki pod kontrolą, bez stresu”. Trzy sceny: dwa krótkie napisy, potem karta końcowa z nazwą aplikacji. Chcę od razu dźwięk: zaprojektuj efekty i skomponuj muzykę narzędziami Studio z kodu (sound.py), zmiksuj i dostarcz MP4 z dźwiękiem. W odpowiedzi podaj: profil rolki i co zaprojektowano dla dźwięku z uzasadnieniem, wynik kontroli timingu, głośność w LUFS i tabelę cue.
```

Expected: an MP4 with sound; two or three sentences on the profile and moods (for example calm and organic); the design log (transition, landing, impact, accent, music with progression and instruments); timing `all_ok: true`; about −14 LUFS; a cue table.

## Step 2: a new variation of the same video

```text
Użyj FrameCore Works Creative Studio. Dla rolki „Spokojny Portfel” z poprzedniej odpowiedzi zaprojektuj dźwięk i muzykę od nowa jako nowy wariant (sound.py plan z --variation 1), bez zmiany obrazu. Zmiksuj i dostarcz MP4. Podaj, czym ten wariant różni się od poprzedniego: rodzaje dźwięków, progresja akordów, instrumenty, oraz wynik timingu i LUFS.
```

Expected: a different design log (other kinds of sound or other music), the picture unchanged, timing passing.

## Step 3: fixing one choice

```text
Użyj FrameCore Works Creative Studio. W rolce „Spokojny Portfel” zostaw resztę projektu dźwięku, ale ustaw instrument prowadzący na pianino i tonację na E-moll (sound.py plan z --set lead=piano i --set key="E minor"). Zmiksuj i dostarcz MP4. Potwierdź w dzienniku projektu, że oba wybory oznaczono jako ustawione przez użytkownika.
```

Expected: the design log shows `lead piano` and the key E minor as set by the user; an MP4 with sound.

## Step 4: a different video (variety)

```text
Użyj FrameCore Works Creative Studio. Zrób krótką rolkę motion graphics 9:16, około 8 sekund, w stylu Color block, zapowiadającą premierę gry mobilnej „Bounce Party”: dwa głośne, krótkie hasła na kolorowych tłach i karta końcowa z datą premiery. Zaprojektuj dźwięk i muzykę narzędziami Studio z kodu, zmiksuj i dostarcz MP4 z dźwiękiem. Podaj profil rolki, co zaprojektowano i dlaczego, wynik timingu i LUFS.
```

Expected: a playful and bold profile at a fast pace; other kinds of sound than in step 1; music on the house kit; the swoosh as text appears clearly quieter than the transitions (the last fix before release).

## Listening

| Point | Question |
| --- | --- |
| A | Do the sounds fit the character of each video (calm against playful)? |
| B | Is any sound too loud, flat or toy-like? |
| C | Does the final card land on the music, and does the music ring out well? |
| D | Does the step 2 variation sound clearly different from step 1? |
| E | Did Studio explain what it designed without being asked again? |

## Report template

```text
Test dźwięku 1.33.0, ChatGPT Work, data: …, ustawienie rozumowania: …
Krok 1: MP4 z dźwiękiem tak/nie; timing ok tak/nie; LUFS: …; uwagi: …
Krok 2: wariant inny tak/nie; uwagi: …
Krok 3: pianino i E-moll ustawione tak/nie; uwagi: …
Krok 4: profil playful/bold tak/nie; swoosh przy tekście ok tak/nie; uwagi: …
Odsłuch A–E: …
Błędy lub komunikaty (wklej dosłownie): …
```

Results go into `verification/` as an owner-reported record (`PASS_REPORTED` or the observed failure), separate from source checks.
