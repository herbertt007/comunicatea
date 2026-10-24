/**
 * ComunicaTEA — atividades.js
 * Utilitários globais das atividades
 */
(function () {
  'use strict';

  /**
   * Registra uma sessão de atividade via AJAX (sem bloquear a UI).
   */
  window.registrarSessao = function (tipo, interacao) {
    try {
      const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]');
      const token = csrfToken ? csrfToken.value : getCookie('csrftoken');
      fetch('/atividades/registrar-sessao/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': token
        },
        body: JSON.stringify({ tipo, interacao }),
      }).catch(() => {}); // falha silenciosamente
    } catch (e) {}
  };

  function getCookie(name) {
    let v = null;
    document.cookie.split(';').some(c => {
      const [k, val] = c.trim().split('=');
      if (k === name) { v = decodeURIComponent(val); return true; }
    });
    return v;
  }

  // Suporte a teclado: Enter/Space ativa cartões clicáveis
  document.addEventListener('keydown', function (e) {
    if ((e.key === 'Enter' || e.key === ' ') && e.target.getAttribute('role') === 'button') {
      e.preventDefault();
      e.target.click();
    }
  });

  // Animação de entrada para cartões
  const cards = document.querySelectorAll('.ctea-pic-card, .ctea-act-card, .ctea-lib-card');
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry, i) => {
      if (entry.isIntersecting) {
        entry.target.style.animationDelay = (i * 0.05) + 's';
        entry.target.classList.add('fade-up');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1 });
  cards.forEach(c => observer.observe(c));
})();
