# Generated by Django 5.0.6 on 2024-05-28 21:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ofertas', '0003_oferta_estado'),
    ]

    operations = [
        migrations.AddField(
            model_name='oferta',
            name='oculta',
            field=models.BooleanField(default=False),
        ),
    ]