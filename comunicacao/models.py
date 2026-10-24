from django.db import models
from django.contrib.auth.models import User


class CategoriaPictograma(models.Model):
    nome = models.CharField(max_length=100, verbose_name='Nome')
    descricao = models.TextField(blank=True, verbose_name='Descrição')
    icone = models.CharField(max_length=10, blank=True, verbose_name='Emoji/Ícone')
    cor = models.CharField(max_length=7, default='#5B4CF5', verbose_name='Cor (hex)')
    ativo = models.BooleanField(default=True)
    ordem = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = 'Categoria de Pictograma'
        verbose_name_plural = 'Categorias de Pictogramas'
        ordering = ['ordem', 'nome']

    def __str__(self):
        return self.nome


class Pictograma(models.Model):
    nome = models.CharField(max_length=100)
    alt_text = models.CharField(max_length=200, verbose_name='Texto alternativo (acessibilidade)')
    imagem = models.ImageField(upload_to='pictogramas/', blank=True, null=True)
    icone_emoji = models.CharField(max_length=10, blank=True, verbose_name='Emoji representativo')
    categoria = models.ForeignKey(
        CategoriaPictograma, on_delete=models.PROTECT,
        related_name='pictogramas', verbose_name='Categoria'
    )
    palavra = models.CharField(max_length=100, verbose_name='Palavra/Mensagem de voz')
    ativo = models.BooleanField(default=True)
    licenca = models.CharField(max_length=100, blank=True, verbose_name='Licença')
    origem = models.CharField(max_length=200, blank=True, verbose_name='Origem/Autor')
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Pictograma'
        verbose_name_plural = 'Pictogramas'
        ordering = ['categoria', 'nome']

    def __str__(self):
        return f"{self.palavra} — {self.categoria.nome}"


class PranchaComunicacao(models.Model):
    titulo = models.CharField(max_length=200, verbose_name='Título')
    descricao = models.TextField(blank=True, verbose_name='Descrição')
    professor = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name='pranchas'
    )
    estudante = models.ForeignKey(
        'estudantes.Estudante', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='pranchas'
    )
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Prancha de Comunicação'
        verbose_name_plural = 'Pranchas de Comunicação'
        ordering = ['-criado_em']

    def __str__(self):
        return self.titulo


class ItemPrancha(models.Model):
    prancha = models.ForeignKey(
        PranchaComunicacao, on_delete=models.CASCADE, related_name='itens'
    )
    pictograma = models.ForeignKey(Pictograma, on_delete=models.PROTECT)
    ordem = models.PositiveIntegerField(default=0)
    configuracoes = models.JSONField(default=dict, blank=True)

    class Meta:
        verbose_name = 'Item da Prancha'
        verbose_name_plural = 'Itens da Prancha'
        ordering = ['ordem']

    def __str__(self):
        return f"{self.prancha.titulo} — {self.pictograma.palavra} (pos {self.ordem})"
