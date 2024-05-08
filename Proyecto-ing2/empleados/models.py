from django.db import models
from usuarios.models import Usuario

class Sede(models.Model):
    nombre = models.CharField(max_length=100)


class EmpleConSede():
    sede= models.ForeignKey(Sede, on_delete=models.SET_NULL, null=True)
    user= models.ForeignKey(Usuario, on_delete=models.CASCADE)