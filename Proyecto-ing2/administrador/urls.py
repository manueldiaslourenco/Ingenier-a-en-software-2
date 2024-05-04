from django.urls import path
from . import views

urlpatterns = [
    path('administracion/', views.index, name="admin"),
    path('administracion/usuarios/', views.usuarios, name="usuarios"),
    path('administracion/empleados/', views.empleados, name="empleados"),
]