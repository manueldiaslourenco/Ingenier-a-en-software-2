from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from .forms import formularioCrearPublicacion, formularioEditarPublicacion
from embarcaciones.models import Embarcacion, ImagenEmbarcacion
from ofertas.models import Oferta
from .models import Publicacion
from .backend import cargar_publicacion_back, eliminar_publicacion_fisica

@login_required(login_url=reverse_lazy('iniciar sesion'))
def cuestionario_cargar_publicacion(request):
    usuario_actual = request.user
    
    embarcaciones = Embarcacion.objects.filter(dueño = usuario_actual)
    embarcaciones = embarcaciones.exclude(matricula__startswith='*')
    embarcaciones = embarcaciones.filter(publicacion__isnull=True)
    embarcaciones = embarcaciones.filter(oferta__isnull=True)
    
    if embarcaciones:
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
        mensaje = "Para crear una publicación, primero debes cargar una embarcación desde tu perfil. (Recorda que para publicar una embarcacion la misma no debe terner ofertas)"
        return render(request, 'index.html', {'mensaje': mensaje})
    
def ver_detalle_publicacion(request, id_publicacion, eliminar):
    try:
        unaPublicacion = Publicacion.objects.get(id=id_publicacion)
        imagenes= ImagenEmbarcacion.objects.filter(embarcacion= unaPublicacion.embarcacion.id)
        ofertas= Oferta.objects.exclude(autor__is_blocked=True).filter(publicacion= id_publicacion).filter(estado= 'Pendiente')

        # Para 'Aceptar oferta'
        ok = False
        acepto = False
        oferta_id = 0
        if request.method == 'POST':
            acepto = request.POST.get('acepto')
            oferta_id = request.POST.get('oferta_id')
            ok = request.POST.get('ok')

        return render(request, 'post_detail.html', {'imagenes': imagenes,
                                                    'publicacion': unaPublicacion,
                                                    'ofertas': ofertas,
                                                    'ok': ok,
                                                    'acepto': acepto,
                                                    'oferta_id': oferta_id,
                                                    'eliminar':eliminar})
    except Embarcacion.DoesNotExist:
        return render(request, '404_not_found.html')

@login_required(login_url=reverse_lazy('iniciar sesion'))
def eliminar_publicacion_vista(request, id_publicacion):
    eliminar_publicacion_fisica(id_publicacion)
    return redirect('home')

@login_required(login_url=reverse_lazy('iniciar sesion'))
def editar_publicacion(request, id_publicacion):

    ok = False
    publicacion = Publicacion.objects.get(id=id_publicacion)
    imagenes= ImagenEmbarcacion.objects.filter(embarcacion= publicacion.embarcacion.id)

    if request.method == 'POST':
        form = formularioEditarPublicacion(request.POST)
        if form.is_valid():
            publicacion.descripcion = form.cleaned_data.get('descripcion')
            publicacion.save()
            ok = True
    else:
        form = formularioEditarPublicacion(initial={
            'descripcion':publicacion.descripcion
        })
    
    context = {
        'ok':ok,
        'publicacion':publicacion,
        'imagenes':imagenes,
        'form':form
    }

    return render(request, 'edit_post.html', {'context':context})
