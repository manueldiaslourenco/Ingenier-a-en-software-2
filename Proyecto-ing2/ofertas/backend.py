from usuarios.models import Usuario
from embarcaciones.models import Embarcacion
from vehiculos.models import Vehiculo
from .models import Oferta
from publicaciones.models import Publicacion
from django.db import IntegrityError


def crear_oferta_back(lista):
    usuario = Usuario.objects.get(mail= lista[0])
    publi= Publicacion.objects.get(id= lista[3])

    try:
        embarcacion = Embarcacion.objects.get(matricula= lista[1])

        Oferta.objects.create(
            monto= lista[2],
            autor=usuario,
            embarcacion_ofertada= embarcacion,
            vehiculo_ofertado= None,
            publicacion= publi
        )
    
    except Embarcacion.DoesNotExist:
        vehiculo= Vehiculo.objects.get(patente= lista[1])

        Oferta.objects.create(
            monto= lista[2],
            autor=usuario,
            embarcacion_ofertada= None,
            vehiculo_ofertado= vehiculo,
            publicacion= publi
        )