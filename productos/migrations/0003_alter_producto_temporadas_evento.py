# Generated by Django 4.2.6 on 2023-11-04 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0002_producto_imagen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='temporadas_evento',
            field=models.ManyToManyField(blank=True, related_name='productos', to='productos.temporadaevento'),
        ),
    ]