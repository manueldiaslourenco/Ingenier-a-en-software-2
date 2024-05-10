from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from .forms import formularioCrearPublicacion
from embarcaciones.models import Embarcacion
from .backend import cargar_publicacion_back

@login_required(login_url=reverse_lazy('iniciar sesion'))
def cuestionario_cargar_publicacion(request):
    ok=False
    form = formularioCrearPublicacion()
    usuario_actual = request.user
    embarcaciones = Embarcacion.objects.filter(dueño=usuario_actual)
    matriculas_embarcaciones = list(embarcaciones.values_list('matricula', flat=True))
    
    if request.method == 'POST':
        form = formularioCrearPublicacion(request.POST)
        ok= False
        if form.is_valid():
            usuario_actual_mail = request.user.mail
            lista= []
            lista.append(usuario_actual_mail)
            lista.append(form.cleaned_data['embarcacion'])
            lista.append(form.cleaned_data['monto'])
            lista.append(form.cleaned_data['descripcion'])
            cargar_publicacion_back(lista, form)
            ok= True

    return render(request, 'register_post.html', {'form': form, 'ok': ok, 'embarcaciones':  matriculas_embarcaciones})
