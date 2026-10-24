"""
Comando de gerenciamento para popular o banco de dados com dados iniciais.
Execute: python manage.py seed_data
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Popula o banco de dados com dados iniciais do ComunicaTEA'

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING('=== ComunicaTEA — Seed Data ==='))

        # ── 1. Categorias de Pictogramas ──────────────────────────────────
        from comunicacao.models import CategoriaPictograma, Pictograma
        categorias_data = [
            {'nome': 'Emoções', 'icone': '😊', 'cor': '#FF6B6B', 'ordem': 1},
            {'nome': 'Necessidades', 'icone': '🙋', 'cor': '#38BDF8', 'ordem': 2},
            {'nome': 'Alimentação', 'icone': '🍎', 'cor': '#4ADE80', 'ordem': 3},
            {'nome': 'Ações', 'icone': '🏃', 'cor': '#A78BFA', 'ordem': 4},
            {'nome': 'Pessoas', 'icone': '👨‍👩‍👧', 'cor': '#F472B6', 'ordem': 5},
            {'nome': 'Lugares', 'icone': '🏫', 'cor': '#FB923C', 'ordem': 6},
            {'nome': 'Rotina Escolar', 'icone': '📚', 'cor': '#34D399', 'ordem': 7},
        ]
        cats = {}
        for d in categorias_data:
            cat, created = CategoriaPictograma.objects.get_or_create(
                nome=d['nome'], defaults={**d}
            )
            cats[d['nome']] = cat
            if created:
                self.stdout.write(f'  ✅ Categoria criada: {d["icone"]} {d["nome"]}')

        # ── 2. Pictogramas ────────────────────────────────────────────────
        pictogramas_data = [
            # Emoções
            {'nome': 'Feliz', 'emoji': '😊', 'palavra': 'Feliz', 'cat': 'Emoções', 'alt': 'Rosto feliz sorrindo'},
            {'nome': 'Triste', 'emoji': '😢', 'palavra': 'Triste', 'cat': 'Emoções', 'alt': 'Rosto triste'},
            {'nome': 'Com medo', 'emoji': '😨', 'palavra': 'Com medo', 'cat': 'Emoções', 'alt': 'Rosto com expressão de medo'},
            {'nome': 'Com raiva', 'emoji': '😠', 'palavra': 'Com raiva', 'cat': 'Emoções', 'alt': 'Rosto irritado'},
            {'nome': 'Cansado', 'emoji': '😴', 'palavra': 'Cansado', 'cat': 'Emoções', 'alt': 'Rosto cansado com olhos fechados'},
            {'nome': 'Calmo', 'emoji': '😌', 'palavra': 'Calmo', 'cat': 'Emoções', 'alt': 'Rosto tranquilo'},
            {'nome': 'Ansioso', 'emoji': '😰', 'palavra': 'Ansioso', 'cat': 'Emoções', 'alt': 'Rosto ansioso'},
            {'nome': 'Animado', 'emoji': '🤩', 'palavra': 'Animado', 'cat': 'Emoções', 'alt': 'Rosto animado com estrelas'},
            # Necessidades
            {'nome': 'Água', 'emoji': '💧', 'palavra': 'Quero água', 'cat': 'Necessidades', 'alt': 'Gota de água'},
            {'nome': 'Ajuda', 'emoji': '🙋', 'palavra': 'Preciso de ajuda', 'cat': 'Necessidades', 'alt': 'Pessoa levantando a mão'},
            {'nome': 'Descanso', 'emoji': '😴', 'palavra': 'Quero descansar', 'cat': 'Necessidades', 'alt': 'Símbolo de descanso'},
            {'nome': 'Banheiro', 'emoji': '🚻', 'palavra': 'Preciso ir ao banheiro', 'cat': 'Necessidades', 'alt': 'Símbolo de banheiro'},
            {'nome': 'Pausa', 'emoji': '⏸️', 'palavra': 'Quero fazer uma pausa', 'cat': 'Necessidades', 'alt': 'Botão de pausa'},
            # Alimentação
            {'nome': 'Almoço', 'emoji': '🍽️', 'palavra': 'Quero comer', 'cat': 'Alimentação', 'alt': 'Prato com talheres'},
            {'nome': 'Fruta', 'emoji': '🍎', 'palavra': 'Fruta', 'cat': 'Alimentação', 'alt': 'Maçã vermelha'},
            {'nome': 'Lanche', 'emoji': '🥪', 'palavra': 'Lanche', 'cat': 'Alimentação', 'alt': 'Sanduíche'},
            # Ações
            {'nome': 'Brincar', 'emoji': '🎮', 'palavra': 'Brincar', 'cat': 'Ações', 'alt': 'Controle de videogame'},
            {'nome': 'Estudar', 'emoji': '📚', 'palavra': 'Estudar', 'cat': 'Ações', 'alt': 'Livros abertos'},
            {'nome': 'Dançar', 'emoji': '💃', 'palavra': 'Quero dançar', 'cat': 'Ações', 'alt': 'Pessoa dançando'},
            {'nome': 'Ouvir música', 'emoji': '🎵', 'palavra': 'Ouvir música', 'cat': 'Ações', 'alt': 'Nota musical'},
            # Pessoas
            {'nome': 'Eu', 'emoji': '🙋', 'palavra': 'Eu', 'cat': 'Pessoas', 'alt': 'Pessoa apontando para si'},
            {'nome': 'Professor', 'emoji': '👨‍🏫', 'palavra': 'Professor', 'cat': 'Pessoas', 'alt': 'Professor'},
            {'nome': 'Amigo', 'emoji': '🤝', 'palavra': 'Amigo', 'cat': 'Pessoas', 'alt': 'Aperto de mão, representando amizade'},
            # Lugares
            {'nome': 'Escola', 'emoji': '🏫', 'palavra': 'Escola', 'cat': 'Lugares', 'alt': 'Prédio da escola'},
            {'nome': 'Casa', 'emoji': '🏠', 'palavra': 'Casa', 'cat': 'Lugares', 'alt': 'Casa familiar'},
            {'nome': 'Parque', 'emoji': '🌳', 'palavra': 'Parque', 'cat': 'Lugares', 'alt': 'Árvore no parque'},
            # Rotina
            {'nome': 'Acordar', 'emoji': '⏰', 'palavra': 'Acordar', 'cat': 'Rotina Escolar', 'alt': 'Despertador'},
            {'nome': 'Café da manhã', 'emoji': '🍳', 'palavra': 'Café da manhã', 'cat': 'Rotina Escolar', 'alt': 'Café da manhã'},
            {'nome': 'Almoço', 'emoji': '🍽️', 'palavra': 'Almoço', 'cat': 'Rotina Escolar', 'alt': 'Prato de almoço'},
            {'nome': 'Dormir', 'emoji': '🌙', 'palavra': 'Hora de dormir', 'cat': 'Rotina Escolar', 'alt': 'Lua, representando noite'},
        ]
        for d in pictogramas_data:
            cat = cats.get(d['cat'])
            if not cat:
                continue
            pic, created = Pictograma.objects.get_or_create(
                nome=d['nome'], categoria=cat,
                defaults={
                    'alt_text': d['alt'],
                    'icone_emoji': d['emoji'],
                    'palavra': d['palavra'],
                    'licenca': 'Emoji — domínio público',
                    'origem': 'Emoji Unicode',
                    'ativo': True,
                }
            )
            if created:
                self.stdout.write(f'  🖼️  Pictograma: {d["emoji"]} {d["nome"]}')

        # ── 3. Atividades ─────────────────────────────────────────────────
        from atividades.models import Atividade
        atividades_data = [
            {
                'titulo': 'Como estou me sentindo?',
                'tipo': 'sentimentos',
                'descricao': 'Expresse seus sentimentos com cartões ilustrados de emoções',
                'objetivo_pedagogico': 'Apoiar a identificação e expressão de emoções de forma não-verbal',
                'instrucoes': 'Apresente os cartões ao estudante e pergunte como ele está se sentindo. Respeite qualquer resposta ou ausência de resposta.',
                'nivel_apoio_visual': 'alto',
                'cor_tema': '#FF6B6B',
                'icone': '😊',
            },
            {
                'titulo': 'O que eu preciso?',
                'tipo': 'necessidades',
                'descricao': 'Comunique necessidades como água, ajuda, banheiro e pausa',
                'objetivo_pedagogico': 'Ampliar a expressão de necessidades básicas por meio de pictogramas',
                'instrucoes': 'Disponibilize a prancha e oriente o estudante a tocar o cartão que representa sua necessidade. O sistema lerá a mensagem em voz alta.',
                'nivel_apoio_visual': 'alto',
                'cor_tema': '#38BDF8',
                'icone': '🙋',
            },
            {
                'titulo': 'Monte sua frase',
                'tipo': 'monte_frase',
                'descricao': 'Construa frases selecionando pictogramas em sequência',
                'objetivo_pedagogico': 'Desenvolver a estruturação de mensagens por meio da organização de símbolos',
                'instrucoes': 'Oriente o estudante a selecionar os pictogramas na ordem: sujeito, verbo, complemento. Use o botão de voz para ouvir a frase.',
                'nivel_apoio_visual': 'medio',
                'cor_tema': '#A78BFA',
                'icone': '💬',
            },
            {
                'titulo': 'Escolha o que prefere',
                'tipo': 'escolha',
                'descricao': 'Expresse preferências escolhendo entre duas opções apresentadas',
                'objetivo_pedagogico': 'Promover a expressão de preferências e a tomada de decisão',
                'instrucoes': 'Apresente cada par de opções e pergunte: O que você prefere? Não classifique nenhuma resposta como certa ou errada.',
                'nivel_apoio_visual': 'alto',
                'cor_tema': '#34D399',
                'icone': '✨',
            },
            {
                'titulo': 'Encontre o pictograma',
                'tipo': 'encontre',
                'descricao': 'Identifique pictogramas a partir de uma instrução dada',
                'objetivo_pedagogico': 'Apoiar o reconhecimento e a compreensão de símbolos visuais',
                'instrucoes': 'Leia a instrução para o estudante ou use o recurso de voz. O sistema dará feedback visual respeitoso. Permita tentativas sem pressão.',
                'nivel_apoio_visual': 'alto',
                'cor_tema': '#FBBF24',
                'icone': '🔍',
            },
            {
                'titulo': 'Minha rotina visual',
                'tipo': 'rotina',
                'descricao': 'Monte, reorganize e acompanhe a rotina do dia com cartões',
                'objetivo_pedagogico': 'Apoiar a antecipação e organização temporal através de rotina visual',
                'instrucoes': 'Ajude o estudante a montar a rotina do dia. Ele pode marcar cada etapa como concluída e reorganizar os cartões arrastando.',
                'nivel_apoio_visual': 'alto',
                'cor_tema': '#F472B6',
                'icone': '📅',
            },
            {
                'titulo': 'Sim ou Não',
                'tipo': 'sim_nao',
                'descricao': 'Expresse concordância, recusa ou incerteza com cartões simples',
                'objetivo_pedagogico': 'Ampliar a capacidade de autorregulação e expressão de respostas binárias',
                'instrucoes': 'Faça perguntas simples para o estudante. Respeite sempre a opção "Não sei" e "Quero outra opção". Não exija respostas.',
                'nivel_apoio_visual': 'alto',
                'cor_tema': '#FB923C',
                'icone': '✅',
            },
            {
                'titulo': 'Leve a fruta até a sombra',
                'tipo': 'frutas_sombras',
                'descricao': 'Associe frutas às suas sombras e ouça o nome de cada fruta ao encontrar o par',
                'objetivo_pedagogico': 'Explorar associação visual, coordenação motora e vocabulário de frutas com retorno de voz opcional',
                'instrucoes': 'Convide o estudante a arrastar ou tocar em uma fruta e depois em sua sombra. Respeite o tempo de exploração e ofereça ajuda quando solicitada.',
                'nivel_apoio_visual': 'alto',
                'cor_tema': '#6B9B5D',
                'icone': '🍎',
            },
            {
                'titulo': 'Leve o animal até a sombra',
                'tipo': 'animais_sombras',
                'descricao': 'Associe animais às suas sombras e ouça o nome de cada animal ao encontrar o par',
                'objetivo_pedagogico': 'Explorar associação visual, coordenação motora e vocabulário de animais com retorno de voz opcional',
                'instrucoes': 'Convide o estudante a arrastar ou tocar em um animal e depois em sua sombra. Respeite o tempo de exploração e ofereça ajuda quando solicitada.',
                'nivel_apoio_visual': 'alto',
                'cor_tema': '#6B9B5D',
                'icone': '🐘',
            },
            {
                'titulo': 'Encaixe as figuras: animais',
                'tipo': 'encaixe_animais',
                'descricao': 'Complete figuras de animais e ouça o nome ao encaixar a peça correta',
                'objetivo_pedagogico': 'Explorar percepção visual, coordenação motora e vocabulário de animais',
                'instrucoes': 'Convide o estudante a selecionar ou arrastar a peça até o espaço correspondente. Ao encaixar, o nome da figura será falado.',
                'nivel_apoio_visual': 'alto',
                'cor_tema': '#F29D38',
                'icone': '🧩',
            },
            {
                'titulo': 'Encaixe as figuras: natureza',
                'tipo': 'encaixe_natureza',
                'descricao': 'Complete figuras da natureza e ouça o nome ao encaixar a peça correta',
                'objetivo_pedagogico': 'Explorar percepção visual, coordenação motora e vocabulário relacionado à natureza',
                'instrucoes': 'Convide o estudante a selecionar ou arrastar a peça até o espaço correspondente. Ao encaixar, o nome da figura será falado.',
                'nivel_apoio_visual': 'alto',
                'cor_tema': '#34A89A',
                'icone': '🌼',
            },
            {
                'titulo': 'Que objeto pode me ajudar?',
                'tipo': 'objeto_acao',
                'descricao': 'Associe situações do cotidiano a objetos que ajudam em cada ação',
                'objetivo_pedagogico': 'Ampliar vocabulário funcional e reconhecimento de recursos usados em ações cotidianas, apoiando comunicação e autonomia.',
                'instrucoes': 'Leia ou reproduza a situação e ofereça tempo para o estudante escolher. Ajuste a quantidade de opções e use os recursos de comunicação e acessibilidade previstos para o estudante. O feedback apoia a exploração e não deve ser usado como avaliação isolada.',
                'nivel_apoio_visual': 'alto',
                'cor_tema': '#38BDF8',
                'icone': '🧼',
            },
        ]
        for d in atividades_data:
            at, created = Atividade.objects.get_or_create(
                tipo=d['tipo'],
                defaults=d
            )
            if created:
                self.stdout.write(f'  🎯 Atividade: {d["icone"]} {d["titulo"]}')

        # ── 4. Usuário de demonstração ────────────────────────────────────
        if not User.objects.filter(username='professor').exists():
            user = User.objects.create_user(
                username='professor',
                password='comunicatea2024',
                first_name='Professor',
                last_name='Demonstração',
                email='professor@exemplo.com',
            )
            self.stdout.write(self.style.SUCCESS(
                f'\n  👨‍🏫 Usuário de demonstração criado!\n'
                f'     Usuário: professor\n'
                f'     Senha:   comunicatea2024\n'
            ))
        else:
            self.stdout.write('  ℹ️  Usuário "professor" já existe.')

        self.stdout.write(self.style.SUCCESS('\n✅ Dados iniciais inseridos com sucesso!'))
        self.stdout.write(self.style.HTTP_INFO(
            '\nPróximos passos:\n'
            '  python manage.py runserver\n'
            '  Acesse: http://127.0.0.1:8000/\n'
        ))
