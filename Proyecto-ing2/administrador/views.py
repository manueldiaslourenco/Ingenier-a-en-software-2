from django.shortcuts import render, redirect, get_object_or_404
from usuarios.models import Usuario
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy

@login_required(login_url=reverse_lazy('home'))
def index(request):
    usuario_actual = request.user
    if not usuario_actual.is_superuser:
        return redirect('home')
    return render(request, 'indexadmin.html')

def calcular_edad(fecha_nacimiento):
    fecha_actual = datetime.now()
    edad = fecha_actual.year - fecha_nacimiento.year - ((fecha_actual.month, fecha_actual.day) < (fecha_nacimiento.month, fecha_nacimiento.day))
    return edad

@login_required(login_url=reverse_lazy('home'))
def usuarios(request):
    usuario_actual = request.user
    if not usuario_actual.is_superuser:
        return redirect('home')
    
    usuarios = Usuario.objects.all()
    for usuario in usuarios:
        usuario.edad = calcular_edad(usuario.fecha_nacimiento)
    return render(request, 'usuarios.html', {
        'usuarios' : usuarios
    })