from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from datetime import datetime, timedelta
from .models import Trueque

# Create your views here.

@login_required(login_url=reverse_lazy('iniciar sesion'))
def ver_trueque(request, id_trueque):

    trueque= Trueque.objects.get(id= id_trueque)
    fecha_actual = datetime.now().date()
    
    if (fecha_actual - trueque.fecha_inicio.date()) >= timedelta(days=30):
        mensaje= "Pasaron mas de 30 dias del incio del trueque se recomienda su cancelación."
        return render(request, 'trueque_detail.html', {'mensaje': mensaje,
                                                       'trueque': trueque})
    else:
        return render(request, 'trueque_detail.html', {'trueque': trueque})
    
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