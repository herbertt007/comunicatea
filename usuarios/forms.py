from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import PerfilUsuario


class RegistroProfessorForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, label='Nome', required=True)
    last_name = forms.CharField(max_length=100, label='Sobrenome', required=True)
    email = forms.EmailField(required=True, label='E-mail')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user


class PerfilForm(forms.ModelForm):
    first_name = forms.CharField(max_length=100, label='Nome', required=False)
    last_name = forms.CharField(max_length=100, label='Sobrenome', required=False)
    email = forms.EmailField(required=False, label='E-mail')

    class Meta:
        model = PerfilUsuario
        fields = ['foto', 'bio']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['first_name'].initial = self.instance.usuario.first_name
            self.fields['last_name'].initial = self.instance.usuario.last_name
            self.fields['email'].initial = self.instance.usuario.email

    def save(self, commit=True):
        perfil = super().save(commit=False)
        perfil.usuario.first_name = self.cleaned_data.get('first_name', '')
        perfil.usuario.last_name = self.cleaned_data.get('last_name', '')
        perfil.usuario.email = self.cleaned_data.get('email', '')
        if commit:
            perfil.usuario.save()
            perfil.save()
        return perfil
