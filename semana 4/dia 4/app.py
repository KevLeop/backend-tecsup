from controllers.categoria import CategoriaController
from flask import Flask, request
from flask_restful import Api
from config.base_datos import bd
from controllers.autor import AutoresController, AutorController
from controllers.categoria import CategoriaController
from controllers.libro import LibrosController,RegistroLibroSedeController
from controllers.sede import (LibroSedeController, SedesController, 
                              LibroCategoriaSedeController
                              )
from models.libro import LibroModel
# from models.sede import SedeModel
# from models.sedeLibro import SedeLibroModel
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
import os

SWAGGER_URL = "" # para indicar en qué endpoint se necontrará la documentacion
API_URL = '/static/swagger.json' # se usa para indicar enq ue parde del proyecto se encuentra el archivo de la documentacion
swagger_blueprint = get_swaggerui_blueprint(
                        SWAGGER_URL,
                        API_URL,
                        config={
                          'app_name': 'Libreria Flask - Swagger Documentation'
                        }
                    )
app=Flask(__name__)
app.register_blueprint(swagger_blueprint)

print(app.config)
# app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:@localhost:3306/flasklibreria'
app.config['SQLALCHEMY_DATABASE_URI']='mysql://gq701i1c5f7mpz9b:u1iv3wj380ztc7o5@td5l74lo6615qq42.cbetxkdyhwsb.us-east-1.rds.amazonaws.com:3306/rb452i44ef2f1sy4'

api = Api(app)
CORS(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False

bd.init_app(app)
# bd.drop_all(app=app)
bd.create_all(app=app)

@app.route('/buscar')
def buscarLibro():
  print(request.args.get('palabra'))
  palabra = request.args.get('palabra')
  
  
  if palabra:
    resultadoBusqueda=LibroModel.query.filter(LibroModel.libroNombre.like('%'+palabra+'%')).all()
    if resultadoBusqueda:
      resultado = []
      for libro in resultadoBusqueda:
        resultado.append(libro.json())
      return {
        'success': True,
        'content': resultado,
        'message': None
      }
    return {
        'success': True,
        'content': None,
        'message': "No se encontraron libros"
        },404


# RUTAS DE MI API RESTFUL
api.add_resource(AutoresController, '/autores')
api.add_resource(AutorController, '/autor/<int:id>')
api.add_resource(CategoriaController, '/categorias', '/categoria')
api.add_resource(LibrosController, '/libros')
api.add_resource(SedesController, '/sedes', '/sede')
api.add_resource(LibroSedeController, '/sedeLibros/<int:id_sede>')
api.add_resource(LibroCategoriaSedeController,'/busquedaLibroSedeCat')
api.add_resource(RegistroLibroSedeController,'/registrarSedesLibro')
if __name__ == '__main__':
  app.run(debug=True)


  