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


#========================================================================================================
#NER RECONOCIDO, SE OBTIENE CIUDADES
#========================================================================================================

#Se obtienen 
def busqueda_origen_destino(texto):
   entidades = glo.ner_texto(texto[0])#Recibe tupla con entidades, y entidadesTipo
   origen_destino =['-1', '-1'] #Creación de lista de origen_destino, donde se almacenará el string de origen [0] y destino [1]. Se inicializa con '-1' para crear correctamente el texto que se le otorgará al automata
   aux = 0 #Variable auxiliar para asignar los valores en origen_destino
   #Se recorren todas las entidades encontradas para así determinar cuales "posiblemente" son locaciones reales
   for i in entidades[1]:
      i_etiquetado = glo.Etiquetar(i) #Etiqueta de entidad
      i_etiquetado_join = ' '.join([w+"<"+t+">" for w,t in i_etiquetado]) #Se une la etiqueta con su entidad
      matching = re.search("<ADP> {}".format(i_etiquetado_join),texto[1]) #Se realiza un search para encontrar en el texto con etiquetas si es que, antes de la entidad con su etiqueta, existe una palabra con la etiqueta adposition (preposiciones o postposiciones) <ADP>
      #Se asigna la localidad encontrada a origen_destino
      if matching != None:
         #Si origen_destino[aux] esta vacio, se asigna el valor encontrado, por el contrario, se asgina al siguiente espacio
         if origen_destino[aux] == '-1':
            origen_destino[aux] =i
            aux +=1
         else:
            aux +=1
            origen_destino[aux] =i

   return origen_destino

#================================================================================
#Inicio de programa principal
#================================================================================
glo.creacion_texto_automata()
while (glo.auto_texto == ''):
   #Lectura de voz de requerimiento inicial
   texto = glo.LeerVoz('¿En que lo puedo servir?')

   #Se determina si existe alguna locación dentro del texto recibido
   origen_destino = busqueda_origen_destino(texto)

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
nQ = 9 # Numero de estados
#Sigma = todos los posibles inputs en los estados
Sigma = {'','fecha_ida>','origen>','origen>destino>','fecha_ida>ida_regreso>fecha_regreso>','origen>destino>fecha_ida>', 'origen>destino>fecha_ida>ida_regreso>','origen>destino>fecha_ida>ida_regreso>fecha_regreso>','fecha_ida>', 'ida_regreso>','origen>fecha_ida>' ,'fecha_regreso>', 'destino>', 'destino>fecha_ida>ida_regreso>fecha_regreso>'}  # 
q0 = 0    # Estado inicial
F = {5}   # Estado final

#Inicialización de tabla automata
TablaTransicion = glo.InicializarDFA(nQ,Sigma)
#Inicialización de preguntas de cada estado
Questions = glo.EspecificarPreguntasDFA()

#Ingreso a automata
status = glo.DFA(q0,F,Sigma,Questions,TablaTransicion)
if (status):
   if glo.dict_elementos['ida_regreso'] == 1:
      print('Su origen es {} con destino a {} para el día {} con fecha de regreso {}'.format(glo.dict_elementos['origen'],glo.dict_elementos['destino'],glo.dict_elementos['fecha_ida'],glo.dict_elementos['fecha_regreso']))
   else:
      print('Su origen es {} con destino a {} para el día {} sin regreso'.format(glo.dict_elementos['origen'],glo.dict_elementos['destino'],glo.dict_elementos['fecha_ida']))
else:
    print("Error en la interacción!")



