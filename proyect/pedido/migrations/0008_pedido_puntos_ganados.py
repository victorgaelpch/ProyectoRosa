# Generated by Django 5.2 on 2025-05-25 01:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pedido', '0007_perfilusuario_puntos'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedido',
            name='puntos_ganados',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
