from django.urls import path
from . import views

urlpatterns = [
    path('administracion/', views.index, name="admin"),
    path('administracion/usuarios/', views.usuarios, name="lista usuarios"),
    path('administracion/crear_usuario/', views.cuestionario_crear_usuario, name="crear usuario"),
    path('administracion/empleados/', views.empleados, name="lista empleados"),
    path('administracion/crear_empleado/', views.cuestionario_crear_empleado, name="crear empleado"),
    path('administracion/usuarios/bloquear_usuario', views.bloquear_usuario, name="bloquear usuario"),
    path('administracion/usuarios/desbloquear_usuario', views.desbloquear_usuario, name="desbloquear usuario"),
]