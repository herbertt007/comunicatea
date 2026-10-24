from django import forms
from .models import ObservacaoPedagogica


class ObservacaoPedagogicaForm(forms.ModelForm):
    class Meta:
        model = ObservacaoPedagogica
        fields = ['estudante', 'atividade', 'descricao']
        widgets = {
            'descricao': forms.Textarea(attrs={
                'rows': 5,
                'placeholder': 'Descreva o que observou durante a atividade...'
            }),
        }

    def __init__(self, professor=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if professor:
            from estudantes.models import Estudante
            self.fields['estudante'].queryset = Estudante.objects.filter(
                professor=professor, ativo=True
            )
