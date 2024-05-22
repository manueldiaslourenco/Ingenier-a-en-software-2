from django.urls import path
from . import views

urlpatterns = [
    path('publicar_oferta/<int:id_publi>/', views.publicar_oferta, name='publicar oferta')
]