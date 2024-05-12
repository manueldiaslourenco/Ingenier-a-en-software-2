from django.contrib.auth import authenticate
from usuarios.models import Usuario
from embarcaciones.models import Embarcacion
from publicaciones.models import Publicacion
from django.db import IntegrityError

def autenticar_usuario(username, password):
    usuario = authenticate(username=username, password=password)
    
    if usuario is not None:
        # El usuario se autenticó correctamente
        return usuario
    else:
        # La autenticación falló
        return None

def cargar_publicacion_back(lista, form):
    embarcacion = Embarcacion.objects.get(matricula= lista[1])

    # Obtén el usuario que será el dueño de la embarcación
    usuario = Usuario.objects.get(mail= lista[0])

    try:
        # Crea una nueva publicacion
        publicacion = Publicacion.objects.create(
            embarcacion= embarcacion,
            monto= lista[2],
            descripcion=lista[3],
            autor=usuario
        )
        publicacion.save()
        return True
    except IntegrityError:
        form.add_error('embarcacion', 'La embarcacion ingresada ya cuenta con una publicación.')
        return False
