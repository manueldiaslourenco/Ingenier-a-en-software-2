from django.core.files.storage import FileSystemStorage
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from .models import Embarcacion, ImagenEmbarcacion, TipoEmbarcacion
from usuarios.models import Usuario
from empleados.models import Sede


def guardar_imagenes(imagenes, embarcacion):
    fs = FileSystemStorage()
    for i, imagen in enumerate(imagenes, start=1):
    # Crear el identificador único de la imagen
        imagen_id = f"{embarcacion.id}{chr(96 + i)}.png"
    
    # Guardar la imagen en el sistema de archivos
        fs.save(imagen_id, imagen)
    
    # Crear el objeto ImagenEmbarcacion y guardarlo en la base de datos
        ImagenEmbarcacion.objects.create(
            nombre_especifico=imagen_id,
            embarcacion=embarcacion,
        )

def cargar_embarcacion_back(lista, imagenes, form):
    sede = Sede.objects.get(nombre= lista[0])

    # Obtén el usuario que será el dueño de la embarcación
    usuario = Usuario.objects.get(mail= lista[1])

    # Obtén el tipo de embarcación
    tipo = TipoEmbarcacion.objects.get(clase= lista[2])

    # Crea una nueva embarcación
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
    except IntegrityError:
        form.add_error('matricula', 'La matricula ingresada ya se encuentra registrada.')

def validar_extensiones(value):
    if not value.name.endswith(('.jpg', '.png')):
        raise ValidationError('Por favor, sube una imagen .jpg o .png')