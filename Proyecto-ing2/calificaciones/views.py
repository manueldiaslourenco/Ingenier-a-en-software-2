from django.shortcuts import render, redirect
from .models import Puntuacion
from trueques.models import Trueque
from usuarios.models import Usuario
# Create your views here.

def calificar_usuario(request, id_trueque, id_usuario_envio, id_usuario_recibio):
    truqeue= Trueque.objects.get(id= id_trueque)
    user_e= Usuario.objects.get(id= id_usuario_envio)
    user_r= Usuario.objects.get(id= id_usuario_recibio)
    if request.method == 'POST':
        rating = request.POST.get('rating')
        Puntuacion.objects.create(
            calificacion= rating,
            user_envio= user_e,
            user_recibio=  user_r,
            contexto= truqeue
        )
    return redirect('ver detalle trueque', id_trueque)