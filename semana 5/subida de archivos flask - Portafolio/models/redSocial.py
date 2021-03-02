from sqlalchemy.sql.sqltypes import String
from config.base_datos import bd
from sqlalchemy import Column, types

class RedSocialModel(bd.Model):
  __tablename__="t_red_social"
  redSocialId=Column(
    name='rs_id',
    type_= types.Integer,
    primary_key=True,
    autoincrement=True,
    unique=True,
    nullable=True

    
  )
  redSocialNombre=Column(
    name='rs_nombre',
    type_=types.String(45),
    nullable=False
    
  )
  redSocialImagen=Column(
    name='rs_imagen',
    type_=types.TEXT,
    nullable=False
  )


  def __init__(self,nombre,imagen):
    self.redSocialNombre=nombre
    self.redSocialImagen=imagen

  def save(self):
    bd.session.add(self)
    bd.session.commit()
