from django.contrib import admin
from .models import RazaModel
from .models import EspecieModel, ClienteModel, PromocionModel,MascotaModel

class RazaAdmin(admin.ModelAdmin):
  # para modifica la vista del modelo en el Aadmin
  list_display=('razaNombre', 'especie')
  # para agregar un buscador; si se quiere hacer una busqueda por un atributo FK, debemos
  # especificar a que columna vamos a hacer la busqueda del padre meidante doble subguion y luego
  # indicar la columna o atributo
  search_fields=('razaNombre', 'especie__especieNombre')
  list_filter =('especie', )
  readonly_fields=('razaId',)
  ordering = ('razaNombre',)


admin.site.register(RazaModel, RazaAdmin)
admin.site.register(EspecieModel)
admin.site.register(ClienteModel)
admin.site.register(PromocionModel)
admin.site.register(MascotaModel)

# Register your models here.
