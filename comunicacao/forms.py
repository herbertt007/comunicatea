from django import forms
from .models import Pictograma, CategoriaPictograma, PranchaComunicacao, ItemPrancha


TIPOS_IMAGEM_PERMITIDOS = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
TAMANHO_MAX_BYTES = 3 * 1024 * 1024  # 3MB


class PictogramaForm(forms.ModelForm):
    class Meta:
        model = Pictograma
        fields = ['nome', 'alt_text', 'imagem', 'icone_emoji', 'categoria', 'palavra', 'licenca', 'origem', 'ativo']
        widgets = {
            'alt_text': forms.TextInput(attrs={'placeholder': 'Descreva a imagem para acessibilidade'}),
        }

    def clean_imagem(self):
        imagem = self.cleaned_data.get('imagem')
        if imagem:
            if imagem.size > TAMANHO_MAX_BYTES:
                raise forms.ValidationError('A imagem deve ter menos de 3MB.')
            if hasattr(imagem, 'content_type') and imagem.content_type not in TIPOS_IMAGEM_PERMITIDOS:
                raise forms.ValidationError('Tipo de arquivo não permitido. Use JPEG, PNG, GIF ou WebP.')
            # Não confie apenas no MIME informado pelo navegador: confirme os bytes.
            from PIL import Image, UnidentifiedImageError
            try:
                imagem.seek(0)
                with Image.open(imagem) as arquivo:
                    if arquivo.format not in {'JPEG', 'PNG', 'GIF', 'WEBP'}:
                        raise forms.ValidationError('O arquivo precisa ser uma imagem JPEG, PNG, GIF ou WebP válida.')
                    arquivo.verify()
            except (UnidentifiedImageError, OSError):
                raise forms.ValidationError('O arquivo enviado não é uma imagem válida.')
            finally:
                imagem.seek(0)
        return imagem


class CategoriaPictogramaForm(forms.ModelForm):
    class Meta:
        model = CategoriaPictograma
        fields = ['nome', 'descricao', 'icone', 'cor', 'ativo', 'ordem']
        widgets = {
            'cor': forms.TextInput(attrs={'type': 'color'}),
        }


class PranchaComunicacaoForm(forms.ModelForm):
    class Meta:
        model = PranchaComunicacao
        fields = ['titulo', 'descricao', 'estudante', 'ativo']
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, professor=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if professor:
            self.fields['estudante'].queryset = professor.estudantes.filter(ativo=True)
