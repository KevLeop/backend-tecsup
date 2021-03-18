from django import db
from django.db import models
from django.db.models.base import Model
from django.db.models.fields import related

# Tipos de modelos: https://docs.djangoproject.com/en/3.1/ref/models/fields/
class RazaModel(models.Model):
  # si NO DEFINIMOS LA p, se creará automaticamente en mi BD con el nombre de la comlumna id
  # solamente una columna por tabla puede ser autofield
  razaId = models.AutoField(primary_key=True, 
                            auto_created=True, 
                            unique=True, 
                            null=False,
                            db_column='raza_id',
                            help_text='Aqui va el id',
                            verbose_name='ID de la raza'
                            )
  razaNombre = models.CharField(
    max_length=45,
    db_column='raza_nombre',
    verbose_name='Nombre de la raza'
  )
  # para definir algunas opciones extras como el nombre de la tabla, e ordenamiento de los resultados,
  # y modifical opciones de visualizacion en el panel administrativo se crea una clase Meta que
  # sirve par apasar los metadatos al padre (a la clase que hemos heredado)
  class Meta:
    # asi se cambia el nombre de la tabla
    db_table='t_raza'


class TipoModel(models.Model):
  tipoId = models.AutoField(
    primary_key=True,
    unique=True,
    null= False,
    db_column='tipo_id'
  )
  tipoNombre = models.CharField(
    max_length=45,
    null=False,
    db_column='tipo_nombre'
  )
  # al momento de eliminar un padre, tenemos que indicar que va a pasar con sus hijos
  # CASCADE => PREMITE ELIMINAR AL PADRE Y CONSEUCENTEMENTE ELIMINAR A LOS HIJOS
  # PROTECT => No permite eliminar al padre mientras tenga hijos
  # SET_NULL => Permite eliminar al padre y luego a sus hijos le cambiará el valor
  #           a NULL, sus hijos quedan sin Padre
  # DO_NOTHING => Permite eliminar al padre y deja su PK sin modificar a los hijos
  # RESTRICT => No permite la eliminacion y lanzara un error de ripo RestrictedError
  # https://docs.djangoproject.com/en/3.1/ref/models/fields/#django.db.models.ForeignKey.on_delete
  raza = models.ForeignKey(
    to=RazaModel,
    on_delete=models.PROTECT,
    db_column='raza_id', #cuando querramos ingresar a su relacion inversa
    related_name='tiposraza',
    verbose_name='Raza',
    help_text='Id de la raza'
    )

  # Para modificar la forma como se  mostrará el objeto por consola
  def __str__(self):
    return self.tipoNombre

  class Meta:
    db_table='t_tipo'
    # los sgtes atributos solamente sirven si vamos a utilizar el panel admin
    verbose_name='Tipo'
    verbose_name_plural='Tipos'


class ClienteModel(models.Model):
  clienteDni= models.CharField(
    max_length=9,
    primary_key=True,
    unique=True,
    null= False,
    db_column='cli_dni'
  )

  clienteNombre = models.CharField(
    max_length=45,
    db_column='cli_nombre',
    null=False
  )
  clienteApellido=models.CharField(
    max_length=45,
    db_column='cli_apellido',
    null=False
  )
  clienteEmail= models.EmailField(
    max_length=45,
    db_column='cli_email',
    null=False
  )
  clienteFono = models.CharField(
    max_length=15,
    db_column='cli_fono',
    null=False
  )

  class Meta:
    db_table='t_cliente'
    verbose_name = 'Cliente'
    verbose_name_plural  = 'Clientes'


class MascotaModel(models.Model):
  SEXO_CHOICES=[('M','Macho'),('H','Hembra')]
  mascotaId = models.AutoField(
    primary_key=True,
    unique=True,
    null= False,
    db_column='mascota_id'
  )
  mascotaNombre = models.CharField(
    max_length=45,
    null=False,
    db_column='mascota_nombre'
  )
  mascotaFechaNacimiento = models.DateField(
    db_column='mascota_fecnac',
    null=False
  )
  mascotaSexo = models.CharField(
    max_length=1,
    choices= SEXO_CHOICES,
    default='M',
    null=False,
    db_column='mascota_sexo',
  )

  cliente = models.ForeignKey(
    to=ClienteModel,
    on_delete=models.PROTECT,
    null=False,
    related_name='mascotasCliente',
    db_column='cli_dni',
  )

  tipo = models.ForeignKey(
    to=TipoModel,
    on_delete=models.PROTECT,
    related_name='mascotasTipo',
    null=False,
    db_column='tipo_id',
  )

  class Meta:
    db_table='t_mascota'
    verbose_name='Mascota'
    verbose_name_plural='Mascotas'


class PromocionModel(models.Model):
  promociionId=models.AutoField(
    primary_key=True,
    unique=True,
    null= False,
    db_column='promo_id'
  )
  promocionDescripcion = models.CharField(
    max_length=50,
    null=False,
    db_column='promo_descripcion'
  )
  promocionEstado = models.BooleanField(
    default=True,
    null=False,
    db_column='promo_estado'
  )

  class Meta:
    db_table='t_promocion'
    verbose_name='Promocion'
    verbose_name_plural='Promociones'


class Historial(models.Model):
  historialId=models.AutoField(
    primary_key=True,
    unique=True,
    null= False,
    db_column='historial_id'
  )

  historialCanje = models.BooleanField(
    default=True,
    null=False,
    db_column='historial_canje'
  )

  mascota = models.ForeignKey(
    to=MascotaModel,
    null=False,
    on_delete=models.PROTECT,
    db_column='mascota_id',
    related_name='historialesMascota'
  )

  promocion = models.ForeignKey(
    to=PromocionModel,
    null=False,
    on_delete=models.PROTECT,
    db_column='promo_id',
    related_name='historialesPromocion'
  )

  class Meta:
    db_table='t_historial'
    verbose_name='Historial'
    verbose_name_plural='Historiales'