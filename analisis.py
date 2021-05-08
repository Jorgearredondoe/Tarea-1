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



texto = glo.LeerVoz('Wena como estay')
origen_destino = busqueda_origen_destino(texto)
glo.creacion_dict(origen_destino) #esta debe estar actualizada con las otras variables
fechas = ff.funcion_fechas(texto[0])
print(fechas)

print(glo.dict_elementos)
glo.creacion_texto_automata()
print(glo.auto_texto)


#=================================================================
#Automata
#=================================================================

nQ = 8 # Numero de estados
Sigma = {'','origen>','origen>destino>','fecha_ida>ida_regreso>fecha_regreso>','origen>destino>fecha_ida>','origen>destino>fecha_ida>ida_regreso>fecha_regreso>','fecha_ida>', 'ida_regreso>', 'fecha_regreso>', 'destino>', 'destino>fecha_ida>ida_regreso>fecha_regreso>'}  # Alfabeto (sigma)
q0 = 0    # Estado inicial
F = {5}   # Estados finales

TablaTransicion = glo.InicializarDFA(nQ,Sigma)
Questions = glo.EspecificarPreguntasDFA()
status = glo.DFA(q0,F,Sigma,Questions,TablaTransicion)
if (status):
    print("Aceptado (llegué a estado final)!")
else:
    print("Error en la interacción!")



