from django.db import models
from usuarios.models import Usuario
from empleados.models import Sede

class TipoEmbarcacion(models.Model):
    clase= models.CharField(max_length=50, unique=True)

class Embarcacion(models.Model):
    matricula = models.CharField(max_length=100, unique=True)
    modelo = models.CharField(max_length=100)
    tipo = models.ForeignKey(TipoEmbarcacion, on_delete=models.SET_NULL, null=True)
    m_eslora = models.DecimalField(max_digits=5, decimal_places=2)
    m_manga = models.DecimalField(max_digits=5, decimal_places=2)
    m_calado = models.DecimalField(max_digits=5, decimal_places=2)
    motor = models.BooleanField(default=False)
    deuda = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    sede = models.ForeignKey(Sede, on_delete=models.SET_NULL, null=True)
    dueño = models.ForeignKey(Usuario, on_delete=models.CASCADE)

class ImagenEmbarcacion(models.Model):
    nombre_especifico= models.CharField(max_length=100)
    embarcacion= models.ForeignKey(Embarcacion, on_delete= models.CASCADE)