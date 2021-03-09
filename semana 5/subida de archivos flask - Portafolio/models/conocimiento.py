from datetime import datetime
from config.base_datos import bd
from sqlalchemy import Column, types
from sqlalchemy.schema import ForeignKey


class ConocimientoModel(bd.Model):
  __tablename__ = 't_conocimiento'
  conocimientoId  = Column(
    name='conocimiento_id',
    type_= types.Integer,
    primary_key=True,
    autoincrement=True,
    unique=True,
    nullable=True

  )
  conocimientoTitulo = Column(
    name='conocimiento_titulo',
    type_=types.String(45),
    nullable=False

  )
  conocimientoPuntuacion = Column(
    name='conocimiento_puntuacion',
    type_=types.Float(2,1),
    nullable=False

  )
  conocimientoImagenTN = Column(
    name='conocimiento_imagen_thumbnail',
    type_=types.TEXT,
    nullable=False
  )
  conocimientoImagenLarge = Column(
    name='conocimiento_image_large',
    type_=types.TEXT,
    nullable=False
  )
  conocimientoDescripcion = Column(
    name='conocimiento_descripcion',
    type_=types.TEXT,
    nullable=False
  )

  categoria= Column(
    ForeignKey('t_categoria.cat_id'),
    name='cat_id',
    type_=types.Integer,
    nullable=False
  )

  usuario = Column(
    ForeignKey('t_usuario.usuario_id'),
    name='usuario_id',
    nullable=False,
    type_=types.Integer
  )

  def __init__(self, titulo, puntuacion, imagen1,imagen2, descripcion,categoria,usuario):
    self.conocimientoTitulo=titulo
    self.conocimientoPuntuacion=puntuacion
    self.conocimientoImagenTN=imagen1
    self.conocimientoImagenLarge=imagen2
    self.conocimientoDescripcion=descripcion
    self.categoria=categoria
    self.usuario=usuario
      