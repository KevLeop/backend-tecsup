from sqlalchemy.sql.expression import null
from config.base_datos import bd
from sqlalchemy import Column, types
from sqlalchemy.orm import relationship
class CategoriaModel(bd.Model):
  __tablename__ ="t_categoria"
  categoriaId = Column(
    name= 'cat_id',
    type_= types.Integer,
    primary_key=True,
    autoincrement=True,
    unique=True,
    nullable=True
  )

  categoriaNombre=Column(
    name='cat_nombre',
    type_=types.String(45),
    nullable=False
  )

  categoriaOrden=Column(
    name='cat_orden',
    type_=types.Integer,
    nullable=False
  )

  categoriaEstado=Column(
    name='cat_estado',
    type_=types.Boolean(),
    default=True,
    nullable=False
  )

  conocimientos = relationship('ConocimientoModel', backref='categoriaConocimientos', cascade='all, delete')

  def __init__(self, nombre, orden, estado):
    self.categoriaNombre = nombre,
    self.categoriaOrden = orden
    if estado:
      self.categoriaEstado=estado

  def save(self):
    bd.session.add(self)
    bd.session.commit()

      