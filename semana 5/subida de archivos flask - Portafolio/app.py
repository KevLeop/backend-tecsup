from flask import Flask,request, send_file
from flask_restful import Api
from config.base_datos import bd
from models.usuario import UsuarioModel
from models.categoria import CategoriaModel
from controllers.redSocial import RedSocialController
# from models.redSocial import RedSocialModel
from models.contacto import ContactoModel
from models.conocimiento import ConocimientoModel  
from models.usuarioRedSocial import UsuarioRedSocialModel
# sirve para que el nombre del archivo que manda el cliente sea validado antes de guardar
# evita que se guarde nombre con caracteres especiales
from werkzeug.utils import secure_filename 
import os
from uuid import uuid4


app = Flask(__name__)
api = Api(app)
# En SQL:ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'root'
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:root@localhost:3306/portfolioFlask'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False

bd.init_app(app)
# bd.drop_all(app=app)
bd.create_all(app=app)
UPLOAD_FOLDER= 'media'
EXTENSIONES_PERMITIDAS_IMAGENES = ['jpg','png','jpeg']

def filtro_extensiones(filename):
  return '.' in filename and \
          filename.rsplit('.',1)[-1].lower() in EXTENSIONES_PERMITIDAS_IMAGENES


@app.route('/uploadFile', methods=['POST'])
def subir_archivo():
  print(request.files)
  if 'archivo' not in request.files:
    return {
      'success': False,
      'content': None,
      'message': 'No hay archivo para subir'
    },400
  archivo = request.files['archivo']
  if archivo.filename == '':
    return {
        'success': False,
        'content': None,
        'message': 'No hay archivo para subir'
      },400

  if filtro_extensiones(archivo.filename) is False:
    return {
      'success': False,
      'content': None,
      'message': 'Archivo no permitido'
    },400
  # print(archivo.mimetype)
  formato=archivo.filename.rsplit(".")[-1]

  nombre_modicado = str(uuid4()) + '.'+formato
  nombre_archivo = secure_filename(nombre_modicado)
  archivo.save(os.path.join(UPLOAD_FOLDER,nombre_archivo))
  return {
    'success':True,
    'content':nombre_archivo,
    'message':'OK Se guardó archivo con éxito'
  },201

@app.route('/devolverImagen/<string:nombre>', methods=['GET'])
def devolver_archivo(nombre):
  try:
    return send_file(os.path.join(UPLOAD_FOLDER,nombre))
  except:
    return send_file(os.path.join(UPLOAD_FOLDER,'default-img.jpg'))

@app.route('/eliminarImagen/<string:nombre>', methods=['DELETE'])
def eliminar_imagen(nombre):
  try:
    os.remove(os.path.join(UPLOAD_FOLDER,nombre))
    return {
      'success':True,
      'content': 'Imagen eliminada exitosamente'
    } # Clase 25 2:31 
  except:
    return {
      'success': False,
      'content': 'No se encontró la imagen a eliminar'
    }
api.add_resource(RedSocialController,'/redsocial')

if __name__ == '__main__':
  app.run(debug=True)

