from django.shortcuts import render, redirect
from usuarios.models import Usuario
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from .backend import calcular_edad, es_mayor_de_18, chequear_admin
from .forms import formularioRegistro

@login_required(login_url=reverse_lazy('home'))
def index(request):
    chequear_admin(request.user)
    
    return render(request, 'indexadmin.html')

@login_required(login_url=reverse_lazy('home'))
def usuarios(request):
    chequear_admin(request.user)
    
    usuarios = Usuario.objects.filter(is_staff=False)
    for usuario in usuarios:
        usuario.edad = calcular_edad(usuario.fecha_nacimiento)
    return render(request, 'usuarios.html', {
        'usuarios' : usuarios
    })

@login_required(login_url=reverse_lazy('home'))
def empleados(request):
    chequear_admin(request.user)
    
    usuarios = Usuario.objects.filter(is_staff=True).filter(is_superuser=False)
    return render(request, 'empleados.html', {
        'usuarios' : usuarios
    })

@login_required(login_url=reverse_lazy('home'))
def cuestionario_crear_cuenta(request):
    chequear_admin(request.user)
    
    ok= False
    form= formularioRegistro()
    if request.method == 'POST':
        form = formularioRegistro(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            apellido= form.cleaned_data['apellido']
            telefono= form.cleaned_data['telefono']
            email = form.cleaned_data['mail']
            contraseña= form.cleaned_data['contraseña']
            fecha_nacimiento= form.cleaned_data['fecha_nacimiento']
            if es_mayor_de_18(fecha_nacimiento):
                usuario = Usuario(
                    nombre=nombre,
                    apellido=apellido,
                    fecha_nacimiento=fecha_nacimiento,
                    telefono=telefono,
                    mail=email,
                    password=contraseña
                )
                try:
                    usuario.save()
                    ok=True
                except IntegrityError:
                    form.add_error('mail', 'El correo ingresado ya se encuentra registrado.')
            else:
                form.add_error('fecha_nacimiento', 'Debe ser mayor de edad (+18) para registrarse.')
    return render(request, 'crear_usuario.html', {'form': form, 'ok': ok})

@login_required(login_url=reverse_lazy('home'))
def bloquear_usuario(request):
    chequear_admin(request.user)
    
    if request.method == 'POST':
        usuario_id = request.POST.get('usuario_id')
        usuario = Usuario.objects.get(id=usuario_id)
        usuario.is_blocked = True
        usuario.save()
    return redirect('usuarios')

@login_required(login_url=reverse_lazy('home'))
def desbloquear_usuario(request):
    chequear_admin(request.user)
    
    if request.method == 'POST':
        usuario_id = request.POST.get('usuario_id')
        usuario = Usuario.objects.get(id=usuario_id)
        usuario.is_blocked = False
        usuario.save()
    return redirect('usuarios')