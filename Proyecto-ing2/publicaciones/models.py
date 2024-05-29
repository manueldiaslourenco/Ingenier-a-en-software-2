from django.db import models
from usuarios.models import Usuario
from embarcaciones.models import Embarcacion

class Publicacion(models.Model):
    monto = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    autor = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True)
    embarcacion = models.OneToOneField(Embarcacion, on_delete=models.SET_NULL, null=True)
    descripcion = models.CharField(max_length=250)
    oculta = models.BooleanField(default=False)