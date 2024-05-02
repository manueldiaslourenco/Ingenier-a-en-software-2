from django.urls import path
from . import views

urlpatterns = [
    path('administracion/', views.index, name="admin"),
    path('usuarios/', views.usuarios, name="usuarios"),
]