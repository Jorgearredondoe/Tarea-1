import  win32com.client
import speech_recognition as sr 
import es_core_news_sm
import Funct_Fechas as ff
from datetime import datetime
global auto_texto
global dict_elementos
import re

# Variable global de texto de input para automata
auto_texto = ''
#Creación diccionario para mapear los datos obtenidos
dict_elementos = {'origen' : '-1',
                  'destino' : '-1',
                  'fecha_ida' : '-1',
                  'ida_regreso' : '-1',
                  'fecha_regreso' : '-1'
                  }



#============================================================================
#TTS
#============================================================================
#Inicialización de tts
def inicializarTTS():
   rate = -2  # de -10 (lento) a 10 (rapido)
   speak = win32com.client.Dispatch('Sapi.SpVoice')
   speak.Voice = speak.GetVoices().Item(1) #Cambiar a 1 logra funcionar bien, default = 2
   speak.Rate = rate
   return(speak.Speak)



#============================================================================
#ASR
#============================================================================
#Función que "lee la voz", esta llama a ASR para determinar el input del usuario, además de realizar la lematización y POS tagging. Este retorna una tupla con tres valores, el texto reconocido por ASR, texto unido con sus etiquetas y las etiquetas.
def LeerVoz(question):
   #speak = inicializarTTS()
   # Sintetizar voz de la pregunta
   #speak(question)
   #  Reconocer respuesta hablada
   print("="*40)
   print(question)
   print('Hable Ahora:')
   texto = ASR() #Se obtiene el input del usuario
   texto = Lematizar(texto) #Lematización del input usuario
   #print('dijiste',texto)
   print()
   etiqueta = Etiquetar(texto) #Etiquetado del input usuario lematizado
   texto_etiqueta = ' '.join([w+"<"+t+">" for w,t in etiqueta]) #Unión de texto lematizado con sus etiquetas ejemplo: "a<ADP> casa<NOUN>"
   return texto,texto_etiqueta,etiqueta

#Automatic Speech Recognition, reconoce cuando el usuario habla y la frase la asigna  la variable texto_reconocido en formato str
def ASR():
   #speak = inicializarTTS()
   texto_reconocido = "" #Creación de string
   r = sr.Recognizer()                                                                                   
   with sr.Microphone() as source:    
      audio = r.listen(source)  
   try:
      texto_reconocido = r.recognize_google(audio, language='es-es') #Reconocimiento de voz, lenguaje español
   #En caso de que no se reconozca el audio o no se obtenga requerimiento se retorna 0
   except sr.UnknownValueError:
      print("Por favor, intente nuevamente")
      return 0
   except sr.RequestError as e:
      print("No obtuve ningun requerimiento {0}".format(e))
      return 0
   return(texto_reconocido)



#============================================================================
#Lematización
#============================================================================
#Realiza lematización de una frase input, retorna un string con cada palabra del input estandarizada
def Lematizar(texto):
   nlp = es_core_news_sm.load()
   try:
      doc = nlp(texto)
      lemas = [token.lemma_ for token in doc]
      return(" ".join(lemas))
   except:
      return 0
   


#============================================================================
#POS Tagging
#============================================================================
#Realiza POS tagging del texto input a partir del corpus es_core_news_sm, este retorna una lista con las etiquetas de cada palabra del texto
def Etiquetar(texto):
   nlp = es_core_news_sm.load()
   doc = nlp(texto)
   Etiquetado = [(t.text,t.pos_) for t in doc]
   return(Etiquetado)



#============================================================================
#NER
#============================================================================
#Función NER para realizar Parsing Parsial al texto input. Las entidades que se identificarán con esta función son Locaciones o ubicaciones (LOC) a partir del corpus es_core_news_sm
def ner_texto(texto):
    nlp = es_core_news_sm.load()
    entidades= ExtraerEntidades(texto) #Extracción de entidades de todo el texto
    entidadesTipo = FiltrarEntidades(entidades,'LOC') #Filtración de entidades deseadas (LOC)
    return entidades,entidadesTipo


#Función que extrae las entidades de un texto input y las retorna en una lista
def ExtraerEntidades(texto):
    nlp = es_core_news_sm.load() 
    doc = nlp(texto) 
    entities = [NE for NE in doc.ents] #Se extraen las entidades
    return(entities) 

#Recibe de input las entidades y el tipo de entidad deseada de filtrar (LOC en este caso) y retorna las entidades que tengan la etiqueta LOC
def FiltrarEntidades(Entidades, tipo_entidad):
   entidades = list()
   for Ent in Entidades:
        if (Ent.label_ == tipo_entidad):
            entidades.append(Ent.text)
   return(entidades)

#============================================================================
#Función de Búqueda Origen y Destino
#============================================================================
def busqueda_origen_destino(texto):
   entidades = ner_texto(texto[0])#Entrega tupla con entidades, y entidadesTipo
   origen_destino =['-1', '-1'] #Creación de lista de origen_destino, donde se almacenará el string de origen [0] y destino [1]. Se inicializa con '-1' para crear correctamente el texto que se le otorgará al automata
   #Se recorren todas las entidades encontradas para así determinar cuales "posiblemente" son locaciones reales
   for i in entidades[1]:
      i_etiquetado = Etiquetar(i) #Etiqueta de entidad
      i_etiquetado_join = ' '.join([w+"<"+t+">" for w,t in i_etiquetado]) #Se une la etiqueta con su entidad
      #print(texto[1])
      matching = re.search("(de<ADP>|desde<ADP>|origen<NOUN>) {}".format(i_etiquetado_join),texto[1]) #Se realiza un search del origen para encontrar en el texto con etiquetas si es que, antes de la entidad con su etiqueta, existe una palabra con la etiqueta correspondiente
      matching2 = re.search("(a<ADP>|hacia<ADP>|para<ADP>|destino<NOUN>) {}".format(i_etiquetado_join),texto[1]) #Se realiza un search del destino para encontrar en el texto con etiquetas si es que, antes de la entidad con su etiqueta, existe una palabra con la etiqueta correspondiente

      #Se asigna el origen y destino
      if matching != None:
         origen_destino[0] =i
      if matching2 != None:
         origen_destino[1] =i

   return origen_destino

#============================================================================
#DFA
#============================================================================
def InicializarDFA(nQ,Sigma):
   _ERROR = (-1)   # Estado de error
   tt = {}
   # Crear tabla de transición vacia (con valor de error)
   for numQ in range (nQ):
      tt[numQ] = {}
      for Sym in Sigma:
         tt[numQ][Sym] = _ERROR

   #Estado 0
   tt[0]['fecha_ida>']   = 12
   tt[0]['origen>']   = 6
   tt[0]['destino>']   = 9
   tt[0]['origen>destino>'] = 1
   tt[0]['origen>fecha_ida>'] = 11
   tt[0]['destino>fecha_ida>']   = 10
   tt[0]['fecha_ida>ida_regreso>fecha_regreso>'] = 7
   tt[0]['origen>destino>fecha_ida>'] = 2
   tt[0]['origen>destino>fecha_ida>ida_regreso>fecha_regreso>'] = 5

   #Estado 1
   tt[1]['origen>destino>']   = 1
   tt[1]['origen>destino>fecha_ida>']   = 2
   tt[1]['origen>destino>fecha_ida>ida_regreso>fecha_regreso>']   = 5
   
   #Estado 2
   tt[2]['origen>destino>fecha_ida>']   = 4
   tt[2]['origen>destino>fecha_ida>ida_regreso>']   = 3 

   #Estado 3
   tt[3]['origen>destino>fecha_ida>ida_regreso>']   = 3
   tt[3]['origen>destino>fecha_ida>ida_regreso>fecha_regreso>']   = 5

   #Estado 4
   tt[4]['origen>destino>fecha_ida>']   = 5

   #Estado 6
   tt[6]['origen>']   = 6
   tt[6]['origen>fecha_ida>ida_regreso>fecha_regreso>'] = 6
   tt[6]['origen>fecha_ida>'] = 8
   tt[6]['origen>destino>fecha_ida>'] = 2
   tt[6]['origen>destino>']   = 1
   tt[6]['origen>destino>fecha_ida>ida_regreso>fecha_regreso>']   = 5

   #Estado 7
   tt[7]['fecha_ida>ida_regreso>fecha_regreso>'] = 7
   tt[7]['origen>destino>fecha_ida>ida_regreso>fecha_regreso>'] = 5
   tt[7]['origen>fecha_ida>ida_regreso>fecha_regreso>'] = 6

   #Estado 8
   tt[8]['origen>fecha_ida>']   = 8
   tt[8]['origen>destino>fecha_ida>']   = 2

   #Estado 9
   tt[9]['destino>']   = 9
   tt[9]['origen>destino>']   = 1
   tt[9]['origen>destino>fecha_ida>']   = 2
   tt[9]['origen>destino>fecha_ida>ida_regreso>fecha_regreso>'] = 5

   #Estado 10
   tt[10]['destino>fecha_ida>']   = 10
   tt[10]['origen>destino>fecha_ida>']   = 2
   tt[10]['origen>destino>fecha_ida>ida_regreso>fecha_regreso>'] = 5

   #Estado 11
   tt[11]['origen>fecha_ida>']   = 10
   tt[11]['origen>destino>fecha_ida>']   = 2
   tt[11]['origen>destino>fecha_ida>ida_regreso>fecha_regreso>'] = 5

   #Estado 12
   tt[12]['fecha_ida>']   = 12
   tt[12]['origen>fecha_ida>']   = 11
   tt[12]['origen>destino>fecha_ida>']   = 2
  
   return(tt)

def EspecificarPreguntasDFA():
   Quest = ["Bienvenido al asistente de LAN.com, ¿En qué lo puedo servir?",
            "Indique su Fecha de Ida", 
            "¿Necesita vuelo de vuelta? ", 
            "¿Para cuando necesita su vuelo de regreso?", 
            "No necesita vuelo de vuelta", 
            "Se esta procesando su consulta", 
            "¿Cuál es su destino?", 
            "¿Cual es su origen y Destino?",
            "Fecha de ida recibida. Indique su Destino",
            "Indique su origen",
            "Indique su origen",
            "Indique su destino",
            "Indique su origen"
            ]
   return(Quest)


def DFA(Q0,F,Sigma,Quest,TablaTrans):
   global auto_texto
   _ERROR = (-1)   # Estado de error
   q=Q0    # Estado inicial
   # Repita hasta que llegue a un estado final o de error
   var_aux = 0 #Variable auxiliar para resetear auto_texto
   while ( not(q in F)   and  (q != _ERROR)):
      #Se resetea auto_texto (global), así no se concatena el string anterior
      if var_aux == 1:
         auto_texto = ''
         var_aux = 0
      #print('estado',q)
      #Si encuentra un estado, activa la función de este estado para solicitar los datos faltantes
      if q == 1:
         q1_input(Quest[q])
      elif q == 2:
         q2_input(Quest[q])
      elif q == 3:
         q3_input(Quest[q])
      elif q == 4:
         q4_input(Quest[q])
      elif q == 6:
         q6_input(Quest[q])
      elif q == 7:
         q7_input(Quest[q])
      elif q == 8:
         q8_input(Quest[q])
      elif q == 9:
         q9_input(Quest[q])
      elif q == 10:
         q10_input(Quest[q])
      elif q == 11:
         q11_input(Quest[q])
      elif q == 12:
         q12_input(Quest[q])
      #print('auto_texto estado {}: {}'.format(q,auto_texto))
      #Se actualiza Sym con auto_texto
      Sym  = auto_texto
      try:
         TablaTrans[q][Sym]
      except KeyError:
         q = _ERROR
         break
      # Asigne el siguiente estado de la tabla o bien ERROR si no existe
      q = (_ERROR if (not(Sym in Sigma)) else TablaTrans[q][Sym])
      var_aux = 1 #Variable auxiliar = 1, se resetea auto_texto
   return(q in F)

#============================================================================
#Estados DFA
#============================================================================

#Estado 1
#Indique su Fecha de Ida
def q1_input(pregunta_estado):
   texto = LeerVoz(pregunta_estado)
   fechas = ff.funcion_fechas(texto[0]) #Se detectan fechas
   fecha_compare = ff.comparar_fechas(fechas) #Se detecta si ingresan más de una fecha
   creacion_dict(['-1','-1'], fechas[0], fecha_compare, fechas[1]) #esta debe estar actualizada con las otras variables
   creacion_texto_automata() #Actualiación texto automata

#Estado 2
#¿Necesita vuelo de vuelta?
def q2_input(pregunta_estado):
   aux_var = 0
   while aux_var == 0:
      texto = LeerVoz(pregunta_estado)
      #Se chequea en el texto que exista la palabra "si" o "no" (sinonimos tambien) y así determinará a que estado seguir
      #Tendra prioridad el si, por lo que si se responde "Si no", será tomado como un si
      if re.search("si", texto[0].lower()) != None or re.search("claro", texto[0].lower()) != None or re.search("afirmativo", texto[0].lower()) != None or re.search("efectivamente", texto[0].lower()) != None or re.search("sí", texto[0].lower()):
         #Se actualiza el diccionario con la variable binaria ida_vuelta = 1
         creacion_dict(['-1','-1'], '-1', 1, '-1') #esta debe estar actualizada con las otras variables
         aux_var = 1
      elif re.search("no", texto[0].lower()) != None or re.search("negativo", texto[0].lower()) != None or re.search("nunca", texto[0].lower()) != None or re.search("jamas", texto[0].lower()) != None:
         aux_var = 1
         pass
      #Requerimiento no valido
      elif re.search("no", texto[0].lower()) == None and (re.search("si", texto[0].lower()) == None or re.search("sí", texto[0].lower()) == None):
         print('Requerimiento no valido, ingrese nuevamente\n')
   creacion_texto_automata() #Actualiación texto automata


#Estado 3
#¿Para cuando necesita su vuelo de regreso?
def q3_input(pregunta_estado):
   texto = LeerVoz(pregunta_estado)
   fechas = ff.funcion_fechas(texto[0]) #Busqueda de fechas
   fecha_compare = ff.comparar_fechas(fechas) #Se determina si es que fueron entregado dos fechas, se determina ida y vuelta
   creacion_dict(['-1','-1'], fechas[1], fecha_compare, fechas[0]) #Actualización de diccionario
   creacion_texto_automata() #Actualiación texto automata

#Estado 4
#No necesita vuelo de vuelta
def q4_input(pregunta_estado):
   print(pregunta_estado) #No realiza acción, pasa a estado final
   creacion_texto_automata() #Actualiación texto automata

#Estado 6
#¿Cuál es su destino?
def q6_input(pregunta_estado):
   texto = LeerVoz(pregunta_estado)
   fechas = ff.funcion_fechas(texto[0]) #busqueda de fechas
   fecha_compare = ff.comparar_fechas(fechas) #Se determina si es que fueron entregado dos fechas, se determina ida y vuelta
   entidades = ner_texto(texto[0])
   try:
      destino = ['-1', str(entidades[0][0])]
      #Se asigna la entidad encontrada en la posicion 2 de locación del diccionario, es decir, destino
      creacion_dict(destino,'-1','-1','-1')
   except:
      pass
   creacion_dict(['-1','-1'],fechas[0],fecha_compare,fechas[1]) #Actualización de diccionario con las fechas
   creacion_texto_automata() #Actualiación texto automata
   

#Estado 7
#¿Cual es su origen y Destino?
def q7_input(pregunta_estado):
   texto = LeerVoz(pregunta_estado)
   entidades = ner_texto(texto[0])
   #Si solo se encuentra una entidad, se asigna como origen
   if len(entidades[0]) == 1:
      origen_arr = [str(entidades[0][0]),'-1']
      #Se asigna la entidad encontrada en la posicion 1 de locación del diccionario, es decir, origen
      creacion_dict(origen_arr,'-1','-1','-1')  
   #Si se encuentran dos, se asigna origen y destino
   elif len(entidades[1]) == 2:
      origen_destino_arr = [str(entidades[0][0]),str(entidades[0][1])]
      #Se asigna las entidades encontradas, en la posicion 1 y 2 de locación del diccionario, es decir, origen y destino
      creacion_dict(origen_destino_arr,'-1','-1','-1')  
   creacion_texto_automata() #Actualiación texto automata


#Estado 8
#Fecha de ida recibida. Indique su Destino
def q8_input(pregunta_estado):
   texto = LeerVoz(pregunta_estado)
   entidades = ner_texto(texto[0])#Recibe tupla con entidades, y entidadesTipo
   try:
      destino = ['-1', str(entidades[0][0])]
      #Se asigna la entidad encontrada, en la posicion 2 de locación del diccionario, es decir, destino
      creacion_dict(destino,'-1','-1','-1')
   except:
      pass
   creacion_texto_automata() #Actualiación texto automata


#Estado 9
#Indique su origen
def q9_input(pregunta_estado):
   texto = LeerVoz(pregunta_estado)
   entidades = ner_texto(texto[0])#Recibe tupla con entidades, y entidadesTipo
   try:
      origen = [str(entidades[0][0]), '-1']
      #Se asigna la entidad encontrada, en la posicion 1 de locación del diccionario, es decir, origen
      creacion_dict(origen,'-1','-1','-1')
   except:
      pass
   #Se revisa si existen fechas en el requerimiento
   fechas = ff.funcion_fechas(texto[0])
   fecha_compare = ff.comparar_fechas(fechas)#Se determina si es que fueron entregado dos fechas, se determina ida y vuelta
   creacion_dict(['-1','-1'],fechas[0],fecha_compare,fechas[1])
   creacion_texto_automata() #Actualiación texto automata



#Estado 10
#Indique su origen
def q10_input(pregunta_estado):
   texto = LeerVoz(pregunta_estado)
   entidades = ner_texto(texto[0])#Recibe tupla con entidades, y entidadesTipo
   try:
      origen = [str(entidades[0][0]), '-1']
      #Se asigna la entidad encontrada, en la posicion 1 de locación del diccionario, es decir, origen
      creacion_dict(origen,'-1','-1','-1')
   except:
      pass
   fechas = ff.funcion_fechas(texto[0])#Se busca si existe fecha de regreso
   if fechas[0] != '-1':
      creacion_dict(['-1','-1'],'-1',1,fechas[0])
   creacion_texto_automata() #Actualiación texto automata


#Estado 11
#Indique su destino
def q11_input(pregunta_estado):
   texto = LeerVoz(pregunta_estado)
   entidades = ner_texto(texto[0])
   try:
      destino = ['-1',str(entidades[0][0])]
      #Se asigna la entidad encontrada, en la posicion 2 de locación del diccionario, es decir, DESTINO
      creacion_dict(destino,'-1','-1','-1')
   except:
      pass
   fechas = ff.funcion_fechas(texto[0]) #Se busca por fecha de regreso, en caso de que exista
   if fechas[0] != '-1':
      creacion_dict(['-1','-1'],'-1',1,fechas[0])
   creacion_texto_automata()#Actualiación texto automata

#Estado 12
#Indique su origen
def q12_input(pregunta_estado):
   texto = LeerVoz(pregunta_estado)
   entidades = ner_texto(texto[0])
   #Se verifica cuantas entidades se encontraron.
   #En caso de ser 1, se asigna de origen. Si se reciben dos, estas se asignan como origen y destino
   if len(entidades[0]) == 1:
      try:
         destino = [str(entidades[0][0]),'-1']
         #Se asigna la entidad encontrada, en la posicion 2 de locación del diccionario, es decir, DESTINO
         creacion_dict(destino,'-1','-1','-1')
      except:
         pass
   elif len(entidades[0]) == 2:
      try:
         destino = [str(entidades[0][0]),str(entidades[0][1])]
         #Se asigna la entidad encontrada, en la posicion 2 de locación del diccionario, es decir, DESTINO
         creacion_dict(destino,'-1','-1','-1')
      except:
         pass
   creacion_texto_automata()#Actualiación texto automata




#============================================================================
#Creación Diccionario (dict_elementos) y texto_automata(auto_texto)
#============================================================================
#Si solo se detecta un LOC, se asignará a destino
def creacion_dict(origen_destino = ['-1','-1'], fecha_ida = '-1',ida_regreso = '-1', fecha_regreso = '-1'): #debe recibir 
   #origen y destino
   if dict_elementos['origen'] == '-1':
      dict_elementos['origen'] = origen_destino[0]
   if dict_elementos['destino'] == '-1':
      dict_elementos['destino'] = origen_destino[1]
   
   #ida y vuelta
   if ida_regreso != '-1' and dict_elementos['ida_regreso'] == '-1':
      dict_elementos['ida_regreso'] = ida_regreso

   #fechas
   if fecha_ida != '-1' and dict_elementos['fecha_ida'] == '-1':
      dict_elementos['fecha_ida'] = fecha_ida
   if fecha_regreso != '-1' and dict_elementos['fecha_regreso'] == '-1':
      dict_elementos['fecha_regreso'] = fecha_regreso
   if dict_elementos['fecha_ida'] != '-1' and dict_elementos['fecha_regreso']!= '-1':
      dates = [dict_elementos['fecha_ida'], dict_elementos['fecha_regreso']]
      #dates.sort(key = lambda date: datetime.strptime(date, '%d/%m/%Y'))
      dict_elementos['fecha_ida'] = dates[0]
      dict_elementos['fecha_regreso'] = dates[1]


#Creación de texto para automata
def creacion_texto_automata():
   global auto_texto
   for key in dict_elementos:
      #Si la key esta vacía ('-1'), significa que ese dato aun no es obtenido, por lo que se genera el auto_texto con lso datos que solamente han sido obtenidos
      if dict_elementos[key] != '-1':
         auto_texto += key+'>'
   