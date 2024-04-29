from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from .forms import formularioRegistro
from .forms import formularioIniciarSesion
from .forms import formularioRecuperarContraseña

def cuestionario_iniciar_sesion(request):
    form = formularioIniciarSesion()
    if request.method == 'POST':
        form = formularioIniciarSesion(request.POST)
        if form.is_valid():
            print(formularioIniciarSesion)
    return render(request, 'login.html', {'form': form})


def cuestionario_crear_cuenta(request):

    #Los print son imprimir en pantalla de prueba.
    form= formularioRegistro()
    if request.method == 'POST':
        form = formularioRegistro(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            apellido= form.cleaned_data['apellido']
            dni= form.cleaned_data['dni']
            fecha_nacimiento= form.cleaned_data['fecha_nacimiento']
            telefono= form.cleaned_data['telefono']
            email = form.cleaned_data['mail']
            contraseña= form.cleaned_data['contraseña']

            # Guardo datos en una lista
            unaP = [nombre,apellido,dni,fecha_nacimiento,telefono,email,contraseña]
            
            print(unaP)
            return redirect('home')
        print('cuestionarioRegistro no valida')
    return render(request, 'signup.html', {'form': form})

def recuperar_contraseña(request):
    form= formularioRecuperarContraseña()
    if request.method == 'POST':
        #mail esta en la base de datos redirijo a ingresar la nueva contraseña.
        form= formularioRecuperarContraseña(request.POST)
        #if mail es valido
        print(form)
        if form.is_valid():
        #redirect parte 2
            return redirect('home')
    return render(request, 'forget_password.html', {'form': form})
