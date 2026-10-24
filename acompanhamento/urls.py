from django.urls import path
from . import views

app_name = 'acompanhamento'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('observacao/nova/', views.observacao_criar, name='observacao_criar'),
    path('observacoes/', views.observacoes_lista, name='observacoes_lista'),
]
