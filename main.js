/**
 * LYRAPOINT - INTERACTIVIDAD Y COMPORTAMIENTO
 */

document.addEventListener('DOMContentLoaded', () => {
  // 1. Menú Móvil
  const mobileToggle = document.getElementById('mobileToggle');
  const navMenu = document.getElementById('navMenu');
  const navLinks = document.querySelectorAll('.nav-link');

  if (mobileToggle && navMenu) {
    mobileToggle.addEventListener('click', () => {
      navMenu.classList.toggle('open');
      const isOpen = navMenu.classList.contains('open');
      mobileToggle.setAttribute('aria-expanded', isOpen);
    });

    // Cerrar menú al presionar un enlace
    navLinks.forEach(link => {
      link.addEventListener('click', () => {
        navMenu.classList.remove('open');
        mobileToggle.setAttribute('aria-expanded', false);
      });
    });
  }

  // 2. Selector de Videos en el Showcase
  const playlistCards = document.querySelectorAll('.playlist-card');
  const mainVideoPlayer = document.getElementById('mainVideoPlayer');
  const videoTitle = document.getElementById('videoTitle');
  const videoDesc = document.getElementById('videoDesc');

  playlistCards.forEach(card => {
    card.addEventListener('click', () => {
      // Remover clase active de todas las tarjetas
      playlistCards.forEach(c => c.classList.remove('active'));
      // Agregar active a la tarjeta seleccionada
      card.classList.add('active');

      // Leer datos de la tarjeta
      const newSrc = card.getAttribute('data-video-src');
      const newTitle = card.getAttribute('data-title');
      const newDesc = card.getAttribute('data-desc');

      // Actualizar reproductor y textos
      if (mainVideoPlayer && newSrc) {
        mainVideoPlayer.src = newSrc;
        if (typeof mainVideoPlayer.load === 'function') {
          mainVideoPlayer.load();
          mainVideoPlayer.play().catch(() => {});
        }
      }
      if (videoTitle && newTitle) {
        videoTitle.textContent = newTitle;
      }
      if (videoDesc && newDesc) {
        videoDesc.textContent = newDesc;
      }
    });
  });

  // 3. Efecto Header al hacer scroll
  const header = document.getElementById('header');
  window.addEventListener('scroll', () => {
    if (window.scrollY > 40) {
      header.style.background = 'rgba(7, 12, 24, 0.95)';
      header.style.boxShadow = '0 4px 20px rgba(0, 0, 0, 0.4)';
    } else {
      header.style.background = 'rgba(7, 12, 24, 0.85)';
      header.style.boxShadow = 'none';
    }
  });
});
