"""Export the deck to slides.pdf (one page per slide, animations off; the demo slide shows a still frame).

Usage:  pip install playwright pillow && playwright install chromium
        python build.py && python export_pdf.py
"""
import asyncio
import pathlib

from PIL import Image
from playwright.async_api import async_playwright

ROOT = pathlib.Path(__file__).parent


async def main() -> None:
    shots = []
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1920, "height": 1080})
        await page.goto((ROOT / "index.html").resolve().as_uri())
        await page.evaluate("document.documentElement.classList.add('static')")
        await page.wait_for_timeout(800)
        n = await page.evaluate("document.querySelectorAll('deck-stage > section').length")
        # On the demo slide, swap the video for its still frame (a PDF cannot play video).
        if (ROOT / "assets" / "demo-poster.jpg").exists():
            await page.evaluate("""() => {
                const v = document.querySelector('.demo-video');
                if (!v) return;
                const img = document.createElement('img');
                img.src = 'assets/demo-poster.jpg';
                img.style.cssText = 'display:block;width:100%;height:100%;object-fit:contain';
                v.closest('.video-frame').classList.remove('missing');
                v.replaceWith(img);
            }""")
            await page.wait_for_timeout(400)
        for i in range(n):
            await page.evaluate(f"document.querySelector('deck-stage')._go({i}, 'api')")
            await page.wait_for_timeout(400)
            # hide the deck's on-screen navigation bar
            await page.evaluate("document.querySelector('deck-stage').shadowRoot"
                                ".querySelectorAll('.overlay,[class*=overlay]').forEach(e => e.style.display = 'none')")
            path = ROOT / f".slide-{i + 1}.png"
            await page.screenshot(path=str(path))
            shots.append(path)
        await browser.close()
    images = [Image.open(s).convert("RGB") for s in shots]
    images[0].save(ROOT / "slides.pdf", save_all=True, append_images=images[1:], resolution=144)
    for s in shots:
        s.unlink()
    print(f"slides.pdf written ({len(images)} pages)")


if __name__ == "__main__":
    asyncio.run(main())
