from django.db.models.aggregates import Count
from rest_framework import serializers
from .models import ClienteModel, EspecieModel, MascotaModel, RazaModel

  

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



class ClienteSerializer(serializers.ModelSerializer):
  class Meta:
    model = ClienteModel
    fields = '__all__'

class RegistroClienteSerializer(serializers.Serializer):
  dni = serializers.CharField(max_length=9, required=True, min_length=8)
  email = serializers.EmailField(max_length=45,trim_whitespace=True)
  telefono = serializers.CharField(max_length = 10, min_length=4)
  direccion = serializers.CharField(max_length=90)

### Relacionado con el ejercicio
class RazaSerializer(serializers.ModelSerializer):
  class Meta:
    model= RazaModel
    fields='__all__'


class MascotaRazaSerializer(serializers.ModelSerializer):
  raza = RazaSerializer()
  class Meta:
    model=MascotaModel
    fields='__all__'


class ClienteMascotaSerializer(serializers.ModelSerializer):
  mascotas = MascotaRazaSerializer(source='mascotasCliente', many=True)
  class Meta:
    model = ClienteModel
    fields = '__all__'