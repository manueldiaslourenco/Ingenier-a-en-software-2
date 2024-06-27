from django.urls import path
from . import views

urlpatterns = [
    path('calificar_usuario/<int:id_trueque>/<int:id_usuario_envio>/<int:id_usuario_recibio>/', views.calificar_usuario, name='calificar usuario'),
]