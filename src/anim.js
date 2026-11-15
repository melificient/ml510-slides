(() => {
  const deck = document.querySelector('deck-stage');
  if (!deck || document.documentElement.classList.contains('static')) return;
  const slides = () => Array.from(deck.children).filter(e => e.tagName === 'SECTION');
  const FLOW = 1;                       // slide 2 (0-based)
  const groups = () => {
    const kids = Array.from(slides()[FLOW].querySelectorAll('.flow > *'));
    const g = []; kids.forEach(k => { if (k.classList.contains('step')) g.push([k]); else if (g.length) g[g.length - 1].push(k); });
    // attach each arrow to the step that follows it
    const out = []; let pending = [];
    kids.forEach(k => { if (k.classList.contains('arrow')) pending.push(k); else { out.push([...pending, k]); pending = []; } });
    return out;
  };
  let shown = 4;
  const render = () => groups().forEach((grp, i) => grp.forEach(el => el.classList.toggle('hidden-step', i >= shown)));
  const orig = deck._go.bind(deck);
  deck._go = (i, reason) => {
    if (document.documentElement.classList.contains('static')) return orig(i, reason);
    const cur = deck._index;
    if (cur === FLOW && i === cur + 1 && shown < 4) { shown++; render(); return; }
    if (cur === FLOW && i === cur - 1 && shown > 1) { shown--; render(); return; }
    if (i === FLOW) { shown = cur < FLOW ? 1 : 4; render(); }
    orig(i, reason);
  };
  // initial play
  requestAnimationFrame(() => { const s = slides()[deck._index || 0]; if (s) s.classList.add('play'); });
  deck.addEventListener('slidechange', e => {
    const s = e.detail.slide;
    s.classList.remove('play'); void s.offsetWidth; s.classList.add('play');
  });
})();
