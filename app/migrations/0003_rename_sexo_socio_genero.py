# Generated by Django 4.1.13 on 2024-11-11 17:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_socio_sexo'),
    ]

    operations = [
        migrations.RenameField(
            model_name='socio',
            old_name='sexo',
            new_name='genero',
        ),
    ]