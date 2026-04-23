// ── Floating Admin FAB — appears after scrolling down ────────────────────────
const fab = document.getElementById('fabAdmin');
if (fab) {
  const THRESHOLD = 280;
  const update = () => fab.classList.toggle('fab-visible', window.scrollY > THRESHOLD);
  update();
  window.addEventListener('scroll', update, { passive: true });
}

// ── Auto-dismiss flash alerts after 4s ──────────────────────────────────────
document.querySelectorAll('.amz-alert').forEach(el => {
  setTimeout(() => {
    try { bootstrap.Alert.getOrCreateInstance(el).close(); } catch(e) {}
  }, 4000);
});

// ── Staggered card entrance animation ───────────────────────────────────────
const cards = document.querySelectorAll('.deal-card');
if (cards.length && 'IntersectionObserver' in window) {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const idx = parseInt(entry.target.dataset.idx || 0);
        setTimeout(() => {
          entry.target.style.opacity = '1';
          entry.target.style.transform = 'translateY(0)';
        }, (idx % 8) * 60);
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.07 });

  cards.forEach((card, i) => {
    card.style.opacity = '0';
    card.style.transform = 'translateY(22px)';
    card.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
    card.dataset.idx = i;
    observer.observe(card);
  });
}

// ── Smooth scroll for anchor links ──────────────────────────────────────────
document.querySelectorAll('a[href^="#"]').forEach(a => {
  a.addEventListener('click', function(e) {
    const target = document.querySelector(this.getAttribute('href'));
    if (target) {
      e.preventDefault();
      target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  });
});
