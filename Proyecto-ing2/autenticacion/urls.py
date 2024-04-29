from django.urls import path
from . import views

urlpatterns = [
    path('iniciar sesion/', views.cuestionario_iniciar_sesion, name='iniciar sesion'),
    path('recuperar contraseña/',views.recuperar_contraseña, name= 'recuperar contraseña'),
    path('crear cuenta/',views.cuestionario_crear_cuenta, name='crear cuenta')
]