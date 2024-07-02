from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.urls import reverse_lazy
from .forms import formularioCargarVehiculo, formularioEditarVehiculo
from .models import TipoVehiculo, Vehiculo, ImagenVehiculo
from ofertas.models import Oferta
from .backend import cargar_vehiculo_back, guardar_imagenes
from usuarios.views import ver_perfil
from trueques.models import Trueque
import os

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

@login_required(login_url=reverse_lazy('iniciar sesion'))
def ver_detalle_vehiculo(request, id_vehiculo, ok):
    try:
        unVehiculo = Vehiculo.objects.exclude(patente__startswith='*').get(id= id_vehiculo)
        imagenes= ImagenVehiculo.objects.filter(vehiculo= unVehiculo.id)
        try:
            Oferta.objects.filter(vehiculo_ofertado= id_vehiculo)
            oferta_aceptada = True
        except Oferta.DoesNotExist:
            oferta_aceptada = False
        vehiculo_en_trueque = Trueque.objects.filter(vehiculo_id=id_vehiculo).exists()
        
        return render(request, 'vehicle_detail.html', {'imagenes':imagenes,
                                                       'vehiculo':unVehiculo,
                                                       'ok':ok,
                                                       'vehiculo_en_trueque':vehiculo_en_trueque,
                                                       'ofertado': oferta_aceptada})
    except Vehiculo.DoesNotExist:
        return render(request, '404_not_found.html')
    
@login_required(login_url=reverse_lazy('iniciar sesion'))
def eliminar_vehiculo(request, vehiculo_id):
    vehiculo = Vehiculo.objects.get(id=vehiculo_id)

    # Eliminar ofertas asociadas al vehículo
    Oferta.objects.filter(vehiculo_ofertado=vehiculo).delete()
    
    # Eliminar el vehículo
    vehiculo.delete()
    return ver_perfil(request,request.user.id)

@login_required(login_url=reverse_lazy('iniciar sesion'))
def editar_vehiculo(request, vehiculo_id):
    ok=False
    form = formularioEditarVehiculo()
    fs = FileSystemStorage(location= 'vehiculos/static/imagenes_vehiculos')
    try:
        vehiculo = Vehiculo.objects.exclude(patente__startswith='*').get(id= vehiculo_id)
        if vehiculo.dueño.id == request.user.id:
            imagenes_a_cargar = ImagenVehiculo.objects.filter(vehiculo= vehiculo_id)
            if request.method == 'POST':
                form = formularioEditarVehiculo(request.POST, request.FILES)
                if form.is_valid():
                    vehiculo.marca = form.cleaned_data.get('marca')
                    vehiculo.modelo = form.cleaned_data.get('modelo')
                    vehiculo.año_fabricacion = form.cleaned_data.get('año_fabricacion')
                    vehiculo.kilometraje = form.cleaned_data.get('kilometraje')

                    vehiculo.save()

                    imagenes_actuales = ImagenVehiculo.objects.filter(vehiculo=vehiculo)

                    for i in range(1,4):
                        imagen_field = form.cleaned_data.get(f'imagen{i}')
                        if imagen_field:
                            try:
                                imagen = imagenes_actuales.get(nombre_especifico=f"{vehiculo.id}{chr(96 + i)}.png")
                                if os.path.isfile(os.path.join(settings.MEDIA_ROOTV, imagen.nombre_especifico)):

                                    os.remove(os.path.join(settings.MEDIA_ROOTV, imagen.nombre_especifico))
                                fs.save(imagen.nombre_especifico, imagen_field)
                            except ImagenVehiculo.DoesNotExist:
                                imagen_id = f'{vehiculo.id}{chr(96 + len(imagenes_actuales) + 1)}.png'
                                fs.save(imagen_id, imagen_field)
                                ImagenVehiculo.objects.create(
                                    nombre_especifico=imagen_id,
                                    vehiculo=vehiculo,
                                )
                    ok= True
        else:
            return render(request, '404_not_found.html')
    except Vehiculo.DoesNotExist:
        return render(request, '404_not_found.html')

    return render(request, 'edit_vehicle.html', {'form': form, 'vehiculo':vehiculo, 'imagenes': imagenes_a_cargar, 'ok':ok})