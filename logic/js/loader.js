document.addEventListener('DOMContentLoaded', () => {
  // Load head.html (favicon, Font Awesome) and inject into <head>
  fetch('/mods/head.html')
    .then(r => r.text())
    .then(html => {
      const parser = new DOMParser();
      const doc = parser.parseFromString(html, 'text/html');
      doc.querySelectorAll('link, meta, base, script').forEach(node => {
        if (node.tagName === 'SCRIPT') {
          const script = document.createElement('script');
          if (node.src) script.src = node.src;
          script.async = node.async;
          if (node.textContent) script.textContent = node.textContent;
          document.head.appendChild(script);
        } else {
          document.head.appendChild(node.cloneNode(true));
        }
      });
    })
    .catch(err => console.error('Error loading head.html:', err));

  // Reusable partials injected into each page (mods/)
  const partials = [
    {src: 'header.html', target: 'header'},
    {src: 'footer.html', target: 'footer'}
  ];

  partials.forEach(({src, target}) => {
    fetch(`/mods/${src}`)
      .then(r => r.text())
      .then(html => {
        const el = document.getElementById(target);
        if (el) {
          el.innerHTML = html;
          if (src === 'header.html') markActiveNav();
        }
      })
      .catch(err => console.error(`Error loading ${src}:`, err));
  });

  // Highlight the current page link in the navbar
  function markActiveNav() {
    let current = location.pathname.split('/').pop().toLowerCase();
    if (current === '' || current === 'index' || current === 'index.html') {
      current = 'index';
    } else {
      current = current.replace(/\.html$/, '');
    }
    document.querySelectorAll('#header a[data-nav]').forEach(link => {
      if (link.getAttribute('data-nav') === current) link.classList.add('nav-active');
    });
  }

  // Mobile menu toggle (event delegation works after async partial load)
  document.addEventListener('click', (e) => {
    const btn = e.target.closest('#mobile-menu-btn');
    if (btn) {
      document.getElementById('mobile-menu')?.classList.toggle('hidden');
      return;
    }
    if (e.target.closest('#mobile-menu a')) {
      document.getElementById('mobile-menu')?.classList.add('hidden');
    }
  });

  // Sticky header: add scrolled state on scroll
  const onScroll = () => {
    const header = document.getElementById('site-header');
    if (header) header.classList.toggle('scrolled', window.scrollY > 20);
  };
  window.addEventListener('scroll', onScroll, {passive: true});
  onScroll();
});
