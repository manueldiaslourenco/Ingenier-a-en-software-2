from django.urls import path
from . import views

urlpatterns = [
    path('cargar_publicacion/', views.cuestionario_cargar_publicacion, name='crear publicacion'),
    path('ver_detalle_publicacion/<int:id_publicacion>/', views.ver_detalle_publicacion, name= 'ver detalle publicacion'),
]