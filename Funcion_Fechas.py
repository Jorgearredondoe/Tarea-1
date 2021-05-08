# -*- coding: utf-8 -*-
"""
Created on Sat May  8 13:20:30 2021

@author: marti
"""

import nltk
import es_core_news_sm
import dateparser
#IMPORTANTE REALIZAR pip install dateparser

def funcion_fechas(texto):
    
  # Se comienza haciendo un Etiquetado
  doc = nlp(texto)
  tagged = [(t.text,t.pos_) for t in doc]
  # el operador "*" significa 0 o más veces
  
  # Se establece la regla gramatical para encontrar las fechas
  grammar = '''                                                                                                              
    FN:                                                                                                                    
       {<NUM><ADP><NOUN><ADP>*<NUM>*}
    '''
  chunker = nltk.chunk.RegexpParser(grammar)
  Arbol = chunker.parse(tagged)
  
  # Se guardan las fechas encontradas en una lista
  fechas = []
  for subarbol in Arbol.subtrees():
        if subarbol.label() == 'FN': 
            #print(subarbol)
            fechas.append(subarbol)

  # Se crea una lista con los numeros del 1 al 31 escritos en palabras
  texto_a_numero = ["uno", "dos", "tres", "cuatro", "cinco", "seis", "siete", "ocho", "nueve", "diez", "once", "doce", "trece", "catorce", "quince", "dieciseis", "dieciciete", "dieciocho", "dievinueve", "veinte", "veintiuno", "veintidos", "veintitres", "veinticuatro", "veinticinco", "veintiseis", "veintisiete", "veintiocho", "veintinueve", "treinta", "treintaiuno"]

  # Se lee cada fecha por separado, se eliminan los caracteres que no aportan en este proceso
  fechas_2 = []
  for fecha in fechas:
        fecha = str(fecha)
        fecha = fecha.replace("(FN ","")
        fecha = fecha.replace(")","")
        fecha = fecha.replace("/NUM","")
        fecha = fecha.replace("/ADP","")
        fecha = fecha.replace("/NOUN","")
      
        # Si la fecha entregada esta escrita en lugar de ser un numero, se reemplaza por el numero correspondiente
        n=1
        for dia in texto_a_numero:
            fecha = fecha.replace(dia,str(n))
            n += 1

        # Se pasa de texto a formato de fecha para realizar la comparasion
        fecha1 = dateparser.parse(fecha)
        
        fechas_2.append(fecha1)

  fechas_2.sort()
  fecha_ida = fechas_2[0].strftime('%d/%m/%Y')
  fecha_regreso = fechas_2[1].strftime('%d/%m/%Y')
  return (fecha_ida,fecha_regreso)



nlp = es_core_news_sm.load()
texto = "miami para irme el 29 de mayo y volver el 12 de mayo"
fechas = funcion_fechas(texto)
print(fechas)