from rest_framework import serializers
from .models import EspecieModel, MascotaModel, RazaModel

  

class MostrarRazaSerializer(serializers.ModelSerializer):
  class Meta:
    model=RazaModel
    fields='__all__'
  

class EspecieSerializer(serializers.ModelSerializer):
  razas = MostrarRazaSerializer(source='especiesRaza',many=True,read_only=True)
  def update(self):
    print(self.instance)
    print(self.validated_data)
    self.instance.especieNombre=self.validated_data.get('especieNombre')
    self.instance.especieEstado=self.validated_data.get('especieEstado')
    # el metodo save() es el metodo de los MODELS que se encarfa de guardar en la BD
    self.instance.save()
    return self.data

  def delete(self):
    self.instance.especieEstado = False
    self.instance.save()
    return self.data

  class Meta:
    # para que haga match con el model, y pueda jalar las columns con sus propiedades
    model = EspecieModel
    # indicar qué columnas(atributos) quiero utilizar en este serializador
    # si queremos usar todos los campos =>'__all__'
    # si quermos solamente usar ciertos campos (minoria) => ['campo1','campo2',...]
    # si queremos usar la mayoria de campos y evitar una minoria => exclude=['campo1','campo2',...]
    fields = '__all__'
  
class EspecieVistaSerializer(serializers.ModelSerializer):
  class Meta:
    model= EspecieModel
    fields='__all__'

class RazaEscrituraSerializer(serializers.ModelSerializer):
  class Meta:
    model=RazaModel
    fields='__all__'
  
class RazaVistaSerializer(serializers.ModelSerializer):
  especie = EspecieVistaSerializer()
  class Meta:
    model=RazaModel
    fields='__all__'

class MascotaSerializer(serializers.ModelSerializer):
  class Meta:
    model=MascotaModel
    fields='__all__'