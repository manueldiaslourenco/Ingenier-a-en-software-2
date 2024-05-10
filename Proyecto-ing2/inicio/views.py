from django.shortcuts import render
from django.shortcuts import redirect
from publicaciones.models import Publicacion

def redirigir_inicio(request):
    return redirect('home')

def inicio(request):
    publicaciones = Publicacion.objects.all()
    return render(request, 'index.html', {'publicaciones' : publicaciones})
