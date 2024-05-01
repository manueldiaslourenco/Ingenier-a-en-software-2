from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

class Usuario(AbstractBaseUser, PermissionsMixin):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    fecha_nacimiento = models.DateField()
    telefono = models.CharField(max_length=13)
    mail = models.EmailField(max_length=50, unique=True)
    password = models.CharField(max_length=128)
    is_staff= models.BooleanField(default=False)
    is_blocked= models.BooleanField(default=False)

    USERNAME_FIELD = 'mail'
    REQUIRED_FIELDS = ['nombre', 'apellido', 'fecha_nacimiento', 'telefono']

    def save(self, *args, **kwargs):
        superuser = kwargs.pop('superuser', False)
        self.is_superuser = superuser
        super().save(*args, **kwargs)

