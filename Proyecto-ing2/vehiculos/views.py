from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from .forms import formularioCargarVehiculo
from .models import TipoVehiculo
from .backend import cargar_vehiculo_back


@login_required(login_url=reverse_lazy('home'))
def cuestionario_cargar_vehiculo(request):
    ok = False
    form = formularioCargarVehiculo()
    tipos = list(TipoVehiculo.objects.all().values_list('clase', flat=True))
    
    if request.method == 'POST':
        form = formularioCargarVehiculo(request.POST, request.FILES)
        ok = False
        if form.is_valid():
            imagenes= []
            if 'imagen1' in request.FILES:
                imagen1 = request.FILES['imagen1']
                imagenes.append(imagen1)
                if 'imagen2' in request.FILES:
                    imagen2 = request.FILES['imagen2']
                    imagenes.append(imagen2)
                if 'imagen3' in request.FILES:
                    imagen3 = request.FILES['imagen3']
                    imagenes.append(imagen3)
            
                usuario_actual_mail = request.user.mail
                lista= []
                lista.append(usuario_actual_mail)
                lista.append(form.cleaned_data['tipo'])
                lista.append(form.cleaned_data['patente'])
                lista.append(form.cleaned_data['marca'])
                lista.append(form.cleaned_data['modelo'])
                lista.append(form.cleaned_data['año_fabricacion'])
                lista.append(form.cleaned_data['kilometraje'])
                ok = cargar_vehiculo_back(lista, imagenes, form)
            else:
                form.add_error('imagen1', 'Se debe ingresar una imagen como minimo.')

    return render(request, 'register_vehicle.html', {
        'form': form,
        'ok': ok,
        'tipos': tipos
    })