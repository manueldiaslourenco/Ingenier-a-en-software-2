from datetime import datetime, date, timedelta
from django.shortcuts import redirect
from django.core.mail import EmailMultiAlternatives
import random, string
from django.template.loader import get_template
from django.conf import settings


def calcular_edad(fecha_nacimiento):
    fecha_actual = datetime.now()
    edad = fecha_actual.year - fecha_nacimiento.year - ((fecha_actual.month, fecha_actual.day) < (fecha_nacimiento.month, fecha_nacimiento.day))
    return edad

def es_mayor_de_18(fecha_nacimiento):
    hace_18_años = date.today() - timedelta(days=365.25*18)
    return fecha_nacimiento <= hace_18_años    
    
def generar_contraseña_aleatoria():
    caracteres = string.ascii_letters + string.digits
    contraseña = ''.join(random.choice(caracteres) for _ in range(10))
    return contraseña

def send_email(mail, contraseña):
    email = EmailMultiAlternatives(
        'Tu cuenta se ha creado exitosamente!',
        'La contraseña para tu nueva cuenta es: %s' % contraseña,
        settings.EMAIL_HOST_USER,
        [mail],
    )
    email.send()