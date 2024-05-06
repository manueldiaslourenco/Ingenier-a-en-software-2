from django.db import models
from usuarios.models import Usuario
from empleados.models import Sede

class Embarcacion(models.Model):
    matricula = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    tipo = models.CharField(max_length=100)
    m_eslora = models.DecimalField(max_digits=5, decimal_places=2)
    m_manga = models.DecimalField(max_digits=5, decimal_places=2)
    m_calado = models.DecimalField(max_digits=5, decimal_places=2)
    motor = models.CharField(max_length=100, null=True, blank=True)
    deuda = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    sede = models.ForeignKey(Sede, on_delete=models.SET_NULL, null=True)
    dueño = models.ForeignKey(Usuario, on_delete=models.CASCADE)