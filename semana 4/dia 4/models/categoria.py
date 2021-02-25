from config.base_datos import bd
from sqlalchemy.orm import relation, relationship

class CategoriaModel(bd.Model):
  __tablename__="t_categoria"
  categoriaId = bd.Column(
                      name="categoria_id", # Nombre de la col en la bd
                      type_=bd.Integer, # tipo de dato en la bd
                      primary_key=True, # setear si es PK(True) o no (False)
                      autoincrement=True, # setear si va a autoincrementarse
                      nullable=False, # seter si va a admitir valores nulos o no
                      unique=True # si no se va a repetir el valor
                      )
  categoriaDescripcion = bd.Column(name="categoria_descripcion", 
                                  type_=bd.String(45), 
                                  nullable=False, 
                                  unique=True)
  # esto no crea las relaciones simplemente sirve para le momento de hacer consultas con JOIN's
  libros = relationship('LibroModel', backref='categoriaLibro', lazy=True)
  
  def __init__(self,nombre):
    self.categoriaDescripcion = nombre

  def save(self):
    bd.session.add(self)
    bd.session.commit()


  def json(self):
    return {
      'categoria_id': self.categoriaId,
      'categoria_nombre': self.categoriaDescripcion,
    }