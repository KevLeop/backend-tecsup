import requests # libreria para consumir apis de terceros
from datetime import date, datetime
from .models import CabeceraComandaModel, ComprobanteModel, DetalleComandaModel

def emitirComprobante(pedido,cabecera_id):
  # sunat_transaccion => sirve para indicar que tipo de transacion estás realizando
  #                   generalmente se usará 1 : "VENTA INTERNA"
  cliente_denominacion = ""
  documento = 0 # el numero de documento que toca crear
  # 6 => RUC, 1=>DNI, -=>varios
  cliente_documento = pedido['cliente_documento']
  cliente_tipo_documento = pedido['cliente_tipo_documento']
  cliente_email=pedido['cliente_email']
  observaciones =pedido['observaciones']
  tipo_comprobante = pedido['tipo_comprobante']
  comanda = CabeceraComandaModel.objects.get(cabeceraId = cabecera_id)
  # sacamos el total del pedido
  total = float(comanda.cabeceraTotal)
  # el valor total sin el IGV
  total_gravada =  total / 1.18
  # el valor total del IGV de la compra
  total_igv = total - total_gravada

  if len(pedido['cliente_documento'])>0:
    # significa que el pedido fue mayor a 700 soles
    # o el cliente dio su DNI para la compra
    base_url_apiperu="https://apiperu.dev/api/"
    if cliente_tipo_documento == "RUC":
      base_url_apiperu = base_url_apiperu+'ruc/{}'.format(cliente_documento)
    elif cliente_tipo_documento == "DNI":
      base_url_apiperu = base_url_apiperu+'dni/{}'.format(cliente_documento)
    headers = {
      "Authorization":"Bearer 9fafa0b641569e2cbb47b2a6fd4ab4081489a884ca32bd45ef8b8f658ea82b48",
      "Content-Type": "application/json"
    }
    respuestaApiPeru = requests.get(url=base_url_apiperu, headers=headers)
    ##print(respuestaApiPeru.json())
    #print(base_url_apiperu)
    if cliente_tipo_documento == 'RUC':
      documento = 6
      cliente_denominacion = respuestaApiPeru.json()['data']['nombre_o_razon_social']
    elif cliente_tipo_documento =='DNI':
      documento = 1
      cliente_denominacion = respuestaApiPeru.json()['data']['nombre_completo']
    #print(cliente_denominacion)
  else:
    if total > 700 :
      return {
        'error':'Para un monto mayor a 700 es necesario una indentificacion'
      }
    # si el monto es menor a 700 soles entonces usaremos una indentificacion genérica para no buscar la indentificaion del cliente
    documento = "-"
    cliente_denominacion="VARIOS"
    cliente_documento = "VARIOS"
  # ahora rellenamos el detalle del comprobante
  # codigo => cofigo interno que manejamos nosotros
  # unidad_de_medida => NIU = Productos | ZZ = Servicios

  items =[]
  # me retorna todo el detalle de un pedido
  for detalle in comanda.cabeceraDetalles.all():
    precio_unitario = float(detalle.detalleSubtotal)
    valor_unitario = precio_unitario /1.18  # sin IGV
    cantidad = detalle.detalleCantidad
    print(precio_unitario)
    print(valor_unitario)
    item = {
      'unidad_de_medida':"NIU",
      'codigo':detalle.plato.platoId,
      'descripcion': detalle.plato.platoDescripcion,
      'cantidad': cantidad,
      'valor_unitario': valor_unitario,
      'precio_unitario':precio_unitario,
      'subtotal': valor_unitario*cantidad,
      'tipo_de_igv':1,
      "igv":(valor_unitario * cantidad)*0.18,
      'total': precio_unitario * cantidad,
      'anticipo_regularizacion': False
      }
    items.append(item)
  # indicar la serie y numero del comprobante
  # Las facturas y notas asociadas con ellas empiezan con F
  # Las boletas y notas asociadas con ellas empieas con B
  serie = ""
  ultimoComprobante = None
  if tipo_comprobante=='BOLETA':
    tipo_comprobante=2
    serie="BBB1" # traer el ultimo omprobante boleta
    ultimoComprobante = ComprobanteModel.objects.filter(comprobanteTipo=2).order_by('-comprobanteNumero').first()
  elif tipo_comprobante=='FACTURA':
    tipo_comprobante=1
    serie='FFF1'
    ultimoComprobante = ComprobanteModel.objects.filter(comprobanteTipo=1).order_by('-comprobanteNumero').first()
  if ultimoComprobante is None:
    numero = 1
  elif ultimoComprobante is not None:
    numero = ultimoComprobante.comprobanteNumero+1

  comprobante_body={
    "operacion": "generar_comprobante",
    "tipo_de_comprobante": tipo_comprobante,
    "serie":serie,
    "numero":numero,
    "sunat_transaction":1,
    "cliente_tipo_de_documento": documento,
    "cliente_numero_de_documento": cliente_documento,
    "cliente_denominacion":cliente_denominacion,
    "cliente_direccion":"",
    "cliente_email": cliente_email,
    "fecha_de_emision": datetime.now().strftime("%d-%m-%Y"),
    "moneda": 1,
    "porcentaje_de_igv": 18.00,
    "total_gravada":total_gravada,
    "total_igv":total_igv,
    "total":total,
    "detraccion":False,
    "observaciones": observaciones,
    "enviar_automaticamente_a_la_sunat":True,
    "enviar_automaticamente_al_cliente":True,
    "medio_de_pago":"EFECTIVO",
    "formato_de_pdf":"A4",
    "items":items
  }
  #print(comprobante_body)
  url_nubefact = "https://api.nubefact.com/api/v1/d17e060b-aa50-422b-9070-33c02136d62c"
  headers_nubefact={
    'Authorization': "0a5de4901def410c9eeff819d3bdc30e93b7119721bd44c284b7b7b921f2234b",
    'Content-Type':"application/json"
  }
  respuestaNubeFact = requests.post(url=url_nubefact, json=comprobante_body, headers=headers_nubefact)
  json = respuestaNubeFact.json()
  if json.get('errors'):
    return json
  else:

    nuevoComprobante = ComprobanteModel.objects.create( 
      comprobanteSerie = serie,
      comprobanteNumero = numero,
      comprobantePdf= json['enlace_del_pdf'],
      comprobanteCdr=json['enlace_del_cdr'],
      comprobanteXml=json['enlace_del_xml'],
      comprobanteRuc = cliente_documento,
      comprobanteTipo = tipo_comprobante
    )
    comanda.comprobante = nuevoComprobante
    comanda.save()
    return respuestaNubeFact.json()

