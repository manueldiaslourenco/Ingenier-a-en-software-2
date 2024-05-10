from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import HttpResponse
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy

@login_required(login_url=reverse_lazy('home'))
def ver_perfil(request, id):
    usuario_actual = request.user
    UserModel = get_user_model()
    try:
        usuario= UserModel.objects.get(pk=id)
        if usuario.is_superuser and usuario_actual.is_superuser:
            return redirect('admin')
        elif usuario.is_staff and usuario_actual.is_staff:
            return redirect('panel empleados')
        elif usuario.is_superuser:
            return HttpResponse("Este elemento no existe.")
        else:
            return render(request, 'profile.html', {'param': usuario})
        
    except UserModel.DoesNotExist:
        return HttpResponse("Este elemento no existe.")