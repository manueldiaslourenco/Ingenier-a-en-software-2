from django.db import models
from usuarios.models import Usuario
from embarcaciones.models import Embarcacion
from vehiculos.models import Vehiculo
from publicaciones.models import Publicacion


class Oferta(models.Model):
    monto = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    autor = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True)
    vehiculo_ofertado = models.ForeignKey(Vehiculo, on_delete=models.SET_NULL, null=True)
    embarcacion_ofertada = models.ForeignKey(Embarcacion, on_delete=models.SET_NULL, null=True)
    publicacion= models.ForeignKey(Publicacion, on_delete=models.CASCADE)