from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.db.models import Count
from .forms import RegistroProfessorForm, PerfilForm
from estudantes.models import Estudante
from atividades.models import SessaoAtividade, Atividade
from acompanhamento.models import ObservacaoPedagogica


def inicio(request):
    atividades = Atividade.objects.filter(ativo=True)
    return render(request, 'inicio.html', {'atividades': atividades})


def registro_professor(request):
    if request.user.is_authenticated:
        return redirect('usuarios:dashboard')
    if request.method == 'POST':
        form = RegistroProfessorForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Conta criada com sucesso! Bem-vindo ao ComunicaTEA.')
            return redirect('usuarios:dashboard')
    else:
        form = RegistroProfessorForm()
    return render(request, 'usuarios/registro.html', {'form': form})


@login_required
def dashboard(request):
    professor = request.user
    estudantes = Estudante.objects.filter(professor=professor, ativo=True)
    sessoes_recentes = SessaoAtividade.objects.filter(
        professor=professor
    ).select_related('atividade', 'estudante').order_by('-iniciada_em')[:10]
    obs_recentes = ObservacaoPedagogica.objects.filter(
        professor=professor
    ).select_related('estudante', 'atividade').order_by('-data_registro')[:5]
    total_sessoes = SessaoAtividade.objects.filter(professor=professor).count()
    atividades = Atividade.objects.filter(ativo=True)
    context = {
        'estudantes': estudantes,
        'sessoes_recentes': sessoes_recentes,
        'obs_recentes': obs_recentes,
        'total_sessoes': total_sessoes,
        'total_estudantes': estudantes.count(),
        'atividades': atividades,
    }
    return render(request, 'usuarios/dashboard.html', context)


@login_required
def perfil(request):
    perfil_obj = request.user.perfil
    if request.method == 'POST':
        form = PerfilForm(request.POST, request.FILES, instance=perfil_obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil atualizado com sucesso!')
            return redirect('usuarios:perfil')
    else:
        form = PerfilForm(instance=perfil_obj)
    return render(request, 'usuarios/perfil.html', {'form': form})


@login_required
def preferencias(request):
    perfil_obj = request.user.perfil
    if request.method == 'POST':
        prefs = {
            'audio': 'audio' in request.POST,
            'animacoes': 'animacoes' in request.POST,
            'alto_contraste': 'alto_contraste' in request.POST,
            'fonte_grande': 'fonte_grande' in request.POST,
        }
        perfil_obj.preferencias_acessibilidade = prefs
        perfil_obj.save()
        messages.success(request, 'Preferências salvas!')
        return redirect('usuarios:dashboard')
    return render(request, 'usuarios/preferencias.html', {'perfil': perfil_obj})
