from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.templatetags.static import static as static_url
from .voz import sintetizar_voz

urlpatterns = [
    path('admin/', admin.site.urls),
    path('favicon.ico', RedirectView.as_view(url=static_url('img/favicon.ico'), permanent=True)),
    path('usuarios/', include('usuarios.urls', namespace='usuarios')),
    path('', RedirectView.as_view(url='/usuarios/', permanent=False), name='home'),
    path('estudantes/', include('estudantes.urls', namespace='estudantes')),
    path('comunicacao/', include('comunicacao.urls', namespace='comunicacao')),
    path('atividades/', include('atividades.urls', namespace='atividades')),
    path('acompanhamento/', include('acompanhamento.urls', namespace='acompanhamento')),
    path('voz/sintetizar/', sintetizar_voz, name='voz_sintetizar'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
