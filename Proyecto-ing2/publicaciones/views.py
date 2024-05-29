from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from .forms import formularioCrearPublicacion
from embarcaciones.models import Embarcacion, ImagenEmbarcacion
from ofertas.models import Oferta
from usuarios.models import Usuario
from .models import Publicacion
from .backend import cargar_publicacion_back

@login_required(login_url=reverse_lazy('iniciar sesion'))
def cuestionario_cargar_publicacion(request):
    usuario_actual = request.user
    embarcaciones = Embarcacion.objects.exclude(matricula__startswith='*').filter(dueño=usuario_actual)
    embarcaciones_con_publicacion = Publicacion.objects.values_list('embarcacion_id', flat=True)
    embarcaciones = embarcaciones.exclude(id__in=embarcaciones_con_publicacion)

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
    
def ver_detalle_publicacion(request, id_publicacion):
    try:
        unaPublicacion = Publicacion.objects.get(id=id_publicacion)
        imagenes= ImagenEmbarcacion.objects.filter(embarcacion= unaPublicacion.embarcacion.id)
        ofertas= Oferta.objects.exclude(autor__is_blocked=True)
        
        #Para 'Aceptar oferta'
        ok = False
        acepto = False
        oferta_id = 0
        if request.method == 'POST':
            acepto = request.POST.get('acepto')
            oferta_id = request.POST.get('oferta_id')
            ok = True
        
        return render(request, 'post_detail.html', {'imagenes': imagenes,
                                                    'publicacion': unaPublicacion,
                                                    'ofertas': ofertas,
                                                    'ok': ok,
                                                    'acepto':acepto,
                                                    'oferta_id':oferta_id})
    except Embarcacion.DoesNotExist:
        return render(request, '404_not_found.html')
