# Generated by Django 5.0.6 on 2024-05-22 17:01

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('embarcaciones', '0002_tipoembarcacion_alter_embarcacion_matricula_and_more'),
        ('publicaciones', '0002_alter_publicacion_embarcacion'),
        ('vehiculos', '0002_alter_vehiculo_año_fabricacion'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Oferta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('monto', models.DecimalField(decimal_places=2, default=0, max_digits=15)),
                ('autor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('embarcacion_ofertada', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='embarcaciones.embarcacion')),
                ('publicacion', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='publicaciones.publicacion')),
                ('vehiculo_ofertado', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='vehiculos.vehiculo')),
            ],
        ),
    ]
