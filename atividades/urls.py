from django.urls import path
from . import views

app_name = 'atividades'

urlpatterns = [
    path('', views.lista, name='lista'),
    path('sentimentos/', views.sentimentos, name='sentimentos'),
    path('necessidades/', views.necessidades, name='necessidades'),
    path('monte-frase/', views.monte_frase, name='monte_frase'),
    path('escolha/', views.escolha, name='escolha'),
    path('encontre/', views.encontre, name='encontre'),
    path('rotina/', views.rotina, name='rotina'),
    path('sim-nao/', views.sim_nao, name='sim_nao'),
    path('frutas-sombras/', views.frutas_sombras, name='frutas_sombras'),
    path('animais-sombras/', views.animais_sombras, name='animais_sombras'),
    path('encaixe/animais/', views.encaixe_animais, name='encaixe_animais'),
    path('encaixe/natureza/', views.encaixe_natureza, name='encaixe_natureza'),
    path('objeto-acao/', views.objeto_acao, name='objeto_acao'),
    path('registrar-sessao/', views.registrar_sessao, name='registrar_sessao'),
]
