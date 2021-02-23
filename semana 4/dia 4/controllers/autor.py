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
    print(nuevoAutor.__dict__)
    return {
      'success': True,
      'content': None,
      'message': 'Autor creado exitosamente'
    },201