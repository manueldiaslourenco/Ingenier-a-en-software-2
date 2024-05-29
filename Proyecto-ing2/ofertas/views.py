from django.shortcuts import render, redirect
from embarcaciones.models import Embarcacion
from vehiculos.models import Vehiculo
from publicaciones.models import Publicacion
from trueques.models import Trueque
from .models import Oferta
from .forms import formularioCrearOferta
from .backend import crear_oferta_back
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy

@login_required(login_url=reverse_lazy('iniciar sesion'))
def publicar_oferta(request, id_publi):
    usuario_actual = request.user
    embarcaciones = Embarcacion.objects.exclude(matricula__startswith='*').filter(dueño=usuario_actual).exclude(id__in=Publicacion.objects.values_list('embarcacion', flat=True))
    vehiculos = Vehiculo.objects.exclude(patente__startswith='*').filter(dueño=usuario_actual)
    if embarcaciones or vehiculos:
        ok=False
        form = formularioCrearOferta()
        matriculas_embarcaciones = list(embarcaciones.values_list('matricula', flat=True))
        patentes_vehiculos= list(vehiculos.values_list('patente', flat=True))

        if request.method == 'POST':
            form = formularioCrearOferta(request.POST)
            if form.is_valid():
                lista= []
                lista.append(usuario_actual.mail)
                lista.append(form.cleaned_data['articulo_cambio'])
                lista.append(form.cleaned_data['monto'])
                lista.append(id_publi)
                crear_oferta_back(lista)
                ok=True
        return render(request, 'register_offer.html' , {'ok': ok,
                                                         'id_publi': id_publi,
                                                         'embarcaciones': matriculas_embarcaciones,
                                                         'vehiculos': patentes_vehiculos})
    else:
        mensaje = 'Para ofertar, primero debes cargar una embarcación o un vehiculo desde tu perfil.'
        return render(request, 'register_offer.html' , {'mensaje': mensaje, 'id_publi': id_publi,})
    

"""cuando se acpeta la oferta que se esconda,
cuando se valide el trueque se elimine la publicaicon 
cuando se rechza el trueque se vuelve a mostar """

@login_required(login_url=reverse_lazy('iniciar sesion'))
def aceptar_oferta(request):
    try:
        publicacion_id = request.POST.get('publicacion_id')
        oferta_id = request.POST.get('oferta_id')
        print('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA')
        print(publicacion_id)
        print(oferta_id)
        print('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA')
        publicacion = Publicacion.objects.get(id=publicacion_id)
        oferta = Oferta.objects.get(id=oferta_id)

        publicacion.oculta = True
        publicacion.save()

        ofertas_relacionadas = Oferta.objects.filter(publicacion=publicacion)
        for oferta_relacionada in ofertas_relacionadas:
            if oferta_relacionada.id != oferta.id:
                oferta_relacionada.estado = "Pausada"
                oferta_relacionada.save()
        
        oferta.oculta = True
        oferta.save()
        
        Trueque.objects.create(
            monto=oferta.monto,
            usuario1=publicacion.autor,
            usuario2=oferta.autor,
            embarcacion1=publicacion.embarcacion,
            embarcacion2=oferta.embarcacion_ofertada,
            vehiculo=oferta.vehiculo_ofertado,
            sede=publicacion.embarcacion.sede,
            estado="Pendiente"
        )
    except:
        return render(request, '404_not_found.html')
    return redirect ('home')
