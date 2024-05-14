from django.db import IntegrityError
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import login, logout
from django.contrib.auth import get_user_model
from .forms import formularioIniciarSesion, formularioRecuperarContraseña, formularioRegistro, formularioCambiarContraseña
from usuarios.models import Usuario
from .backend import autenticar_usuario, es_mayor_de_18, send_email, generate_key

def cuestionario_iniciar_sesion(request):
    ok=False
    form = formularioIniciarSesion()
    usuario_actual = request.user
    if usuario_actual.is_authenticated:
        ok= True
    if request.method == 'POST':
        form = formularioIniciarSesion(request.POST)
        if form.is_valid():
            usuario = autenticar_usuario(username=form.cleaned_data['mail'], password=form.cleaned_data['password'])
        
            if usuario is not None:
                if usuario.is_superuser:
                    login(request, usuario)
                    return redirect('admin')
                elif usuario.is_staff:
                    login(request,usuario)
                    return redirect('panel empleados')
                elif not usuario.is_blocked: 
                    login(request, usuario)
                    return redirect('home')
                else:
                    form.add_error('password', 'La cuenta ingresada se encuentra bloqueada.')
            else:
                form.add_error('password', 'Las credenciales ingresadas no son correspondientes.')
    return render(request, 'login.html', {'form': form, 'ok': ok})

def cerrar_sesion(request):
    logout(request)
    return  redirect('iniciar sesion')

def cuestionario_crear_cuenta(request):
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
    return render(request, 'signup.html', {'form': form, 'ok': ok})

def recuperar_contraseña(request):
    form= formularioRecuperarContraseña()
    if request.method == 'POST':
        form= formularioRecuperarContraseña(request.POST)
        if form.is_valid():
            try: 
                UserModel = get_user_model()
                mail=form.cleaned_data['mail']
                usuario= UserModel.objects.get(mail=mail)
                if usuario.is_blocked:
                    form.add_error('mail', 'La cuenta ingresada se encuentra bloqueada.')
                else:
                    security_token = generate_key()
                    send_email(mail, security_token)
                    session_id = request.COOKIES.get('sessionid')
                    request.session['token'] = security_token
                    request.session['sessionid'] = session_id
                    request.session['mail'] = mail
                    return redirect('ingresar nueva contraseña')
            except UserModel.DoesNotExist:
                 form.add_error('mail', 'Mail inexistente.')
    return render(request, 'forget_password.html', {'form': form})

def ingresar_nueva_contraseña(request):
    ok = False
    form = formularioCambiarContraseña()
    if request.method == 'POST':
        form = formularioCambiarContraseña(request.POST)
        check_session = request.session.pop('sessionid', None)
        check_token = request.session.pop('token', None)
        mail = request.session.pop('mail', None)
        if form.is_valid():
            session = request.COOKIES.get('sessionid')
            token = form.cleaned_data['token'] 
            new_pass = form.cleaned_data['contraseña']
            if token == check_token and session == check_session:
                    UserModel = get_user_model()
                    user = UserModel.objects.get(mail=mail)
                    user.password = new_pass
                    user.save()
                    ok = True
            else:
                form.add_error('token', 'El codigo de recuperacion ingresado es incorrecto.')
    return render(request, 'change_password.html', {'form': form, 'ok': ok})