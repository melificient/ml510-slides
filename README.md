# ML510 · Triage secondaire des appels 911 

Six-slide presentation for the ML510 integrative project (Polytechnique Montréal, fall 2026).

**View the slides:** https://melificient.github.io/ml510-slides/
**PDF:** https://melificient.github.io/ml510-slides/slides.pdf (rebuilt automatically on every push)
Use ← / → (or space) to navigate and F11 for full screen. On slide 2, → reveals the four steps one at a time.
The last slide (« Démo », after the conclusion) plays `assets/demo.mp4`: it starts on arrival, Space or K pauses/resumes.

## How it's built

The deck is plain HTML/CSS/JS. `build.py` assembles everything into a single self-contained
`index.html` (fonts, photo and scripts inlined), which GitHub Pages serves as is.

```
src/slides.html     content of the 6 slides (French)
src/style.css       Biennale Yellow styling, layout, charts, animations
src/anim.js         step-by-step reveal on slide 2, bars growing in, ambulance slide-in
assets/             ambulance photo, fonts (woff2, latin subset), demo.mp4 (not inlined)
vendor/             deck-stage.js — 1920×1080 stage that scales to any screen
build.py            builds index.html (standard library only)
export_pdf.py       optional: exports slides.pdf with animations off
```

To change a slide: edit a file in `src/` (on github.com or locally) and push. The GitHub Actions workflow
(`.github/workflows/build.yml`) runs `build.py` and publishes the result to GitHub Pages.
Pages must be set to **Settings → Pages → Source: GitHub Actions**. Don't edit `index.html` by hand.

## Data sources

- Model and extraction results: outputs of the project's scripts 01–05 (NHAMCS 2019–2022, synthetic call narratives, 19 published SAMU excerpts).
- Context figures (slide 2): Urgences-santé, *Rapport annuel de gestion 2024-2025*.

## Credits

- Slide template: [frontend-slides](https://github.com/zarazhangrui/frontend-slides), Biennale Yellow style, MIT License, © 2025 Zara Zhang (`vendor/LICENSE-frontend-slides.txt`).
- Fonts: Instrument Serif, Archivo, JetBrains Mono, SIL Open Font License, via Fontsource (`assets/fonts/`).
- Photo (slide 1): La Presse canadienne / Christopher Katsarov, March 11, 2026. Not covered by any open licence.
- Drafted with help from Claude (Anthropic); see the project's `NOTES_UTILISATION_IA.md`.
