# Generated by Django 5.0.6 on 2024-05-22 23:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('embarcaciones', '0002_tipoembarcacion_alter_embarcacion_matricula_and_more'),
        ('ofertas', '0001_initial'),
        ('publicaciones', '0002_alter_publicacion_embarcacion'),
        ('vehiculos', '0002_alter_vehiculo_año_fabricacion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='oferta',
            name='embarcacion_ofertada',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='embarcaciones.embarcacion'),
        ),
        migrations.AlterField(
            model_name='oferta',
            name='publicacion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='publicaciones.publicacion'),
        ),
        migrations.AlterField(
            model_name='oferta',
            name='vehiculo_ofertado',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='vehiculos.vehiculo'),
        ),
    ]
