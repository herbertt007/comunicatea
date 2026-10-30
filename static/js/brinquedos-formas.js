(function () {
  'use strict';

  const root = document.getElementById('shapeGame');
  if (!root) return;

  const intro = document.getElementById('shapeIntro');
  const play = document.getElementById('shapePlay');
  const board = document.getElementById('shapeBoard');
  const tray = document.getElementById('shapeTray');
  const feedback = document.getElementById('shapeFeedback');
  const progressText = document.getElementById('shapeProgressText');
  const progressBar = document.getElementById('shapeProgressBar');
  const progressFill = document.getElementById('shapeProgressFill');
  const levelLabel = document.getElementById('shapeLevelLabel');
  const completePanel = document.getElementById('shapeComplete');
  const allPieces = Array.from(tray.querySelectorAll('.shape-piece'));
  const allSlots = Array.from(board.querySelectorAll('.shape-slot'));
  const levelNames = { 1: 'Nível 1 · Fácil', 2: 'Nível 2 · Intermediário', 3: 'Nível 3 · Avançado' };
  const levelShapes = {
    1: ['circulo', 'quadrado', 'triangulo'],
    2: ['circulo', 'quadrado', 'triangulo', 'retangulo', 'losango'],
    3: ['circulo', 'quadrado', 'triangulo', 'retangulo', 'losango', 'estrela', 'hexagono', 'oval'],
  };
  const praise = ['Muito bem!', 'Você conseguiu!', 'Parabéns!', 'Excelente trabalho!'];
  let currentLevel = 1;
  let activeShapes = levelShapes[currentLevel];
  let selectedPiece = null;
  let completed = 0;
  let started = false;
  let soundOn = true;
  let audioContext = null;
  let drag = null;
  let suppressClick = false;

  function shuffled(items) {
    const result = items.slice();
    for (let index = result.length - 1; index > 0; index -= 1) {
      const swapIndex = Math.floor(Math.random() * (index + 1));
      [result[index], result[swapIndex]] = [result[swapIndex], result[index]];
    }
    return result;
  }

  function updateLevelButtons() {
    document.querySelectorAll('.shape-level[data-level]').forEach((button) => {
      const active = Number(button.dataset.level) === currentLevel;
      button.classList.toggle('is-active', active);
      button.setAttribute('aria-pressed', String(active));
    });
  }

  function setLevel(level) {
    currentLevel = Number(level);
    activeShapes = levelShapes[currentLevel];
    updateLevelButtons();
    if (started) renderLevel();
  }

  function updateProgress() {
    const total = activeShapes.length;
    progressText.textContent = `${completed} de ${total} peças encaixadas`;
    progressBar.setAttribute('aria-valuemax', String(total));
    progressBar.setAttribute('aria-valuenow', String(completed));
    progressFill.style.width = `${(completed / total) * 100}%`;
  }

  function ensureAudio() {
    if (!soundOn) return null;
    const AudioContextClass = window.AudioContext || window.webkitAudioContext;
    if (!AudioContextClass) return null;
    if (!audioContext) audioContext = new AudioContextClass();
    if (audioContext.state === 'suspended') audioContext.resume().catch(() => {});
    return audioContext;
  }

  function playChime(finale) {
    const context = ensureAudio();
    if (!context) return;
    const notes = finale ? [523.25, 659.25, 783.99, 1046.5] : [659.25, 783.99];
    const startAt = context.currentTime;
    notes.forEach((frequency, index) => {
      const oscillator = context.createOscillator();
      const gain = context.createGain();
      oscillator.type = 'sine';
      oscillator.frequency.value = frequency;
      gain.gain.setValueAtTime(0.0001, startAt + index * 0.105);
      gain.gain.exponentialRampToValueAtTime(0.16, startAt + index * 0.105 + 0.025);
      gain.gain.exponentialRampToValueAtTime(0.0001, startAt + index * 0.105 + 0.26);
      oscillator.connect(gain);
      gain.connect(context.destination);
      oscillator.start(startAt + index * 0.105);
      oscillator.stop(startAt + index * 0.105 + 0.28);
    });
  }

  function selectPiece(piece) {
    if (!piece || piece.disabled || !started) return;
    selectedPiece = piece;
    allPieces.forEach((item) => item.classList.toggle('is-selected', item === piece));
    feedback.textContent = `${piece.querySelector('strong').textContent} escolhida. Encontre o espaço igual.`;
  }

  function placePiece(slot, piece) {
    if (!slot || !piece || slot.disabled || piece.disabled) return;
    if (slot.dataset.shape !== piece.dataset.shape) {
      slot.classList.remove('fit-wrong');
      void slot.offsetWidth;
      slot.classList.add('fit-wrong');
      feedback.textContent = 'Quase! Vamos tentar outra peça.';
      window.setTimeout(() => slot.classList.remove('fit-wrong'), 400);
      return;
    }

    slot.disabled = true;
    slot.classList.add('is-filled');
    slot.style.setProperty('--piece-color', piece.dataset.color);
    slot.setAttribute('aria-label', `${piece.querySelector('strong').textContent} encaixado`);
    piece.disabled = true;
    piece.classList.remove('is-selected');
    piece.classList.add('is-used');
    selectedPiece = null;
    completed += 1;
    updateProgress();
    const name = piece.querySelector('strong').textContent;
    feedback.textContent = `${praise[(completed - 1) % praise.length]} ${name} encaixado!`;
    playChime(false);

    if (window.registrarSessao) window.registrarSessao(root.dataset.activityType, `encaixou ${name}`);
    if (completed === activeShapes.length) {
      feedback.textContent = 'Excelente trabalho! Todas as formas encontraram seu lugar.';
      completePanel.hidden = false;
      completePanel.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
      playChime(true);
      if (window.registrarSessao) window.registrarSessao(root.dataset.activityType, 'concluiu o nível ' + currentLevel);
    }
  }

  function renderLevel() {
    started = true;
    completed = 0;
    selectedPiece = null;
    completePanel.hidden = true;
    intro.hidden = true;
    play.hidden = false;
    activeShapes = levelShapes[currentLevel];
    root.dataset.level = String(currentLevel);
    board.dataset.level = String(currentLevel);
    levelLabel.textContent = levelNames[currentLevel];
    allPieces.forEach((piece) => {
      const active = activeShapes.includes(piece.dataset.shape);
      piece.hidden = !active;
      piece.disabled = false;
      piece.classList.remove('is-used', 'is-selected');
    });
    allSlots.forEach((slot) => {
      const active = activeShapes.includes(slot.dataset.shape);
      slot.hidden = !active;
      slot.disabled = false;
      slot.classList.remove('is-filled', 'is-over', 'fit-wrong');
      slot.style.removeProperty('--piece-color');
      const name = slot.querySelector('.shape-slot__name').textContent;
      slot.setAttribute('aria-label', `Espaço da forma: ${name}`);
    });
    shuffled(activeShapes)
      .map((shape) => allSlots.find((slot) => slot.dataset.shape === shape))
      .forEach((slot) => board.appendChild(slot));
    shuffled(activeShapes)
      .map((shape) => allPieces.find((piece) => piece.dataset.shape === shape))
      .forEach((piece) => tray.appendChild(piece));
    feedback.textContent = 'Escolha uma peça para começar.';
    updateProgress();
  }

  function startDrag(event, piece) {
    if (!started || piece.disabled || event.button > 0) return;
    selectedPiece = piece;
    allPieces.forEach((item) => item.classList.toggle('is-selected', item === piece));
    drag = { piece, pointerId: event.pointerId, startX: event.clientX, startY: event.clientY, ghost: null, moved: false };
    piece.setPointerCapture?.(event.pointerId);
  }

  function moveDrag(event) {
    if (!drag || event.pointerId !== drag.pointerId) return;
    const distance = Math.hypot(event.clientX - drag.startX, event.clientY - drag.startY);
    if (!drag.moved && distance < 8) return;
    drag.moved = true;
    event.preventDefault();
    if (!drag.ghost) {
      drag.ghost = drag.piece.cloneNode(true);
      drag.ghost.removeAttribute('id');
      drag.ghost.disabled = true;
      drag.ghost.classList.remove('is-selected', 'is-used');
      drag.ghost.classList.add('shape-drag-ghost');
      drag.ghost.style.width = `${drag.piece.getBoundingClientRect().width}px`;
      document.body.appendChild(drag.ghost);
      drag.piece.classList.add('is-selected');
    }
    drag.ghost.style.left = `${event.clientX}px`;
    drag.ghost.style.top = `${event.clientY}px`;
    allSlots.forEach((slot) => slot.classList.remove('is-over'));
    const target = document.elementFromPoint(event.clientX, event.clientY)?.closest('.shape-slot');
    if (target && !target.disabled && !target.hidden) target.classList.add('is-over');
  }

  function endDrag(event) {
    if (!drag || event.pointerId !== drag.pointerId) return;
    const current = drag;
    drag = null;
    allSlots.forEach((slot) => slot.classList.remove('is-over'));
    if (!current.moved) {
      current.ghost?.remove();
      return;
    }
    suppressClick = true;
    window.setTimeout(() => { suppressClick = false; }, 0);
    const target = document.elementFromPoint(event.clientX, event.clientY)?.closest('.shape-slot');
    const correctTarget = target && !target.disabled && !target.hidden && target.dataset.shape === current.piece.dataset.shape;
    if (correctTarget) {
      current.ghost?.remove();
      placePiece(target, current.piece);
    } else {
      if (target && !target.disabled && !target.hidden) placePiece(target, current.piece);
      else feedback.textContent = 'A peça voltou para a bandeja. Tente outro espaço.';
      if (current.ghost) {
        const rect = current.piece.getBoundingClientRect();
        current.ghost.style.transition = 'left .22s ease, top .22s ease, transform .22s ease, opacity .22s ease';
        current.ghost.style.left = `${rect.left + rect.width / 2}px`;
        current.ghost.style.top = `${rect.top + rect.height / 2}px`;
        current.ghost.style.transform = 'translate(-50%, -50%) scale(.65)';
        current.ghost.style.opacity = '.15';
        window.setTimeout(() => current.ghost?.remove(), 230);
      }
    }
  }

  allPieces.forEach((piece) => {
    piece.addEventListener('pointerdown', (event) => startDrag(event, piece));
    piece.addEventListener('pointermove', moveDrag);
    piece.addEventListener('pointerup', endDrag);
    piece.addEventListener('pointercancel', endDrag);
    piece.addEventListener('click', () => {
      if (!suppressClick && started) selectPiece(piece);
    });
  });

  allSlots.forEach((slot) => {
    slot.addEventListener('click', () => {
      if (selectedPiece) placePiece(slot, selectedPiece);
    });
  });

  document.querySelectorAll('.shape-level[data-level]').forEach((button) => {
    button.addEventListener('click', () => setLevel(button.dataset.level));
  });

  document.getElementById('shapeStart').addEventListener('click', () => {
    ensureAudio();
    renderLevel();
  });
  document.getElementById('shapeReset').addEventListener('click', renderLevel);
  document.getElementById('shapePlayAgain').addEventListener('click', renderLevel);
  document.getElementById('shapeSound').addEventListener('click', (event) => {
    soundOn = !soundOn;
    event.currentTarget.setAttribute('aria-pressed', String(soundOn));
    event.currentTarget.textContent = soundOn ? '🔊 Som ligado' : '🔇 Som desligado';
    if (soundOn) ensureAudio();
  });

  updateLevelButtons();
})();
