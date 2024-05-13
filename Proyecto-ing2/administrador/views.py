from django.shortcuts import render, redirect
from usuarios.models import Usuario
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from .backend import calcular_edad, es_mayor_de_18, generar_contraseña_aleatoria, send_email
from .forms import formularioRegistro, formularioRegistroEmpleado
from datetime import date
from django.contrib.auth.hashers import make_password
from empleados.models import EmpleConSede, Sede
from embarcaciones.models import Embarcacion

@login_required(login_url=reverse_lazy('home'))
def index(request):
    user = request.user
    if not user.is_superuser:
        return redirect('home')
    
    return render(request, 'index_admin.html')

@login_required(login_url=reverse_lazy('home'))
def empleados(request):
    user = request.user
    if not user.is_superuser:
        return redirect('home')
    
    empleados = Usuario.objects.filter(is_staff=True, is_superuser=False)
    for empleado in empleados:
        emple_sede = EmpleConSede.objects.get(user_id=empleado.id)
        sede = Sede.objects.get(id=emple_sede.sede_id)
        empleado.sede = sede.nombre
    return render(request, 'employees.html', {
        'empleados' : empleados
    })

@login_required(login_url=reverse_lazy('home'))
def cuestionario_crear_empleado(request):
    user = request.user
    if not user.is_superuser:
        return redirect('home')
    
    ok= False
    form= formularioRegistroEmpleado()
    #sedes = list(Sede.objects.all().values_list('nombre', flat=True))
    sedes = Sede.objects.all()
    if request.method == 'POST':
        form = formularioRegistroEmpleado(request.POST)
        if form.is_valid():
            email = form.cleaned_data['mail']
            sede = form.cleaned_data['sede']
            contraseña = generar_contraseña_aleatoria()
            usuario = Usuario(
                nombre="",
                apellido="",
                fecha_nacimiento=date.today(),
                telefono="0000000000",
                mail=email,
                password = make_password(contraseña),
                is_staff = True
            )
            try:
                #usr_emple = Usuario.objects.get(mail = email)
                #usr_emple.save()
                usuario.save()
                ok=True
                emple_sede = EmpleConSede.objects.create(
                    sede = sede,
                    user = usuario
                )
                emple_sede.save()
                send_email(email,contraseña)
            except IntegrityError:
                form.add_error('mail', 'El correo ingresado ya se encuentra registrado.')
    return render(request, 'create_employee.html', {'form': form, 'ok': ok, 'sedes': sedes})


@login_required(login_url=reverse_lazy('home'))
def usuarios(request):
    user = request.user
    if not user.is_superuser:
        return redirect('home')
    
    usuarios = Usuario.objects.filter(is_staff=False)
    for usuario in usuarios:
        usuario.edad = calcular_edad(usuario.fecha_nacimiento)
    return render(request, 'users.html', {
        'usuarios' : usuarios
    })

@login_required(login_url=reverse_lazy('home'))
def cuestionario_crear_usuario(request):
    user = request.user
    if not user.is_superuser:
        return redirect('home')
    
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
    return render(request, 'create_user.html', {'form': form, 'ok': ok})

@login_required(login_url=reverse_lazy('home'))
def bloquear_usuario(request):
    user = request.user
    if not user.is_superuser:
        return redirect('home')
    
    if request.method == 'POST':
        usuario_id = request.POST.get('usuario_id')
        usuario = Usuario.objects.get(id=usuario_id)
        usuario.is_blocked = True
        usuario.save()
    return redirect('lista usuarios')

@login_required(login_url=reverse_lazy('home'))
def desbloquear_usuario(request):
    user = request.user
    if not user.is_superuser:
        return redirect('home')
    
    if request.method == 'POST':
        usuario_id = request.POST.get('usuario_id')
        usuario = Usuario.objects.get(id=usuario_id)
        usuario.is_blocked = False
        usuario.save()
    return redirect('lista usuarios')

login_required(login_url=reverse_lazy('home'))
def embarcaciones(request):
    user = request.user
    if not user.is_superuser:
        return redirect('home')
    
    embarcaciones = Embarcacion.objects.all()
    return render(request, 'boats.html', {'embarcaciones' : embarcaciones})