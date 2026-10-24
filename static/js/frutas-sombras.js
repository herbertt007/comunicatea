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

  pieces.forEach(piece => {
    piece.addEventListener('click', () => selectPiece(piece));
    piece.addEventListener('dragstart', event => {
      selectPiece(piece);
      event.dataTransfer.setData('text/plain', piece.dataset.fruit);
      event.dataTransfer.effectAllowed = 'move';
    });
  });

  targets.forEach(target => {
    target.addEventListener('click', () => placeFruit(target, selected));
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

  document.getElementById('fruit-reset').addEventListener('click', () => {
    completed = 0;
    selected = null;
    pieces.forEach(piece => {
      piece.disabled = false;
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
