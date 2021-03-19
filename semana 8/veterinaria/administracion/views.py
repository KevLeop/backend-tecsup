from .models import EspecieModel
from .serializers import EspecieSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework import status

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
    if respuesta.instance is not None:
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
    pass
  def delete (self,request,id):
    pass