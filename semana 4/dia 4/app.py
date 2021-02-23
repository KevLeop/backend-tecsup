from flask import Flask
from flask_restful import Api
from config.base_datos import bd
from controllers.autor import AutoresController
from models.categoria import CategoriaModel
from models.libro import LibroModel
from models.sede import SedeModel
from models.sedeLibro import SedeLibroModel

app=Flask(__name__)

print(app.config)
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:@localhost:3306/flasklibreria'
api = Api(app)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False

bd.init_app(app)
# bd.drop_all(app=app)
bd.create_all(app=app)



# RUTAS DE MI API RESTFUL
api.add_resource(AutoresController, '/autores')


if __name__ == '__main__':
  app.run(debug=True)


  