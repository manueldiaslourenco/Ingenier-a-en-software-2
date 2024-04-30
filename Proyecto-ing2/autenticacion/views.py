from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from .forms import formularioRegistro
from .forms import formularioIniciarSesion
from .forms import formularioRecuperarContraseña
from usuarios.models import Usuario

def cuestionario_iniciar_sesion(request):
    form = formularioIniciarSesion()
    if request.method == 'POST':
        form = formularioIniciarSesion(request.POST)
        if form.is_valid():
            return redirect('home')
    return render(request, 'login.html', {'form': form})


def cuestionario_crear_cuenta(request):

    #Los print son imprimir en pantalla de prueba.
    form= formularioRegistro()
    if request.method == 'POST':
        form = formularioRegistro(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            apellido= form.cleaned_data['apellido']
            fecha_nacimiento= form.cleaned_data['fecha_nacimiento']
            telefono= form.cleaned_data['telefono']
            email = form.cleaned_data['mail']
            contraseña= form.cleaned_data['contraseña']

            usuario = Usuario(
                nombre=nombre,
                apellido=apellido,
                fecha_nacimiento=fecha_nacimiento,
                telefono=telefono,
                mail=email,
                contraseña=contraseña
            )
            #usuario.save()
            
            return redirect('home')
    return render(request, 'signup.html', {'form': form})

def recuperar_contraseña(request):
    form= formularioRecuperarContraseña()
    if request.method == 'POST':
        #mail esta en la base de datos redirijo a ingresar la nueva contraseña.
        form= formularioRecuperarContraseña(request.POST)
        #if mail es valido
        print(form)
        if form.is_valid():
        #no me toquen lo de abajo que estoy haciendo pruebas    
        #redirect parte 2
            #usuario = Usuario.objects.get(id=1)
        # Elimina el usuario
           # usuario.delete()
            return redirect('home')
    return render(request, 'forget_password.html', {'form': form})
