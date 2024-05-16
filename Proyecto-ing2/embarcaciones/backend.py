import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.utils import timezone
from .models import Embarcacion, ImagenEmbarcacion, TipoEmbarcacion
from usuarios.models import Usuario
from empleados.models import Sede


def guardar_imagenes(imagenes, embarcacion):
    fs = FileSystemStorage()
    for i, imagen in enumerate(imagenes, start=1):
        imagen_id = f"{embarcacion.id}{chr(96 + i)}.png"
        fs.save(imagen_id, imagen)

        ImagenEmbarcacion.objects.create(
            nombre_especifico=imagen_id,
            embarcacion=embarcacion,
        )

def cargar_embarcacion_back(lista, imagenes, form):
    sede = Sede.objects.get(nombre= lista[0])
    usuario = Usuario.objects.get(mail= lista[1])
    tipo = TipoEmbarcacion.objects.get(clase= lista[2])
    try:
        embarcacion = Embarcacion.objects.create(
            matricula= lista[3],
            modelo= lista[4],
            tipo=tipo,
            m_eslora= lista[5],  # eslora de la embarcación
            m_manga= lista[6],  # manga de la embarcación
            m_calado= lista[7],  # calado de la embarcación
            motor= lista[8],  # si la embarcación tiene motor
            deuda= lista[9],  # deuda de la embarcación
            sede=sede,
            dueño=usuario,
        )
        guardar_imagenes(imagenes, embarcacion)
        return True
    except IntegrityError:
        form.add_error('matricula', 'La matricula ingresada ya se encuentra registrada.')
        return False

def validar_extensiones(value):
    if not value.name.endswith(('.jpg', '.png')):
        raise ValidationError('No se pudo agregar la imagen por formato inválido (.jpg o .png).')
    
def eliminar_logicamente_embarcacion(objeto):
    timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
    objeto.matricula = '*' + objeto.matricula + timestamp
    objeto.save()

def eliminar_imagenes_y_objeto_tabla(id_embarcacion):
    imagenes = ImagenEmbarcacion.objects.filter(embarcacion_id=id_embarcacion)

    for imagen in imagenes:
        #ruta al archivo
        file_path = os.path.join(settings.MEDIA_ROOT, imagen.nombre_especifico)

        if os.path.isfile(file_path):
            os.remove(file_path)
        imagen.delete()