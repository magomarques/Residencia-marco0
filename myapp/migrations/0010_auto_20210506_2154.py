# Generated by Django 3.1.3 on 2021-05-07 00:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0009_projeto_matricula_colaborador'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projeto',
            name='matricula_colaborador',
            field=models.CharField(default=0, max_length=10),
        ),
    ]