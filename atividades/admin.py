from django.contrib import admin
from .models import Atividade, SessaoAtividade


@admin.register(Atividade)
class AtividadeAdmin(admin.ModelAdmin):
    list_display = ['icone', 'titulo', 'tipo', 'nivel_apoio_visual', 'ativo']
    list_filter = ['tipo', 'ativo', 'nivel_apoio_visual']
    search_fields = ['titulo', 'descricao']


@admin.register(SessaoAtividade)
class SessaoAtividadeAdmin(admin.ModelAdmin):
    list_display = ['atividade', 'estudante', 'professor', 'iniciada_em']
    list_filter = ['atividade', 'iniciada_em']
    readonly_fields = ['iniciada_em']
