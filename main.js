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
  if (header) {
    window.addEventListener('scroll', () => {
      if (window.scrollY > 40) {
        header.style.background = 'rgba(28, 58, 112, 0.96)';
        header.style.boxShadow = '0 4px 20px rgba(0, 0, 0, 0.35)';
      } else {
        header.style.background = 'rgba(28, 58, 112, 0.90)';
        header.style.boxShadow = 'none';
      }
    });
  }

  // 4. Enviar datos del formulario por Correo a Lyrasoft2026@gmail.com (Rutina AJAX)
  const contactForm = document.getElementById('contactForm');
  const formStatusMessage = document.getElementById('formStatusMessage');

  if (contactForm) {
    contactForm.addEventListener('submit', async (e) => {
      e.preventDefault();

      const nombre = document.getElementById('nombre')?.value.trim();
      const tel = document.getElementById('telefono')?.value.trim();
      const email = document.getElementById('correo')?.value.trim();
      const ciudad = document.getElementById('ciudad')?.value.trim();
      const tipo = document.getElementById('tipo_negocio')?.value.trim();
      const asunto = document.getElementById('asunto')?.value.trim();

      const submitBtn = contactForm.querySelector('button[type="submit"]');
      const originalBtnHtml = submitBtn ? submitBtn.innerHTML : 'Enviar Solicitud';

      if (!nombre || !tel || !email || !ciudad || !tipo || !asunto) {
        if (formStatusMessage) {
          formStatusMessage.innerHTML = `
            <div class="form-alert error">
              <div style="font-size: 1.6rem; line-height: 1;">⚠️</div>
              <div>
                <h4>Campos Incompletos</h4>
                <p>Por favor, completa todos los campos requeridos antes de enviar.</p>
              </div>
            </div>`;
        }
        return;
      }

      // Estado de carga
      if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.innerHTML = `<span class="btn-spinner"></span> Enviando a Lyrasoft2026@gmail.com...`;
      }
      if (formStatusMessage) formStatusMessage.innerHTML = '';

      const payload = {
        _subject: `Nueva Solicitud de Información LYRAPOINT: ${nombre}`,
        _template: 'table',
        _captcha: 'false',
        'Empresa_o_Solicitante': nombre,
        'Telefono_Contacto': tel,
        'Correo_Electronico': email,
        'Ciudad': ciudad,
        'Tipo_de_Negocio': tipo,
        'Asunto_o_Consulta': asunto
      };

      try {
        const response = await fetch('https://formsubmit.co/ajax/Lyrasoft2026@gmail.com', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
          },
          body: JSON.stringify(payload)
        });

        const data = await response.json();

        if (response.ok && (data.success === 'true' || data.success === true)) {
          contactForm.reset();
          if (formStatusMessage) {
            formStatusMessage.innerHTML = `
              <div class="form-alert success">
                <div style="font-size: 1.8rem; line-height: 1;">✅</div>
                <div>
                  <h4>¡Solicitud enviada con éxito!</h4>
                  <p>Hemos recibido tus datos y los hemos enviado directamente al correo <strong>Lyrasoft2026@gmail.com</strong>. Nuestro equipo se comunicará contigo a la brevedad.</p>
                </div>
              </div>`;
            formStatusMessage.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
          }
        } else {
          throw new Error(data.message || 'Error al procesar el envío');
        }
      } catch (err) {
        console.error('Error al enviar formulario:', err);
        if (formStatusMessage) {
          const mailtoFallback = `mailto:Lyrasoft2026@gmail.com?subject=${encodeURIComponent('Solicitud LYRAPOINT - ' + nombre)}&body=${encodeURIComponent(
            `Empresa/Solicitante: ${nombre}\nTeléfono: ${tel}\nCorreo: ${email}\nCiudad: ${ciudad}\nTipo de Negocio: ${tipo}\nAsunto: ${asunto}`
          )}`;
          formStatusMessage.innerHTML = `
            <div class="form-alert error">
              <div style="font-size: 1.6rem; line-height: 1;">⚠️</div>
              <div>
                <h4>No pudimos conectar con el servidor de correo</h4>
                <p>Por favor verifica tu conexión o haz clic en el siguiente enlace para enviar tu consulta directamente:</p>
                <a href="${mailtoFallback}" class="btn btn-sm btn-primary" style="margin-top: 0.6rem; display: inline-flex; align-items: center; gap: 0.4rem;">
                  ✉ Enviar directamente a Lyrasoft2026@gmail.com
                </a>
              </div>
            </div>`;
        }
      } finally {
        if (submitBtn) {
          submitBtn.disabled = false;
          submitBtn.innerHTML = originalBtnHtml;
        }
      }
    });
  }

  // 5. Enviar datos del formulario por WhatsApp
  const btnWhatsapp = document.getElementById('btnWhatsappForm');
  if (btnWhatsapp) {
    btnWhatsapp.addEventListener('click', () => {
      const nombre = document.getElementById('nombre')?.value.trim();
      const tel = document.getElementById('telefono')?.value.trim();
      const email = document.getElementById('correo')?.value.trim();
      const ciudad = document.getElementById('ciudad')?.value.trim();
      const tipo = document.getElementById('tipo_negocio')?.value.trim();
      const asunto = document.getElementById('asunto')?.value.trim();

      if (!nombre || !tel) {
        alert('Por favor, indica al menos el nombre de la empresa/solicitante y un teléfono de contacto.');
        return;
      }

      const text = `*SOLICITUD DE INFORMACIÓN - LYRAPOINT*\n\n` +
        `*Empresa / Solicitante:* ${nombre || 'No indicado'}\n` +
        `*Teléfono:* ${tel || 'No indicado'}\n` +
        `*Correo:* ${email || 'No indicado'}\n` +
        `*Ciudad:* ${ciudad || 'No indicada'}\n` +
        `*Tipo de Negocio:* ${tipo || 'No indicado'}\n` +
        `*Asunto:* ${asunto || 'Consulta general'}`;

      window.open(`https://wa.me/?text=${encodeURIComponent(text)}`, '_blank');
    });
  }

  // 5. Manejador de Recursos Exclusivos de Clientes (Modal)
  const clientTriggers = document.querySelectorAll('.client-modal-trigger');
  const clientModal = document.getElementById('clientModal');
  const closeClientModal = document.getElementById('closeClientModal');
  const clientModalTitle = document.getElementById('clientModalTitle');
  const clientModalDesc = document.getElementById('clientModalDesc');
  const modalWhatsappBtn = document.getElementById('modalWhatsappBtn');
  const modalContactBtn = document.getElementById('modalContactBtn');

  if (clientModal) {
    clientTriggers.forEach(trigger => {
      trigger.addEventListener('click', (e) => {
        e.preventDefault();
        const resourceName = trigger.getAttribute('data-resource') || 'Recurso de Clientes';
        const resourceDesc = trigger.getAttribute('data-desc') || '';

        if (clientModalTitle) clientModalTitle.textContent = resourceName;
        if (clientModalDesc && resourceDesc) {
          clientModalDesc.innerHTML = `${resourceDesc}<br><br><span style="color: #fbbf24; font-weight: 600;">🔒 Acceso Exclusivo:</span> Este recurso está disponible <strong>únicamente para clientes que ya adquirieron el sistema LYRAPOINT</strong> con licencia activa.`;
        }

        if (modalWhatsappBtn) {
          const msg = `Hola, soy cliente de LYRAPOINT con licencia activa y deseo solicitar acceso a: *${resourceName}*.`;
          modalWhatsappBtn.href = `https://wa.me/?text=${encodeURIComponent(msg)}`;
        }

        clientModal.classList.add('active');
        clientModal.setAttribute('aria-hidden', 'false');
      });
    });

    const closeModal = () => {
      clientModal.classList.remove('active');
      clientModal.setAttribute('aria-hidden', 'true');
    };

    if (closeClientModal) {
      closeClientModal.addEventListener('click', closeModal);
    }

    clientModal.addEventListener('click', (e) => {
      if (e.target === clientModal) {
        closeModal();
      }
    });

    if (modalContactBtn) {
      modalContactBtn.addEventListener('click', () => {
        closeModal();
      });
    }

    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && clientModal.classList.contains('active')) {
        closeModal();
      }
    });
  }
});
