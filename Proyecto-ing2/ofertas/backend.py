from usuarios.models import Usuario
from embarcaciones.models import Embarcacion
from vehiculos.models import Vehiculo
from .models import Oferta
from publicaciones.models import Publicacion
from django.db import IntegrityError
from django.conf import settings
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives


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

def send_mail(mail, sede, telefono_publicante, embarcacion):
    context = {'mail':mail, 'sede':sede, 'telefono_publicante': telefono_publicante, 'embarcacion':embarcacion}

    template = get_template('mail_offer.html')
    content = template.render(context)

    email = EmailMultiAlternatives(
        'Tu oferta ha sido aceptada',
        'Hemos recibido la notificacion de que tu oferta ha sido aceptada',
        settings.EMAIL_HOST_USER,
        [mail],
    )
    email.attach_alternative(content, 'text/html')
    email.send()

def send_mail_oferta_rechazada(mail, embarcacion):
    context = {'mail':mail, 'embarcacion':embarcacion}

    template = get_template('mail_reject_offer.html')
    content = template.render(context)

    email = EmailMultiAlternatives(
        'Tu oferta ha sido rechazada',
        'Hemos recibido la notificacion de que tu oferta ha sido rechazada',
        settings.EMAIL_HOST_USER,
        [mail],
    )
    email.attach_alternative(content, 'text/html')
    email.send()

def eliminar_oferta(oferta_id):
    oferta = Oferta.objects.get(id=oferta_id)
    oferta.delete()