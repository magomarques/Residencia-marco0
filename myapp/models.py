from django.db import models

# Create your models here.

'''
class Projeto(models.Model):
    registro = models.CharField(
        max_length=255,
        null=False,
        blank=False
    )
'''

class Projeto(models.Model):
    nome_projeto = models.CharField(
        default=0,
        max_length=255,
        null=False,
        blank=False
    )

    nome_cliente = models.CharField(
        default=0,
        max_length=255,
        null=False,
        blank=False
    )

    status_projeto = models.CharField(
        default=0,
        max_length=255,
        null=False,
        blank=False
    )

    mês_início_projeto = models.CharField(
        default=0,
        max_length=10,
        null=False,
        blank=False
    )

    ano_início_projeto = models.IntegerField(
        default=0,
        null=False,
        blank=False
    )

    duração_projeto = models.IntegerField(
        default=0,
        null=False,
        blank=False
    )

    matricula_colaborador = models.CharField(
        max_length=10,
        default=0,
        null=False,
        blank=False
    )

    colaborador = models.CharField(
        default=0,
        max_length=255,
        null=False,
        blank=False
    )

    chave_matricula = models.CharField(
        default=0,
        max_length=10,
        null=False,
        blank=False
    )

    função_colaborador = models.CharField(
        default=0,
        max_length=255,
        null=False,
        blank=False
    )

    alocação_mensal = models.CharField(
        default=0,
        max_length=255,
        null=False,
        blank=False
    )

    resumo = models.CharField(
        default=0,
        max_length=255,
        null=False,
        blank=False
    )
