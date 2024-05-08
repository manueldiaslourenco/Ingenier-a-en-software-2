from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from .forms import formularioCargaEmbarcacion

@login_required(login_url=reverse_lazy('home'))
def cuestionario_cargar_embarcacion(request):
    ok=False
    form = formularioCargaEmbarcacion()
    tipos= ["velero", "moto de agua", "kayak"]
    if request.method == 'POST':
        form = formularioCargaEmbarcacion(request.POST)
        
        if form.is_valid():
            print("es correcto")
        #print("incorrecto")
    return render(request, 'register_boat.html', {'form': form, 'ok': ok, 'tipos': tipos})