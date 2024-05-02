from django.shortcuts import render, redirect, get_object_or_404
from usuarios.models import Usuario
from datetime import datetime

# Create your views here.

def index(request):
    return render(request, 'indexadmin.html')

def calcular_edad(fecha_nacimiento):
    fecha_actual = datetime.now()
    edad = fecha_actual.year - fecha_nacimiento.year - ((fecha_actual.month, fecha_actual.day) < (fecha_nacimiento.month, fecha_nacimiento.day))
    return edad

def usuarios(request):
    usuarios = Usuario.objects.all()
    for usuario in usuarios:
        usuario.edad = calcular_edad(usuario.fecha_nacimiento)
    return render(request, 'usuarios.html', {
        'usuarios' : usuarios
    })