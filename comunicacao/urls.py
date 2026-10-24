from django.urls import path
from . import views

app_name = 'comunicacao'

urlpatterns = [
    path('', views.biblioteca, name='biblioteca'),
    path('pictograma/novo/', views.pictograma_criar, name='pictograma_criar'),
    path('pictograma/<int:pk>/editar/', views.pictograma_editar, name='pictograma_editar'),
    path('pranchas/', views.prancha_lista, name='prancha_lista'),
    path('pranchas/nova/', views.prancha_criar, name='prancha_criar'),
    path('pranchas/<int:pk>/', views.prancha_detalhe, name='prancha_detalhe'),
    path('pranchas/<int:pk>/publica/', views.prancha_publica, name='prancha_publica'),
    path('pranchas/<int:prancha_pk>/adicionar/', views.prancha_adicionar_item, name='prancha_adicionar_item'),
    path('pranchas/<int:prancha_pk>/remover/<int:item_pk>/', views.prancha_remover_item, name='prancha_remover_item'),
]
