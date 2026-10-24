/**
 * ComunicaTEA — voz.js
 * Mantém a voz feminina pt-BR em todo o ComunicaTEA.
 * Usa gravações locais para vocabulário frequente e sintetiza qualquer outra fala com a mesma voz.
 */
(function () {
  'use strict';

  const synth = window.speechSynthesis;
  const audioBase = '/static/audio/voz/pt-br-francisca/';
  const sintetizarUrl = '/voz/sintetizar/?texto=';
  const audios = {
    casa: 'casa', borboleta: 'borboleta', caracol: 'caracol', sol: 'sol',
    flor: 'flor', arvore: 'arvore', nuvem: 'nuvem', 'arco-iris': 'arco-iris',
    maca: 'maca', melancia: 'melancia', mamao: 'mamao', cereja: 'cereja', banana: 'banana',
    gato: 'gato', cachorro: 'cachorro', elefante: 'elefante', girafa: 'girafa', peixe: 'peixe'
  };
  let vozPt = null;
  let audioAtual = null;

  function carregarVoz() {
    if (!synth) return;
    const vozes = synth.getVoices();
    const portuguesBrasil = vozes.filter(v => v.lang.toLowerCase() === 'pt-br');
    const vozFemininaPt = portuguesBrasil.filter(v => /francisca|maria|luciana|fernanda|camila|bruna|juliana|beatriz|monica|ana\b|female|feminina/i.test(v.name));
    vozPt = vozFemininaPt.find(v => /natural|online|enhanced|premium/i.test(v.name)) ||
            vozFemininaPt[0] ||
            portuguesBrasil.find(v => /natural|online|enhanced|premium/i.test(v.name)) ||
            portuguesBrasil[0] || null;
  }

  if (synth && synth.onvoiceschanged !== undefined) synth.onvoiceschanged = carregarVoz;
  carregarVoz();

  function pararAudio() {
    if (audioAtual) {
      audioAtual.pause();
      audioAtual.currentTime = 0;
      audioAtual = null;
    }
  }

  function falarComNavegador(texto, velocidade) {
    if (!synth) return;
    const utterance = new SpeechSynthesisUtterance(texto);
    utterance.lang = 'pt-BR';
    utterance.rate = velocidade || 0.86;
    utterance.pitch = 1.08;
    utterance.volume = 1;
    if (vozPt) utterance.voice = vozPt;
    synth.speak(utterance);
  }

  function tocarAudio(url, texto, velocidade) {
    const audio = new Audio(url);
    audio.volume = 1;
    audioAtual = audio;
    let fallbackUsado = false;
    const fallback = () => {
      if (fallbackUsado) return;
      fallbackUsado = true;
      if (audioAtual === audio) audioAtual = null;
      falarComNavegador(texto, velocidade);
    };
    audio.addEventListener('ended', () => {
      if (audioAtual === audio) audioAtual = null;
    }, { once: true });
    audio.addEventListener('error', fallback, { once: true });
    audio.play().catch(fallback);
  }

  window.falarTexto = function (texto, velocidade) {
    if (!texto) return;
    window.atualizarFalaLibras?.(String(texto));
    if (synth) synth.cancel();
    pararAudio();

    const chave = String(texto).trim().replace(/[.!?…]+$/u, '')
      .normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase();
    const arquivo = audios[chave];
    if (arquivo) {
      tocarAudio(audioBase + arquivo + '.mp3', texto, velocidade);
      return;
    }

    tocarAudio(sintetizarUrl + encodeURIComponent(String(texto)), texto, velocidade);
  };

  window.pararVoz = function () {
    if (synth) synth.cancel();
    pararAudio();
  };
})();
