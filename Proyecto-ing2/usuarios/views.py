from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.contrib.auth import get_user_model


def ver_perfil(request, id):
    # Supongamos que 'lista' es tu lista de usuarios.
    UserModel = get_user_model()
    try:
        usuario= UserModel.objects.get(pk=id)
        return render(request, 'profile.html', {'param': usuario})
    except UserModel.DoesNotExist:
        return HttpResponse("Este elemento no existe.")