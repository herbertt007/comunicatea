from django.db import models
from django.contrib.auth.models import User


class ObservacaoPedagogica(models.Model):
    estudante = models.ForeignKey(
        'estudantes.Estudante', on_delete=models.PROTECT, related_name='observacoes'
    )
    professor = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name='observacoes'
    )
    atividade = models.ForeignKey(
        'atividades.Atividade', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='observacoes',
        verbose_name='Atividade relacionada (opcional)'
    )
    descricao = models.TextField(verbose_name='Observação pedagógica')
    data_registro = models.DateField(auto_now_add=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Observação Pedagógica'
        verbose_name_plural = 'Observações Pedagógicas'
        ordering = ['-data_registro']

    def __str__(self):
        return f"Obs. de {self.estudante} em {self.data_registro:%d/%m/%Y}"
