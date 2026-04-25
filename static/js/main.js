// ── Floating Admin FAB ───────────────────────────────────────────────────────
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

// ── Smooth scroll (skip category bar) ───────────────────────────────────────
document.querySelectorAll('a[href^="#"]').forEach(a => {
  if (a.closest('.category-scroll')) return;
  a.addEventListener('click', function(e) {
    const target = document.querySelector(this.getAttribute('href'));
    if (target) { e.preventDefault(); target.scrollIntoView({ behavior: 'smooth', block: 'start' }); }
  });
});

// ═══════════════════════════════════════════════════════════════════════════
//  SUBCATEGORY DROPDOWN
//  window.SENZONE_SUBS is set in <head> via {% block head %} in index.html
//  so it is always defined BEFORE this script runs.
//  Panel is a direct child of <body> with position:fixed — nothing can hide it.
// ═══════════════════════════════════════════════════════════════════════════
(function () {
  var pills = document.querySelectorAll('.cat-pill--has-sub');
  if (!pills.length) return;   // not on the index page

  var subs = window.SENZONE_SUBS || {};
  var activeSub = window.SENZONE_ACTIVE_SUB || '';

  // ── Create one shared panel on <body> ────────────────────────────────────
  var panel = document.createElement('div');
  panel.id  = 'senzoneSubDrop';
  panel.innerHTML = '<div class="ssd-inner"></div>';
  document.body.appendChild(panel);
  var inner = panel.querySelector('.ssd-inner');
  var activePill = null;

  // ── Position below a pill using fixed viewport coords ────────────────────
  function positionPanel(pill) {
    var r = pill.getBoundingClientRect();
    panel.style.top  = (r.bottom + 8) + 'px';
    panel.style.left = Math.min(r.left, window.innerWidth - 220) + 'px';
  }

  // ── Build subcategory links ──────────────────────────────────────────────
  function buildInner(cat) {
    var list = subs[cat] || [];
    var base = '/?category=' + encodeURIComponent(cat);
    var html = '<a class="ssd-item ssd-item--all" href="' + base + '#products">'
             + '<i class="bi bi-grid-fill" style="margin-right:8px"></i>All ' + cat + '</a>';
    list.forEach(function(sub) {
      var url   = base + '&subcategory=' + encodeURIComponent(sub) + '#products';
      var cls   = sub === activeSub ? ' ssd-item--active' : '';
      html += '<a class="ssd-item' + cls + '" href="' + url + '">' + sub + '</a>';
    });
    return html;
  }

  // ── Show ─────────────────────────────────────────────────────────────────
  function openPanel(pill) {
    var cat  = pill.dataset.cat;
    var list = subs[cat] || [];
    if (!list.length) return;

    inner.innerHTML = buildInner(cat);
    positionPanel(pill);
    panel.style.display = 'block';

    pill.classList.add('cat-pill--drop-open');
    var arrow = pill.querySelector('.cat-pill__arrow');
    if (arrow) arrow.style.transform = 'rotate(180deg)';
    activePill = pill;
  }

  // ── Hide ─────────────────────────────────────────────────────────────────
  function closePanel() {
    panel.style.display = 'none';
    if (activePill) {
      activePill.classList.remove('cat-pill--drop-open');
      var arrow = activePill.querySelector('.cat-pill__arrow');
      if (arrow) arrow.style.transform = '';
      activePill = null;
    }
  }

  // ── Pill click handler ───────────────────────────────────────────────────
  pills.forEach(function(pill) {
    pill.addEventListener('click', function(e) {
      e.preventDefault();
      e.stopPropagation();
      if (activePill === pill) { closePanel(); return; }
      closePanel();
      openPanel(pill);
    });
  });

  // ── Keep panel open when clicking inside it ──────────────────────────────
  panel.addEventListener('click', function(e) { e.stopPropagation(); });

  // ── Close on outside click ───────────────────────────────────────────────
  document.addEventListener('click', function() { closePanel(); });

  // ── Reposition on scroll/resize ──────────────────────────────────────────
  window.addEventListener('scroll', function() { if (activePill) positionPanel(activePill); }, { passive: true });
  window.addEventListener('resize', function() { if (activePill) positionPanel(activePill); });
})();
