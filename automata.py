import  win32com.client
import speech_recognition as sr 
import es_core_news_sm
import Funct_Fechas as ff
from datetime import datetime
global auto_texto
global dict_elementos

# Variable global de texto de input para automata
auto_texto = ''
#Creación diccionario para mapear los datos obtenidos
dict_elementos = {'origen' : '-1',
                  'destino' : '-1',
                  'fecha_ida' : '-1',
                  'ida_regreso' : '-1',
                  'fecha_regreso' : '-1'
                  }




#Función que "lee la voz", esta llama a ASR para determinar el input del usuario, además de realizar la lematización y POS tagging. Este retorna una tupla con tres valores, el texto reconocido por ASR, texto unido con sus etiquetas y las etiquetas.
def LeerVoz(question):
   #speak = inicializarTTS()
   # Sintetizar voz de la pregunta
   #speak(question)
   #  Reconocer respuesta hablada
   print(question)
   print('habla ahora')
   texto = ASR() #Se obtiene el input del usuario
   texto = Lematizar(texto) #Lematización del input usuario
   print('dijiste',texto)
   etiqueta = Etiquetar(texto) #Etiquetado del input usuario lematizado
   texto_etiqueta = ' '.join([w+"<"+t+">" for w,t in etiqueta]) #Unión de texto lematizado con sus etiquetas ejemplo: "a<ADP> casa<NOUN>"
   print(texto_etiqueta)
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
      #speak("Por favor, intente nuevamente")
      print("Por favor, intente nuevamente")
      return 0
   except sr.RequestError as e:
      #speak("No obtuve ningun requerimiento {0}".format(e))
      print("No obtuve ningun requerimiento {0}".format(e))
      return 0
   return(texto_reconocido)

#Realiza lematización de una frase input, retorna un string con cada palabra del input estandarizada
def Lematizar(texto):
   nlp       = es_core_news_sm.load()
   doc = nlp(texto)
   lemas = [token.lemma_ for token in doc]
   return(" ".join(lemas))

#Realiza POS tagging del texto input a partir del corpus es_core_news_sm, este retorna una lista con las etiquetas de cada palabra del texto
def Etiquetar(texto):
   nlp = es_core_news_sm.load()
   doc = nlp(texto)
   Etiquetado = [(t.text,t.pos_) for t in doc]
   return(Etiquetado)


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


def InicializarDFA(nQ,Sigma):
   _ERROR = (-1)   # Estado de error
   tt = {}
   # Crear tabla de transición vacia (con valor de error)
   for numQ in range (nQ):
      tt[numQ] = {}
      for Sym in Sigma:
         tt[numQ][Sym] = _ERROR

   # LLenar transiciones no vacias
   #Estado 0
   tt[0]['']   = 0
   tt[0]['fecha_ida>']   = 0
   tt[0]['origen>']   = 6
   tt[0]['origen>destino>'] = 1
   tt[0]['fecha_ida>ida_regreso>fecha_regreso>'] = 7
   tt[0]['origen>destino>fecha_ida>'] = 2
   tt[0]['origen>destino>fecha_ida>ida_regreso>fecha_regreso>'] = 5

   #Estado 1
   tt[1]['origen>destino>']   = 1
   tt[1]['origen>destino>fecha_ida>']   = 2
   tt[1]['origen>destino>fecha_ida>ida_regreso>fecha_regreso>']   = 5
   
   #Estado 2
   tt[2]['origen>destino>fecha_ida>']   = 4
   tt[2]['origen>destino>fecha_ida>ida_regreso>']   = 3 #revisar ida_regreso

   #Estado 3
   tt[3]['origen>destino>fecha_ida>ida_regreso>']   = 3
   tt[3]['origen>destino>fecha_ida>ida_regreso>fecha_regreso>']   = 5

   #Estado 4
   tt[4]['origen>destino>fecha_ida>']   = 5

   #Estado 6
   tt[6]['origen>']   = 6
   tt[6]['origen>fecha_ida>ida_regreso>fecha_regreso>'] = 6
   tt[6]['origen>destino>']   = 1
   tt[6]['origen>destino>fecha_ida>ida_regreso>fecha_regreso>']   = 5

   #Estado 7
   tt[7]['fecha_ida>ida_regreso>fecha_regreso>'] = 7
   tt[7]['origen>destino>fecha_ida>ida_regreso>fecha_regreso>'] = 5
   tt[7]['origen>fecha_ida>ida_regreso>fecha_regreso>'] = 6

   


   return(tt)

def EspecificarPreguntasDFA():
   Quest = ["Por favor ingrese una respuesta valida (ejemplo: localización, fechas, etc)",
            "¿Indique su Fecha de Ida", 
            "¿Necesita vuelo de vuelta? ", 
            "¿Para cuando necesita su vuelo de regreso?", 
            "No necesita vuelo de vuelta", 
            "Se esta procesando su consulta", 
            "¿Cuál es su destino?", #
            "¿Cual es su origen y Destino"
            ]
   return(Quest)


def DFA(Q0,F,Sigma,Quest,TablaTrans):
   global auto_texto
   _ERROR = (-1)   # Estado de error
   q=Q0    # Estado inicial
   # Repita hasta que llegue a un estado final o de error
   var_aux = 0
   while ( not(q in F)   and  (q != _ERROR)):
      #Se resetea auto_texto (global), así no se concatena el strign anterior
      if var_aux == 1:
         auto_texto = ''
         var_aux = 0
      
      #print('estado',q)
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
      
      print('auto_texto estado {}: {}'.format(q,auto_texto))
      Sym  = auto_texto
      try:
         TablaTrans[q][Sym]
      except KeyError:
         q = _ERROR
         break
      # Asigne el siguiente estado de la tabla o bien ERROR si no existe
      q = (_ERROR if (not(Sym in Sigma)) else TablaTrans[q][Sym])
      var_aux = 1
   return(q in F)


def q1_input(pregunta_estado):
   texto = LeerVoz(pregunta_estado)
   #llamar buqueda fecha
   fechas = ff.funcion_fechas(texto[0])
   fecha_compare = ff.comparar_fechas(fechas)
   creacion_dict(['-1','-1'], fechas[0], fecha_compare, fechas[1]) #esta debe estar actualizada con las otras variables
   creacion_texto_automata()


def q2_input(pregunta_estado):
   while aux == 0:
      texto = LeerVoz(pregunta_estado)
      #Se chequea en el texto que exista la palabra "si" o "no" (sinonimos tambien) y así determinará a que estado seguir
      #Tendra prioridad el si, por lo que si se responde "Si no", será tomado como un si
      if re.search("si", texto.lower()) != None or re.search("claro", texto.lower()) != None or re.search("afirmativo", texto.lower()) != None or re.search("efectivamente", texto.lower()) != None:
         creacion_dict(['-1','-1'], '-1', 1, '-1' #esta debe estar actualizada con las otras variables
         aux = 1
      elif re.search("no", texto.lower()) != None or re.search("negativo", texto.lower()) != None or re.search("nunca", texto.lower()) != None or re.search("jamas", texto.lower()) != None:
         aux = 1
         pass
      elif re.search("no", texto.lower()) == None and re.search("si", texto.lower()) == None:
         print('Requerimiento no valido, ingrese nuevamente\n')
   creacion_texto_automata()

def q3_input(pregunta_estado):
   texto = LeerVoz(pregunta_estado)
   #llamar buqueda fecha
   fechas = ff.funcion_fechas(texto[0])
   fecha_compare = ff.comparar_fechas(fechas)
   creacion_dict(['-1','-1'], fechas[0], fecha_compare, fechas[1]) #esta debe estar actualizada con las otras variables
   creacion_texto_automata()


def q4_input(pregunta_estado):
   print(pregunta_estado)

def q6_input(pregunta_estado):
   texto = LeerVoz('Indicame el destino')
   entidades = ner_texto(texto[0])#Recibe tupla con entidades, y entidadesTipo
   print(entidades[1])
   destino = ['-1', entidades[1]]
   creacion_dict(destino,-1,-1,-1) #esta debe estar actualizada con las otras variables
   creacion_texto_automata()
   

def q7_input(pregunta_estado):
   print('Indicame Placeholder')




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
      if dict_elementos[key] != '-1':
         auto_texto += key+'>'