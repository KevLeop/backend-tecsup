from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db.models.fields.related import create_many_to_many_intermediary_model
from .authmanager import UsuarioManager

# Create your models here.

class PersonalModel(AbstractBaseUser, PermissionsMixin):
  TIPO_PERSONAL = [(1,'ADMINISTRADOR'),(2,'CAJERO'),(3,'MOZO')]
  personalId=models.AutoField(
    primary_key=True,
    unique=True,
    db_column='personal_id'
  )
  personalCorreo = models.EmailField(
    db_column='personal_correo',
    max_length=30,
    unique=True,
    verbose_name='Correo del usuario'
  )
  personalTipo= models.IntegerField(
    db_column='personal_tipo',
    choices=TIPO_PERSONAL,
    verbose_name='Tipo de usuario'
  )
  personalNombre= models.CharField(
    max_length=45, 
    db_column='personal_nombre',
    verbose_name='Nombre del personal'
    )
  personalApellido= models.CharField(
    max_length=45, 
    db_column='personal_apellido',
    verbose_name='Apellido del personal'
    )
  password = models.TextField(
    db_column='personal_password',
    verbose_name='Contraseña del personal'
  )
  is_active = models.BooleanField(default=True)
  is_staff = models.BooleanField(default=False)

  # asignamos el comportamiento del modelo
  objects = UsuarioManager()

  # ahora indicamos que columna va aser la encargada del login
  # esto hace que la columna sea unica y no-nullable
  USERNAME_FIELD = 'personalCorreo'

  # para solivitar los campos al momento de crear el superuser por consola
  REQUIRED_FIELDS=['personalNombre','personalTipo','personalApellido']

  class Meta:
    db_table='t_personal'
    verbose_name='personal'
    verbose_name_plural = 'personales'


class MesaModel(models.Model):
  mesaId=models.AutoField(
    primary_key=True,
    db_column='mesa_id',
    null=False
  )

  mesaNumero = models.CharField(
    db_column='mesa_numero',
    max_length=10,
    null=False,
    verbose_name='Numero de la mesa'
  )

  mesaCapacidad = models.IntegerField(
    db_column='mesa_capacidad',
    null=False,
    verbose_name='Capacidad de la mesa'
  )

  mesaEstado = models.BooleanField(
    db_column='mesa_estado',
    null=False,
    default=True,
    verbose_name='Estado de la mesa'
  )

  class Meta:
    db_table='t_mesa'
    verbose_name='Mesa'

class PlatoModel(models.Model):
  platoId=models.AutoField(
    primary_key=True,
    db_column='plato_id',
    null=False
  )

  platoDescripcion=models.CharField(
    db_column='plato_descripcion',
    max_length=50,
    null=False,
    verbose_name='Descripcion del plato'
  )
  platoCantidad=models.IntegerField(
    db_column='plato_cantidad',
    null=False,
    verbose_name='Cantidad de platos'
  )
  platoFoto=models.ImageField(
    upload_to='platos/',
    db_column='plato_foto',
    null=False,
    verbose_name='Foto del plato',
  )
  platoPrecio=models.DecimalField(
    db_column='plato_precio',
    max_digits=5,
    decimal_places=2,
    null=False,
    verbose_name='Precio del plato'
  )

  createdAt = models.DateTimeField(
    auto_now_add=True,
    db_column='created_at'
  )

  updatedAt = models.DateTimeField(
    auto_now_add=True,
    db_column='updated_at'
  )

  class Meta:
    db_table='t_plato'
    verbose_name='Plato'
  
class ComprobanteModel(models.Model):
  comprobanteId=models.AutoField(
    primary_key=True,
    unique=True,
    db_column='comprobante_id'
  )

  comprobanteSerie = models.CharField(
    max_length=4,
    db_column='comprobante_serie'
  )

  comprobanteNumero = models.IntegerField(
    db_column='comprobante_numero'
  )

  comprobantePdf = models.URLField(
    db_column='comprobante_pdf'
  )

  comprobanteCdr = models.URLField(
    db_column='comprobante_cdr'
  )

  comprobanteXml = models.URLField(
    db_column='comprobante_xml'
  )

  comprobanteRuc = models.CharField(
    max_length=11,
    db_column='comprobante_ruc'

  )

  class Meta:
    db_table='t_comprobante'
    verbose_name='Comprobante'


class CabeceraComandaModel(models.Model):
  cabeceraId= models.AutoField(
    primary_key=True,
    db_column='cabecera_id',
    unique=True,
  )

  cabeceraFecha=models.DateField(
    db_column='cabecera_fecha',
    null=False,
  )
  cabeceraTotal=models.DecimalField(
    db_column='cabecera_total',
    max_digits=5,
    decimal_places=2,
    null=False
  )

  cabeceraCliente = models.TextField(
    db_column='cabecera_cliente',
    null=False
  )

  mozo = models.ForeignKey(
    to=PersonalModel,
    on_delete=models.PROTECT,
    null=False,
    db_column='mozo_id',
    related_name='mozoCabeceras'
  )

  mesa = models.ForeignKey(
    to=MesaModel,
    on_delete=models.PROTECT,
    null=False,
    db_column='mesa_id',
  )

  comprobante= models.OneToOneField(
    to=ComprobanteModel,
    on_delete=models.CASCADE,
    null=True,
    db_column='comprobante_id'
  )

  class Meta:
    db_table = 't_comanda_cabecera'
    verbose_name='Comanda Cabecera'

class DetalleComandaModel(models.Model):
  detalleId = models.AutoField(
      primary_key=True,
      unique=True,
      db_column='detalle_id'
  )
  detalleCantidad = models.IntegerField(
      db_column='detalle_cantidad'
  )
  detalleSubtotal = models.DecimalField(
      max_digits=5,
      decimal_places=2,
      db_column='detalle_subtotal'
  )
  plato = models.ForeignKey(
      to=PlatoModel,
      db_column='plato_id',
      on_delete=models.PROTECT,
      null=False,
      related_name='platoDetalles'
  )
  cabecera = models.ForeignKey(
      to=CabeceraComandaModel,
      db_column='cabecera_id',
      on_delete=models.PROTECT,
      null=False,
      related_name='cabeceraDetalles'
  )

  class Meta:
      db_table = 't_comanda_detalle'
      verbose_name = 'detalle comanda'