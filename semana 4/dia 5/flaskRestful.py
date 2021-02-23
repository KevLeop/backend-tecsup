from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
app = Flask(__name__)
productos =[]
# 1. Crear instancia de mi clase Api para poder declarar las turas 
# de mis Resource
api =Api(app)
CORS(app,
  # resources={r"/producto/*":{"origins":"*"}, "/almacen":{"origins":"mipagina.com"}})
  # origins=['mipagina.com','otrapagina.com']
  methods=['POST','PUT','DELETE','GET']


# CORS(app,resources={"*":{"origins":"*"}})



@app.route('/',methods=['GET','POST'])
def start():
  return 'Bienvenido a mi API'


# servicio restful de Flask
class Producto(Resource):
  def post(self):
    # request.data devuelve lo que nos manda el front en formato texto plano
    # reques.get_json() devuelve lo que manda el front en diccionario 
    # print(request.get_json())
    # nuevo_producto = request.get_json()
    nuevo_producto= serializer.parse_args()
    productos.append(nuevo_producto)
    print('ingreso al POST')
    return {
      'success':True,
      'content':nuevo_producto,
      'message': "Producto creado exitosamente"

    }

  def get(self):
    return {
      'success':True,
      'content':productos,
      'message': None
    }


serializer = reqparse.RequestParser()
serializer.add_argument(
  'producto_nombre',
  type=str,
  required=True,
  help='Falta el producto_nombre',
  location='json'
)
serializer.add_argument(
  'producto_precio',
  type=float,
  required=True,
  help='Falta producto_precio',
  location='json'
)
serializer.add_argument(
  'producto_cantidad',
  type=int,
  required=True,
  help="Falta producto_cantidad",
  location='json'
)

class ProductoUnico(Resource):
  
  def get(self,id):
    longitud=len(productos)
    if longitud > id:
      return {
        'success':True,
        'content':productos[id],
        'message': None
      }
    else:
      return {
        'success':False,
        'content':productos[id],
        'message': 'Producto con id ${} no existe'.format(id)
      },400

  def put(self,id):
    longitud = len(productos)
    data = serializer.parse_args()
    if longitud >id:
      #existe
      productos[id]=data
      return {
        'success':True,
        'content':productos[id],
        'message': "Producto eliminado con exito"
      }, 201
    else:
      return {
        'success':False,
        'content':None,
        'message': 'Producto con id {} no existe'.format(id)
      }, 400

  def delete(self,id):
    longitud = len(productos)
    data = serializer.parse_args()
    if longitud >id:
      #existe
      productos[id]=data
      return {
        'success':True,
        'content':productos[id],
        'message': "Producto actualizado con exito"
      }, 201
    else:
      return {
        'success':False,
        'content':None,
        'message': 'Producto con id {} no existe'.format(id)
      }, 400 



# Con el uso de flask restful ya no se necesitan decoradores
# solo se declara el Resource y todas las rutas que queramos que
# funcionen para esos metodos
api.add_resource(Producto,'/producto','/otro')
api.add_resource(ProductoUnico,'/producto/<int:id>')
app.run(debug=True)


