from enum import auto
from flask_restful import Resource, reqparse
from models.autor import AutorModel

serializer = reqparse.RequestParser()
serializer.add_argument(
  'autor_nombre',
  type = str,
  required =True,
  help ='Falta el autor_nombre'
)


class AutoresController(Resource):
  def post(self):
    informacion = serializer.parse_args()
  
    # creamos una nueva instancia de nuestro modelo del Autor pero aun no se ha creado en la BD,
    # esto sirve para validar que los campos ingresador cumplan con las definiciones de las columnas
    nuevoAutor= AutorModel(informacion['autor_nombre'])
    # aahora si se guarda en la BD, si hubiese algun problema dará el error de la BD
    # pero el indice (pk), si es autoincrementable, se saltará una posición
    nuevoAutor.save()
    print("//////////////////////////////////////////////////////////")
    print(nuevoAutor)

    
    
    return {
      'success': True,
      'content': nuevoAutor.json(),
      'message': 'Autor creado exitosamente'
    },201

  
  def get(self):
    # SELECT * FROM T_AUTOR
    print("///////////////////////////////////////////////////////////////////////////////////")
    resultado=[]
    lista_autores=AutorModel.query.all()
    for autor in lista_autores:
      resultado.append(autor.json())

    return {
      'success':True,
      'content':resultado,
      'message': None
    }


class AutorController(Resource):
  def get(self, id):
    # .all => retorna todas las coincidencias => Una lista de instancias
    # .first => retorna el primer registro de las coincidencias => retorna una instancia
    autorEncontrado = AutorModel.query.filter_by(autorId=id).first()
    print("///////////////////////////////////////////////////////////////////////////////////")
    print(autorEncontrado)
    if autorEncontrado:
      return {
        'success': True,
        'content': autorEncontrado.json(),
        'message': 'OK'
      }
    else:
      return {
        'success': False,
        'content': None,
        'message': 'No se encontró autor'
      },404

    

  def put(self,id):
    autorEncontrado = AutorModel.query.filter_by(autorId=id).first()
    # no siempre es necesaria hacer la validacion de que el objeto exista,
    # el front se encarga de la validacion
    if autorEncontrado:
      data = serializer.parse_args()
      autorEncontrado.autorNombre = data['autor_nombre']
      autorEncontrado.save()
      return {
        'success': True,
        'content': autorEncontrado.json(),
        'message': 'Se actualizo el autor con exito'
      },201
    return {
      'success': False,
      'content': None,
      'message': 'No se encontro el autor a actualizar'
    },404


  def delete(self,id):
    autorEncontrado = AutorModel.query.filter_by(autorId=id).first()
    if autorEncontrado:
      autorEncontrado.delete()
      return {
        'success': True,
        'content': None,
        'message': 'Autor eliminado exitosamente'
      }
    return{
      'success': False,
      'content': None,
      'message':"No se encontró autor a eliminar"
    },404

    
  