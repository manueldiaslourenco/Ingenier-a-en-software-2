from django.db import IntegrityError
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import login, logout
from .forms import formularioIniciarSesion, formularioRecuperarContraseña, formularioRegistro
from usuarios.models import Usuario
from .backend import autenticar_usuario, es_mayor_de_18

def cuestionario_iniciar_sesion(request):
    ok=False
    form = formularioIniciarSesion()
    usuario_actual = request.user
    if usuario_actual.is_authenticated:
        ok= True
    if request.method == 'POST':
        form = formularioIniciarSesion(request.POST)
        if form.is_valid():
            usuario = autenticar_usuario(username=form.cleaned_data['mail'], password=form.cleaned_data['password'])
        
            if usuario is not None:
                print("El usuario se autenticó correctamente.")
                if usuario.is_superuser:
                    login(request, usuario)
                    return redirect('admin')
                #queda hacer empleado
                elif not usuario.is_blocked: 
                    login(request, usuario)
                    return redirect('home')
                else:
                    form.add_error('password', 'La cuenta ingresada se encuentra bloqueada.')
            else:
                form.add_error('password', 'Las credenciales ingresadas no son correspondientes.')
    return render(request, 'login.html', {'form': form, 'ok': ok})

def cerrar_sesion(request):
    logout(request)
    return  redirect('home')

def cuestionario_crear_cuenta(request):
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
    return render(request, 'signup.html', {'form': form, 'ok': ok})

def recuperar_contraseña(request):
    form= formularioRecuperarContraseña()
    if request.method == 'POST':
        #mail esta en la base de datos redirijo a ingresar la nueva contraseña.
        form= formularioRecuperarContraseña(request.POST)
        if form.is_valid():
        #no me toquen lo de abajo que estoy haciendo pruebas    
        #redirect parte 2
            #usuario = Usuario.objects.get(id=2)
        #Elimina el usuario
            #usuario.delete()
            return redirect('home')
    return render(request, 'forget_password.html', {'form': form})
