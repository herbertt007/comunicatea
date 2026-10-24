from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class PerfilUsuario(models.Model):
    TIPO_CHOICES = [
        ('professor', 'Professor AEE'),
        ('admin', 'Administrador'),
    ]
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='professor')
    foto = models.ImageField(upload_to='fotos_perfil/', blank=True, null=True)
    bio = models.TextField(blank=True, verbose_name='Sobre mim')
    preferencias_acessibilidade = models.JSONField(default=dict, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Perfil de Usuário'
        verbose_name_plural = 'Perfis de Usuários'

    def __str__(self):
        return f"{self.usuario.get_full_name() or self.usuario.username} ({self.get_tipo_display()})"

    def get_preferencia(self, chave, default=False):
        return self.preferencias_acessibilidade.get(chave, default)


@receiver(post_save, sender=User)
def criar_ou_salvar_perfil(sender, instance, created, **kwargs):
    if created:
        PerfilUsuario.objects.create(usuario=instance)
    elif hasattr(instance, 'perfil'):
        instance.perfil.save()
