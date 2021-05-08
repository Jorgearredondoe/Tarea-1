#loc1
#loc2
#fecha1
#fecha2
#ida_vuelta

#dateparser.parse

import es_core_news_sm
import  win32com.client
import speech_recognition as sr 
import re

#Variable global de texto de input para automata
global auto_texto =''
#Creación diccionario para mapear los datos obtenidos
global dict_elementos ={'Origen' : '-1',
                  'Destino' : '-1',
                  'fecha_ida' : '-1',
                  'fecha_regreso' : '-1',
                  'ida_regreso' : '-1'}

def inicializarTTS():
  rate = -2  # de -10 (lento) a 10 (rapido)
  speak = win32com.client.Dispatch('Sapi.SpVoice')
  speak.Voice = speak.GetVoices().Item(1) #Cambiar a 1 funciona, default = 2
  speak.Rate = rate
  return(speak.Speak)

def Etiquetar(texto):
    nlp = es_core_news_sm.load()
    doc = nlp(texto)
    Etiquetado = [(t.text,t.pos_) for t in doc]
    return(Etiquetado)

def ASR():
    #speak = inicializarTTS()
    texto_reconocido="" #Creación de string
    r = sr.Recognizer()                                                                                   
    with sr.Microphone() as source:    
       audio = r.listen(source)  
    try:
       texto_reconocido = r.recognize_google(audio, language='es-es') #Reconocimiento de voz, lenguaje español
    #En caso de que no se reconozca el audio o no se obtenga requerimiento se retorna 0
    except sr.UnknownValueError:
       speak("Por favor, intente nuevamente")
       #print("Por favor, intente nuevamente")
       return 0
    except sr.RequestError as e:
       speak("No obtuve ningun requerimiento {0}".format(e))
       #print("No obtuve ningun requerimiento {0}".format(e))
       return 0
    return(texto_reconocido)

def Lematizar(oracion):
   nlp       = es_core_news_sm.load()
   doc = nlp(oracion)
   lemas = [token.lemma_ for token in doc]
   return(" ".join(lemas))

def Etiquetar(texto):
    nlp = es_core_news_sm.load()
    doc = nlp(texto)
    Etiquetado = [(t.text,t.pos_) for t in doc]
    return(Etiquetado)

def LeerVoz(question):
        #speak = inicializarTTS()
        # Sintetizar voz de la pregunta
        #speak(question)
        #  Reconocer respuesta hablada
        print('habla ahora')
        texto = ASR()
        texto = Lematizar(texto)
        print('dijiste',texto)
        etiqueta = Etiquetar(texto)
        texto_etiqueta = ' '.join([w+"<"+t+">" for w,t in etiqueta])
        print(texto_etiqueta)
        return texto,texto_etiqueta,etiqueta

#========================================================================================================
#Texto reconocido!
#========================================================================================================

def ExtraerEntidades(texto):
    nlp = es_core_news_sm.load()
    doc = nlp(texto) 
    entities = [NE for NE in doc.ents]
    return(entities)


def FiltrarEntidades(Entidades, tipo_entidad):
   entidades = list()
   for Ent in Entidades:
        if (Ent.label_ == tipo_entidad):
            entidades.append(Ent.text)
   return(entidades)

def ner_texto(texto):
    nlp = es_core_news_sm.load()

    entidades= ExtraerEntidades(texto)
    entidadesTipo = FiltrarEntidades(entidades,'LOC')

    return entidades,entidadesTipo

#========================================================================================================
#NER RECONOCIDO, SE OBTIENE CIUDADES
#========================================================================================================

#Se verifica que la palabra anterior a la entidad (loc) corresponda a un ADP, de esta forma se deberían obtener dos entidades

def busqueda_origen_destino(texto):
   entidades = ner_texto(texto[0])
   origen_destino =['-1', '-1']
   aux = 0
   for i in entidades[1]:
      i_etiquetado = Etiquetar(i)
      i_etiquetado_join = ' '.join([w+"<"+t+">" for w,t in i_etiquetado])
      matching = re.search("<ADP> {}".format(i_etiquetado_join),texto[1])
      if matching != None:
         origen_destino[aux] =i
         aux +=1

   return origen_destino

#print(origen_destino)

#Si solo se detecta un LOC, se asumira que es destino
def creacion_dict(origen_destino)#debe recibir origen_destino, fecha1,fecha2, ida_vuelta
if len(origen_destino)<2:
   dict_elementos['Destino'] = origen_destino[0]
else:
   dict_elementos['Origen'] = origen_destino[0]
   dict_elementos['Destino'] = origen_destino[1]



#Creación de texto para automata
def creacion_texto_automata()
for key in dict_elementos:
   if dict_elementos[key] != '-1':
      auto_texto += key+'>'



texto = LeerVoz('Wena como estay')
origen_destino = busqueda_origen_destino(texto)
creacion_dict(origen_destino) #esta debe estar actualizada con las otras variables
creacion_texto_automata()
print(auto_texto)


