from rest_framework.permissions import BasePermission, SAFE_METHODS

class soloAdministrador(BasePermission):
  def has_permission(self, request, view):
      if request.user.personalTipo ==1:
        return True
      # el request nos dara los mismo atributos que nos da el request
      # de las vistas genericas
      print(view)
      # en los customs permissions tenemos que retornar SIEMPRE 
      # un boolean  porque si es True procederá con el sgte permiso
      # o con el controlador final (es un middleware)
      return False

class administradorPost(BasePermission):
  def has_permission(self, request, view):

    if request.method =='POST':
      
      if request.user.personalTipo ==1:
        return True
      else:
        return False
    else:
      return True,
      
class soloMozos(BasePermission):
  def has_permission(self, request, view):
    if request.user.personalTipo == 3:
      return True
    else:
      return False
