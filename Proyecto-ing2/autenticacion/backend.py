from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from datetime import date, timedelta
from django.contrib.auth import authenticate
from django.conf import settings
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
import binascii, os

class UsuarioBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            usuario = UserModel.objects.get(mail=username)
            if usuario.check_password(password):
                return usuario
        except UserModel.DoesNotExist:
            return None

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None

def autenticar_usuario(username, password):
    usuario = authenticate(username=username, password=password)
    
    if usuario is not None:
        # El usuario se autenticó correctamente
        return usuario
    else:
        # La autenticación falló
        return None
    
def generate_key():
    return binascii.hexlify(os.urandom(20)).decode()

def send_email(mail, token):
    context = {'mail':mail, "token":token}

    template = get_template('mail.html')
    content = template.render(context)

    email = EmailMultiAlternatives(
        'Solicitud de cambio de contraseña',
        'Hemos recibido una solicitud de cambio de contraseña',
        settings.EMAIL_HOST_USER,
        [mail],
    )
    email.attach_alternative(content, 'text/html')
    email.send()

    
def es_mayor_de_18(fecha_nacimiento):
    hace_18_años = date.today() - timedelta(days=365.25*18)
    return fecha_nacimiento <= hace_18_años