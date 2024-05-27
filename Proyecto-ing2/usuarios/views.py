from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from embarcaciones.models import Embarcacion
from publicaciones.models import Publicacion
from vehiculos.models import Vehiculo
from ofertas.models import Oferta

@login_required(login_url=reverse_lazy('home'))
def ver_perfil(request, id):
    usuario_actual = request.user
    UserModel = get_user_model()
    try:
        usuario= UserModel.objects.get(pk=id)
        if usuario.is_superuser and usuario_actual.is_superuser:
            return redirect('admin')
        elif usuario.is_staff and usuario_actual.is_staff:
            return redirect('panel empleados')
        elif usuario.is_blocked and not usuario_actual.is_superuser:
            return render(request, '404_not_found.html')
        elif usuario.is_staff:
            return render(request, '404_not_found.html')
        elif usuario.is_superuser:
            return render(request, '404_not_found.html')
        else:
            try:
                embarcaciones = Embarcacion.objects.exclude(matricula__startswith='*').filter(dueño = id)
            except Embarcacion.DoesNotExist:
                embarcaciones = []

            try:
                publicaciones = Publicacion.objects.filter(autor = id)
            except Publicacion.DoesNotExist:
                publicaciones = []

            try:
                vehiculos = Vehiculo.objects.filter(dueño = id)
            except Vehiculo.DoesNotExist:
                vehiculos = []

            try:
                ofertas = Oferta.objects.filter(autor= id)
            except Oferta.DoesNotExist:
                ofertas = []

                
            trueques= []

            return render(request, 'profile.html', {
                'param': usuario,
                'embarcaciones': embarcaciones,
                'publicaciones': publicaciones,
                'vehiculos': vehiculos,
                'ofertas': ofertas,
                'trueques': trueques,
            })
        
    except UserModel.DoesNotExist:
        return render(request, '404_not_found.html')