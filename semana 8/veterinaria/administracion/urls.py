from django.urls import path
from .views import EspeciesController, EspecieController

urlpatterns = [
    path('especies/', EspeciesController.as_view()),
    path('especie/<int:id>', EspecieController.as_view())
]

