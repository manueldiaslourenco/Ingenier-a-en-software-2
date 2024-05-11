from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from .backend import  chequear_empleado
from empleados.models import EmpleConSede, Sede

@login_required(login_url=reverse_lazy('home'))
def index(request):
    chequear_empleado(request.user)

    id = request.user.id
    #MUESTRA ERROR AL INTENTAR ACCEDER CON USER TIPO ADMIN DA ERROR DOES NOT EXIST
    emple_sede = EmpleConSede.objects.get(user_id=id)
    sede = Sede.objects.get(id=emple_sede.sede_id)

    return render(request, 'employees_index.html', { 'nombre_sede' : sede.nombre})

