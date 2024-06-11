from django.urls import path
from . import views

urlpatterns = [
    path('publicar_oferta/<int:id_publi>/', views.publicar_oferta, name='publicar oferta'),
    path('aceptar_oferta/', views.aceptar_oferta, name='aceptar oferta'),
    path('rechazar_oferta/', views.rechazar_oferta, name='rechazar oferta')
]