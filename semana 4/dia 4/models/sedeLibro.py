from config.base_datos import bd
from sqlalchemy import Column, types
from sqlalchemy.schema import ForeignKey

class SedeLibroModel(bd.Model):
  __tablename__ = "t_sede_libro"
  # es exactamente lo miosmo usar bd.Column() que llamar a
  # sqlalchemy, la diferencia es que nos brinda ayuda.
  sedeLibroId= Column(name='sede_libro_id', type_=types.Integer, primary_key = True,
                      auto_increment=True, unique=True)
  sede = Column(ForeignKey('t_sede.sede_id'), name ='sede_id',type_=types.Integer)
  libro = Column(ForeignKey('t_libro.libro_id'), name="libro_id", type_=types.Integer)
