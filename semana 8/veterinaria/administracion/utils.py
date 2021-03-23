import requests

def consultarDNI(dni):
  base_url='https://apiperu.dev/api/'
  solicitud = requests.get(url=base_url+'dni/'+dni, headers={
    'Content-Type': "application/json",
    'Authorization':"Bearer 9fafa0b641569e2cbb47b2a6fd4ab4081489a884ca32bd45ef8b8f658ea82b48"
  })
  print(solicitud.json())
  print(solicitud.status_code)
  return solicitud.json()
  
  
