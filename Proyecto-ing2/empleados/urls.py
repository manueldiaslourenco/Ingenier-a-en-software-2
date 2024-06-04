from django.urls import path
from . import views

urlpatterns = [
    path('empleados/', views.index, name="panel empleados"),
    path('empleados/trueques', views.listar_trueques, name='ver trueques')
]