/** Texto atual enviado à voz e que pode ser traduzido pelo VLibras. */
(function () {
  'use strict';

  const painel = document.getElementById('libras-fala');
  const textoAtual = document.getElementById('libras-fala-texto');
  const fechar = document.getElementById('libras-fala-fechar');
  if (!painel || !textoAtual) return;

  fechar?.addEventListener('click', () => {
    painel.hidden = true;
  });

  window.atualizarFalaLibras = function (texto) {
    textoAtual.textContent = String(texto || '').trim();
    painel.hidden = !textoAtual.textContent;
  };
})();
