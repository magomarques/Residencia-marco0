# Generated by Django 2.0.3 on 2021-04-21 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_auto_20210420_1852'),
    ]

    operations = [
        migrations.AddField(
            model_name='projeto',
            name='teste',
            field=models.CharField(default=0, max_length=255),
        ),
        migrations.AlterField(
            model_name='projeto',
            name='alocação_mensal',
            field=models.CharField(default=0, max_length=255),
        ),
    ]
