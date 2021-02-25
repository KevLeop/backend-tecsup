from re import search
from flask_restful import Resource, reqparse
from werkzeug.exceptions import RequestURITooLarge
from models.categoria import CategoriaModel

serializer = reqparse.RequestParser()
serializer.add_argument(
  'categoria_descripcion',
  type=str,
  required = True,
  help= ' Falta la categoria descripcion',
  location = 'json' # Por defecto intenta buscar en todos
  # los campos posibles y si lo encuentra no retorna error, 
  # pero si queremos indicar exactamente por qué medio me lo tiene que
  # pasar debemos indicar el location.
  # https://flask-restful.readthedocs.io/en/latest/reqparse.html#argument-locations

)


class CategoriaController(Resource):
  def get (self):

    resultado=[]
    categorias = CategoriaModel.query.all()
    print("/////////////////////////////////////////////////////////77")
    print(categorias)
    for categoria in categorias:
      resultado.append(categoria.json())
    return {
      'success':True,
      'content': resultado,
      'message': None
    }

  def post(self):
    data = serializer.parse_args()
    nuevaCategoria = CategoriaModel(data['categoria_descripcion'])
    nuevaCategoria.save()
    return {
      'success':True,
      'content':nuevaCategoria.json(),
      'mesage': 'Categoria creada exitosamente'
    },201