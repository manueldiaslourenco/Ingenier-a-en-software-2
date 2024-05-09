from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from .backend import  chequear_empleado

@login_required(login_url=reverse_lazy('home'))
def index(request):
    chequear_empleado(request.user)
    
    return render(request, 'employees_index.html')