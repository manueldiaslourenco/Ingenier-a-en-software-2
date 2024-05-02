from django.shortcuts import render, redirect, get_object_or_404
from usuarios.models import Usuario
from datetime import datetime

# Create your views here.

def redirigir_usuarios(request):
    return redirect('usuarios')

def calcular_edad(fecha_nacimiento):
    fecha_actual = datetime.now()
    edad = fecha_actual.year - fecha_nacimiento.year - ((fecha_actual.month, fecha_actual.day) < (fecha_nacimiento.month, fecha_nacimiento.day))
    return edad

def usuarios(request):
    usuarios = Usuario.objects.all()
    for usuario in usuarios:
        usuario.edad = calcular_edad(usuario.fecha_nacimiento)
    return render(request, 'usuarios/usuarios.html', {
        'usuarios' : usuarios
    })

def detalle_usuario(request, id):
    usuario = get_object_or_404(Usuario, id=id)
#Para cuando tengamos embarcaciones, vehiculos, publicaciones, ofertas
#   embarcaciones = Embarcacion.objects.filter(usuario_id=id)
    return render(request, 'usuarios/detalle.html', {
        'usuario':usuario,
#       'embarcaciones':embarcaciones,
    })