from django.db import models
from usuarios.models import Usuario

class TipoVehiculo(models.Model):
    clase = models.CharField(max_length=50, unique=True)

class Vehiculo(models.Model):
    patente = models.CharField(max_length=100, unique=True)
    marca = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    tipo = models.ForeignKey(TipoVehiculo, on_delete=models.SET_NULL, null=True)
    año_fabricacion = models.DecimalField(max_digits=4, decimal_places=0, default=2000)
    kilometraje = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    dueño = models.ForeignKey(Usuario, on_delete=models.CASCADE)

class ImagenVehiculo(models.Model):
    nombre_especifico = models.CharField(max_length=100)
    vehiculo = models.ForeignKey(Vehiculo, on_delete= models.CASCADE)