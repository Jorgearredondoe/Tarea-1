import nltk
from nltk.parse import ChartParser
import es_core_news_sm

# ************************************************************
# Función: Parsing(gramatica,oracion)
# Objetivo: Realizar chart parsing de una oracion en Espanol dada una gramática
# Salida: Muestra árboles sintácticos posibles
# ************************************************************
def Parsing(gram,oracion):
  Parser = ChartParser(gram)
  Trees =  Parser.parse(oracion)
  for Arbol in Trees:
      print(Arbol)
      Arbol.draw()


#**********************************************    
#  Programa Principal
#**********************************************    

# Modifique con la ubicación en donde está la gramática dada por el profesor
def parsing_tree(raw_sentence):
    PATH1   = 'C:/Users/yoshy/Desktop/Procesamiento de Lenguaje Natural/Tarea 1/airline.cfg'
    #PATH2   = 'C:/Users/yoshy/Desktop/Procesamiento de Lenguaje Natural/Tarea 1/airline1.cfg'
    #PATH3   = 'C:/Users/yoshy/Desktop/Procesamiento de Lenguaje Natural/Tarea 1/airline2.cfg'

    nlp = es_core_news_sm.load()
    RAIZ = "S"
    # Cargar una gramática CFG y generar árbol de parsing
    gramatica = nltk.data.load("file:"+PATH)
    sentence = raw_sentence.split()

    Parsing(gramatica,sentence)
