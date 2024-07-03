from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.dateparse import parse_date
from datetime import date
from .backend import calcular_edad, es_mayor_de_18, generar_contraseña_aleatoria, send_email
from .forms import formularioRegistro, formularioRegistroEmpleado
from embarcaciones.backend import eliminar_logicamente_embarcacion, eliminar_imagenes_y_objeto_tabla
from embarcaciones.models import Embarcacion
from empleados.models import EmpleConSede, Sede
from ofertas.models import Oferta
from publicaciones.backend import eliminar_publicacion_fisica
from publicaciones.models import Publicacion
from trueques.models import Trueque
from usuarios.backend import eliminar_logicamente_usuario
from usuarios.models import Usuario
from vehiculos.backend import eliminar_logicamente_vehiculo, eliminar_imagenes_y_objeto_tabla
from vehiculos.models import Vehiculo


@login_required(login_url=reverse_lazy('home'))
def index(request):
    user = request.user
    if not user.is_superuser:
        return redirect('home')
    
    return render(request, 'index_admin.html')

@login_required(login_url=reverse_lazy('home'))
def empleados(request):
    user = request.user
    if not user.is_superuser:
        return redirect('home')
    
    empleados = Usuario.objects.filter(is_staff=True, is_superuser=False)
    for empleado in empleados:
        emple_sede = EmpleConSede.objects.get(user_id=empleado.id)
        sede = Sede.objects.get(id=emple_sede.sede_id)
        empleado.sede = sede.nombre
    return render(request, 'employees.html', {
        'empleados' : empleados
    })

@login_required(login_url=reverse_lazy('home'))
def cuestionario_crear_empleado(request):
    user = request.user
    if not user.is_superuser:
        return redirect('home')
    
    ok= False
    form= formularioRegistroEmpleado()
    #sedes = list(Sede.objects.all().values_list('nombre', flat=True))
    sedes = Sede.objects.all()
    if request.method == 'POST':
        form = formularioRegistroEmpleado(request.POST)
        if form.is_valid():
            email = form.cleaned_data['mail']
            sede = form.cleaned_data['sede']
            contraseña = generar_contraseña_aleatoria()
            usuario = Usuario(
                nombre="",
                apellido="",
                fecha_nacimiento=date.today(),
                telefono="0000000000",
                mail=email,
                password = make_password(contraseña),
                is_staff = True
            )
            try:
                #usr_emple = Usuario.objects.get(mail = email)
                #usr_emple.save()
                usuario.save()
                ok=True
                emple_sede = EmpleConSede.objects.create(
                    sede = sede,
                    user = usuario
                )
                emple_sede.save()
                send_email(email,contraseña)
            except IntegrityError:
                form.add_error('mail', 'El correo ingresado ya se encuentra registrado.')
    return render(request, 'create_employee.html', {'form': form, 'ok': ok, 'sedes': sedes})

@login_required(login_url=reverse_lazy('home'))
def ver_perfil_empleado(request, empleado_id):
    user = request.user
    if not user.is_superuser:
        return redirect('home')
    
    # Obtener el usuario actual (empleado)
    empleado = Usuario.objects.get(id=empleado_id)

    return render(request, 'employee.html', {'empleado':empleado})

@login_required(login_url=reverse_lazy('home'))
def usuarios(request):
    user = request.user
    if not user.is_superuser:
        return redirect('home')
    
    usuarios = Usuario.objects.filter(is_staff=False).exclude(mail__startswith='*')
    for usuario in usuarios:
        usuario.edad = calcular_edad(usuario.fecha_nacimiento)
    return render(request, 'users.html', {
        'usuarios' : usuarios
    })

@login_required(login_url=reverse_lazy('home'))
def cuestionario_crear_usuario(request):
    user = request.user
    if not user.is_superuser:
        return redirect('home')
    
    ok= False
    form= formularioRegistro()
    if request.method == 'POST':
        form = formularioRegistro(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            apellido= form.cleaned_data['apellido']
            telefono= form.cleaned_data['telefono']
            email = form.cleaned_data['mail']
            contraseña= form.cleaned_data['contraseña']
            fecha_nacimiento= form.cleaned_data['fecha_nacimiento']
            if es_mayor_de_18(fecha_nacimiento):
                usuario = Usuario(
                    nombre=nombre,
                    apellido=apellido,
                    fecha_nacimiento=fecha_nacimiento,
                    telefono=telefono,
                    mail=email,
                    password=contraseña
                )
                try:
                    usuario.save()
                    ok=True
                except IntegrityError:
                    form.add_error('mail', 'El correo ingresado ya se encuentra registrado.')
            else:
                form.add_error('fecha_nacimiento', 'Debe ser mayor de edad (+18) para registrarse.')
    return render(request, 'create_user.html', {'form': form, 'ok': ok})

@login_required(login_url=reverse_lazy('home'))
def bloquear_usuario(request):
    user = request.user
    if not user.is_superuser:
        return redirect('home')
    
    if request.method == 'POST':
        usuario_id = request.POST.get('usuario_id')
        usuario = Usuario.objects.get(id=usuario_id)
        usuario.is_blocked = True
        usuario.save()
    return redirect('lista usuarios')

@login_required(login_url=reverse_lazy('home'))
def desbloquear_usuario(request):
    user = request.user
    if not user.is_superuser:
        return redirect('home')
    
    if request.method == 'POST':
        usuario_id = request.POST.get('usuario_id')
        usuario = Usuario.objects.get(id=usuario_id)
        usuario.is_blocked = False
        usuario.save()
    return redirect('lista usuarios')

login_required(login_url=reverse_lazy('home'))
def embarcaciones(request):
    user = request.user
    if not user.is_superuser:
        return redirect('home')
    
    embarcaciones = Embarcacion.objects.exclude(matricula__startswith='*')
    return render(request, 'boats.html', {'embarcaciones' : embarcaciones})

@login_required(login_url=reverse_lazy('home'))
def listar_vehiculos(request):
    user = request.user
    if not user.is_superuser:
        return redirect('home')
    
    vehiculos = Vehiculo.objects.exclude(patente__startswith='*')
    return render(request, 'vehicles.html', {'vehiculos': vehiculos})

@login_required(login_url=reverse_lazy('home'))
def listar_ofertas(request):
    user = request.user
    if not user.is_superuser:
        return redirect('home')
    
    ofertas = Oferta.objects.exclude(oculta = True)
    return render(request, 'offers.html', {'ofertas': ofertas})

@login_required(login_url=reverse_lazy('home'))
def listar_publicaciones(request):
    user = request.user
    if not user.is_superuser:
        return redirect('home')
    
    publicaciones = Publicacion.objects.exclude(oculta = True)
    return render(request, 'posts.html', {'publicaciones': publicaciones})

@login_required(login_url=reverse_lazy('home'))
def listar_trueques(request):
    user = request.user
    if not user.is_staff:
        return redirect('home')
    
    trueques = Trueque.objects.all()
    return render(request, 'trades.html', {'trueques': trueques})


@login_required(login_url=reverse_lazy('home'))
def eliminar_empleado(request):
    user = request.user
    if not user.is_superuser:
        return redirect('home')

    if request.method == 'POST':
        empleado_id = request.POST.get('usuario_id')
        empleado = Usuario.objects.get(id=empleado_id)
        
        eliminar = request.POST.get('eliminar')

        context = {
            'empleado':empleado,
            'eliminar':eliminar
        }
        if eliminar == "2":
            empleado.delete()
    
    empleados = Usuario.objects.filter(is_staff=True, is_superuser=False)
    for empleado in empleados:
        emple_sede = EmpleConSede.objects.get(user_id=empleado.id)
        sede = Sede.objects.get(id=emple_sede.sede_id)
        empleado.sede = sede.nombre

    return render(request,'employees.html',{'context':context,
                                            'empleados':empleados})


@login_required(login_url=reverse_lazy('home'))
def eliminar_usuario(request):
    user = request.user
    if not user.is_superuser:
        return redirect('home')

    if request.method == 'POST':
        usr_id = request.POST.get('usuario_id')
        usr = Usuario.objects.get(id=usr_id)
        
        eliminar = request.POST.get('eliminar')

        context = {
            'usuario':usr,
            'eliminar':eliminar
        }

        if eliminar == "2":
        
            eliminar_logicamente_usuario(usr)
            # Modificar las embarcaciones del usuario
            embarcaciones = Embarcacion.objects.filter(dueño_id=usr_id)
            for embarcacion in embarcaciones:
                eliminar_logicamente_embarcacion(embarcacion)
                eliminar_imagenes_y_objeto_tabla(embarcacion.id)
                publicaciones= Publicacion.objects.filter(embarcacion= embarcacion.id)
                for publi in publicaciones:
                    eliminar_publicacion_fisica(publi.id)
                
            # Modificar los vehículos del usuario
            vehiculos = Vehiculo.objects.filter(dueño_id=usr_id)
            for vehiculo in vehiculos:
                eliminar_logicamente_vehiculo(vehiculo)
                eliminar_imagenes_y_objeto_tabla(vehiculo.id)
            
            ofertas = Oferta.objects.filter(autor_id=usr_id)
            for oferta in ofertas:
                oferta.delete()

            trueques = Trueque.objects.filter(usuario1_id=usr_id)
            for trueque in trueques:
                trueque.estado= "Anulado"
                trueque.save()
                
            trueques2 = Trueque.objects.filter(usuario2_id=usr_id)
            for trueque in trueques2:
                trueque.estado= "Anulado"
                trueque.save()

        usuarios = Usuario.objects.filter(is_staff=False).exclude(mail__startswith='*')
        for usuario in usuarios:
            usuario.edad = calcular_edad(usuario.fecha_nacimiento)

    return render(request,'users.html', {'usuarios':usuarios,
                                         'context':context})


@login_required(login_url=reverse_lazy('home'))
def estadisticas(request):
    if not request.user.is_superuser:
        return redirect('home')    
    return render(request, 'layouts/stats.html')

@login_required(login_url=reverse_lazy('home'))
def trueques_concretados(request):
    if not request.user.is_superuser:
        return redirect('home')
    
    #Inicializo
    trueques_concretados = 0
    trueques_pendientes = 0
    trueques_cancelados = 0
    trueques_anulados = 0
    rango = '-'

    #Busco al entrar en stats
    if request.method == 'GET':
        trueques_concretados = Trueque.objects.filter(estado='Completado').count()
        trueques_pendientes = Trueque.objects.filter(estado='Pendiente').count()
        trueques_cancelados = Trueque.objects.filter(estado='Cancelado').count()
        trueques_anulados = Trueque.objects.filter(estado='Anulado').count()
        rango = 'Histórico'

    mensaje_error = None
    fecha_actual = date.today()

    #Busco al entrar desde el botón
    if request.method == 'POST':
        fecha_desde = parse_date(request.POST.get('fechaDesde'))
        fecha_hasta = parse_date(request.POST.get('fechaHasta'))

        if fecha_desde and fecha_hasta:
            if fecha_desde > fecha_hasta:
                mensaje_error = "La primera fecha no debe ser posterior a la segunda."
            elif fecha_hasta > fecha_actual:
                mensaje_error = f'La segunda fecha no debe ser posterior a la actual ({fecha_actual}).'
            else:
                trueques_rango = Trueque.objects.filter(fecha_cierre__range=(fecha_desde, fecha_hasta))

                trueques_concretados = trueques_rango.filter(estado='Completado').count()
                trueques_pendientes = Trueque.objects.filter(estado='Pendiente', fecha_inicio__range=(fecha_desde, fecha_hasta)).count()
                trueques_cancelados = trueques_rango.filter(estado='Cancelado').count()
                trueques_anulados = trueques_rango.filter(estado='Anulado').count()

                rango = f'{fecha_desde} - {fecha_hasta}'

                if trueques_concretados + trueques_pendientes + trueques_cancelados + trueques_anulados == 0:
                    mensaje_error = f'No existen trueques entre la fecha {fecha_desde} y la fecha {fecha_hasta}.'
        else:
            mensaje_error = "Debe ingresar ambas fechas."

    context = {
        'trueques_concretados': trueques_concretados,
        'trueques_pendientes': trueques_pendientes,
        'trueques_cancelados': trueques_cancelados,
        'trueques_anulados': trueques_anulados,
        'rango':rango,
        'mensaje_error':mensaje_error,
        'fecha_actual':fecha_actual
    }

    return render(request, 'trades_completed.html', {'context':context})

@login_required(login_url=reverse_lazy('home'))
def trueques_por_sede(request):
    if not request.user.is_superuser:
        return redirect('home')
    
    #Inicializo
    trueques_tigre = 0
    trueques_quilmes = 0
    trueques_rio_santiago = 0
    rango = '-'

    #Busco al entrar en stats
    if request.method == 'GET':
        trueques_concretados = Trueque.objects.filter(estado='Completado')
        
        trueques_tigre = trueques_concretados.filter(sede__nombre='Tigre').count()
        trueques_quilmes = trueques_concretados.filter(sede__nombre='Quilmes (La rivera)').count()
        trueques_rio_santiago = trueques_concretados.filter(sede__nombre='Río Santiago').count()

        rango = 'Histórico'

    mensaje_error = None
    fecha_actual = date.today()

    #Busco al entrar desde el botón
    if request.method == 'POST':
        fecha_desde = parse_date(request.POST.get('fechaDesde'))
        fecha_hasta = parse_date(request.POST.get('fechaHasta'))

        if fecha_desde and fecha_hasta:
            if fecha_desde > fecha_hasta:
                mensaje_error = "La primera fecha no debe ser posterior a la segunda."
            elif fecha_hasta > fecha_actual:
                mensaje_error = f'La segunda fecha no debe ser posterior a la actual ({fecha_actual}).'
            else:
                trueques_concretados = Trueque.objects.filter(estado='Completado')
                trueques_rango = trueques_concretados.filter(fecha_cierre__range=(fecha_desde, fecha_hasta))
                
                trueques_tigre = trueques_rango.filter(sede__nombre='Tigre').count()
                trueques_quilmes = trueques_rango.filter(sede__nombre='Quilmes (La rivera)').count()
                trueques_rio_santiago = trueques_rango.filter(sede__nombre='Río Santiago').count()
                
                rango = f'{fecha_desde} - {fecha_hasta}'
                
                if trueques_tigre + trueques_quilmes + trueques_rio_santiago == 0:
                    mensaje_error = f'No existen trueques entre la fecha {fecha_desde} y la fecha {fecha_hasta}.'
        else:
            mensaje_error = "Debe ingresar ambas fechas."

    context = {
        'trueques_tigre': trueques_tigre,
        'trueques_quilmes': trueques_quilmes,
        'trueques_rio_santiago': trueques_rio_santiago,
        'rango':rango,
        'mensaje_error':mensaje_error,
        'fecha_actual':fecha_actual
    }

    return render(request, 'trades_sedes.html', {'context':context})    

@login_required(login_url=reverse_lazy('home'))
def trueques_ratio_vehiculos(request):
    if not request.user.is_superuser:
        return redirect('home')
        
    #Inicializo
    trueques_catamaran_auto = 0
    trueques_catamaran_camioneta = 0
    trueques_catamaran_moto = 0

    trueques_crucero_auto = 0
    trueques_crucero_camioneta = 0
    trueques_crucero_moto = 0

    trueques_lancha_auto = 0
    trueques_lancha_camioneta = 0
    trueques_lancha_moto = 0

    trueques_velero_auto = 0
    trueques_velero_camioneta = 0
    trueques_velero_moto = 0

    rango = '-'

    #Busco al entrar en stats
    if request.method == 'GET':
        trueques_concretados = Trueque.objects.filter(estado='Completado')

        trueques_catamaran = trueques_concretados.filter(embarcacion1__tipo__clase='Catamaran')
        trueques_catamaran_auto = trueques_catamaran.filter(vehiculo__tipo__clase='Auto').count()
        trueques_catamaran_camioneta = trueques_catamaran.filter(vehiculo__tipo__clase='Camioneta').count()
        trueques_catamaran_moto = trueques_catamaran.filter(vehiculo__tipo__clase='Moto').count()

        trueques_crucero = trueques_concretados.filter(embarcacion1__tipo__clase='Crucero')
        trueques_crucero_auto = trueques_catamaran.filter(vehiculo__tipo__clase='Auto').count()
        trueques_crucero_camioneta = trueques_catamaran.filter(vehiculo__tipo__clase='Camioneta').count()
        trueques_crucero_moto = trueques_catamaran.filter(vehiculo__tipo__clase='Moto').count()

        trueques_lancha = trueques_concretados.filter(embarcacion1__tipo__clase='Lancha')
        trueques_lancha_auto = trueques_catamaran.filter(vehiculo__tipo__clase='Auto').count()
        trueques_lancha_camioneta = trueques_catamaran.filter(vehiculo__tipo__clase='Camioneta').count()
        trueques_lancha_moto = trueques_catamaran.filter(vehiculo__tipo__clase='Moto').count()

        trueques_velero = trueques_concretados.filter(embarcacion1__tipo__clase='Velero')
        trueques_velero_auto = trueques_catamaran.filter(vehiculo__tipo__clase='Auto').count()
        trueques_velero_camioneta = trueques_catamaran.filter(vehiculo__tipo__clase='Camioneta').count()
        trueques_velero_moto = trueques_catamaran.filter(vehiculo__tipo__clase='Moto').count()

        rango = 'Histórico'

    mensaje_error_fecha = None
    mensaje_error_sin_trueque = None
    error_catamaran = False
    error_crucero = False
    error_lancha = False
    error_velero = False
    error_general = 0
    fecha_actual = date.today()

    #Busco al entrar desde el botón
    if request.method == 'POST':
        fecha_desde = parse_date(request.POST.get('fechaDesde'))
        fecha_hasta = parse_date(request.POST.get('fechaHasta'))

        if fecha_desde and fecha_hasta:
            if fecha_desde > fecha_hasta:
                mensaje_error_fecha = "La primera fecha no debe ser posterior a la segunda."
            elif fecha_hasta > fecha_actual:
                mensaje_error_fecha = f'La segunda fecha no debe ser posterior a la actual ({fecha_actual}).'
            else:
                rango = f'{fecha_desde} - {fecha_hasta}'

                trueques_concretados = Trueque.objects.filter(estado='Completado')
                trueques_rango = trueques_concretados.filter(fecha_cierre__range=(fecha_desde, fecha_hasta))

                trueques_catamaran = trueques_rango.filter(embarcacion1__tipo__clase='Catamaran')
                trueques_catamaran_auto = trueques_catamaran.filter(vehiculo__tipo__clase='Auto').count()
                trueques_catamaran_camioneta = trueques_catamaran.filter(vehiculo__tipo__clase='Camioneta').count()
                trueques_catamaran_moto = trueques_catamaran.filter(vehiculo__tipo__clase='Moto').count()

                trueques_crucero = trueques_rango.filter(embarcacion1__tipo__clase='Crucero')
                trueques_crucero_auto = trueques_crucero.filter(vehiculo__tipo__clase='Auto').count()
                trueques_crucero_camioneta = trueques_crucero.filter(vehiculo__tipo__clase='Camioneta').count()
                trueques_crucero_moto = trueques_crucero.filter(vehiculo__tipo__clase='Moto').count()

                trueques_lancha = trueques_rango.filter(embarcacion1__tipo__clase='Lancha')
                trueques_lancha_auto = trueques_lancha.filter(vehiculo__tipo__clase='Auto').count()
                trueques_lancha_camioneta = trueques_lancha.filter(vehiculo__tipo__clase='Camioneta').count()
                trueques_lancha_moto = trueques_lancha.filter(vehiculo__tipo__clase='Moto').count()

                trueques_velero = trueques_rango.filter(embarcacion1__tipo__clase='Velero')
                trueques_velero_auto = trueques_velero.filter(vehiculo__tipo__clase='Auto').count()
                trueques_velero_camioneta = trueques_velero.filter(vehiculo__tipo__clase='Camioneta').count()
                trueques_velero_moto = trueques_velero.filter(vehiculo__tipo__clase='Moto').count()

                if trueques_catamaran_auto + trueques_catamaran_camioneta + trueques_catamaran_moto == 0:
                    error_catamaran = True
                    error_general += 1
                
                if trueques_crucero_auto + trueques_crucero_camioneta + trueques_crucero_moto == 0:
                    error_crucero = True
                    error_general += 1

                if trueques_lancha_auto + trueques_lancha_camioneta + trueques_lancha_moto == 0:
                    error_lancha = True
                    error_general += 1

                if trueques_velero_auto + trueques_velero_camioneta + trueques_velero_moto == 0:
                    error_velero = True
                    error_general += 1
                
                mensaje_error_sin_trueque = f'No existen trueques entre la fecha {fecha_desde} y la fecha {fecha_hasta}.'
                
        else:
            mensaje_error_fecha = "Debe ingresar ambas fechas."

    context = {
        'trueques_catamaran_auto':trueques_catamaran_auto,
        'trueques_catamaran_camioneta':trueques_catamaran_camioneta,
        'trueques_catamaran_moto':trueques_catamaran_moto,

        'trueques_crucero_auto':trueques_crucero_auto,
        'trueques_crucero_camioneta':trueques_crucero_camioneta,
        'trueques_crucero_moto':trueques_crucero_moto,

        'trueques_lancha_auto':trueques_lancha_auto,
        'trueques_lancha_camioneta':trueques_lancha_camioneta,
        'trueques_lancha_moto':trueques_lancha_moto,

        'trueques_velero_auto':trueques_velero_auto,
        'trueques_velero_camioneta':trueques_velero_camioneta,
        'trueques_velero_moto':trueques_velero_moto,

        'rango':rango,

        'mensaje_error_fecha':mensaje_error_fecha,
        'mensaje_error_sin_trueque':mensaje_error_sin_trueque,
        'error_catamaran':error_catamaran,
        'error_crucero':error_crucero,
        'error_lancha':error_lancha,
        'error_velero':error_velero,
        'error_general':error_general,
        'fecha_actual':fecha_actual
    }

    return render(request, 'trades_vehicles.html', {'context':context})