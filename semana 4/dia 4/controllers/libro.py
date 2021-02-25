from flask_restful import Resource, reqparse
from models.libro import LibroModel

serializer = reqparse.RequestParser()
serializer.add_argument(
  'libro_nombre',
  type=str,
  required=True,
  help="Falta libro_nombre",
  location='json'
)

serializer.add_argument(
  'libro_cant',
  type=int,
  required=True,
  help="Falta libro_cantidad",
  location='json'
)

serializer.add_argument(
  'libro_edicion',
  type=str,
  required=True,
  help="Falta libro_edicion",
  location='json'
)

serializer.add_argument(
  'autor_id',
  type=int,
  required=True,
  help="Falta autor_id",
  location='json'
)

serializer.add_argument(
  'categoria_id',
  type=int,
  required=True,
  help="Falta categoria_id",
  location='json'
)

class LibrosController(Resource):
  def post (self):
    data=serializer.parse_args()
    nuevoLibro=LibroModel(data['libro_nombre'],data['libro_cant'],data['libro_edicion'],
                          data['autor_id'],data['categoria_id'])
    nuevoLibro.save()
    return {
      'success': True,
      'content': nuevoLibro.json(),
      'message': 'Se creo el libro exitosamente'
    },201

  def get(self):
    resultado=[]
    libros = LibroModel.query.all()
    for libro in libros:
      resultado_temporal= libro.json()
      resultado_temporal['autor']= libro.autorLibro.json()
      resultado_temporal['categoria']= libro.categoriaLibro.json()
      resultado.append(resultado_temporal)
    return {
      'success': True,
      'content': resultado,
      'message': None
    }
