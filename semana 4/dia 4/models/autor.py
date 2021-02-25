from config.base_datos import bd
# si aun no sabemos los tipos de dato, podemos usar ...
# from sqlalchemy import types
# https://docs.sqlalchemy.org/en/13/core/type_basics.html?highlight=datatypes
class AutorModel(bd.Model):
  # Para cambiar el nombre de la tabla a crearse
  __tablename__="t_autor"
  autorId = bd.Column(
                      name="autor_id", # Nombre de la col en la bd
                      type_=bd.Integer, # tipo de dato en la bd
                      primary_key=True, # setear si es PK(True) o no (False)
                      autoincrement=True, # setear si va a autoincrementarse
                      nullable=False, # seter si va a admitir valores nulos o no
                      unique=True # si no se va a repetir el valor
                      )
  autorNombre = bd.Column(name="autor_nombre", type_=bd.String(45))
  # https://docs.sqlalchemy.org/en/14/orm/relationship_api.html#sqlalchemy.orm.relationship
  # en el caso de FK se apunta al nombre de la tabla
  # backref sirve para usarse en el modelo hijo (para que nos devuelva los daos del padre)
  # lazy => define cuando SQLAlchemy va a cargar la data de la base de datos
  #   'select'/ True => valor por defecto, SQLAlchemy cargará los datos segun sea necesario
  #   'join'/ False => le dice a SQLAlchemy que cargue la relacion en la misma consulta unsa un JOIN
  #   'subquery' => Trabaja como un JOIN pero en lugar de hacerlo en una misma consulta lo hará en
  #    una subconsulta
  #   'dynamic' => es especial si se tiene muchos elementos y se desea aplicar filtros adicionales.
  #    SQLAlchemy devolverá otro objeto de consulta que se puede customizar antes de cargar los elementos
  #    de la bd
  libros = bd.relationship('LibroModel', backref='autorLibro') 
  # mientras que en los relationship se apunta al nombre del modelo.
  # en el caso de los relationship normal no puede estar creada la tablla aun


  def __init__(self, nombreAutor):
    self.autorNombre = nombreAutor

  def __str__(self):
      return '{}:{}'.format(self.autorId,self.autorNombre)
  
  def save(self):
    # el metodo session devuelve la sesion actual y evita que se cree una nueva sesion
    # y asi relentizar la conexión a mi BD
    # el metodo .add sirve para agregar toda mi instancia ( nuevo autor) 
    # a un formato que sea valido para la bd
    bd.session.add(self)
    bd.session.commit()


  def json(self):
      return {
        'autor_id': self.autorId,
        'autor_nombre': self.autorNombre
      }
  
  def delete(self):
    # con el delete se hace la eliminacion temporal de la BD
    bd.session.delete(self)
    bd.session.commit() # 



  