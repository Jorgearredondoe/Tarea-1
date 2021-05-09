"""
Created on Sat May  8 13:20:30 2021

@author: marti
"""

import nltk
import es_core_news_sm
import dateparser

def funcion_fechas(texto):
  nlp       = es_core_news_sm.load()
  texto = str(texto)
  texto = texto.replace("<NUM>","")
  texto = texto.replace("<ADP>","")
  texto = texto.replace("<NOUN>","")
   
  # Se comienza haciendo un Etiquetado
  doc = nlp(texto)
  tagged = [(t.text,t.pos_) for t in doc]
  #print(tagged)
  
  # el operador "*" significa 0 o más veces
  # Se establece la regla gramatical para encontrar las fechas
  grammar = '''                                                                                                              
    FN:
       {<NUM><ADP><NUM><ADP><NOUN>}  
    FN2:                                                                                                                    
       {<NUM><ADP><NOUN>}
    '''
  chunker = nltk.chunk.RegexpParser(grammar)
  Arbol = chunker.parse(tagged)
  
  # Se guardan las fechas encontradas en una lista
  fechas = []
  for subarbol in Arbol.subtrees():
        if subarbol.label() == 'FN': 
            #print(subarbol)
            fechas.append(subarbol)
        elif subarbol.label() == 'FN2':
            #print(subarbol)
            fechas.append(subarbol)

  # Se crea una lista con los numeros del 1 al 31 escritos en palabras
  texto_a_numero = ["uno", "dos", "tres", "cuatro", "cinco", "seis", "siete", "ocho", "nueve", "diez", "once", "doce", "trece", "catorce", "quince", "dieciseis", "dieciciete", "dieciocho", "dievinueve", "veinte", "veintiuno", "veintidos", "veintitres", "veinticuatro", "veinticinco", "veintiseis", "veintisiete", "veintiocho", "veintinueve", "treinta", "treintaiuno"]
  meses = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]

  # Se lee cada fecha por separado, se eliminan los caracteres que no aportan en este proceso
  fechas_2 = []
  numero_de_fechas = len(fechas)
  
  for fecha in fechas:

        fecha = str(fecha)      

        fecha = fecha.replace("(FN ","")
        fecha = fecha.replace("(FN2 ","")
        fecha = fecha.replace(")","")
        fecha = fecha.replace("/ADP","")
        fecha = fecha.replace("/NOUN","")        
        
        repeticiones = 0
        for caracter in fecha:
            if caracter == '/':
                repeticiones += 1

        if numero_de_fechas == 2 or repeticiones == 1:
            fecha = fecha.replace("/NUM","")
        
            # Si la fecha entregada esta escrita en lugar de ser un numero, se reemplaza por el numero correspondiente
            n=1
            for dia in texto_a_numero:
                fecha = fecha.replace(dia,str(n))
                n += 1

            # Se pasa de texto a formato de fecha para realizar la comparasion
            fecha1 = dateparser.parse(fecha)
        
            fechas_2.append(fecha1)
        
        elif numero_de_fechas == 1:
            for mes in meses:
                if mes in fecha:
                    mes_solicitado = mes
            posicion = fecha.find("/")
            
            primer_dia = fecha[:posicion]

            primera_fecha = str(primer_dia)+'/'+mes_solicitado
            fecha1 = dateparser.parse(primera_fecha)
            
            auxiliar = fecha[posicion+4:]            
            posicion2 = auxiliar.find("/")

            segundo_dia = auxiliar[posicion2-2:posicion2]
            segunda_fecha = str(segundo_dia)+'/'+mes_solicitado
            fecha2 = dateparser.parse(segunda_fecha)
            
            fechas_2.append(fecha1)
            fechas_2.append(fecha2)

  fechas_2.sort()
  if len(fechas_2) == 2:
        fecha_ida = fechas_2[0].strftime('%d/%m/%Y')
        fecha_regreso = fechas_2[1].strftime('%d/%m/%Y')
        return (fecha_ida,fecha_regreso)
  elif len(fechas_2) == 1:
      encontrada = fechas_2[0].strftime('%d/%m/%Y')
      return (encontrada,"-1")
  else:
      return ("-1","-1")


def comparar_fechas(fechas_list):
   if fechas_list[0] != '-1' and fechas_list[1] != '-1':
      return 1
   else:
      return '-1'



