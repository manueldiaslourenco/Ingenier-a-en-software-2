from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from .forms import formularioCrearPublicacion
from embarcaciones.models import Embarcacion, ImagenEmbarcacion
from .models import Publicacion
from .backend import cargar_publicacion_back

@login_required(login_url=reverse_lazy('iniciar sesion'))
def cuestionario_cargar_publicacion(request):
    usuario_actual = request.user
    embarcaciones = Embarcacion.objects.exclude(matricula__startswith='*').filter(dueño=usuario_actual)
    tiene_embarcaciones = embarcaciones.exists()
    
    if tiene_embarcaciones:
        ok=False
        form = formularioCrearPublicacion()
        usuario_actual = request.user
        matriculas_embarcaciones = list(embarcaciones.values_list('matricula', flat=True))
        
        if request.method == 'POST':
            form = formularioCrearPublicacion(request.POST)
            ok= False
            if form.is_valid():
                usuario_actual_mail = request.user.mail
                lista= []
                lista.append(usuario_actual_mail)
                lista.append(form.cleaned_data['embarcacion'])
                lista.append(form.cleaned_data['monto'])
                lista.append(form.cleaned_data['descripcion'])
                ok = cargar_publicacion_back(lista, form)

        return render(request, 'register_post.html', {'form': form, 'ok': ok, 'embarcaciones':  matriculas_embarcaciones})
    else:
        mensaje = "Para crear una publicación, primero debes cargar una embarcación desde tu perfil."
        return render(request, 'index.html', {'mensaje': mensaje})
    
@login_required(login_url=reverse_lazy('home'))
def ver_detalle_publicacion(request, id_publicacion):
    try:
        unaPublicacion = Publicacion.objects.get(id=id_publicacion)
        if unaPublicacion.autor.id == request.user.id or request.user.is_superuser:
            imagenes= ImagenEmbarcacion.objects.filter(embarcacion= unaPublicacion.embarcacion.id)
            return render(request, 'post_detail.html', {'imagenes': imagenes, 'publicacion':  unaPublicacion})
        else:
            return render(request, '404_not_found.html')
    except Embarcacion.DoesNotExist:
        return render(request, '404_not_found.html')
