from django.db import models
from usuarios.models import Usuario
from trueques.models import Trueque

# Create your models here.

class Puntuacion(models.Model):
    calificacion = models.IntegerField()
    user_envio = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, related_name='puntuaciones_enviadas')
    user_recibio = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, related_name='puntuaciones_recibidas')
    contexto = models.ForeignKey(Trueque, on_delete=models.SET_NULL, null=True)
