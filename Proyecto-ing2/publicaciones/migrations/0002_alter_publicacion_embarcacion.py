# Generated by Django 5.0.6 on 2024-05-10 23:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('embarcaciones', '0002_tipoembarcacion_alter_embarcacion_matricula_and_more'),
        ('publicaciones', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publicacion',
            name='embarcacion',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='embarcaciones.embarcacion'),
        ),
    ]
