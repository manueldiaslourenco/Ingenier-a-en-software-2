from django.urls import path
from . import views

urlpatterns = [
    path('cargar_embarcacion/', views.cuestionario_cargar_embarcacion, name='cargar embarcacion'),
    path('ver_detalle_embarcacion/<int:id_embarcacion>/', views.ver_detalle_embarcacion, name= 'ver detalle embarcacion'),
    path('eliminar_embarcacion/<int:id_embarcacion>/', views.eliminar_embarcacion, name= 'eliminar embarcacion')
]