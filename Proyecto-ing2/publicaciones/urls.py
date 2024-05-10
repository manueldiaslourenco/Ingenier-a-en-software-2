from django.urls import path
from . import views

urlpatterns = [
    path('cargar_publicacion/', views.cuestionario_cargar_publicacion, name='crear publicacion'),
]