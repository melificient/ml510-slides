"""Build index.html: one self-contained file (fonts, photo and scripts inlined).

Usage:  python build.py
Edit the slides in src/, then rebuild. Only the Python standard library is needed.
"""
import base64
import pathlib

ROOT = pathlib.Path(__file__).parent
SRC, ASSETS = ROOT / "src", ROOT / "assets"

FONTS = [  # (family, file, weight, style)
    ("Instrument Serif", "instrument-serif-latin-400-normal.woff2", 400, "normal"),
    ("Instrument Serif", "instrument-serif-latin-400-italic.woff2", 400, "italic"),
    ("Archivo", "archivo-latin-400-normal.woff2", 400, "normal"),
    ("Archivo", "archivo-latin-600-normal.woff2", 600, "normal"),
    ("Archivo", "archivo-latin-400-italic.woff2", 400, "italic"),
    ("JetBrains Mono", "jetbrains-mono-latin-400-normal.woff2", 400, "normal"),
]


def b64(path: pathlib.Path) -> str:
    return base64.b64encode(path.read_bytes()).decode()


def font_faces() -> str:
    return "".join(
        f"@font-face{{font-family:'{fam}';font-weight:{w};font-style:{st};font-display:block;"
        f"src:url(data:font/woff2;base64,{b64(ASSETS / 'fonts' / f)}) format('woff2')}}\n"
        for fam, f, w, st in FONTS
    )


def main() -> None:
    slides = (SRC / "slides.html").read_text(encoding="utf-8").replace(
        "__AMB__", "data:image/jpeg;base64," + b64(ASSETS / "ambulance.jpg"))
    html = f"""<!DOCTYPE html>
<html lang="fr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Triage secondaire des appels 911 · ML510</title>
<style>{font_faces()}{(SRC / 'style.css').read_text(encoding='utf-8')}</style>
</head><body>
<deck-stage width="1920" height="1080">
{slides}
</deck-stage>
<script>{(ROOT / 'vendor' / 'deck-stage.js').read_text(encoding='utf-8')}</script>
<script>{(SRC / 'anim.js').read_text(encoding='utf-8')}</script>
</body></html>"""
    (ROOT / "index.html").write_text(html, encoding="utf-8")
    print(f"index.html written ({len(html) // 1024} KB)")


if __name__ == "__main__":
    main()
