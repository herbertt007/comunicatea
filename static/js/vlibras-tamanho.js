/** Reduz o painel flutuante do VLibras sem alterar seus controles ou o avatar. */
(() => {
  const estiloId = 'comunicatea-vlibras-tamanho';
  const regras = `
    #vlibras-app {
      --widget-width: 250px !important;
      --player-height: 310px !important;
    }

    @media (max-width: 480px) {
      #vlibras-app {
        --widget-width: 220px !important;
        --player-height: 275px !important;
      }
    }
  `;

  function ajustarPainel() {
    const raiz = document.querySelector('#vlibras-app-root')?.shadowRoot;
    if (!raiz || raiz.getElementById(estiloId)) return Boolean(raiz);

    const estilo = document.createElement('style');
    estilo.id = estiloId;
    estilo.textContent = regras;
    raiz.append(estilo);
    return true;
  }

  if (ajustarPainel()) return;

  const observador = new MutationObserver(() => {
    if (ajustarPainel()) observador.disconnect();
  });
  observador.observe(document.documentElement, { childList: true, subtree: true });
})();
