from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json
from estudantes.models import Estudante
from .models import Atividade, SessaoAtividade
from comunicacao.models import Pictograma, CategoriaPictograma


def lista(request):
    atividades = Atividade.objects.filter(ativo=True)
    return render(request, 'atividades/lista.html', {'atividades': atividades})


def sentimentos(request):
    atividade = Atividade.objects.filter(tipo='sentimentos', ativo=True).first()
    cartoes = [
        {'emoji': '😊', 'label': 'Feliz', 'mensagem': 'Estou me sentindo feliz!', 'cor': '#FBBF24'},
        {'emoji': '😢', 'label': 'Triste', 'mensagem': 'Estou me sentindo triste.', 'cor': '#60A5FA'},
        {'emoji': '😨', 'label': 'Com medo', 'mensagem': 'Estou com medo.', 'cor': '#A78BFA'},
        {'emoji': '😠', 'label': 'Com raiva', 'mensagem': 'Estou com raiva.', 'cor': '#F87171'},
        {'emoji': '😴', 'label': 'Cansado', 'mensagem': 'Estou cansado.', 'cor': '#94A3B8'},
        {'emoji': '😌', 'label': 'Calmo', 'mensagem': 'Estou me sentindo calmo.', 'cor': '#34D399'},
        {'emoji': '😰', 'label': 'Ansioso', 'mensagem': 'Estou ansioso.', 'cor': '#FB923C'},
        {'emoji': '🤩', 'label': 'Animado', 'mensagem': 'Estou animado!', 'cor': '#F472B6'},
        {'emoji': '🤔', 'label': 'Não sei', 'mensagem': 'Não sei como estou me sentindo.', 'cor': '#9CA3AF'},
        {'emoji': '🙊', 'label': 'Prefiro não dizer', 'mensagem': 'Prefiro não responder.', 'cor': '#D1D5DB'},
    ]
    return render(request, 'atividades/sentimentos.html', {'cartoes': cartoes, 'atividade': atividade})


def necessidades(request):
    atividade = Atividade.objects.filter(tipo='necessidades', ativo=True).first()
    cartoes = [
        {'emoji': '💧', 'label': 'Água', 'mensagem': 'Quero água.', 'cor': '#38BDF8'},
        {'emoji': '🍎', 'label': 'Comer', 'mensagem': 'Quero comer.', 'cor': '#4ADE80'},
        {'emoji': '🙋', 'label': 'Ajuda', 'mensagem': 'Preciso de ajuda.', 'cor': '#FBBF24'},
        {'emoji': '😴', 'label': 'Descansar', 'mensagem': 'Quero descansar.', 'cor': '#94A3B8'},
        {'emoji': '🚻', 'label': 'Banheiro', 'mensagem': 'Preciso ir ao banheiro.', 'cor': '#60A5FA'},
        {'emoji': '⏸️', 'label': 'Pausa', 'mensagem': 'Quero fazer uma pausa.', 'cor': '#A78BFA'},
        {'emoji': '🤕', 'label': 'Dor', 'mensagem': 'Estou com dor.', 'cor': '#F87171'},
        {'emoji': '🔄', 'label': 'Outra opção', 'mensagem': 'Quero outra opção.', 'cor': '#FB923C'},
    ]
    return render(request, 'atividades/necessidades.html', {'cartoes': cartoes, 'atividade': atividade})


def monte_frase(request):
    atividade = Atividade.objects.filter(tipo='monte_frase', ativo=True).first()
    sujeitos = [
        {'emoji': '🙋', 'label': 'Eu', 'palavra': 'Eu'},
    ]
    verbos = [
        {'emoji': '💚', 'label': 'Quero', 'palavra': 'quero'},
        {'emoji': '😊', 'label': 'Gosto', 'palavra': 'gosto de'},
        {'emoji': '✋', 'label': 'Não quero', 'palavra': 'não quero'},
        {'emoji': '🙏', 'label': 'Preciso', 'palavra': 'preciso de'},
    ]
    complementos = [
        {'emoji': '💧', 'label': 'Água', 'palavra': 'água'},
        {'emoji': '🍎', 'label': 'Comer', 'palavra': 'comer'},
        {'emoji': '🎮', 'label': 'Brincar', 'palavra': 'brincar'},
        {'emoji': '😴', 'label': 'Descansar', 'palavra': 'descansar'},
        {'emoji': '🙋', 'label': 'Ajuda', 'palavra': 'ajuda'},
        {'emoji': '📚', 'label': 'Estudar', 'palavra': 'estudar'},
        {'emoji': '🎵', 'label': 'Música', 'palavra': 'música'},
        {'emoji': '🏃', 'label': 'Sair', 'palavra': 'sair'},
    ]
    return render(request, 'atividades/monte_frase.html', {
        'sujeitos': sujeitos, 'verbos': verbos,
        'complementos': complementos, 'atividade': atividade
    })


def escolha(request):
    atividade = Atividade.objects.filter(tipo='escolha', ativo=True).first()
    pares = [
        {'opt1': {'emoji': '✏️', 'label': 'Desenhar'}, 'opt2': {'emoji': '🎨', 'label': 'Pintar'}},
        {'opt1': {'emoji': '📖', 'label': 'Ouvir história'}, 'opt2': {'emoji': '🎵', 'label': 'Ouvir música'}},
        {'opt1': {'emoji': '🎮', 'label': 'Brincar'}, 'opt2': {'emoji': '😴', 'label': 'Descansar'}},
        {'opt1': {'emoji': '🧩', 'label': 'Montar quebra-cabeça'}, 'opt2': {'emoji': '🖍️', 'label': 'Colorir'}},
    ]
    return render(request, 'atividades/escolha.html', {'pares': pares, 'atividade': atividade})


def encontre(request):
    atividade = Atividade.objects.filter(tipo='encontre', ativo=True).first()
    rodadas = [
        {
            'instrucao': 'Encontre a ÁGUA',
            'alvo': 'Água',
            'cartoes': [
                {'emoji': '💧', 'label': 'Água', 'correto': True},
                {'emoji': '🍎', 'label': 'Maçã', 'correto': False},
                {'emoji': '🐶', 'label': 'Cachorro', 'correto': False},
                {'emoji': '🏠', 'label': 'Casa', 'correto': False},
            ]
        },
        {
            'instrucao': 'Encontre o GATO',
            'alvo': 'Gato',
            'cartoes': [
                {'emoji': '🐶', 'label': 'Cachorro', 'correto': False},
                {'emoji': '🐱', 'label': 'Gato', 'correto': True},
                {'emoji': '💧', 'label': 'Água', 'correto': False},
                {'emoji': '🍎', 'label': 'Maçã', 'correto': False},
            ]
        },
        {
            'instrucao': 'Encontre a ESCOLA',
            'alvo': 'Escola',
            'cartoes': [
                {'emoji': '🏠', 'label': 'Casa', 'correto': False},
                {'emoji': '🏥', 'label': 'Hospital', 'correto': False},
                {'emoji': '🏫', 'label': 'Escola', 'correto': True},
                {'emoji': '🌳', 'label': 'Árvore', 'correto': False},
            ]
        },
    ]
    import json
    return render(request, 'atividades/encontre.html', {
        'rodadas_json': json.dumps(rodadas, ensure_ascii=False),
        'atividade': atividade
    })


def rotina(request):
    atividade = Atividade.objects.filter(tipo='rotina', ativo=True).first()
    etapas_padrao = [
        {'emoji': '⏰', 'label': 'Acordar'},
        {'emoji': '🪥', 'label': 'Escovar os dentes'},
        {'emoji': '🍳', 'label': 'Tomar café da manhã'},
        {'emoji': '👕', 'label': 'Se vestir'},
        {'emoji': '🎒', 'label': 'Pegar a mochila'},
        {'emoji': '📚', 'label': 'Estudar'},
        {'emoji': '🍽️', 'label': 'Almoçar'},
        {'emoji': '🎮', 'label': 'Brincar'},
        {'emoji': '😴', 'label': 'Descansar'},
    ]
    import json
    return render(request, 'atividades/rotina.html', {
        'etapas_json': json.dumps(etapas_padrao, ensure_ascii=False),
        'atividade': atividade
    })


def sim_nao(request):
    atividade = Atividade.objects.filter(tipo='sim_nao', ativo=True).first()
    perguntas = [
        'Você quer brincar?',
        'Você gostaria de ouvir uma história?',
        'Você quer fazer uma pausa?',
        'Você quer ajuda?',
        'Você quer continuar ou prefere parar?',
    ]
    cartoes = [
        {'emoji': '✅', 'label': 'Sim', 'cor': '#4ADE80'},
        {'emoji': '❌', 'label': 'Não', 'cor': '#F87171'},
        {'emoji': '🤔', 'label': 'Talvez', 'cor': '#FBBF24'},
        {'emoji': '❓', 'label': 'Não sei', 'cor': '#94A3B8'},
        {'emoji': '🔄', 'label': 'Outra opção', 'cor': '#60A5FA'},
    ]
    import json
    return render(request, 'atividades/sim_nao.html', {
        'perguntas_json': json.dumps(perguntas, ensure_ascii=False),
        'cartoes': cartoes,
        'atividade': atividade
    })


def objeto_acao(request):
    atividade = Atividade.objects.filter(tipo='objeto_acao', ativo=True).first()
    rodadas = [
        {
            'situacao': 'O que pode ajudar a escovar os dentes?',
            'opcoes': [
                {'emoji': '🦷', 'nome': 'Escova de dentes', 'correta': True},
                {'emoji': '⚽', 'nome': 'Bola', 'correta': False},
                {'emoji': '📖', 'nome': 'Livro', 'correta': False},
            ],
        },
        {
            'situacao': 'O que pode ajudar a tomar água?',
            'opcoes': [
                {'emoji': '🥤', 'nome': 'Copo', 'correta': True},
                {'emoji': '🧸', 'nome': 'Brinquedo', 'correta': False},
                {'emoji': '🧦', 'nome': 'Meia', 'correta': False},
            ],
        },
        {
            'situacao': 'O que pode ajudar a lavar as mãos?',
            'opcoes': [
                {'emoji': '🧼', 'nome': 'Sabonete', 'correta': True},
                {'emoji': '🎈', 'nome': 'Balão', 'correta': False},
                {'emoji': '✏️', 'nome': 'Lápis', 'correta': False},
            ],
        },
        {
            'situacao': 'O que pode ajudar a desenhar?',
            'opcoes': [
                {'emoji': '🖍️', 'nome': 'Giz de cera', 'correta': True},
                {'emoji': '🍽️', 'nome': 'Prato', 'correta': False},
                {'emoji': '🦷', 'nome': 'Escova de dentes', 'correta': False},
            ],
        },
    ]
    return render(request, 'atividades/objeto_acao.html', {
        'rodadas_json': json.dumps(rodadas, ensure_ascii=False),
        'atividade': atividade,
    })


def frutas_sombras(request):
    atividade = Atividade.objects.filter(tipo='frutas_sombras', ativo=True).first()
    frutas = [
        {'id': 'maca', 'nome': 'Maçã', 'emoji': '🍎'},
        {'id': 'melancia', 'nome': 'Melancia', 'emoji': '🍉'},
        {'id': 'mamao', 'nome': 'Mamão', 'emoji': '🥭'},
        {'id': 'cereja', 'nome': 'Cereja', 'emoji': '🍒'},
        {'id': 'banana', 'nome': 'Banana', 'emoji': '🍌'},
    ]
    return render(request, 'atividades/associacao_sombras.html', {
        'atividade': atividade,
        'itens': frutas,
        'titulo': 'Leve cada fruta até a sua sombra',
        'instrucao': 'Arraste uma fruta para a sombra igual. Você também pode tocar em uma fruta e depois na sombra.',
        'nome_coluna': 'Frutas',
        'nome_alvo': 'Sombras',
        'singular': 'fruta',
        'plural': 'frutas',
        'tipo': 'frutas_sombras',
    })


def animais_sombras(request):
    atividade = Atividade.objects.filter(tipo='animais_sombras', ativo=True).first()
    animais = [
        {'id': 'gato', 'nome': 'Gato', 'emoji': '🐱'},
        {'id': 'cachorro', 'nome': 'Cachorro', 'emoji': '🐶'},
        {'id': 'elefante', 'nome': 'Elefante', 'emoji': '🐘'},
        {'id': 'girafa', 'nome': 'Girafa', 'emoji': '🦒'},
        {'id': 'peixe', 'nome': 'Peixe', 'emoji': '🐟'},
    ]
    return render(request, 'atividades/associacao_sombras.html', {
        'atividade': atividade,
        'itens': animais,
        'titulo': 'Leve cada animal até a sua sombra',
        'instrucao': 'Arraste um animal para a sombra igual. Você também pode tocar em um animal e depois na sombra.',
        'nome_coluna': 'Animais',
        'nome_alvo': 'Sombras',
        'singular': 'animal',
        'plural': 'animais',
        'tipo': 'animais_sombras',
    })


def _encaixe_figuras(request, tipo):
    temas = {
        'encaixe_animais': {
            'atividade': 'encaixe_animais',
            'titulo': 'Encaixe as figuras: animais',
            'descricao': 'Encontre a peça que completa cada figura. Ao encaixar, você ouvirá o nome dela.',
            'itens': [
                {'id': 'casa', 'nome': 'Casa', 'slot': 'tl', 'viewbox': '0 0 50 50'},
                {'id': 'borboleta', 'nome': 'Borboleta', 'slot': 'br', 'viewbox': '50 50 50 50'},
                {'id': 'caracol', 'nome': 'Caracol', 'slot': 'bl', 'viewbox': '0 50 50 50'},
                {'id': 'sol', 'nome': 'Sol', 'slot': 'tr', 'viewbox': '50 0 50 50'},
            ],
        },
        'encaixe_natureza': {
            'atividade': 'encaixe_natureza',
            'titulo': 'Encaixe as figuras: natureza',
            'descricao': 'Complete cada figura da natureza. Ao encaixar, você ouvirá o nome da figura.',
            'itens': [
                {'id': 'flor', 'nome': 'Flor', 'slot': 'tr', 'viewbox': '50 0 50 50'},
                {'id': 'arvore', 'nome': 'Árvore', 'slot': 'bl', 'viewbox': '0 50 50 50'},
                {'id': 'nuvem', 'nome': 'Nuvem', 'slot': 'tl', 'viewbox': '0 0 50 50'},
                {'id': 'arco-iris', 'nome': 'Arco-íris', 'slot': 'br', 'viewbox': '50 50 50 50'},
            ],
        },
    }
    dados = temas[tipo]
    dados['atividade_obj'] = Atividade.objects.filter(tipo=tipo, ativo=True).first()
    return render(request, 'atividades/encaixe_figuras.html', dados)


def encaixe_animais(request):
    return _encaixe_figuras(request, 'encaixe_animais')


def encaixe_natureza(request):
    return _encaixe_figuras(request, 'encaixe_natureza')


@require_POST
def registrar_sessao(request):
    """Endpoint AJAX para registrar uma sessão de atividade."""
    try:
        data = json.loads(request.body)
        if not isinstance(data, dict):
            return JsonResponse({'ok': False, 'erro': 'Dados inválidos.'}, status=400)
        atividade_tipo = data.get('tipo')
        atividade = Atividade.objects.filter(tipo=atividade_tipo, ativo=True).first()
        if not atividade:
            return JsonResponse({'ok': False, 'erro': 'Atividade indisponível.'}, status=404)

        sessao = SessaoAtividade(atividade=atividade)
        if request.user.is_authenticated:
            sessao.professor = request.user
            estudante_id = data.get('estudante_id')
            if estudante_id:
                sessao.estudante = Estudante.objects.get(
                    pk=estudante_id, professor=request.user, ativo=True
                )
        sessao.tipo_interacao = str(data.get('interacao', ''))[:200]
        sessao.save()
        return JsonResponse({'ok': True, 'sessao_id': sessao.pk})
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse({'ok': False, 'erro': 'JSON inválido.'}, status=400)
    except Estudante.DoesNotExist:
        return JsonResponse({'ok': False, 'erro': 'Estudante indisponível.'}, status=404)
