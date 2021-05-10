#loc1
#loc2
#fecha1
#fecha2
#ida_vuelta

#dateparser.parse

import es_core_news_sm
import re
import automata as glo
import Funct_Fechas as ff
import busqueda_iata as bi

#Inicialización de tts
def inicializarTTS():
   rate = -2  # de -10 (lento) a 10 (rapido)
   speak = win32com.client.Dispatch('Sapi.SpVoice')
   speak.Voice = speak.GetVoices().Item(1) #Cambiar a 1 logra funcionar bien, default = 2
   speak.Rate = rate
   return(speak.Speak)

#========================================================================================================
#Texto reconocido!
#========================================================================================================





#================================================================================
#Inicio de programa principal
#================================================================================
glo.creacion_texto_automata()
while (glo.auto_texto == ''):
   #Lectura de voz de requerimiento inicial
   texto = glo.LeerVoz('¿En que lo puedo servir?')

   #Se determina si existe alguna locación dentro del texto recibido
   origen_destino = glo.busqueda_origen_destino(texto)

   #Se determina si existe alguna fecha dentro del texto recibido
   fechas = ff.funcion_fechas(texto[0])

   #En caso de existir dos fechas en la variable anterior (ida y regreso) la variable ida_regreso_var será igual a 1
   ida_regreso_var = ff.comparar_fechas(fechas)
   #Se inicializa el diccionario con los valores del requerimiento inicial
   glo.creacion_dict(origen_destino,fechas[0],ida_regreso_var ,fechas[1]) 

   #Se crea el texto de verificación del automata
   glo.creacion_texto_automata()
#=================================================================
#Automata
#=================================================================
#Se crean las variables del automata
nQ = 11 # Numero de estados
#Sigma = todos los posibles inputs en los estados
Sigma = {'','fecha_ida>','origen>','origen>destino>','fecha_ida>ida_regreso>fecha_regreso>','origen>destino>fecha_ida>', 'origen>destino>fecha_ida>ida_regreso>','origen>destino>fecha_ida>ida_regreso>fecha_regreso>','fecha_ida>', 'ida_regreso>','origen>fecha_ida>' ,'fecha_regreso>', 'destino>', 'destino>fecha_ida>ida_regreso>fecha_regreso>', 'origen>fecha_ida>ida_regreso>fecha_regreso>', 'destino>','destino>fecha_ida>'}  # 
q0 = 0    # Estado inicial
F = {5}   # Estado final

#Inicialización de tabla automata
TablaTransicion = glo.InicializarDFA(nQ,Sigma)
#Inicialización de preguntas de cada estado
Questions = glo.EspecificarPreguntasDFA()

#Ingreso a automata
status = glo.DFA(q0,F,Sigma,Questions,TablaTransicion)
if (status):
   print()
   print('='*50)
   if glo.dict_elementos['ida_regreso'] == 1:
      print('Su origen es {} con destino a {} para el día {} con fecha de regreso {}'.format(glo.dict_elementos['origen'],glo.dict_elementos['destino'],glo.dict_elementos['fecha_ida'],glo.dict_elementos['fecha_regreso']))

      iata_code = (bi.busqueda_iata_code(glo.dict_elementos['origen']),bi.busqueda_iata_code(glo.dict_elementos['destino']))

      if '-1' in iata_code:
         print('Error Ciudad código IATA no encontrado para ciudad',iata_code.index('-1'))
      else:
         print("https://www.latam.com/es_cl/apps/personas/booking?fecha2_dia={}&country=cl&vuelos_fecha_salida_ddmmaaaa={}&auAvailability=1&language=es&nadults=1&cabina=Y&ninfants=0&fecha2_anomes={}-{}&ida_vuelta=ida_vuelta&fecha1_dia={}&fecha1_anomes={}-{}&from_city2={}&from_city1={}&flex=1&vuelos_fecha_regreso_ddmmaaaa={}&to_city1={}&nchildren=0&to_city2={}#/'".format(glo.dict_elementos['fecha_regreso'][:2], glo.dict_elementos['fecha_ida'], glo.dict_elementos['fecha_regreso'][-4:], glo.dict_elementos['fecha_regreso'][3:5], glo.dict_elementos['fecha_ida'][:2], glo.dict_elementos['fecha_ida'][-4:], glo.dict_elementos['fecha_ida'][3:5], iata_code[0], iata_code[0], glo.dict_elementos['fecha_regreso'], iata_code[1], iata_code[1]))

   else:
      print('Su origen es {} con destino a {} para el día {} sin regreso'.format(glo.dict_elementos['origen'],glo.dict_elementos['destino'],glo.dict_elementos['fecha_ida']))

      iata_code = (bi.busqueda_iata_code(glo.dict_elementos['origen']),bi.busqueda_iata_code(glo.dict_elementos['destino']))
      if '-1' in iata_code:
         print('Error Ciudad código IATA no encontrado para ciudad',iata_code.index('-1'))
      else:
         print("https://www.latam.com/es_cl/apps/personas/booking?fecha2_dia=20&country=cl&vuelos_fecha_salida_ddmmaaaa={}&auAvailability=1&language=es&nadults=1&cabina=Y&ninfants=0&fecha2_anomes=2021-05&ida_vuelta=ida&fecha1_dia={}&fecha1_anomes={}-{}&from_city2={}&from_city1={}&flex=1&vuelos_fecha_regreso_ddmmaaaa=20/05/2021&to_city1={}&nchildren=0&to_city2={}#/".format(glo.dict_elementos['fecha_ida'], glo.dict_elementos['fecha_ida'][:2], glo.dict_elementos['fecha_ida'][-4:], glo.dict_elementos['fecha_ida'][3:5], iata_code[0], iata_code[0], iata_code[1], iata_code[1]))

   
   
else:
    print("Error en la interacción!")




