from django.urls import path
from . import views

urlpatterns = [
    path('empleados/', views.index, name="panel empleados"),
    path('empleados/trueques', views.listar_trueques, name='ver trueques'),
    path('empleados/perfil', views.ver_perfil, name='mi perfil'),
    path('empleados/perfil/editar/<int:empleado_id>/', views.editar_empleado, name='editar_empleado'),
]
