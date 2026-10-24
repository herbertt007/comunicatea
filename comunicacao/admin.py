from django.contrib import admin
from .models import CategoriaPictograma, Pictograma, PranchaComunicacao, ItemPrancha


@admin.register(CategoriaPictograma)
class CategoriaPictogramaAdmin(admin.ModelAdmin):
    list_display = ['icone', 'nome', 'cor', 'ativo', 'ordem']
    list_editable = ['ativo', 'ordem']
    search_fields = ['nome']


class ItemPranchaInline(admin.TabularInline):
    model = ItemPrancha
    extra = 1


@admin.register(Pictograma)
class PictogramaAdmin(admin.ModelAdmin):
    list_display = ['icone_emoji', 'nome', 'palavra', 'categoria', 'ativo']
    list_filter = ['categoria', 'ativo']
    search_fields = ['nome', 'palavra', 'alt_text']


@admin.register(PranchaComunicacao)
class PranchaComunicacaoAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'professor', 'estudante', 'ativo', 'criado_em']
    list_filter = ['ativo', 'professor']
    inlines = [ItemPranchaInline]
