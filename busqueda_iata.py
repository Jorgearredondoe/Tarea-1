import pandas as pd

def busqueda_iata_code(ciudad):
  #Se transforma el input a lowercase y se transforman los tildes a sus vocales originales
  ciudad = ciudad.lower()
  vocals = ['a','e','i','o','u']
  vocals_acc = ['á','é','í','ó','ú']
  for i in range(len(vocals)):
    ciudad = ciudad.replace(vocals_acc[i],vocals[i])

  #Lectura de csv de aeropuerto
  df = pd.read_csv('airports.csv')  
  #Se botan columnas que no importan para este caso
  df = df.drop(['id','wikipedia_link','keywords','iso_region', 'iso_country' , 'home_link', 'scheduled_service', 'continent', 'latitude_deg', 'longitude_deg', 'ident', 'local_code', 'gps_code', 'elevation_ft', 'name'], axis=1)
  
  #Se eliminan los aeropuertos cerrados, helipueros, pequeños y otros
  arr_delete = ['heliport','closed','small_airport','seaplane_base','balloonport']
  for i in arr_delete:
    df = df[df.type != i]
  
  #Se eliminan los iata vacios
  df = df.dropna(axis='rows')
  df = df.sort_values(by='iata_code') #Se ordenan por orden alfabetico
  df['municipality'] = df['municipality'].str.lower() #Se transforman todas las ciudades a lowercase
  
  #Busqueda de ciudad
  try:
    busqueda = df[df['municipality'].str.contains(ciudad)]
    resultado = busqueda['iata_code'].iloc[0]
    return resultado
  except:
    return '-1'


busqueda_iata_code('santiago')