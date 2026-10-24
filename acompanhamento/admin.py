from django.contrib import admin
from .models import ObservacaoPedagogica


@admin.register(ObservacaoPedagogica)
class ObservacaoPedagogicaAdmin(admin.ModelAdmin):
    list_display = ['estudante', 'professor', 'atividade', 'data_registro']
    list_filter = ['professor', 'data_registro', 'atividade']
    search_fields = ['estudante__nome_pedagogico', 'descricao']
    readonly_fields = ['data_registro', 'criado_em']
