(() => {
  const deck = document.querySelector('deck-stage');
  if (!deck || document.documentElement.classList.contains('static')) return;
  const slides = () => Array.from(deck.children).filter(e => e.tagName === 'SECTION');
  const FLOW = 1;                       // slide 2 (0-based)
  const groups = () => {
    const els = Array.from(slides()[FLOW].querySelectorAll('[data-step]'));
    const n = Math.max(0, ...els.map(e => +e.dataset.step));
    return Array.from({ length: n }, (_, k) => els.filter(e => +e.dataset.step === k + 1));
  };
  const N = () => groups().length;
  let shown = 99;
  const render = () => groups().forEach((grp, i) => grp.forEach(el => el.classList.toggle('hidden-step', i >= shown)));
  const orig = deck._go.bind(deck);
  deck._go = (i, reason) => {
    if (document.documentElement.classList.contains('static')) return orig(i, reason);
    const cur = deck._index;
    if (cur === FLOW && i === cur + 1 && shown < N()) { shown++; render(); return; }
    if (cur === FLOW && i === cur - 1 && shown > 1) { shown--; render(); return; }
    if (i === FLOW) { shown = cur < FLOW ? 1 : N(); render(); }
    orig(i, reason);
  };
  // initial play
  requestAnimationFrame(() => { const s = slides()[deck._index || 0]; if (s) s.classList.add('play'); });
  deck.addEventListener('slidechange', e => {
    const s = e.detail.slide;
    s.classList.remove('play'); void s.offsetWidth; s.classList.add('play');
  });
})();

// ---- demo video (last slide): play on arrival, pause on leave, Space toggles ----
(() => {
  const deck = document.querySelector('deck-stage');
  const video = document.querySelector('.demo-video');
  if (!deck || !video) return;
  const frame = video.closest('.video-frame');
  video.addEventListener('error', () => frame.classList.add('missing'));
  const demoSlide = video.closest('section');
  deck.addEventListener('slidechange', e => {
    if (e.detail.slide === demoSlide) {
      if (!document.documentElement.classList.contains('static')) {
        const p = video.play(); if (p) p.catch(() => {});
      }
    } else if (!video.paused) {
      video.pause();
    }
  });
  window.addEventListener('keydown', e => {
    if ((e.key === ' ' || e.key === 'k' || e.key === 'K') && deck._slides &&
        deck._slides[deck._index] === demoSlide) {
      e.preventDefault(); e.stopImmediatePropagation();
      video.paused ? video.play().catch(() => {}) : video.pause();
    }
  }, true);
})();
