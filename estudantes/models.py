from django.db import models
from django.contrib.auth.models import User


class Estudante(models.Model):
    codigo = models.CharField(max_length=50, unique=True, verbose_name='Código Pedagógico',
                              help_text='Identificador pedagógico — não use o nome real.')
    nome_pedagogico = models.CharField(max_length=100, verbose_name='Nome/Identificação Pedagógica')
    professor = models.ForeignKey(
        User, on_delete=models.PROTECT,
        related_name='estudantes', verbose_name='Professor Responsável'
    )
    preferencias = models.JSONField(
        default=dict, blank=True,
        verbose_name='Preferências de Acessibilidade',
        help_text='Ex: {"audio": true, "animacoes": false}'
    )
    observacoes_gerais = models.TextField(blank=True, verbose_name='Observações Gerais')
    ativo = models.BooleanField(default=True, verbose_name='Ativo')
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Estudante'
        verbose_name_plural = 'Estudantes'
        ordering = ['nome_pedagogico']
        constraints = [
            models.UniqueConstraint(
                fields=['codigo', 'professor'],
                name='unique_codigo_professor'
            )
        ]

    def __str__(self):
        return f"{self.nome_pedagogico} ({self.codigo})"

    def get_preferencia(self, chave, default=True):
        return self.preferencias.get(chave, default)
