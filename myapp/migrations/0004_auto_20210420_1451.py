# Generated by Django 2.0.3 on 2021-04-20 17:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_auto_20210420_1435'),
    ]

    operations = [
        migrations.RenameField(
            model_name='projeto',
            old_name='projeto',
            new_name='registro',
        ),
    ]