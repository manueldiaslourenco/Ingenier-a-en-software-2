from django.shortcuts import redirect

def chequear_empleado(user):
    if not user.is_staff:
        return redirect('home')