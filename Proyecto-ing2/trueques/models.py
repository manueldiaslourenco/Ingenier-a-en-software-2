from django.db import models
from usuarios.models import Usuario
from embarcaciones.models import Embarcacion
from empleados.models import Sede
from vehiculos.models import Vehiculo

class Trueque(models.Model):
    monto = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    usuario1 = models.ForeignKey(Usuario, related_name='trueques_como_usuario1', on_delete=models.SET_NULL, null=True)
    usuario2 = models.ForeignKey(Usuario, related_name='trueques_como_usuario2', on_delete=models.SET_NULL, null=True)
    embarcacion1 = models.ForeignKey(Embarcacion, related_name='trueques_como_embarcacion1', on_delete=models.SET_NULL, null=True)
    embarcacion2 = models.ForeignKey(Embarcacion, related_name='trueques_como_embarcacion2', on_delete=models.SET_NULL, null=True)
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.SET_NULL, null=True)
    sede = models.ForeignKey(Sede, on_delete=models.SET_NULL, null=True)
    estado= models.CharField(max_length=50, default='Pendiente')

