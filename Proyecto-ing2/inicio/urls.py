from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.inicio, name='home'),
    path('', views.redirigir_inicio)
]