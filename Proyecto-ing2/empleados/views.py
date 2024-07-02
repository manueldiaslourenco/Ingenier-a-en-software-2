from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from empleados.models import EmpleConSede, Sede
from trueques.models import Trueque
from .models import Sede
from .forms import FormularioEditarEmpleado


@login_required(login_url=reverse_lazy('home'))
def index(request):
    user = request.user
    if user.is_superuser or not user.is_staff:
        return redirect('home')

    id = request.user.id
    emple_sede = EmpleConSede.objects.get(user_id=id)
    sede = Sede.objects.get(id=emple_sede.sede_id)

    return render(request, 'employees_index.html', { 'nombre_sede' : sede.nombre})

@login_required(login_url=reverse_lazy('home'))
def listar_trueques(request):
    user = request.user
    if user.is_superuser or not user.is_staff:
        return redirect('home')
    
    emple_sede = EmpleConSede.objects.get(user_id=user.id)
    sede = Sede.objects.get(id=emple_sede.sede_id)

    trueques = Trueque.objects.filter(sede_id=sede.id)
    return render(request, 'employees_trueques.html', {'trueques': trueques,
                                                       'nombre_sede':sede.nombre})

@login_required(login_url=reverse_lazy('home'))
def ver_perfil(request):
    user = request.user
    if user.is_superuser or not user.is_staff:
        return redirect('home')
    
    # Obtener el usuario actual (empleado)
    empleado = request.user

    id = request.user.id
    emple_sede = EmpleConSede.objects.get(user_id=id)
    sede = Sede.objects.get(id=emple_sede.sede_id)
    return render(request, 'employees_profile.html', {'empleado': empleado,
                                                      'nombre_sede':sede.nombre})

@login_required(login_url=reverse_lazy('home'))
def editar_empleado(request):
    user = request.user
    if user.is_superuser or not user.is_staff:
        return redirect('home')
    
    ok = False

    empleado = request.user


    if request.method == 'POST':
        form = FormularioEditarEmpleado(request.POST)
        if form.is_valid():
            # Actualiza los campos del empleado solo si no están vacíos en el formulario
            if form.cleaned_data.get('nombre'):
                empleado.nombre = form.cleaned_data.get('nombre')
            if form.cleaned_data.get('apellido'):
                empleado.apellido = form.cleaned_data.get('apellido')
            if form.cleaned_data.get('fecha_nacimiento'):
                empleado.fecha_nacimiento = form.cleaned_data.get('fecha_nacimiento')
            if form.cleaned_data.get('telefono'):
                empleado.telefono = form.cleaned_data.get('telefono')

            # Guarda los cambios en la base de datos
            empleado.save()
            ok = True
    else:
        form = FormularioEditarEmpleado(initial={
            'nombre': empleado.nombre,
            'apellido': empleado.apellido,
            'fecha_nacimiento': empleado.fecha_nacimiento,
            'telefono': empleado.telefono,
        })


    id = request.user.id
    emple_sede = EmpleConSede.objects.get(user_id=id)
    sede = Sede.objects.get(id=emple_sede.sede_id)
    context = {'form': form, 'empleado': empleado, 'ok': ok}
    return render(request, 'edit_employees.html', {'context':context,
                                                   'nombre_sede':sede.nombre})

