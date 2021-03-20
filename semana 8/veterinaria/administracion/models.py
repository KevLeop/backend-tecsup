from django import db
from django.db import models
from django.db.models.base import Model
from django.db.models.fields import related

class EspecieModel(models.Model):
  especieId = models.AutoField(
    primary_key=True,
    unique=True,
    null= False,
    db_column='especie_id'
  )
  especieNombre = models.CharField(
    max_length=45,
    unique=True,
    null=False,
    db_column='especie_nombre',
    verbose_name='Nombre de la especie'
  )
  especieEstado = models.BooleanField(
    default=True,
    null=False,
    db_column='especie_estado'
  )
  

  # Para modificar la forma como se  mostrará el objeto por consola
  def __str__(self):
    return "Objeto "+self.especieNombre

  class Meta:
    db_table='t_especie'
    # los sgtes atributos solamente sirven si vamos a utilizar el panel admin
    verbose_name='Especie'
    verbose_name_plural='Especies'


# Tipos de modelos: https://docs.djangoproject.com/en/3.1/ref/models/fields/
class RazaModel(models.Model):
  # si NO DEFINIMOS LA p, se creará automaticamente en mi BD con el nombre de la comlumna id
  # solamente una columna por tabla puede ser autofield
  razaId = models.AutoField(primary_key=True, 
                            auto_created=True, 
                            unique=True, 
                            null=False,
                            db_column='raza_id',
                            help_text='ID de la raza',
                            verbose_name='ID de la raza'

                            )

  def __str__(self):
    return self.razaNombre

  razaNombre = models.CharField(
    max_length=45,
    db_column='raza_nombre',
    verbose_name='Nombre de la raza'
  )
  # al momento de eliminar un padre, tenemos que indicar que va a pasar con sus hijos
  # CASCADE => PREMITE ELIMINAR AL PADRE Y CONSEUCENTEMENTE ELIMINAR A LOS HIJOS
  # PROTECT => No permite eliminar al padre mientras tenga hijos
  # SET_NULL => Permite eliminar al padre y luego a sus hijos le cambiará el valor
  #           a NULL, sus hijos quedan sin Padre
  # DO_NOTHING => Permite eliminar al padre y deja su PK sin modificar a los hijos
  # RESTRICT => No permite la eliminacion y lanzara un error de ripo RestrictedError
  # https://docs.djangoproject.com/en/3.1/ref/models/fields/#django.db.models.ForeignKey.on_delete
  especie = models.ForeignKey(
    to=EspecieModel,
    on_delete=models.PROTECT,
    db_column='especie_id', #cuando querramos ingresar a su relacion inversa
    related_name='especiesRaza',
    verbose_name='Especie',
    help_text='Id de la Especie'
    )
  # para definir algunas opciones extras como el nombre de la tabla, e ordenamiento de los resultados,
  # y modifical opciones de visualizacion en el panel administrativo se crea una clase Meta que
  # sirve par apasar los metadatos al padre (a la clase que hemos heredado)
  class Meta:
    # asi se cambia el nombre de la tabla
    db_table='t_raza'
    verbose_name='Raza'
    verbose_name_plural='Razas'




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

  raza = models.ForeignKey(
        to=RazaModel,
        on_delete=models.PROTECT,
        db_column='raza_id',
        related_name='mascotasRaza',
        null=False
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

  def __str__(self):
    return 'La promocion es: {} y su estado es: {}'.format(self.promocionDescripcion,self.promocionEstado)

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