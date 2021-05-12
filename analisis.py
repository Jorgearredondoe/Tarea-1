import es_core_news_sm
import re
import automata as glo
import Funct_Fechas as ff
import busqueda_iata as bi

#================================================================================
#Inicio de programa principal
#================================================================================
#Se inicializa la variable global auto_texto, variable encargada del progreso del DFA
glo.creacion_texto_automata()
#Ciclo inicial que permite que el usuario entregue una respuesta valida
while (glo.auto_texto == ''):
   #Lectura de voz de requerimiento inicial
   texto = glo.LeerVoz('Bienvenido al asistente de LATAM.com, ¿En qué lo puedo servir?')
   
   #Se determina si existe alguna locación dentro del texto recibido
   origen_destino = glo.busqueda_origen_destino(texto)

   #Se determina si existe alguna fecha dentro del texto recibido
   fechas = ff.funcion_fechas(texto[0])

   #En caso de existir dos fechas en la variable anterior (ida y regreso) la variable ida_regreso_var será igual a 1
   ida_regreso_var = ff.comparar_fechas(fechas)

   #Se inicializa el diccionario con los valores del requerimiento inicial
   #Este diccionario es utilizado para crear auto_texto, variable encargada del progreso dentro del DFA
   glo.creacion_dict(origen_destino,fechas[0],ida_regreso_var ,fechas[1]) 

   #Se crea el texto de verificación del DFA
   glo.creacion_texto_automata()

#=================================================================
#Inicia Automata
#=================================================================
#Se crean las variables del automata
nQ = 13 # Numero de estados
#Sigma: todos los posibles inputs en los estados
Sigma = {'','fecha_ida>','origen>','origen>destino>','fecha_ida>ida_regreso>fecha_regreso>','origen>destino>fecha_ida>', 'origen>destino>fecha_ida>ida_regreso>','origen>destino>fecha_ida>ida_regreso>fecha_regreso>','fecha_ida>', 'ida_regreso>','origen>fecha_ida>' ,'fecha_regreso>', 'destino>', 'destino>fecha_ida>ida_regreso>fecha_regreso>', 'origen>fecha_ida>ida_regreso>fecha_regreso>', 'destino>','destino>fecha_ida>'}  # 
q0 = 0    # Estado inicial
F = {5}   # Estado final

#Inicialización de tabla automata
TablaTransicion = glo.InicializarDFA(nQ,Sigma)

#Inicialización de preguntas de cada estado
Questions = glo.EspecificarPreguntasDFA()

#Ingreso a automata
status = glo.DFA(q0,F,Sigma,Questions,TablaTransicion)
speak = glo.inicializarTTS()
if (status):
   #Variables que alojan el nombre de las ciudades origen y destino, en caso de que no se encuentre su código IATA, esta lista será llamada para entregar el nombre de la ciudad con problema.
   ciudades = [glo.dict_elementos['origen'] ,glo.dict_elementos['destino']]
   print()
   print('='*50)

   #Vuelo con ida y vuelta
   if glo.dict_elementos['ida_regreso'] == 1:
      #Print de todos los datos encontrados
      print('Su origen es {} con destino a {} para el día {} con fecha de regreso {}'.format(glo.dict_elementos['origen'],glo.dict_elementos['destino'],glo.dict_elementos['fecha_ida'],glo.dict_elementos['fecha_regreso']))
      speak('Su origen es {} con destino a {} para el día {} con fecha de regreso {}'.format(glo.dict_elementos['origen'],glo.dict_elementos['destino'],glo.dict_elementos['fecha_ida'],glo.dict_elementos['fecha_regreso']))
      print()
      #Búsqueda de codigos IATA para general el link, estos códigos son búscadas en una base de datos externa
      iata_code = (bi.busqueda_iata_code(glo.dict_elementos['origen']),bi.busqueda_iata_code(glo.dict_elementos['destino']))
      #En caso de no encontrar código IATA, se indica que este no pudo ser encontrado
      if '-1' in iata_code:
         print('Error Ciudad código IATA no encontrado para ciudad',ciudades[iata_code.index('-1')])
      else:
         #Print del link
         print("Para acceder a su requerimiento y confirmar la reserva, debe hacer click: https://www.latam.com/es_cl/apps/personas/booking?fecha2_dia={}&country=cl&vuelos_fecha_salida_ddmmaaaa={}&auAvailability=1&language=es&nadults=1&cabina=Y&ninfants=0&fecha2_anomes={}-{}&ida_vuelta=ida_vuelta&fecha1_dia={}&fecha1_anomes={}-{}&from_city2={}&from_city1={}&flex=1&vuelos_fecha_regreso_ddmmaaaa={}&to_city1={}&nchildren=0&to_city2={}#/'".format(glo.dict_elementos['fecha_regreso'][:2], glo.dict_elementos['fecha_ida'], glo.dict_elementos['fecha_regreso'][-4:], glo.dict_elementos['fecha_regreso'][3:5], glo.dict_elementos['fecha_ida'][:2], glo.dict_elementos['fecha_ida'][-4:], glo.dict_elementos['fecha_ida'][3:5], iata_code[0], iata_code[0], glo.dict_elementos['fecha_regreso'], iata_code[1], iata_code[1]))
         speak("Para acceder a su requerimiento y confirmar la reserva, debe hacer click:")

   #Vuelo sin regreso, solo ida
   else:
      #Print de todos los datos encontrados
      print('Su origen es {} con destino a {} para el día {} sin regreso'.format(glo.dict_elementos['origen'],glo.dict_elementos['destino'],glo.dict_elementos['fecha_ida']))
      print()
      speak('Su origen es {} con destino a {} para el día {} sin regreso'.format(glo.dict_elementos['origen'],glo.dict_elementos['destino'],glo.dict_elementos['fecha_ida']))
      #Búsqueda de codigos IATA para general el link, estos códigos son búscadas en una base de datos externa
      iata_code = (bi.busqueda_iata_code(glo.dict_elementos['origen']),bi.busqueda_iata_code(glo.dict_elementos['destino']))
      #En caso de no encontrar código IATA, se indica que este no pudo ser encontrado
      if '-1' in iata_code:
         print('Error Ciudad código IATA no encontrado para ciudad',ciudades[iata_code.index('-1')])
      else:
         #Print del link
         print("Para acceder a su requerimiento y confirmar la reserva, debe hacer click: https://www.latam.com/es_cl/apps/personas/booking?fecha2_dia=20&country=cl&vuelos_fecha_salida_ddmmaaaa={}&auAvailability=1&language=es&nadults=1&cabina=Y&ninfants=0&fecha2_anomes=2021-05&ida_vuelta=ida&fecha1_dia={}&fecha1_anomes={}-{}&from_city2={}&from_city1={}&flex=1&vuelos_fecha_regreso_ddmmaaaa=20/05/2021&to_city1={}&nchildren=0&to_city2={}#/".format(glo.dict_elementos['fecha_ida'], glo.dict_elementos['fecha_ida'][:2], glo.dict_elementos['fecha_ida'][-4:], glo.dict_elementos['fecha_ida'][3:5], iata_code[0], iata_code[0], iata_code[1], iata_code[1]))
         speak("Para acceder a su requerimiento y confirmar la reserva, debe hacer click:")


   print('='*50)

#Error en caso de no llegar al final del automata
else:
    print("Error en la interacción!")
    speak("Error en la interacción!")




