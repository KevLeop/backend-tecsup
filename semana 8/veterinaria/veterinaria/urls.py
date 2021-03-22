from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title='Api de Gestion de Veterinaria',
        default_version='1.0',
        description='API usando DRF para el manejo de mascotas de una veterinaria',
        terms_of_service="http://www.google.com",
        contact=openapi.Contact(name="Kevin Valverde",email="kevinleo93@gmail.com"),
        license=openapi.License(name='MIT', url="https://es.wikipedia.org/wiki/Licencia_de_software")
    
    ),
    public=True,
    permission_classes=[permissions.AllowAny]

)

urlpatterns = [
    path('',schema_view.with_ui('swagger')),
    path('redoc',schema_view.with_ui('redoc')),
    path('admin/', admin.site.urls),
    path('', include('administracion.urls'))

]
