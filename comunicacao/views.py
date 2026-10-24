from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Pictograma, CategoriaPictograma, PranchaComunicacao, ItemPrancha
from .forms import PictogramaForm, CategoriaPictogramaForm, PranchaComunicacaoForm


def biblioteca(request):
    categorias = CategoriaPictograma.objects.filter(ativo=True)
    pictogramas = Pictograma.objects.filter(ativo=True).select_related('categoria')
    cat_id = request.GET.get('categoria')
    busca = request.GET.get('q', '').strip()
    if cat_id:
        pictogramas = pictogramas.filter(categoria_id=cat_id)
    if busca:
        pictogramas = pictogramas.filter(
            Q(nome__icontains=busca) | Q(palavra__icontains=busca) | Q(alt_text__icontains=busca)
        )
    return render(request, 'comunicacao/biblioteca.html', {
        'pictogramas': pictogramas,
        'categorias': categorias,
        'cat_selecionada': cat_id,
        'busca': busca,
    })


@login_required
def pictograma_criar(request):
    if request.method == 'POST':
        form = PictogramaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Pictograma criado!')
            return redirect('comunicacao:biblioteca')
    else:
        form = PictogramaForm()
    return render(request, 'comunicacao/pictograma_form.html', {'form': form, 'titulo': 'Novo Pictograma'})


@login_required
def pictograma_editar(request, pk):
    pic = get_object_or_404(Pictograma, pk=pk)
    if request.method == 'POST':
        form = PictogramaForm(request.POST, request.FILES, instance=pic)
        if form.is_valid():
            form.save()
            messages.success(request, 'Pictograma atualizado!')
            return redirect('comunicacao:biblioteca')
    else:
        form = PictogramaForm(instance=pic)
    return render(request, 'comunicacao/pictograma_form.html', {'form': form, 'titulo': 'Editar Pictograma'})


@login_required
def prancha_lista(request):
    pranchas = PranchaComunicacao.objects.filter(professor=request.user).select_related('estudante')
    return render(request, 'comunicacao/prancha_lista.html', {'pranchas': pranchas})


@login_required
def prancha_detalhe(request, pk):
    prancha = get_object_or_404(PranchaComunicacao, pk=pk, professor=request.user)
    itens = prancha.itens.select_related('pictograma__categoria').all()
    pictogramas_disponiveis = Pictograma.objects.filter(ativo=True).select_related('categoria')
    return render(request, 'comunicacao/prancha_detalhe.html', {
        'prancha': prancha,
        'itens': itens,
        'pictogramas_disponiveis': pictogramas_disponiveis,
    })


def prancha_publica(request, pk):
    """Pranchas gerais podem ser abertas no modo estudante; as individuais são privadas."""
    pranchas = PranchaComunicacao.objects.filter(pk=pk, ativo=True)
    if request.user.is_authenticated:
        pranchas = pranchas.filter(Q(estudante__isnull=True) | Q(professor=request.user))
    else:
        pranchas = pranchas.filter(estudante__isnull=True)
    prancha = get_object_or_404(pranchas)
    itens = prancha.itens.select_related('pictograma').all()
    return render(request, 'comunicacao/prancha_publica.html', {'prancha': prancha, 'itens': itens})


@login_required
def prancha_criar(request):
    if request.method == 'POST':
        form = PranchaComunicacaoForm(professor=request.user, data=request.POST)
        if form.is_valid():
            prancha = form.save(commit=False)
            prancha.professor = request.user
            prancha.save()
            messages.success(request, 'Prancha criada!')
            return redirect('comunicacao:prancha_detalhe', pk=prancha.pk)
    else:
        form = PranchaComunicacaoForm(professor=request.user)
    return render(request, 'comunicacao/prancha_form.html', {'form': form, 'titulo': 'Nova Prancha'})


@login_required
def prancha_adicionar_item(request, prancha_pk):
    prancha = get_object_or_404(PranchaComunicacao, pk=prancha_pk, professor=request.user)
    if request.method == 'POST':
        pic_id = request.POST.get('pictograma_id')
        pic = get_object_or_404(Pictograma, pk=pic_id)
        ordem = prancha.itens.count()
        ItemPrancha.objects.create(prancha=prancha, pictograma=pic, ordem=ordem)
        messages.success(request, f'"{pic.palavra}" adicionado à prancha.')
    return redirect('comunicacao:prancha_detalhe', pk=prancha_pk)


@login_required
def prancha_remover_item(request, prancha_pk, item_pk):
    prancha = get_object_or_404(PranchaComunicacao, pk=prancha_pk, professor=request.user)
    item = get_object_or_404(ItemPrancha, pk=item_pk, prancha=prancha)
    if request.method == 'POST':
        item.delete()
        messages.success(request, 'Item removido.')
    return redirect('comunicacao:prancha_detalhe', pk=prancha_pk)
