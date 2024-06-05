from django.urls import path
from . import views

urlpatterns = [
    path('ver_detalle_trueque/<int:id_trueque>/', views.ver_trueque, name='ver detalle trueque'),
    path('completar_trueque/<int:id_trueque>/', views.completar_trueque, name= 'completar trueque')
]