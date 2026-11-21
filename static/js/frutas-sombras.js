(function () {
  'use strict';

  const board = document.getElementById('fruit-board');
  if (!board) return;

  const pieces = Array.from(board.querySelectorAll('.fruit-piece'));
  const targets = Array.from(board.querySelectorAll('.fruit-target'));
  const feedback = document.getElementById('fruit-feedback');
  const singular = board.dataset.singular || 'figura';
  const plural = board.dataset.plural || 'figuras';
  let selected = null;
  let completed = 0;

  /* ── helpers ──────────────────────────────────────────────── */

  function selectPiece(piece) {
    if (piece.disabled) return;
    pieces.forEach(item => item.classList.toggle('is-selected', item === piece));
    selected = piece;
    feedback.textContent = piece.getAttribute('aria-label') + ' escolhido. Agora encontre a sombra igual.';
  }

  function speakFruit(name) {
    if (window.falarTexto) {
      window.falarTexto(name + '.', 0.86);
      return;
    }
    if (!('speechSynthesis' in window)) return;
    window.speechSynthesis.cancel();
    const message = new SpeechSynthesisUtterance(name + '.');
    message.lang = 'pt-BR';
    message.rate = 0.86;
    message.pitch = 1.08;
    message.volume = 1;
    window.speechSynthesis.speak(message);
  }

  function placeFruit(target, piece) {
    if (!piece || target.classList.contains('is-complete')) return;
    if (piece.dataset.fruit !== target.dataset.target) {
      target.classList.remove('is-wrong');
      void target.offsetWidth;
      target.classList.add('is-wrong');
      feedback.textContent = 'Esse par parece diferente. Você pode tentar outra sombra.';
      window.setTimeout(() => target.classList.remove('is-wrong'), 500);
      return;
    }

    const name = piece.querySelector('.fruit-name').textContent;
    const emoji = piece.querySelector('.fruit-emoji').textContent;
    target.classList.add('is-complete');
    target.setAttribute('aria-label', 'Sombra combinada com ' + name);
    target.querySelector('.shadow-emoji').textContent = emoji;
    target.querySelector('.target-label').textContent = name;
    piece.disabled = true;
    piece.classList.remove('is-selected');
    selected = null;
    completed += 1;
    feedback.textContent = name + '! Par encontrado.';
    speakFruit(name);

    if (completed === pieces.length) {
      feedback.textContent = 'Todas as figuras encontraram suas sombras. Muito bem!';
      window.registrarSessao?.(board.dataset.activityType, `associou ${plural} às sombras`);
    }
  }

  /* ── click (funciona em qualquer dispositivo) ────────────── */

  pieces.forEach(piece => {
    piece.addEventListener('click', () => selectPiece(piece));
  });

  targets.forEach(target => {
    target.addEventListener('click', () => placeFruit(target, selected));
  });

  /* ── HTML5 drag (desktop com mouse) ──────────────────────── */

  pieces.forEach(piece => {
    piece.addEventListener('dragstart', event => {
      selectPiece(piece);
      event.dataTransfer.setData('text/plain', piece.dataset.fruit);
      event.dataTransfer.effectAllowed = 'move';
    });
  });

  targets.forEach(target => {
    target.addEventListener('dragover', event => {
      if (!target.classList.contains('is-complete')) {
        event.preventDefault();
        target.classList.add('is-over');
      }
    });
    target.addEventListener('dragleave', () => target.classList.remove('is-over'));
    target.addEventListener('drop', event => {
      event.preventDefault();
      target.classList.remove('is-over');
      const fruitId = event.dataTransfer.getData('text/plain');
      const piece = pieces.find(item => item.dataset.fruit === fruitId);
      placeFruit(target, piece);
    });
  });

  /* ── Touch drag (celular / tablet) ───────────────────────── */

  let dragPiece = null;
  let dragClone = null;
  let touchOffsetX = 0;
  let touchOffsetY = 0;

  function getTargetUnder(x, y) {
    /* Esconde o clone para que elementFromPoint ache o alvo real */
    if (dragClone) dragClone.style.display = 'none';
    const el = document.elementFromPoint(x, y);
    if (dragClone) dragClone.style.display = '';
    if (!el) return null;
    return el.closest('.fruit-target');
  }

  pieces.forEach(piece => {
    piece.addEventListener('touchstart', e => {
      if (piece.disabled) return;
      e.preventDefault();

      dragPiece = piece;
      selectPiece(piece);

      const touch = e.touches[0];
      const rect = piece.getBoundingClientRect();
      touchOffsetX = touch.clientX - rect.left;
      touchOffsetY = touch.clientY - rect.top;

      /* Cria um clone visual que segue o dedo */
      dragClone = piece.cloneNode(true);
      dragClone.classList.add('fruit-drag-clone');
      dragClone.style.cssText = `
        position: fixed;
        z-index: 9999;
        pointer-events: none;
        width: ${rect.width}px;
        height: ${rect.height}px;
        opacity: 0.88;
        transform: scale(1.08);
        left: ${touch.clientX - touchOffsetX}px;
        top: ${touch.clientY - touchOffsetY}px;
        border-radius: 18px;
        box-shadow: 0 8px 24px rgba(0,0,0,.18);
        transition: none;
      `;
      document.body.appendChild(dragClone);
      piece.style.opacity = '0.35';
    }, { passive: false });
  });

  document.addEventListener('touchmove', e => {
    if (!dragClone) return;
    e.preventDefault();
    const touch = e.touches[0];
    dragClone.style.left = (touch.clientX - touchOffsetX) + 'px';
    dragClone.style.top = (touch.clientY - touchOffsetY) + 'px';

    /* Destaca o alvo sob o dedo */
    targets.forEach(t => t.classList.remove('is-over'));
    const target = getTargetUnder(touch.clientX, touch.clientY);
    if (target && !target.classList.contains('is-complete')) {
      target.classList.add('is-over');
    }
  }, { passive: false });

  document.addEventListener('touchend', e => {
    if (!dragClone || !dragPiece) return;

    const touch = e.changedTouches[0];
    const target = getTargetUnder(touch.clientX, touch.clientY);

    targets.forEach(t => t.classList.remove('is-over'));

    if (target) {
      placeFruit(target, dragPiece);
    }

    /* Limpa o clone e restaura a peça */
    dragClone.remove();
    dragClone = null;
    if (dragPiece && !dragPiece.disabled) {
      dragPiece.style.opacity = '';
    }
    dragPiece = null;
  });

  document.addEventListener('touchcancel', () => {
    if (dragClone) dragClone.remove();
    dragClone = null;
    if (dragPiece) dragPiece.style.opacity = '';
    dragPiece = null;
    targets.forEach(t => t.classList.remove('is-over'));
  });

  /* ── Reset ───────────────────────────────────────────────── */

  document.getElementById('fruit-reset').addEventListener('click', () => {
    completed = 0;
    selected = null;
    dragPiece = null;
    if (dragClone) { dragClone.remove(); dragClone = null; }
    pieces.forEach(piece => {
      piece.disabled = false;
      piece.style.opacity = '';
      piece.classList.remove('is-selected');
    });
    targets.forEach(target => {
      target.classList.remove('is-complete', 'is-over', 'is-wrong');
      target.setAttribute('aria-label', `Sombra de ${singular}`);
      const id = target.dataset.target;
      target.querySelector('.shadow-emoji').textContent = pieces.find(piece => piece.dataset.fruit === id).querySelector('.fruit-emoji').textContent;
      target.querySelector('.shadow-emoji').classList.add('shadow-emoji');
      target.querySelector('.target-label').textContent = 'Solte aqui';
    });
    feedback.textContent = 'Escolha uma figura para começar.';
  });
})();
