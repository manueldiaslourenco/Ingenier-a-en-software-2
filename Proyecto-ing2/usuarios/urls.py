from django.urls import path
from . import views

urlpatterns = [
    path('perfil/<int:id>/', views.ver_perfil, name='ver_perfil'),
]
