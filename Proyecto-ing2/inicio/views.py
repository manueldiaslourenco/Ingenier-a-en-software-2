from django.shortcuts import render
from django.shortcuts import redirect

def redirigir_inicio(request):
    return redirect('home')

def inicio(request):
    return render(request, 'index.html')
