# Generated by Django 2.0.3 on 2021-04-16 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Projeto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_projeto', models.CharField(max_length=255)),
                ('nome_cliente', models.CharField(max_length=255)),
                ('status_projeto', models.CharField(max_length=255)),
                ('colaborador', models.CharField(max_length=255)),
                ('função_colaborador', models.CharField(max_length=255)),
                ('alocação_mensal', models.CharField(max_length=255)),
            ],
        ),
    ]
