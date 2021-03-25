from django.contrib.auth.models import BaseUserManager

# clase que sirve para modificar el comportamiento del modelo Auth del proyecto de django
class UsuarioManager(BaseUserManager):
  def create_user(self,email,nombre,apellido,tipo, password=None):
    if not email:
      raise ValueError('El usuario debe tener obligatoriamente un correo')
    email = self.normalize_email(email) #para normalizar el email/validar
    # creo mi objeto de usuario pero aun no lo guardo en la bd
    usuario = self.model(personalCorreo=email,
                        personalNombre=nombre,
                        personalApellido=apellido,
                        personalTipo=tipo)
    usuario.set_password(password)
    usuario.save(using=self._db) # sirve para referenciar a la bd
    return usuario

  def create_superuser(self, personalCorreo, personalNombre, personalApellido, password, personalTipo):
    usuario = self.create_user(personalCorreo, personalNombre,personalApellido,personalTipo,password)
    usuario.is_superuser=True
    usuario.is_staff = True #para poder ingresar al panel administrativo
    usuario.save(using=self._db)