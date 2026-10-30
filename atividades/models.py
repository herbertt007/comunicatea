from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


TIPO_ATIVIDADE_CHOICES = [
    ('sentimentos', 'Como estou me sentindo?'),
    ('necessidades', 'O que eu preciso?'),
    ('monte_frase', 'Monte sua frase'),
    ('escolha', 'Escolha o que prefere'),
    ('encontre', 'Encontre o pictograma'),
    ('rotina', 'Minha rotina visual'),
    ('sim_nao', 'Sim ou não'),
    ('frutas_sombras', 'Leve a fruta até a sua sombra'),
    ('animais_sombras', 'Leve o animal até a sua sombra'),
    ('encaixe_animais', 'Encaixe as figuras: animais'),
    ('encaixe_natureza', 'Encaixe as figuras: natureza'),
    ('brinquedos_formas', 'Brinquedos de encaixar: formas geométricas'),
    ('objeto_acao', 'Que objeto pode me ajudar?'),
]

NIVEL_APOIO_CHOICES = [
    ('alto', 'Alto — muitas imagens e suportes visuais'),
    ('medio', 'Médio — imagens e texto'),
    ('basico', 'Básico — texto com imagens de apoio'),
]


class Atividade(models.Model):
    titulo = models.CharField(max_length=200, verbose_name='Título')
    descricao = models.TextField(verbose_name='Descrição')
    tipo = models.CharField(max_length=30, choices=TIPO_ATIVIDADE_CHOICES, verbose_name='Tipo')
    objetivo_pedagogico = models.TextField(verbose_name='Objetivo Pedagógico')
    instrucoes = models.TextField(verbose_name='Instruções para o professor')
    nivel_apoio_visual = models.CharField(
        max_length=10, choices=NIVEL_APOIO_CHOICES,
        default='alto', verbose_name='Nível de apoio visual'
    )
    cor_tema = models.CharField(max_length=7, default='#5B4CF5', verbose_name='Cor do tema (hex)')
    icone = models.CharField(max_length=10, default='🧩', verbose_name='Emoji')
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Atividade'
        verbose_name_plural = 'Atividades'
        ordering = ['tipo']

    def __str__(self):
        return self.titulo

    def get_absolute_url(self):
        url_map = {
            'sentimentos': 'atividades:sentimentos',
            'necessidades': 'atividades:necessidades',
            'monte_frase': 'atividades:monte_frase',
            'escolha': 'atividades:escolha',
            'encontre': 'atividades:encontre',
            'rotina': 'atividades:rotina',
            'sim_nao': 'atividades:sim_nao',
            'frutas_sombras': 'atividades:frutas_sombras',
            'animais_sombras': 'atividades:animais_sombras',
            'encaixe_animais': 'atividades:encaixe_animais',
            'encaixe_natureza': 'atividades:encaixe_natureza',
            'brinquedos_formas': 'atividades:brinquedos_formas',
            'objeto_acao': 'atividades:objeto_acao',
        }
        name = url_map.get(self.tipo, 'atividades:lista')
        return reverse(name)


class SessaoAtividade(models.Model):
    estudante = models.ForeignKey(
        'estudantes.Estudante', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='sessoes'
    )
    atividade = models.ForeignKey(
        Atividade, on_delete=models.PROTECT, related_name='sessoes'
    )
    professor = models.ForeignKey(
        User, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='sessoes_supervisionadas'
    )
    iniciada_em = models.DateTimeField(auto_now_add=True)
    tipo_interacao = models.CharField(max_length=200, blank=True, verbose_name='Tipo de interação observada')
    comentario = models.TextField(blank=True, verbose_name='Comentário')

    class Meta:
        verbose_name = 'Sessão de Atividade'
        verbose_name_plural = 'Sessões de Atividades'
        ordering = ['-iniciada_em']

    def __str__(self):
        est = str(self.estudante) if self.estudante else 'Anônimo'
        return f"{est} — {self.atividade.titulo} ({self.iniciada_em:%d/%m/%Y %H:%M})"
