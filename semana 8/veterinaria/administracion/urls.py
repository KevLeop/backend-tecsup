from django.urls import path
from .views import (BusquedaController, CustomController, EspeciesController, EspecieController, 
                    MascotasController, RazasController, contabilizar_sexo, ClienteController,buscar_mascotas)

urlpatterns = [
    path('especies', EspeciesController.as_view()),
    path('especie/<int:id>', EspecieController.as_view()),
    path('raza', RazasController.as_view()),
    path('mascota',MascotasController.as_view()),
    path('prueba',CustomController.as_view()),
    path('buscarMascota',BusquedaController.as_view()),
    path('contabilizarSexo',contabilizar_sexo),
    path('clientes',ClienteController.as_view()),
    path('buscar',buscar_mascotas),

]

