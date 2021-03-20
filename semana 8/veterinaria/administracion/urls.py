from django.urls import path
from .views import EspeciesController, EspecieController, RazasController

urlpatterns = [
    path('especies', EspeciesController.as_view()),
    path('especie/<int:id>', EspecieController.as_view()),
    path('raza', RazasController.as_view())
]

