from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from .forms import formularioCargaEmbarcacion
from .models import TipoEmbarcacion
from empleados.models import Sede
from .backend import cargar_embarcacion_back

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
                cargar_embarcacion_back(lista, imagenes, form)
                ok= True
            else:
                form.add_error('imagen1', 'Se debe ingresar una imagen como minimo.')

    return render(request, 'register_boat.html', {'form': form, 'ok': ok, 'tipos': tipos, 'sedes': sedes})