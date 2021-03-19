from abc import abstractproperty
from enum import auto
from re import A
from typing import Any
from rest_framework import serializers
from .models import EspecieModel

class EspecieSerializer(serializers.ModelSerializer):
  class Meta:
    # para que haga match con el model, y pueda jalar las columns con sus propiedades
    model = EspecieModel
    # indicar qué columnas(atributos) quiero utilizar en este serializador
    # si queremos usar todos los campos =>'__all__'
    # si quermos solamente usar ciertos campos (minoria) => ['campo1','campo2',...]
    # si queremos usar la mayoria de campos y evitar una minoria => exclude=['campo1','campo2',...]
    fields = '__all__'

  