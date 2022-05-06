from django.urls import path
from . import views

#home es el nombre de la función en views/siempre coma al final
urlpatterns = [
    path('cargar/', views.cargaMasiva, name='carga'),
]