# Generated by Django 5.0.4 on 2024-05-01 20:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0004_usuario_is_staff'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='is_blocked',
            field=models.BooleanField(default=False),
        ),
    ]
