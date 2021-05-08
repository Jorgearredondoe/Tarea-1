import  win32com.client
import speech_recognition as sr 
import es_core_news_sm
import Funct_Fechas as ff

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
   tt[4]['origen>destino>fecha_ida>ida_regreso>']   = 5

   #Estado 6
   tt[6]['origen>destino>']   = 1
   tt[6]['origen>destino>fecha_ida>ida_regreso>fecha_regreso>']   = 7

   #Estado 7
   tt[7]['origen>destino>fecha_ida>ida_regreso>fecha_regreso>'] = 5


   return(tt)

def EspecificarPreguntasDFA():
   Quest = ["Qué tipo de servicio requiere? ",
            "¿Cual es su fecha de ida? ",
            "¿Necesita vuelo de vuelta? ",
            "¿Para cuando necesita su vuelo de vuelta?",
            "No necesita vuelo de vuelta",
            "Se esta procesando su consulta",
            "¿Cuál es su destino?",
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
      if var_aux == 1:
         auto_texto = ''
         var_aux = 0
      
      #print('estado',q)
      if q == 1:
         print('Llegue al estado 1')
         #Sym = q1_input()#si auto_texto es global, no será necesario que retorne nada
      elif q == 2:
         Sym = q2_input()
      elif q == 3:
         Sym = q3_input()
      elif q == 4:
         Sym = q4_input()
      elif q == 5:
         Sym = q5_input()
      elif q == 6:
         print('Llegue al estado 6')
         Sym = q6_input()
      else:
         print(auto_texto)
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


def q1_input():
   #tal vez hay que poner un while variable distinto de None, se repita el loop y vuelva a preguntar
   print('Indicame fecha ida y de regreso')
   texto = LeerVoz('Wena como estay')
   #llamar buqueda fecha
   creacion_dict(origen_destino) #esta debe estar actualizada con las otras variables
   creacion_texto_automata()
   



def q2_input():
      print('Indicame Placeholder')

def q3_input():
   print('Indicame Placeholder')

def q4_input():
   print('Indicame Placeholder')

def q5_input():
   print('Indicame Placeholder')

def q6_input():
   texto = LeerVoz('Indicame el destino')
   entidades = ner_texto(texto[0])#Recibe tupla con entidades, y entidadesTipo
   print(entidades[1])
   destino = ['-1', entidades[1]]
   creacion_dict(destino) #esta debe estar actualizada con las otras variables
   creacion_texto_automata()
   print(dict_elementos)
   print(auto_texto)



#Si solo se detecta un LOC, se asignará a destino
def creacion_dict(origen_destino = '-1', fecha_ida = '-1', fecha_regreso = '-1',ida_regreso = 0): #debe recibir origen_destino, fecha1,fecha2, ida_vuelta
   if dict_elementos['origen'] == '-1':
      dict_elementos['origen'] = origen_destino[0]
   if dict_elementos['destino'] == '-1':
      dict_elementos['destino'] = origen_destino[1]



#Creación de texto para automata
def creacion_texto_automata():
   global auto_texto
   for key in dict_elementos:
      if dict_elementos[key] != '-1':
         auto_texto += key+'>'
   
