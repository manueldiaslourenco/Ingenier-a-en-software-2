from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.hashers import make_password

class Usuario(AbstractBaseUser, PermissionsMixin):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    fecha_nacimiento = models.DateField()
    telefono = models.CharField(max_length=13)
    mail = models.EmailField(max_length=50, unique=True)
    password = models.CharField(max_length=128)

    USERNAME_FIELD = 'mail'
    REQUIRED_FIELDS = ['nombre', 'apellido', 'fecha_nacimiento', 'telefono']

    def save(self, *args, **kwargs):
        self.password = make_password(self.password)
        super().save(*args, **kwargs)

