# Generated by Django 2.0.3 on 2021-05-03 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0008_projeto_resumo'),
    ]

    operations = [
        migrations.AddField(
            model_name='projeto',
            name='matricula_colaborador',
            field=models.IntegerField(default=0),
        ),
    ]
