from django.shortcuts import render
from django.shortcuts import HttpResponse


def ver_perfil(request, id):
    # Supongamos que 'lista' es tu lista de usuarios.
    lista = ["Elemento 1", "Elemento 2", "Elemento 3"]
    if id < len(lista):
        elemento = lista[id]
        return HttpResponse(f"Estás viendo el elemento: {elemento}")
    else:
        return HttpResponse("Este elemento no existe.")