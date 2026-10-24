from django.contrib import admin
from .models import Estudante


@admin.register(Estudante)
class EstudanteAdmin(admin.ModelAdmin):
    list_display = ['nome_pedagogico', 'codigo', 'professor', 'ativo', 'criado_em']
    list_filter = ['ativo', 'professor']
    search_fields = ['nome_pedagogico', 'codigo']
    readonly_fields = ['criado_em', 'atualizado_em']
