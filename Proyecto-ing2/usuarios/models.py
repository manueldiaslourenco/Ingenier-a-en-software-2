from django.db import models
from django.contrib.auth.hashers import make_password

class Usuario(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    fecha_nacimiento = models.DateField()
    telefono = models.CharField(max_length=13)
    mail = models.EmailField(max_length=50, unique=True)
    contraseña = models.CharField(max_length=50)

    def save(self, *args, **kwargs):
        self.contraseña = make_password(self.contraseña)
        super().save(*args, **kwargs)
