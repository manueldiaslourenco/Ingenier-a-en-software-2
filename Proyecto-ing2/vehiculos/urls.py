from django.urls import path
from . import views

urlpatterns = [
    path('cargar_vehiculo/', views.cuestionario_cargar_vehiculo, name='cargar vehiculo'),
    path('ver_detalle_vehiculo/<int:id_vehiculo>/<int:ok>', views.ver_detalle_vehiculo, name= 'ver detalle vehiculo'),
    path('vehiculo/eliminar/<int:vehiculo_id>', views.eliminar_vehiculo, name='eliminar vehiculo'),
    path('editar_vehiculo/<int:vehiculo_id>/', views.editar_vehiculo, name='editar vehiculo')
]