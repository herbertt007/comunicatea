from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from .models import ObservacaoPedagogica
from .forms import ObservacaoPedagogicaForm
from estudantes.models import Estudante
from atividades.models import SessaoAtividade, Atividade


@login_required
def dashboard(request):
    professor = request.user
    estudantes = Estudante.objects.filter(professor=professor, ativo=True)
    trinta_dias = timezone.now() - timedelta(days=30)
    sessoes = SessaoAtividade.objects.filter(
        professor=professor, iniciada_em__gte=trinta_dias
    ).select_related('atividade', 'estudante')
    obs = ObservacaoPedagogica.objects.filter(
        professor=professor
    ).select_related('estudante', 'atividade').order_by('-data_registro')[:10]
    atividades_usadas = Atividade.objects.filter(
        sessoes__professor=professor
    ).annotate(total=__import__('django').db.models.Count('sessoes')).order_by('-total')[:5]
    estudante_id = request.GET.get('estudante')
    estudante_sel = None
    sessoes_estudante = None
    if estudante_id:
        estudante_sel = get_object_or_404(Estudante, pk=estudante_id, professor=professor)
        sessoes_estudante = SessaoAtividade.objects.filter(
            estudante=estudante_sel
        ).select_related('atividade').order_by('-iniciada_em')[:20]
    return render(request, 'acompanhamento/dashboard.html', {
        'estudantes': estudantes,
        'sessoes': sessoes,
        'obs': obs,
        'atividades_usadas': atividades_usadas,
        'total_sessoes_mes': sessoes.count(),
        'estudante_sel': estudante_sel,
        'sessoes_estudante': sessoes_estudante,
    })


@login_required
def observacao_criar(request):
    if request.method == 'POST':
        form = ObservacaoPedagogicaForm(professor=request.user, data=request.POST)
        if form.is_valid():
            obs = form.save(commit=False)
            obs.professor = request.user
            obs.save()
            messages.success(request, 'Observação registrada com sucesso!')
            return redirect('acompanhamento:dashboard')
    else:
        form = ObservacaoPedagogicaForm(professor=request.user)
    return render(request, 'acompanhamento/observacao_form.html', {'form': form})


@login_required
def observacoes_lista(request):
    obs = ObservacaoPedagogica.objects.filter(
        professor=request.user
    ).select_related('estudante', 'atividade').order_by('-data_registro')
    estudante_id = request.GET.get('estudante')
    if estudante_id:
        obs = obs.filter(estudante_id=estudante_id)
    estudantes = Estudante.objects.filter(professor=request.user)
    return render(request, 'acompanhamento/observacoes_lista.html', {
        'obs': obs,
        'estudantes': estudantes,
        'estudante_sel': estudante_id,
    })
