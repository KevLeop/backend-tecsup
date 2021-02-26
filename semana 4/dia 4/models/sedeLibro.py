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


  def __init__(self,sede_id,libro_id):  
    self.sede = sede_id,
    self.libro=libro_id


  def save(self):
    bd.session.add(self)
    bd.session.commit()

  def json(self):
    return {
      'sede_libro_id': self.sedeLibroId,
      'sede': self.sede,
      'libro': self.libro
    }