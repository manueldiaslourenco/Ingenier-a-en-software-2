from django.shortcuts import render
from django.shortcuts import redirect
from publicaciones.models import Publicacion
from embarcaciones.models import ImagenEmbarcacion

def redirigir_inicio(request):
    return redirect('home')

def inicio(request):
    publicaciones = Publicacion.objects.all()
    for publicacion in publicaciones:
        post_image = ImagenEmbarcacion.objects.get(embarcacion=publicacion.embarcacion.id)
        publicacion.imagen = post_image.nombre_especifico
    return render(request, 'index.html', {'publicaciones' : publicaciones})
