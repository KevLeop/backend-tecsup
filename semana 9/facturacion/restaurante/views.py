from rest_framework import generics, status
from .serializers import *
from rest_framework.response import Response
from uuid import uuid4
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from .permissions import *
import os
from django.conf import settings
from datetime import date

class PlatosController(generics.ListCreateAPIView):
    queryset = PlatoModel.objects.all()
    serializer_class = PlatoSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, administradorPost]
    def get(self, request):
      respuesta = self.serializer_class(instance=self.get_queryset(),many=True)
      return Response({
          'success': True,
          'content':respuesta.data,
          'message':None
      })

    def post(self, request):
      archivo = request.FILES['platoFoto']
      tipo_archivo = archivo.content_type.split('/')[1]
      print(tipo_archivo)
      print(archivo.content_type)
      print(archivo.name)
      print(archivo.size)
      request.FILES['platoFoto'].name = str(uuid4()) + '.'+tipo_archivo
      respuesta = self.serializer_class(data=request.data)
      if respuesta.is_valid():
        respuesta.save()
        
        return Response({
            'success': True,
            'content': respuesta.data,
            'message': 'Se registro el palto exitosamente'
        })
      else:
        return Response({
          'success':False,
          'content':respuesta.errors,
          'message':'Error al registrar el plato'
        },status.HTTP_400_BAD_REQUEST)

   

class PlatoController(generics.RetrieveUpdateDestroyAPIView):
  queryset = PlatoModel.objects.all()
  serializer_class = PlatoSerializer
  def get_queryset(self, id):
    return PlatoModel.objects.get(platoId = id)

  def get(self,request,id):
    resultado = self.serializer_class(instance=self.get_queryset(id))
    return Response({
      'success':True,
      'content': resultado.data,
      'message': None
    })

  def put(self,request,id):
    pass

  def delete(self,request,id):
    plato = self.get_queryset(id)
    print(settings.BASE_DIR)
    try:

      foto = str(plato.platoFoto)
      ruta_imagen = settings.MEDIA_ROOT / foto
      os.remove(ruta_imagen)
      print(ruta_imagen)
    except:
      print('Foto del plato no existe')
    plato.delete()
    return Response({
      'success':True,
      'content': None,
      'message': 'Plato eliminado exitosamente'
    })


class RegistrarPersonalController(generics.CreateAPIView):
  serializer_class = RegistroSerializer

  def post(self,request):
    nuevoPersonal = self.serializer_class(data=request.data)
    if nuevoPersonal.is_valid():
      nuevoPersonal.save()
      return Response({
        'success': True,
        'content': nuevoPersonal.data,
        'message': 'Usuario registrado'
      }, status.HTTP_200_OK)
    else:
      return Response({
        'success': False,
        'content': nuevoPersonal.errors,
        'message': 'Error al crear el nuevo personal'
      }, status.HTTP_400_BAD_REQUEST)

class CustomPayloadController(TokenObtainPairView):
  permission_classes=[AllowAny]
  serializer_class = CustomPayloadSerializer

class MesaController(generics.ListCreateAPIView):
  queryset = MesaModel.objects.all()
  serializer_class = MesaSerializer
  permission_classes=[soloAdministrador]
  # [AllowAny] => Permite sin token ni validacion
  # [IsAuthenticated] => Valida token valida
  # [IsAuthenticatedOrReadOnly] => solamente pedira la token en el caso
  #   que no sea lectura (POST, PUT, DELETE)
  # [isAdminUser] => Valida que el usuario que está intentando acceder
  # a cualquiera de los metodos sea is_staff

  def get(self, request):
    print(request.user)
    print(request.auth)
    resultado = self.serializer_class(instance=self.get_queryset(),many=True)
    return Response({
      'success':True,
      'content': resultado.data,
      'message':None
    })

  def post(self,request):
    resultado = self.serializer_class(data=request.data)
    if resultado.is_valid():
      resultado.save()
      return Response({
        'success':True,
        'content':resultado.data,
        'message': 'Mesa creada exitosamente'
      })
    else:
      return Response({
        'success':False,
        'content': resultado.errors,
        'message': 'Error al guardar la mesa'
      },status.HTTP_400_BAD_REQUEST)

class NotaPedidoController(generics.CreateAPIView):
  serializer_class = NotaPedidoCreacionSerializer
  permission_classes=[IsAuthenticated, soloMozos]
  def post(self, request):
    # crear la cabecera
    data = self.serializer_class(data = request.data)
    data.is_valid(raise_exception=True)
    numeroMesa = data.validated_data['mesa']
    objMesa = MesaModel.objects.filter(mesaId=numeroMesa).first()
    nuevaCabecera = CabeceraComandaModel(
      cabeceraFecha=date.today(),
      cabeceraTotal = 0,
      cabeceraCliente= data.validated_data['cliente'],
      mozo = request.user,
      mesa = objMesa
      )
    nuevaCabecera.save()
    # crear el detalle
    detalle = data.validated_data['detalle']
    for det in detalle:
      # al momento de crear el detalle validaar si existe el plato
      objPlato = PlatoModel.objects.filter(platoId = det['plato']).first()
      DetalleComandaModel(
        detalleCantidad= det['cantidad'],
        detalleSubtotal = det['subtotal'],
        plato = objPlato,
        cabecera= nuevaCabecera
        ).save()
      # restar la cantidad vendida de los platos
      objPlato.platoCantidad -= det['cantidad']
      objPlato.save()
    resultado = MostrarPedidoSerializer(instance=nuevaCabecera)

    return Response({
      'success':True,
      'content': resultado.data,
      'message': 'Venta creada exitosamente'

    })

class MozoMesasController(generics.ListAPIView):
  queryset = PersonalModel.objects.all()
  serializer_class = PersonalSerializer
  permission_classes=[IsAuthenticated, soloMozos]
  def get_queryset(self, id):
    return PersonalModel.objects.get(personalId = id)
  
  def get(self,request,id):
    resultado = self.serializer_class(instance=self.get_queryset(id))
    return Response({
      'success':True,
      'content': resultado.data,
      'message': None
    })

