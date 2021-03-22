from re import M
from django.db.models.query import QuerySet
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from .models import EspecieModel, MascotaModel, RazaModel
from .serializers import EspecieSerializer, MascotaSerializer, RazaEscrituraSerializer, RazaVistaSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework import serializers, status
from django.db.models import Count
# # Create your views here.
class EspeciesController(ListCreateAPIView):

  # queryset: Consulta que se realizará a la BD  en todo el controlador
  queryset = EspecieModel.objects.all() #SELECT * FROM t_especie
  serializer_class = EspecieSerializer

  # def get_queryset(self):
  #     return self.queryset.all()

  # todo lo que concierne al request => https://www.django-rest-framework.org/api-guide/requests/
  def get(self,request):
    # en el request se almacenan todos lo datos que manda el front
    print(self.queryset)
    respuesta=self.serializer_class(instance=self.get_queryset(), many=True)
    print(respuesta.data)
    return Response(data={
      "success":True,
      "content":respuesta.data,
      "message":None
    },status=200)

  def post(self,request):
    # en el request se almacenan todos lo datos que manda el front
    print(request.data)
    data = self.serializer_class(data=request.data)
    # Si indicamos el parametro raise_exception=True este detendrá el proceidimiento
    # para responder los errores que esten en el serializer
    print(data.is_valid())
    print(data.errors)
    if(data.is_valid()):
      data.save()

      return Response(data={
        "success":True,
        "content":data.data,
        "message":None
      },status=201)
    else:
      print(data.errors.get("especieNombre")[0])
      texto = "{} ya se encuentra registrado".format(request.data.get("especieNombre"))
      data.errors.get('especieNombre')[0]=texto
      return Response(data={
        'success':False,
        'content': data.errors,
        'message': 'Hubo un error al guardar la especie'
      },status=status.HTTP_400_BAD_REQUEST)

  # def put(self, request):
  #   return Response('ok')


class EspecieController(RetrieveUpdateDestroyAPIView):
  queryset = EspecieModel.objects.all()
  serializer_class=EspecieSerializer
  def get_queryset(self,id):
    return EspecieModel.objects.filter(especieId=id).first()
      
  def get(self,request,id):
    especie = self.get_queryset(id)
    respuesta = self.serializer_class(instance=especie)
    print(respuesta.instance)
    
    # if respuesta.data.get('especieId'):
    # if especie
    if respuesta.instance:
      return Response(data={
        'success':True,
        'content':respuesta.data,
        'message':"Consulta exitosa"
      }, status=status.HTTP_200_OK)
    else:
      return Response(data={
        'success':False,
        'content':None,
        'message':"ID de especie no existe"
      }, status=status.HTTP_400_BAD_REQUEST)
  
  def put(self,request,id):
    especie = self.get_queryset(id)
    respuesta = self.serializer_class(instance=especie,data=request.data)
    if respuesta.is_valid():
      resultado = respuesta.update()
      return Response(data={
        "success":True,
        "content": resultado,
        'message':'Se actualizó la especie exitosamente'
      })
    else:
      return Response(data={
        'success':False,
        'content':respuesta.errors,
        'message':'Data incorrecta'
      })

  def delete (self,request,id):
    especie=self.get_queryset(id)

    if especie:
      respuesta = self.serializer_class(instance=especie)
      respuesta.delete()
      return Response(data={
        'success':True,
        'content':None,
        'message':'Se inhabilitó la especie'
      })
    else: 
      return Response(data={
        'success':False,
        'content':None,
        'message':'Especie no existe'
      })

class RazasController(ListCreateAPIView):
  queryset = RazaModel.objects.all()
  serializer_class = RazaEscrituraSerializer
  def post(self,request):
    respuesta = self.serializer_class(data=request.data)
    if respuesta.is_valid():
      respuesta.save()
      return Response(data={
        'success': True,
        'content':respuesta.data,
        'message':'Raza creada exitosamente'
      },status=status.HTTP_201_CREATED)
    else:
      return Response(data={
        'success':False,
        'content':respuesta.errors,
        'message': 'Data incorrecta'
      },status=status.HTTP_400_BAD_REQUEST)

  def filtrar_razas(self):
    razas = RazaModel.objects.all()
    resultado =[]
    for raza in razas:
      if (raza.especie.especieEstado):
        resultado.append(raza)
    return resultado


  def get(self,request):
    respuesta = RazaVistaSerializer(instance=self.filtrar_razas(),many=True)
    print(self.get_queryset()[0].especie.especieNombre)
    return Response({
      'success':True,
      'content': respuesta.data,
      'message':None
    })


class MascotasController(ListCreateAPIView):
  queryset= MascotaModel.objects.all()
  serializer_class=MascotaSerializer

  def post(self,request):
    resultado = self.serializer_class(data=request.data)
    if resultado.is_valid():
      resultado.save()
      return Response(data={
        'success':True,
        'content': resultado.data,
        'message': 'Mascota registrada exitosamente'
      },status=status.HTTP_200_OK)
    else:
      return Response(data={
        'success':False,
        'content': resultado.errors,
        'message': 'Hubo un error al registrar mascota'

      },status=status.HTTP_400_BAD_REQUEST)

  def get(self,request):
    resultado = self.serializer_class(instance=self.get_queryset(), many=True) 
    return Response(
      {
        'success':True,
        'content': resultado.data,
        'message':"None"
      }
    )

class CustomController(APIView):
  def get(self,request):
    return Response({
      "Prueba con custom controller"
    })
  
# @api_view([GET,POST])
# def prueba2(request):
#   print(request.method)
#   print(request.data)
#   if (request.method=='POST'):
#     pass
#   return Response({
#     'message':'Esto es un controlador'
#   })

class BusquedaController(ListCreateAPIView):
  queryset = MascotaModel.objects.all()
  serializer_class = MascotaSerializer
  # https://docs.djangoproject.com/en/3.1/ref/models/querysets/#gt
  def get(self,request):
    if request.query_params.get('fecha'):
      anio = request.query_params.get('fecha')
      # mascotas = MascotaModel.objects.filter(mascotaFechaNacimiento__range=(anio+"-01-01",anio+"-12-31"))

      mascotas = MascotaModel.objects.filter(mascotaFechaNacimiento__year=anio).all()
      resultado = self.serializer_class(instance=mascotas,many=True)
      return Response(data={
        'success':True,
        'content':resultado.data,
        'message':'ok'
        })
    else:
      return Response(data={
        'success':False,
        'content':None,
        'message':'No se tienen campos de fecha'
      })

#  En el ORM seria => MascotaModel.objects.filter(mascotaFechaNacimiento__range=("2018-01-01","2018-12-31"))

#constrolador para contabilizar cuantas masotas son machos y cuantas hembras


@api_view(['GET'])
def contabilizar_sexo(request):
  resultado =MascotaModel.objects.values('mascotaSexo').annotate(Count('mascotaSexo')).order_by('-mascotaSexo')
  pruebas = MascotaModel.objects.order_by('raza__razaNombre').all()
  pruebas2 = MascotaModel.objects.filter(raza__razaNombre='Shitzu')
  print(pruebas2)
  # print(pruebas)
  return Response({
    'success':True,
    'content': resultado,
    'message': 'OK'
  })
