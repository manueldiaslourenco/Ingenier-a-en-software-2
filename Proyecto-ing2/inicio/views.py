from django.shortcuts import render
from django.shortcuts import redirect
from publicaciones.models import Publicacion
from embarcaciones.models import ImagenEmbarcacion
from usuarios.models import Usuario

def redirigir_inicio(request):
    return redirect('home')

def inicio(request):
    user = request.user
    publicaciones= Publicacion.objects.exclude(autor__is_blocked= True).exclude(oculta=True)

    mensaje_error = None

    if request.method == 'POST':
        catamaran = bool(request.POST.get('catamaran'))
        crucero = bool(request.POST.get('crucero'))
        lancha = bool(request.POST.get('lancha'))
        velero = bool(request.POST.get('velero'))
        publicaciones_filtradas = []
        if (catamaran or crucero or lancha or velero):
            if (catamaran):
                publicaciones_filtradas += publicaciones.filter(embarcacion__tipo__clase='Catamaran')
            if (crucero):
                publicaciones_filtradas += publicaciones.filter(embarcacion__tipo__clase='Cucero')
            if (lancha):
                publicaciones_filtradas += publicaciones.filter(embarcacion__tipo__clase='Lancha')
            if (velero):
                publicaciones_filtradas += publicaciones.filter(embarcacion__tipo__clase='Velero')
            publicaciones_filtradas.sort(key=lambda publicacion: publicacion.id)
            publicaciones = publicaciones_filtradas

    checkboxes = {
        'catamaran': bool(request.POST.get('catamaran')),
        'crucero': bool(request.POST.get('crucero')),
        'lancha': bool(request.POST.get('lancha')),
        'velero': bool(request.POST.get('velero')),
    }

    for publicacion in publicaciones:
        post_image = ImagenEmbarcacion.objects.filter(embarcacion=publicacion.embarcacion.id)
        publicacion.imagen = post_image[0].nombre_especifico
    return render(request, 'index.html', {'publicaciones' : publicaciones,
                                          'user':user,
                                          'mensaje_error':mensaje_error,
                                          'checkboxes':checkboxes})