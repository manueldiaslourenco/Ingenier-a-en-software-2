from django.urls import path
from . import views

urlpatterns = [
    path('usuario/<int:id>/', views.ver_perfil, name='ver perfil'),
]
