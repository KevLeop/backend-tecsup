from flask_restful import Resource, reqparse
from models.sede import SedeModel

# get all sede
# create sede
# vincula una sede con varios libros y viceversa(un libro con varias sedes)
# busqueda de todos los libros de una sede
serializer = reqparse.RequestParser(bundle_errors=True)
serializer.add_argument(
  'sede_ubicacion',
  type=str,
  required=True,
  help='Falta sede_ubicacion',
  location='json',
  dest='ubicacion'
)
serializer.add_argument(
  'sede_latitud',
  type=float,
  required=True,
  help='Falta la sede_latitud',
  location='json',
  dest='latitud'
)

serializer.add_argument(
  'sede_longitud',
  type=float,
  required=True,
  help='Falta la sede_longitud',
  location='json',
  dest='longitud'
)

class SedesController(Resource):
  def post(self):
    data=serializer.parse_args()
    print(data)
    # Los tipos de datos que no son ni numéricos, ni estrings,decimal, o fecha,
    # no pueden hacer la conversion automática
    nuevaSede =   SedeModel(data['ubicacion'],data['latitud'],data['longitud'])
    nuevaSede.save()
    return {
      'success': True,
      'content': nuevaSede.json(),
      'message': "Sede creada exitosamente"
    }

  def get(self):
    resultado = []
    sedes = SedeModel.query.all()
    for sede in sedes:
      resultado.append(sede.json())
    return {
      'success': True,
      'content': resultado,
      'message': None
    }

class LibroSedeController(Resource):
  def get(self, id_sede):
    # de acuerdo al id de la sede devolver todos los libros que hay en esa sede
    libros= []
    sede = SedeModel.query.filter_by(sedeId=id_sede).first()
    sedeLibros = sede.libros
    
    print("/////////////////////////////////////////////")
    print(sedeLibros)
    for sedeLibro in sedeLibros:
      libro = sedeLibro.libroSede.json()
      # libros.append(libro)
      libro['autor']= sedeLibro.libroSede.autorLibro.json()
      libros.append(libro)

    resultado = sede.json()
    resultado['libros']=libros
         
    return {
      'success':True,
      'content': resultado,
      'message': None
    }




