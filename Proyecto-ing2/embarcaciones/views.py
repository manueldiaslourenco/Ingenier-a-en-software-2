import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from .forms import formularioCargaEmbarcacion, formularioEditarEmbarcacion
from .models import TipoEmbarcacion, Embarcacion, ImagenEmbarcacion
from publicaciones.models import Publicacion
from ofertas.models import Oferta
from empleados.models import Sede
from .backend import cargar_embarcacion_back, eliminar_logicamente_embarcacion, eliminar_imagenes_y_objeto_tabla

@login_required(login_url=reverse_lazy('home'))
def cuestionario_cargar_embarcacion(request):
    ok=False
    form = formularioCargaEmbarcacion()
    tipos = list(TipoEmbarcacion.objects.all().values_list('clase', flat=True))
    sedes = list(Sede.objects.all().values_list('nombre', flat=True))
    
    if request.method == 'POST':
        form = formularioCargaEmbarcacion(request.POST, request.FILES)
        ok= False
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
                lista.append(form.cleaned_data['sede'])
                lista.append(usuario_actual_mail)
                lista.append(form.cleaned_data['tipo'])
                lista.append(form.cleaned_data['matricula'])
                lista.append(form.cleaned_data['modelo'])
                lista.append(form.cleaned_data['eslora'])
                lista.append(form.cleaned_data['manga'])
                lista.append(form.cleaned_data['calado'])
                lista.append(form.cleaned_data['motor'])
                if form.cleaned_data['deuda'] != None:
                    lista.append(form.cleaned_data['deuda'])
                else:
                    lista.append(0)
                ok = cargar_embarcacion_back(lista, imagenes, form)
            else:
                form.add_error('imagen1', 'Se debe ingresar una imagen como minimo.')

    return render(request, 'register_boat.html', {'form': form, 'ok': ok, 'tipos': tipos, 'sedes': sedes})

@login_required(login_url=reverse_lazy('iniciar sesion'))
def ver_detalle_embarcacion(request, id_embarcacion, ok):
    try:
        unaEmbarcacion = Embarcacion.objects.exclude(matricula__startswith='*').get(id= id_embarcacion)
        imagenes= ImagenEmbarcacion.objects.filter(embarcacion= unaEmbarcacion.id)
        try:
            Oferta.objects.filter(embarcacion_ofertada= id_embarcacion)
            oferta_aceptada= True
        except Oferta.DoesNotExist:
            oferta_aceptada= False
        return render(request, 'boat_detail.html', {'imagenes': imagenes, 'embarcacion':  unaEmbarcacion, 'ok':ok, 'oferta_aceptada': oferta_aceptada})
    except Embarcacion.DoesNotExist:
        return render(request, '404_not_found.html')

@login_required(login_url=reverse_lazy('home'))
def eliminar_embarcacion(request, id_embarcacion):
    try:
        embarcacion = Embarcacion.objects.exclude(matricula__startswith='*').get(id= id_embarcacion)
        if embarcacion.dueño.id == request.user.id or request.user.is_superuser:
            eliminar_logicamente_embarcacion(embarcacion)
            eliminar_imagenes_y_objeto_tabla(id_embarcacion)
            publicaciones= Publicacion.objects.filter(embarcacion= embarcacion.id)
            for publi in publicaciones:
                publi.delete()
            #mostrar cartel lindo de eliminacion correcta
            return redirect('ver perfil', id= request.user.id)
        else:
            return render(request, '404_not_found.html')
    except Embarcacion.DoesNotExist:
        return render(request, '404_not_found.html')
    
@login_required(login_url=reverse_lazy('home'))
def editar_embarcacion(request, id_embarcacion):
    ok= False
    form = formularioEditarEmbarcacion()
    fs = FileSystemStorage()
    sedes = list(Sede.objects.all().values_list('nombre', flat=True))
    try:
        embarcacion= Embarcacion.objects.exclude(matricula__startswith='*').get(id= id_embarcacion)
        if embarcacion.dueño.id == request.user.id:
            imagenes_a_cargar= ImagenEmbarcacion.objects.filter(embarcacion= embarcacion.id)
            if request.method == 'POST':
                form = formularioEditarEmbarcacion(request.POST, request.FILES)
                if form.is_valid():
                    embarcacion.m_eslora = form.cleaned_data.get('eslora')
                    embarcacion.m_manga = form.cleaned_data.get('manga')
                    embarcacion.m_calado = form.cleaned_data.get('calado')
                    embarcacion.motor = form.cleaned_data.get('motor')
                    if form.cleaned_data.get('deuda') != None:
                        embarcacion.deuda = form.cleaned_data.get('deuda')
                    else:
                        embarcacion.deuda = 0
                    try:
                        embarcacion.sede = Sede.objects.get(nombre= form.cleaned_data.get('sede'))
                    except Sede.DoesNotExist:
                        pass
                    
                    # Guarda los cambios en la base de datos
                    embarcacion.save()
                    imagenes_actuales = ImagenEmbarcacion.objects.filter(embarcacion=embarcacion)

                    for i in range(1, 4):
                        imagen_field = form.cleaned_data.get(f'imagen{i}')
                        if imagen_field:
                            try:
                                imagen = imagenes_actuales.get(nombre_especifico=f"{embarcacion.id}{chr(96 + i)}.png")
                                # Borra el archivo de imagen antiguo del sistema de archivos
                                if os.path.isfile(os.path.join(settings.MEDIA_ROOT, imagen.nombre_especifico)):
                                    os.remove(os.path.join(settings.MEDIA_ROOT, imagen.nombre_especifico))
                                # Guarda la nueva imagen con el mismo nombre de archivo
                                fs.save(imagen.nombre_especifico, imagen_field)
                            except ImagenEmbarcacion.DoesNotExist:
                                # Crea una nueva imagen si no existía una imagen antigua
                                imagen_id = f"{embarcacion.id}{chr(96 + len(imagenes_actuales) + 1)}.png"
                                fs.save(imagen_id, imagen_field)
                                ImagenEmbarcacion.objects.create(
                                nombre_especifico=imagen_id,
                                embarcacion=embarcacion,
                                )
                    ok= True
        else:
            return render(request, '404_not_found.html')
    except Embarcacion.DoesNotExist:
        return render(request, '404_not_found.html')
    
    return render(request, 'edit_boat.html', {'form': form,'embarcacion': embarcacion, 'imagenes': imagenes_a_cargar, 'sedes': sedes, 'ok':ok})
