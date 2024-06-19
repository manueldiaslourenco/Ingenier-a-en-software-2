from django.core.files.storage import FileSystemStorage
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from usuarios.models import Usuario
from .models import Vehiculo, ImagenVehiculo, TipoVehiculo
from django.utils import timezone
import os
from django.conf import settings



def validar_extensiones(value):
    if not value.name.endswith(('.jpg', '.png')):
        raise ValidationError('No se pudo agregar la imagen por formato inválido (.jpg o .png).')

def guardar_imagenes(imagenes, vehiculo):
    ruta = 'vehiculos/static/imagenes_vehiculos'
    fs = FileSystemStorage(location = ruta)
    for i, imagen in enumerate(imagenes, start=1):
        imagen_id = f"{vehiculo.id}{chr(96 + i)}.png"
        fs.save(imagen_id, imagen)

        ImagenVehiculo.objects.create(
            nombre_especifico = imagen_id,
            vehiculo = vehiculo,
        )

def cargar_vehiculo_back(lista, imagenes, form):
    usuario = Usuario.objects.get(mail = lista[0])
    tipo = TipoVehiculo.objects.get(clase = lista[1])
    try:
        vehiculo = Vehiculo.objects.create(
            patente = lista[2],
            marca = lista[3],
            modelo = lista[4],
            año_fabricacion = lista[5],
            kilometraje = lista[6],
            tipo = tipo,
            dueño=usuario,
        )
        guardar_imagenes(imagenes, vehiculo)
        return True
    except IntegrityError:
        form.add_error('patente', 'La patente ingresada ya se encuentra registrada.')
        return False

def eliminar_logicamente_vehiculo(objeto):
    timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
    objeto.patente = '*' + objeto.patente + timestamp
    objeto.save()

def eliminar_imagenes_y_objeto_tabla(id_vehiculo):
    imagenes = ImagenVehiculo.objects.filter(vehiculo_id=id_vehiculo)

    for imagen in imagenes:
        #ruta al archivo
        file_path = os.path.join(settings.MEDIA_ROOT, imagen.nombre_especifico)

        if os.path.isfile(file_path):
            os.remove(file_path)
        imagen.delete()