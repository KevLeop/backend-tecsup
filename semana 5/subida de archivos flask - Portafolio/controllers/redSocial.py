from flask_restful import Resource, reqparse
from models.redSocial import RedSocialModel

serializer = reqparse.RequestParser(bundle_errors=True)
serializer.add_argument(
  'rs_nombre',
  type= str,
  required=True,
  help="Falta el rs_nombre(nombre de la red social",
  location='json'
)
serializer.add_argument(
  'rs_imagen',
  type= str,
  required=True,
  help="Falta el rs_imagen",
  location='json'
)


class RedSocialController(Resource):

  def post(self):
    pass

  def put(self):
    pass

  def get(self):
    pass