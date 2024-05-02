from django.urls import path
from . import views

urlpatterns = [
    path('', views.redirigir_usuarios),
    path('usuarios/', views.usuarios, name="usuarios"),
    path('usuarios/<int:id>', views.detalle_usuario, name="detalle_usuario"),
]