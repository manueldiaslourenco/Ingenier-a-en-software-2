from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from .forms import cuestionarioRegistro

def mi_vista(request):
    form = cuestionarioRegistro()
    if request.method == 'POST':
        form = cuestionarioRegistro(request.POST)
        if form.is_valid():
            print(cuestionarioRegistro)
    return render(request, 'login.html', {'form': form})


def formulario_crear_cuenta(request):

    #Los print son imprimir en pantalla de prueba.
    form= cuestionarioRegistro()
    if request.method == 'POST':
        form = cuestionarioRegistro(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            apellido= form.cleaned_data['apellido']
            email = form.cleaned_data['mail']
            dni= form.cleaned_data['dni']
            contraseña= form.cleaned_data['contraseña']
            # Guardo datos en una lista
            unaP = [nombre,apellido,email,contraseña,dni]
            
            print(unaP)
            return redirect('home')
        print('cuestionarioRegistro no valida')
    return render(request, 'signup.html', {'form': form})
