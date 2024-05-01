from django.urls import path
from . import views

urlpatterns = [
    path('iniciar_sesion/', views.cuestionario_iniciar_sesion, name='iniciar sesion'),
    path('cerrar_sesion/',views.cerrar_sesion, name='cerrar sesion'),
    path('recuperar_contraseña/',views.recuperar_contraseña, name= 'recuperar contraseña'),
    path('crear_cuenta/',views.cuestionario_crear_cuenta, name='crear cuenta')
]