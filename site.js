(() => {
  const dialog = document.querySelector('#figure-dialog');
  let previousFocus;
  document.querySelectorAll('.figure-gallery').forEach(gallery => {
    gallery.querySelectorAll('.figure-choice').forEach(button => {
      button.addEventListener('click', () => {
        gallery.querySelectorAll('.figure-choice').forEach(choice => choice.setAttribute('aria-pressed', String(choice === button)));
        gallery.querySelectorAll('.research-figure').forEach(figure => { figure.hidden = figure.id !== button.getAttribute('aria-controls'); });
      });
    });
  });
  document.querySelectorAll('.expand-figure').forEach(button => {
    button.addEventListener('click', () => {
      const figure = button.closest('figure');
      const original = figure.querySelector('img');
      document.querySelector('#dialog-title').textContent = figure.querySelector('h4').textContent;
      const enlarged = document.querySelector('#dialog-image');
      enlarged.src = original.src;
      enlarged.alt = original.alt;
      document.querySelector('#dialog-caption-text').textContent = figure.querySelector('figcaption p').textContent;
      document.querySelector('#dialog-credit').replaceChildren(...[...figure.querySelector('small').childNodes].map(node => node.cloneNode(true)));
      document.querySelector('#dialog-original').href = original.src;
      previousFocus = button;
      dialog.showModal();
      document.body.classList.add('modal-open');
      dialog.scrollTop = 0;
    });
  });
  dialog.querySelector('.dialog-close').addEventListener('click', () => dialog.close());
  dialog.addEventListener('click', event => { if (event.target === dialog) { const r = dialog.getBoundingClientRect(); if (event.clientX < r.left || event.clientX > r.right || event.clientY < r.top || event.clientY > r.bottom) dialog.close(); } });
  dialog.addEventListener('close', () => { document.body.classList.remove('modal-open'); previousFocus?.focus({preventScroll:true}); });
  const links = [...document.querySelectorAll('.topic-nav a')];
  const sections = [...document.querySelectorAll('.topic-section')];
  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) links.forEach(link => {
          const active = link.hash === '#' + entry.target.id;
          link.classList.toggle('active', active);
          if (active) link.setAttribute('aria-current', 'location'); else link.removeAttribute('aria-current');
        });
      });
    }, {rootMargin:'-10% 0px -65% 0px', threshold:0});
    sections.forEach(section => observer.observe(section));
  }
})();
