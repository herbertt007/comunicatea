from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('atividades', '0005_alter_atividade_tipo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='atividade',
            name='tipo',
            field=models.CharField(choices=[
                ('sentimentos', 'Como estou me sentindo?'),
                ('necessidades', 'O que eu preciso?'),
                ('monte_frase', 'Monte sua frase'),
                ('escolha', 'Escolha o que prefere'),
                ('encontre', 'Encontre o pictograma'),
                ('rotina', 'Minha rotina visual'),
                ('sim_nao', 'Sim ou não'),
                ('frutas_sombras', 'Leve a fruta até a sua sombra'),
                ('animais_sombras', 'Leve o animal até a sua sombra'),
                ('encaixe_animais', 'Encaixe as figuras: animais'),
                ('encaixe_natureza', 'Encaixe as figuras: natureza'),
                ('brinquedos_formas', 'Brinquedos de encaixar: formas geométricas'),
                ('objeto_acao', 'Que objeto pode me ajudar?'),
            ], max_length=30, verbose_name='Tipo'),
        ),
    ]
