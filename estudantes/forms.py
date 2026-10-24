from django import forms
from .models import Estudante


class EstudanteForm(forms.ModelForm):
    class Meta:
        model = Estudante
        fields = ['codigo', 'nome_pedagogico', 'observacoes_gerais', 'ativo']
        widgets = {
            'observacoes_gerais': forms.Textarea(attrs={'rows': 4}),
            'codigo': forms.TextInput(attrs={'placeholder': 'Ex: EST001'}),
        }
        help_texts = {
            'codigo': 'Identificador único. Não use o nome real do estudante.',
            'nome_pedagogico': 'Nome ou apelido para uso na plataforma.',
        }
