(function () {
  'use strict';

  async function fetchJSON(url) {
    const res = await fetch(url);
    if (!res.ok) throw new Error(`Error ${res.status} en ${url}`);
    return res.json();
  }

  function escapeHtml(value) {
    return String(value).replace(/[&<>"']/g, (c) => ({
      '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
    }[c]));
  }

  // Mapeo de acentos a clases Tailwind
  const PRODUCT_ACCENT = {
    indigo: { gradient: 'from-indigo-500 to-blue-500', glow: 'bg-indigo-500/20', shadow: 'shadow-indigo-500/40', btn: 'bg-indigo-600 hover:bg-indigo-500' },
    purple: { gradient: 'from-purple-500 to-pink-500', glow: 'bg-purple-500/20', shadow: 'shadow-purple-500/40', btn: 'bg-purple-600 hover:bg-purple-500' },
    pink:   { gradient: 'from-pink-500 to-rose-500', glow: 'bg-pink-500/20', shadow: 'shadow-pink-500/40', btn: 'bg-pink-600 hover:bg-pink-500' }
  };
  const VALUE_ACCENT = {
    indigo:  { bg: 'bg-indigo-500/20', text: 'text-indigo-400' },
    purple:  { bg: 'bg-purple-500/20', text: 'text-purple-400' },
    pink:    { bg: 'bg-pink-500/20', text: 'text-pink-400' },
    emerald: { bg: 'bg-emerald-500/20', text: 'text-emerald-400' }
  };

  function renderStats(stats, container) {
    container.innerHTML = stats.map((s) => `
      <div class="glass-card rounded-2xl p-6">
        <div class="text-3xl font-extrabold text-white mb-1">${escapeHtml(s.value)}</div>
        <div class="text-sm text-slate-400">${escapeHtml(s.label)}</div>
      </div>`).join('');
  }

  function renderProducts(products, container, mode) {
    const full = mode === 'full';
    container.innerHTML = products.map((p) => {
      const a = PRODUCT_ACCENT[p.accent] || PRODUCT_ACCENT.indigo;
      const features = (p.features || []).map((f) => `
        <li class="flex items-center gap-2"><i class="fas fa-check-circle text-emerald-400"></i> ${escapeHtml(f)}</li>`).join('');
      const featuresBlock = full
        ? `<ul class="space-y-3 mb-8 text-sm text-slate-300">${features}</ul>`
        : '';
      const cta = full
        ? `<a href="/contact" class="inline-flex items-center gap-2 w-full justify-center ${a.btn} text-white font-semibold py-3 rounded-xl transition-all hover:-translate-y-0.5">Solicitar demo <i class="fas fa-arrow-right text-sm"></i></a>`
        : `<a href="/products" class="inline-flex items-center gap-2 w-full justify-center ${a.btn} text-white font-semibold py-3 rounded-xl transition-all hover:-translate-y-0.5">Más información <i class="fas fa-arrow-right text-sm"></i></a>`;
      return `
        <div class="product-card relative rounded-3xl border border-white/10 bg-gradient-to-b from-white/10 to-white/5 p-8 overflow-hidden">
          <div class="absolute -top-16 -right-16 w-40 h-40 ${a.glow} rounded-full blur-3xl"></div>
          <div class="relative">
            <div class="w-16 h-16 rounded-2xl bg-gradient-to-br ${a.gradient} flex items-center justify-center text-2xl text-white mb-6 shadow-lg ${a.shadow}">
              <i class="${escapeHtml(p.icon)}"></i>
            </div>
            <h3 class="text-2xl font-bold text-white mb-3">${escapeHtml(p.name)}</h3>
            <p class="text-slate-400 mb-6 leading-relaxed">${escapeHtml(p.description)}</p>
            ${featuresBlock}
            ${cta}
          </div>
        </div>`;
    }).join('');
  }

  function renderValues(values, container) {
    container.innerHTML = values.map((v) => {
      const a = VALUE_ACCENT[v.accent] || VALUE_ACCENT.indigo;
      return `
        <div class="feature-card rounded-2xl p-8 border border-white/10 bg-white/5">
          <div class="w-14 h-14 rounded-2xl ${a.bg} ${a.text} flex items-center justify-center text-2xl mb-5">
            <i class="${escapeHtml(v.icon)}"></i>
          </div>
          <h3 class="text-xl font-bold text-white mb-3">${escapeHtml(v.title)}</h3>
          <p class="text-slate-400 leading-relaxed">${escapeHtml(v.description)}</p>
        </div>`;
    }).join('');
  }

  function applySiteText(site) {
    document.querySelectorAll('[data-field]').forEach((el) => {
      const key = el.getAttribute('data-field');
      if (site[key] != null) el.textContent = site[key];
    });
  }

  async function init() {
    try {
      const [site, stats, products, values] = await Promise.all([
        fetchJSON('/api/site'),
        fetchJSON('/api/stats'),
        fetchJSON('/api/products'),
        fetchJSON('/api/values')
      ]);

      applySiteText(site);

      const statsEl = document.getElementById('stats-grid');
      if (statsEl) renderStats(stats, statsEl);

      document.querySelectorAll('[data-products]').forEach((el) => {
        renderProducts(products, el, el.getAttribute('data-products'));
      });

      const valuesEl = document.getElementById('values-grid');
      if (valuesEl) renderValues(values, valuesEl);
    } catch (err) {
      console.error('Error cargando datos desde la API:', err);
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
