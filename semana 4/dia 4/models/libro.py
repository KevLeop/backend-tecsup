from config.base_datos import bd
from sqlalchemy.dialects import mysql
from sqlalchemy.orm import relationship
# from models.categoria import CategoriaModel

class LibroModel(bd.Model):
  __tablename__ = "t_libro"
  libroId = bd.Column(name="libro_id", 
                      type_=bd.Integer,
                      primary_key=True, # setear si es PK(True) o no (False)
                      autoincrement=True, # setear si va a autoincrementarse
                      nullable=False, # seter si va a admitir valores nulos o no
                      unique=True)
  libroNombre = bd.Column(name="libro_nombre", type_=bd.String(45))
  libroCant = bd.Column(name="libro_cant", type_=bd.Integer)
  libroEdicion = bd.Column(name="libro_edicion", type_=mysql.YEAR())
  
  #Relaciones  (fk)
  autor = bd.Column(bd.ForeignKey('t_autor.autor_id'), name="autor_id", type_=bd.Integer, nullable=False)
  categoria = bd.Column(
                        bd.ForeignKey('t_categoria.categoria_id'), 
                        name="categoria_id",
                        type_=bd.Integer,
                        nullable=False
                        )

  sedes = relationship('SedeLibroModel', backref='libroSede')
  
  def __init__(self, nombre, cantidad, edicion, autor,categoria):
    self.libroNombre=nombre
    self.libroCantidad=cantidad
    self.libroEdicion=edicion
    self.autor = autor,
    self.categoria = categoria

  def save(self):
    bd.session.add(self)
    bd.session.commit()

  def json(self):
    return {
      'libro_id': self.libroId,
      'libro_nombre': self.libroNombre,
      'libro_cant': self.libroCant,
      'autor': self.autor,
      'categoria': self.categoria
    }



