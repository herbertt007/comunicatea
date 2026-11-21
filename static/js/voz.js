/**
 * ComunicaTEA — voz.js
 * Mantém a voz feminina pt-BR padronizada em todo o ComunicaTEA.
 * Suporta mobile (iOS/Android) com desbloqueio no primeiro toque,
 * reprodução de áudio compartilhado e síntese via SpeechSynthesis robusta.
 */
(function () {
  'use strict';

  const synth = window.speechSynthesis;
  const audioBase = '/static/audio/voz/pt-br-francisca/';
  const sintetizarUrl = '/voz/sintetizar/?texto=';

  // 18 palavras frequentes pré-gravadas na voz Francisca
  const audios = {
    casa: 'casa', borboleta: 'borboleta', caracol: 'caracol', sol: 'sol',
    flor: 'flor', arvore: 'arvore', nuvem: 'nuvem', 'arco-iris': 'arco-iris',
    maca: 'maca', melancia: 'melancia', mamao: 'mamao', cereja: 'cereja', banana: 'banana',
    gato: 'gato', cachorro: 'cachorro', elefante: 'elefante', girafa: 'girafa', peixe: 'peixe'
  };

  let sharedAudio = null;
  let audioUnlocked = false;
  let vozPt = null;

  function getSharedAudio() {
    if (!sharedAudio) {
      sharedAudio = new Audio();
      sharedAudio.preload = 'auto';
    }
    return sharedAudio;
  }

  /**
   * Desbloqueia o subsistema de áudio nos navegadores móveis (iOS Safari / Android Chrome)
   * através do primeiro gesto explícito do usuário na página.
   */
  function desbloquearAudioMobile() {
    if (audioUnlocked) return;
    audioUnlocked = true;

    // 1. Desbloqueia elemento de áudio com buffer silencioso WAV (1 amostra)
    try {
      const audio = getSharedAudio();
      audio.src = 'data:audio/wav;base64,UklGRigAAABXQVZFZm10IBIAAAABAAEARKwAAIhYAQACABAAAABkYXRhAgAAAAEA';
      const playPromise = audio.play();
      if (playPromise !== undefined) {
        playPromise.then(() => {
          audio.pause();
          audio.currentTime = 0;
        }).catch(() => {});
      }
    } catch (e) {}

    // 2. Desbloqueia a API Web Speech
    if (synth) {
      try {
        const dummy = new SpeechSynthesisUtterance('');
        dummy.volume = 0;
        synth.speak(dummy);
      } catch (e) {}
    }

    carregarVoz();
  }

  // Escuta os primeiros eventos de toque/clique para desbloquear áudio imediatamente
  ['touchstart', 'touchend', 'pointerdown', 'mousedown', 'click'].forEach(evt => {
    document.addEventListener(evt, desbloquearAudioMobile, { once: true, passive: true });
  });

  function normalizarTexto(texto) {
    return String(texto || '').trim().replace(/[.!?…]+$/u, '')
      .normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase();
  }

  function carregarVoz() {
    if (!synth) return null;
    const vozes = synth.getVoices() || [];
    if (!vozes.length) return vozPt;

    const ptBrasil = vozes.filter(v => {
      const lang = (v.lang || '').toLowerCase().replace('_', '-');
      return lang === 'pt-br' || lang.startsWith('pt');
    });

    // 1. Procura vozes femininas brasileiras
    const vozFemininaPt = ptBrasil.filter(v =>
      /francisca|maria|luciana|fernanda|camila|bruna|juliana|beatriz|monica|ana\b|leticia|female|feminina/i.test(v.name)
    );

    vozPt = vozFemininaPt.find(v => /natural|online|enhanced|premium/i.test(v.name)) ||
            vozFemininaPt[0] ||
            ptBrasil.find(v => /natural|online|enhanced|premium/i.test(v.name)) ||
            ptBrasil[0] ||
            vozes[0] || null;

    return vozPt;
  }

  if (synth && synth.onvoiceschanged !== undefined) {
    synth.onvoiceschanged = carregarVoz;
  }
  carregarVoz();

  function pararAudio() {
    if (sharedAudio) {
      try {
        sharedAudio.pause();
        sharedAudio.currentTime = 0;
      } catch (e) {}
    }
  }

  function falarComNavegador(texto, velocidade) {
    if (!synth) return;
    try {
      synth.cancel();
      if (synth.paused) synth.resume();

      const utterance = new SpeechSynthesisUtterance(texto);
      utterance.lang = 'pt-BR';
      utterance.rate = velocidade || 0.88;
      utterance.pitch = 1.05;
      utterance.volume = 1;

      const voz = carregarVoz() || vozPt;
      if (voz) utterance.voice = voz;

      // Proteção contra garbage collection antecipado em navegadores Android
      window._cteaUtterance = utterance;
      utterance.onend = () => { window._cteaUtterance = null; };
      utterance.onerror = () => { window._cteaUtterance = null; };

      synth.speak(utterance);
    } catch (e) {
      console.warn('Erro na síntese do navegador:', e);
    }
  }

  function tocarAudio(url, texto, velocidade) {
    const audio = getSharedAudio();
    let fallbackUsado = false;

    const fallback = () => {
      if (fallbackUsado) return;
      fallbackUsado = true;
      falarComNavegador(texto, velocidade);
    };

    audio.onended = () => {
      audio.onended = null;
      audio.onerror = null;
    };

    audio.onerror = () => {
      audio.onended = null;
      audio.onerror = null;
      fallback();
    };

    try {
      audio.src = url;
      audio.currentTime = 0;
      const playPromise = audio.play();
      if (playPromise !== undefined) {
        playPromise.catch(() => fallback());
      }
    } catch (e) {
      fallback();
    }
  }

  window.falarTexto = function (texto, velocidade) {
    if (!texto) return;
    const strTexto = String(texto).trim();
    if (!strTexto) return;

    desbloquearAudioMobile();
    window.atualizarFalaLibras?.(strTexto);

    if (synth) synth.cancel();
    pararAudio();

    // 1. Checa se é uma das palavras com gravação estática
    const chave = normalizarTexto(strTexto);
    const arquivo = audios[chave];
    if (arquivo) {
      tocarAudio(audioBase + arquivo + '.mp3', strTexto, velocidade);
      return;
    }

    // 2. Tenta síntese neural Francisca no servidor (compatível com Vercel /tmp)
    tocarAudio(sintetizarUrl + encodeURIComponent(strTexto), strTexto, velocidade);
  };

  window.pararVoz = function () {
    if (synth) synth.cancel();
    pararAudio();
  };
})();
