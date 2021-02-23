from config.base_datos import bd
from sqlalchemy.orm import relationship

class SedeModel(bd.Model):
  __tablename__ ="t_sede"
  sedeId = bd.Column(
                    name = "sede_id",
                    type_=bd.Integer, # tipo de dato en la bd
                    primary_key=True, # setear si es PK(True) o no (False)
                    autoincrement=True, # setear si va a autoincrementarse
                    nullable=False, # seter si va a admitir valores nulos o no
                    unique=True # si no se va a repetir el valor
  )
  sedeUbicacion = bd.Column(name="sede_ubicacion",
                            type_=bd.String(45))
  sedeLatitud = bd.Column(name="sede_latitud", type_= bd.Float(),nullable=False)
  sedeLongitud =bd.Column(name="sede_longitud", type_= bd.Float(),nullable=False)

  libros = relationship('SedeLibroModel', backref='sedeLibro')



  # def __init__(self, nombreSede):

