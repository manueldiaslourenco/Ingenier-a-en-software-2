from django.urls import path
from . import views

urlpatterns = [
    path('cargar_embarcacion/', views.cuestionario_cargar_embarcacion, name='cargar embarcacion'),
]