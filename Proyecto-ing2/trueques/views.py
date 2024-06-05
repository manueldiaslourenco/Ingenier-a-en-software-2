from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from datetime import datetime, timedelta
from .models import Trueque
from embarcaciones.models import ImagenEmbarcacion
from vehiculos.models import ImagenVehiculo

# Create your views here.

@login_required(login_url=reverse_lazy('iniciar sesion'))
def ver_trueque(request, id_trueque):

    trueque= Trueque.objects.get(id= id_trueque)
    imagenes_publicacion = ImagenEmbarcacion.objects.filter(embarcacion= trueque.embarcacion1.id)
    if trueque.embarcacion2:
        imagenes_oferta = ImagenEmbarcacion.objects.filter(embarcacion= trueque.embarcacion2.id)
    elif trueque.vehiculo:
        imagenes_oferta = ImagenVehiculo.objects.filter(vehiculo= trueque.vehiculo.id)
    fecha_actual = datetime.now().date()
    
    if (fecha_actual - trueque.fecha_inicio.date()) >= timedelta(days=30):
        mensaje= "Pasaron mas de 30 dias del incio del trueque se recomienda su cancelación."
        return render(request, 'trueque_detail.html', {'mensaje': mensaje, 'trueque':trueque, 'imagenes_publicacion': imagenes_publicacion, 'imagenes_oferta':imagenes_oferta})
    else:
        return render(request, 'trueque_detail.html', {'trueque':trueque, 'imagenes_publicacion': imagenes_publicacion, 'imagenes_oferta':imagenes_oferta})
    
@login_required(login_url=reverse_lazy('iniciar sesion'))
def completar_trueque(request, id_trueque):

    trueque= Trueque.objects.get(id= id_trueque)
    trueque.estado= 'Completado'
    trueque.save()

    embarcacion= trueque.embarcacion1
    embarcacion.dueño= trueque.usuario2
    embarcacion.save()
    if trueque.vehiculo_id:
        vehiculo= trueque.vehiculo
        vehiculo.dueño= trueque.usuario1
        vehiculo.save()
    else:
        embarcacion2= trueque.embarcacion2
        embarcacion2.dueño= trueque.usuario1
        embarcacion2.save()

    return redirect('ver detalle trueque', id_trueque)

@login_required(login_url=reverse_lazy('iniciar_sesion'))
def cancelar_trueque(request, id_trueque):
    trueque = Trueque.objects.get(id= id_trueque)
    trueque.estado = 'Cancelado'
    trueque.save()

    return redirect('ver detalle trueque', id_trueque)