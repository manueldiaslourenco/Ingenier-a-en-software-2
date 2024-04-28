from django.urls import path
from . import views

urlpatterns = [
    path('iniciar sesion/', views.mi_vista, name='iniciar sesion'),
    path('crear cuenta/',views.formulario_crear_cuenta, name='crear cuenta')
]