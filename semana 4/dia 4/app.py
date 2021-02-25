from controllers.categoria import CategoriaController
from flask import Flask, request
from flask_restful import Api
from config.base_datos import bd
from controllers.autor import AutoresController, AutorController
from controllers.categoria import CategoriaController
from controllers.libro import LibrosController
from controllers.sede import LibroSedeController, SedesController
from models.libro import LibroModel
# from models.sede import SedeModel
from models.sedeLibro import SedeLibroModel

app=Flask(__name__)

print(app.config)
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:@localhost:3306/flasklibreria'
api = Api(app)

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
if __name__ == '__main__':
  app.run(debug=True)


  