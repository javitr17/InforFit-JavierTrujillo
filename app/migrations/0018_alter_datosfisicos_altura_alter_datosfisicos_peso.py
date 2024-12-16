# Generated by Django 4.1.13 on 2024-12-16 21:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0017_alter_datosfisicos_peso'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datosfisicos',
            name='altura',
            field=models.DecimalField(blank=True, decimal_places=1, max_digits=4, null=True),
        ),
        migrations.AlterField(
            model_name='datosfisicos',
            name='peso',
            field=models.DecimalField(decimal_places=3, default=70, max_digits=6),
        ),
    ]