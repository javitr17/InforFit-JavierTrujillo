# Generated by Django 4.1.13 on 2024-12-18 00:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0023_alter_datosfisicos_altura_alter_datosfisicos_imc_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datosfisicos',
            name='peso',
            field=models.DecimalField(decimal_places=3, max_digits=6, null=True),
        ),
    ]
