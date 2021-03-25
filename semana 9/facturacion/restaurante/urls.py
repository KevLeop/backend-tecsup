from django.urls import path
from .views import *

urlpatterns = [
  path('plato', PlatosController.as_view()),
  path('plato/<int:id>', PlatoController.as_view())
]