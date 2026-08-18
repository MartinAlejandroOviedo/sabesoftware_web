(function () {
  'use strict';

  async function fetchJSON(url) {
    const res = await fetch(url);
    if (!res.ok) throw new Error(`Error ${res.status} en ${url}`);
    return res.json();
  }

  function escapeHtml(value) {
    return String(value).replace(/[&<>"']/g, (c) => ({
      '&': '&', '<': '<', '>': '>', '"': '"', "'": "'"
    }[c]));
  }

  const PRODUCT_ACCENT = {
    indigo: { gradient: 'from-indigo-500 to-blue-500', glow: 'bg-indigo-500/20', shadow: 'shadow-indigo-500/40', btn: 'bg-indigo-600 hover:bg-indigo-500', text: 'text-indigo-400', bg: 'bg-indigo-500/20' },
    purple: { gradient: 'from-purple-500 to-pink-500', glow: 'bg-purple-500/20', shadow: 'shadow-purple-500/40', btn: 'bg-purple-600 hover:bg-purple-500', text: 'text-purple-400', bg: 'bg-purple-500/20' },
    pink:   { gradient: 'from-pink-500 to-rose-500', glow: 'bg-pink-500/20', shadow: 'shadow-pink-500/40', btn: 'bg-pink-600 hover:bg-pink-500', text: 'text-pink-400', bg: 'bg-pink-500/20' },
    emerald: { gradient: 'from-emerald-500 to-teal-500', glow: 'bg-emerald-500/20', shadow: 'shadow-emerald-500/40', btn: 'bg-emerald-600 hover:bg-emerald-500', text: 'text-emerald-400', bg: 'bg-emerald-500/20' }
  };

  function renderProduct(product) {
    const a = PRODUCT_ACCENT[product.accent] || PRODUCT_ACCENT.indigo;

    // Show the hero section
    const hero = document.getElementById('product-hero');
    console.log('renderProduct called, hero classes before:', hero.className);
    hero.classList.remove('hidden');
    console.log('hero classes after:', hero.className);

    // Title
    document.getElementById('product-title').textContent = product.name;

    // Subtitle / short description
    document.getElementById('product-subtitle').textContent = product.description;

    // Icon
    const iconEl = document.getElementById('product-icon');
    iconEl.className = `w-24 h-24 rounded-2xl flex items-center justify-center text-3xl text-white mb-8 shadow-lg ${a.shadow} ${a.gradient}`;
    iconEl.innerHTML = `<i class="${escapeHtml(product.icon)}"></i>`;

    // Description
    document.getElementById('product-description').textContent = product.description;

    // Features list
    const featuresEl = document.getElementById('product-features');
    featuresEl.innerHTML = product.features.map(f => `
      <li class="flex items-center gap-3 p-4 rounded-xl bg-white/5 border border-white/10 hover:bg-white/10 transition-colors">
        <span class="w-10 h-10 rounded-lg ${a.bg} ${a.text} flex items-center justify-center flex-shrink-0">
          <i class="fas fa-check"></i>
        </span>
        <span class="text-slate-300">${escapeHtml(f)}</span>
      </li>
    `).join('');

    // Show the main content
    document.querySelector('#product-hero + section').style.display = 'block';
  }

  async function init() {
    try {
      // La URL visible es /products/<slug>, extraer slug del pathname
      const pathParts = window.location.pathname.split('/').filter(Boolean);
      const slug = pathParts[pathParts.length - 1];
      if (!slug || slug === 'products') {
        console.error('No slug found in URL');
        return;
      }
      console.log('Loading product:', slug);

      const product = await fetchJSON(`/api/products/${slug}`);
      console.log('Product loaded:', product);
      if (!product) {
        console.error('Product not found');
        return;
      }

      renderProduct(product);
    } catch (err) {
      console.error('Error cargando producto:', err);
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();