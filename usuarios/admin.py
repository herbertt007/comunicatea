from django.contrib import admin
from .models import PerfilUsuario


@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'tipo', 'criado_em']
    list_filter = ['tipo']
    search_fields = ['usuario__username', 'usuario__first_name', 'usuario__last_name']
