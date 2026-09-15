/* Scroll position is the animation clock: no timers, scroll interception or layout changes. */
(() => {
  const name = document.querySelector('.hero-name');
  const intro = document.querySelector('.welcome');
  const content = document.querySelector('.welcome-content');
  if (!name || !intro || !content) return;
  const root = document.documentElement;
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  let frame = 0, startTop = 0, targetScale = 1, distance = 280, fadeStart = 0;
  const clamp = value => Math.max(0, Math.min(1, value));
  function render() {
    frame = 0;
    const y = Math.max(0, window.scrollY);
    const p = clamp(y / distance);
    const ease = p * p * (3 - 2 * p);
    const mobile = window.innerWidth <= 600;
    const scale = reduced.matches ? targetScale : 1 + (targetScale - 1) * ease;
    const travel = reduced.matches ? 1 : ease;
    name.style.transform = `translateY(${((mobile ? 23 : 27) - startTop) * travel}px) scale(${scale})`;
    root.style.setProperty('--header-opacity', reduced.matches ? '1' : String(clamp(y / 160)));
    // Keep the complete bio readable, including on tall mobile introductions.
    const fade = reduced.matches ? 0 : clamp((y - fadeStart) / 220);
    content.style.opacity = String(1 - fade);
    content.style.transform = reduced.matches ? 'none' : `scale(${1 - fade * .025})`;
    content.style.visibility = fade === 1 ? 'hidden' : 'visible';
  }
  function measure() {
    const box = intro.getBoundingClientRect();
    const mobile = window.innerWidth <= 600;
    startTop = mobile ? 104 : 116;
    root.style.setProperty('--name-left', `${box.left}px`);
    targetScale = (mobile ? 20 : 26) / parseFloat(getComputedStyle(name).fontSize);
    distance = mobile ? 240 : 320;
    fadeStart = Math.max(distance, box.height - 330);
    root.classList.add('motion-ready');
    render();
  }
  function schedule() { if (!frame) frame = requestAnimationFrame(render); }
  window.addEventListener('scroll', schedule, { passive: true });
  window.addEventListener('resize', measure, { passive: true });
  window.addEventListener('pageshow', measure);
  reduced.addEventListener('change', measure);
  measure();
  if (document.fonts) document.fonts.ready.then(measure);
})();
