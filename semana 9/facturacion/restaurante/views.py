from rest_framework import generics, status
from .serializers import *
from rest_framework.response import Response
from uuid import uuid4

class PlatosController(generics.ListCreateAPIView):
    queryset = PlatoModel.objects.all()
    serializer_class = PlatoSerializer

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
    plato.delete()
    return Response({
      'success':True,
      'content': None,
      'message': 'Plato eliminado exitosamente'
    })