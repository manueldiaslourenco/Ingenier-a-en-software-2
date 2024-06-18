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
    path('administracion/embarcaciones/', views.embarcaciones, name="lista embarcaciones"),
    path('administrador/vehiculos/', views.listar_vehiculos, name='lista vehiculos'),
    path('administrador/ofertas/', views.listar_ofertas, name='lista ofertas'),
    path('administracion/publicaciones/', views.listar_publicaciones, name='lista publicaciones'),
    path('administracion/trueques/', views.listar_trueques, name='lista trueques'),
    path('administracion/empleados/eliminar_empleado/', views.eliminar_empleado, name='eliminar empleado'),
    path('administracion/usuarios/eliminar_usuario/', views.eliminar_usuario, name='eliminar usuario'),
]