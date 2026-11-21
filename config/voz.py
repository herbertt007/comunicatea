"""Síntese sob demanda com a voz feminina brasileira usada no ComunicaTEA."""
import asyncio
import hashlib
import os
import tempfile
from pathlib import Path

from django.conf import settings
from django.core.cache import cache
from django.http import FileResponse, HttpResponse, HttpResponseBadRequest


MAX_TEXTO = 300
VOZ = 'pt-BR-FranciscaNeural'


async def _gerar_audio(texto):
    import edge_tts

    comunicacao = edge_tts.Communicate(
        texto,
        voice=VOZ,
        rate='+0%',
        volume='+15%',
        pitch='+0Hz',
    )
    audio = bytearray()
    async for parte in comunicacao.stream():
        if parte['type'] == 'audio':
            audio.extend(parte['data'])
    if not audio:
        raise RuntimeError('A síntese não retornou áudio.')
    return bytes(audio)


async def sintetizar_voz(request):
    if request.method != 'GET':
        return HttpResponse(status=405)

    texto = ' '.join(request.GET.get('texto', '').split())
    if not texto or len(texto) > MAX_TEXTO:
        return HttpResponseBadRequest('Informe um texto de até 300 caracteres.')

    ip = request.META.get('REMOTE_ADDR', 'desconhecido')
    chave_ip = hashlib.sha256(ip.encode('utf-8')).hexdigest()[:20]
    chave_limite = f'voz-limite:{chave_ip}'
    cache.add(chave_limite, 0, timeout=60)
    if cache.incr(chave_limite) > 60:
        return HttpResponse('Limite temporário de falas atingido.', status=429)

    chave_audio = hashlib.sha256((VOZ + '\0' + texto).encode('utf-8')).hexdigest()
    # Usar tempfile garante escrita mesmo em ambientes serverless como a Vercel (/tmp)
    diretorio = Path(tempfile.gettempdir()) / 'comunicatea-voz-cache'
    caminho = diretorio / f'{chave_audio}.mp3'

    if caminho.is_file():
        try:
            resposta = FileResponse(caminho.open('rb'), content_type='audio/mpeg')
            resposta['Cache-Control'] = 'public, max-age=604800, immutable'
            resposta['Accept-Ranges'] = 'bytes'
            return resposta
        except Exception:
            pass

    try:
        conteudo = await _gerar_audio(texto)
    except Exception:
        return HttpResponse('Não foi possível gerar a voz agora.', status=503)

    try:
        diretorio.mkdir(parents=True, exist_ok=True)
        temporario = diretorio / f'{chave_audio}.{os.getpid()}.tmp'
        temporario.write_bytes(conteudo)
        os.replace(temporario, caminho)
        resposta = FileResponse(caminho.open('rb'), content_type='audio/mpeg')
    except Exception:
        # Se o sistema de arquivos falhar, responde diretamente com o conteúdo em memória
        resposta = HttpResponse(conteudo, content_type='audio/mpeg')

    resposta['Cache-Control'] = 'public, max-age=604800, immutable'
    resposta['Accept-Ranges'] = 'bytes'
    return resposta
