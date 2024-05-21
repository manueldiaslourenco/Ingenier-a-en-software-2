from django.shortcuts import render
from django.shortcuts import redirect
from publicaciones.models import Publicacion
from embarcaciones.models import ImagenEmbarcacion
from usuarios.models import Usuario

def redirigir_inicio(request):
    return redirect('home')

def inicio(request):
    publicaciones= Publicacion.objects.exclude(autor__is_blocked= True)
    for publicacion in publicaciones:
        post_image = ImagenEmbarcacion.objects.filter(embarcacion=publicacion.embarcacion.id)
        publicacion.imagen = post_image[0].nombre_especifico
    return render(request, 'index.html', {'publicaciones' : publicaciones})
