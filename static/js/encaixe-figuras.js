(function () {
  'use strict';

  const board = document.getElementById('fit-puzzles');
  if (!board) return;

  const pieces = Array.from(document.querySelectorAll('.fit-piece'));
  const puzzles = Array.from(board.querySelectorAll('.fit-puzzle'));
  const slots = Array.from(board.querySelectorAll('.missing-slot'));
  const feedback = document.getElementById('fit-feedback');
  let selected = null;
  let completed = 0;
  const slotViews = {
    tl: '0 0 50 50', tr: '50 0 50 50',
    bl: '0 50 50 50', br: '50 50 50 50'
  };

  function shuffle(items) {
    const result = items.slice();
    for (let i = result.length - 1; i > 0; i -= 1) {
      const j = Math.floor(Math.random() * (i + 1));
      [result[i], result[j]] = [result[j], result[i]];
    }
    return result;
  }

  function choosePiece(piece) {
    if (piece.disabled) return;
    selected = piece;
    pieces.forEach(option => option.classList.toggle('is-selected', option === piece));
    feedback.textContent = piece.querySelector('strong').textContent + ' selecionada. Encontre o encaixe correspondente.';
  }

  function speak(name) {
    if (window.falarTexto) {
      window.falarTexto(name + '.', 0.86);
      return;
    }
    if (!('speechSynthesis' in window)) return;
    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(name + '.');
    utterance.lang = 'pt-BR';
    utterance.rate = 0.86;
    utterance.pitch = 1.08;
    utterance.volume = 1;
    window.speechSynthesis.speak(utterance);
  }

  function fitPiece(slot, piece) {
    if (!piece || slot.disabled) return;
    const puzzle = slot.closest('.fit-puzzle');
    if (piece.dataset.piece !== puzzle.dataset.target) {
      slot.classList.remove('fit-wrong');
      void slot.offsetWidth;
      slot.classList.add('fit-wrong');
      feedback.textContent = 'Essa peça parece diferente. Você pode tentar outra.';
      window.setTimeout(() => slot.classList.remove('fit-wrong'), 450);
      return;
    }

    const name = puzzle.dataset.name;
    slot.disabled = true;
    slot.classList.add('is-filled');
    puzzle.classList.add('is-complete');
    piece.disabled = true;
    piece.classList.remove('is-selected');
    selected = null;
    completed += 1;
    feedback.textContent = name + '! Figura encaixada.';
    speak(name);

    if (completed === puzzles.length) {
      feedback.textContent = 'Todas as figuras foram encaixadas. Muito bem!';
      window.registrarSessao?.(board.dataset.activityType, 'encaixou todas as figuras');
    }
  }

  pieces.forEach(piece => {
    piece.addEventListener('click', () => choosePiece(piece));
    piece.addEventListener('dragstart', event => {
      choosePiece(piece);
      event.dataTransfer.setData('text/plain', piece.dataset.piece);
      event.dataTransfer.effectAllowed = 'move';
    });
  });

  slots.forEach(slot => {
    slot.addEventListener('click', () => fitPiece(slot, selected));
    slot.addEventListener('dragover', event => {
      if (!slot.disabled) {
        event.preventDefault();
        slot.classList.add('is-over');
      }
    });
    slot.addEventListener('dragleave', () => slot.classList.remove('is-over'));
    slot.addEventListener('drop', event => {
      event.preventDefault();
      slot.classList.remove('is-over');
      const pieceId = event.dataTransfer.getData('text/plain');
      fitPiece(slot, pieces.find(piece => piece.dataset.piece === pieceId));
    });
  });

  document.getElementById('fit-reset').addEventListener('click', () => {
    selected = null;
    completed = 0;
    const shuffledSlots = shuffle(Object.keys(slotViews));
    puzzles.forEach((puzzle, index) => {
      const position = shuffledSlots[index];
      const viewBox = slotViews[position];
      puzzle.dataset.slot = position;
      puzzle.dataset.viewbox = viewBox;
      const slot = puzzle.querySelector('.missing-slot');
      slot.classList.remove('slot-tl', 'slot-tr', 'slot-bl', 'slot-br');
      slot.classList.add('slot-' + position);
      slot.querySelector('.slot-content').setAttribute('viewBox', viewBox);
      const piece = pieces.find(option => option.dataset.piece === puzzle.dataset.target);
      piece.querySelector('.piece-art').setAttribute('viewBox', viewBox);
    });
    const tray = document.getElementById('fit-pieces');
    shuffle(pieces).forEach(piece => tray.appendChild(piece));
    pieces.forEach(piece => {
      piece.disabled = false;
      piece.classList.remove('is-selected');
    });
    puzzles.forEach(puzzle => puzzle.classList.remove('is-complete'));
    slots.forEach(slot => {
      slot.disabled = false;
      slot.classList.remove('is-filled', 'is-over', 'fit-wrong');
    });
    feedback.textContent = 'Escolha uma peça para começar.';
  });
})();
