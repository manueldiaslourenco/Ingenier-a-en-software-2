from django.urls import path
from . import views

urlpatterns = [
    path('cargar_vehiculo/', views.cuestionario_cargar_vehiculo, name='cargar vehiculo'),
]