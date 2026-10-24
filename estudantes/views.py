from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Estudante
from .forms import EstudanteForm
from acompanhamento.models import ObservacaoPedagogica
from atividades.models import SessaoAtividade


@login_required
def lista(request):
    estudantes = Estudante.objects.filter(professor=request.user).order_by('nome_pedagogico')
    return render(request, 'estudantes/lista.html', {'estudantes': estudantes})


@login_required
def criar(request):
    if request.method == 'POST':
        form = EstudanteForm(request.POST)
        if form.is_valid():
            estudante = form.save(commit=False)
            estudante.professor = request.user
            estudante.save()
            messages.success(request, f'Estudante "{estudante.nome_pedagogico}" cadastrado!')
            return redirect('estudantes:lista')
    else:
        form = EstudanteForm()
    return render(request, 'estudantes/form.html', {'form': form, 'titulo': 'Novo Estudante'})


@login_required
def editar(request, pk):
    estudante = get_object_or_404(Estudante, pk=pk, professor=request.user)
    if request.method == 'POST':
        form = EstudanteForm(request.POST, instance=estudante)
        if form.is_valid():
            form.save()
            messages.success(request, 'Dados atualizados!')
            return redirect('estudantes:detalhe', pk=pk)
    else:
        form = EstudanteForm(instance=estudante)
    return render(request, 'estudantes/form.html', {'form': form, 'titulo': 'Editar Estudante', 'estudante': estudante})


@login_required
def detalhe(request, pk):
    estudante = get_object_or_404(Estudante, pk=pk, professor=request.user)
    sessoes = SessaoAtividade.objects.filter(estudante=estudante).select_related('atividade').order_by('-iniciada_em')[:20]
    observacoes = ObservacaoPedagogica.objects.filter(estudante=estudante).order_by('-data_registro')[:10]
    return render(request, 'estudantes/detalhe.html', {
        'estudante': estudante,
        'sessoes': sessoes,
        'observacoes': observacoes,
    })


@login_required
def desativar(request, pk):
    estudante = get_object_or_404(Estudante, pk=pk, professor=request.user)
    if request.method == 'POST':
        estudante.ativo = not estudante.ativo
        estudante.save()
        status = 'ativado' if estudante.ativo else 'desativado'
        messages.success(request, f'Estudante {status}.')
    return redirect('estudantes:lista')
