from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from datetime import date, timedelta
from django.contrib.auth import authenticate


class UsuarioBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(mail=username)
            if user.check_password(password):
                return user
        except UserModel.DoesNotExist:
            return None

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None

def autenticar_usuario(correo, contraseña):
    # Intentar autenticar al usuario
    user = authenticate(username=correo, password=contraseña)
    
    if user is not None:
        # El usuario se autenticó correctamente
        return user
    else:
        # La autenticación falló
        return None

def es_mayor_de_18(fecha_nacimiento):
    hace_18_años = date.today() - timedelta(days=365.25*18)
    return fecha_nacimiento <= hace_18_años