from django.shortcuts import render
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
        return render(request, 'trueque_detail.html', {'mensaje': mensaje})
    else:
        return render(request, 'trueque_detail.html')