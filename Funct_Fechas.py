import nltk
import es_core_news_sm
import dateparser
from datetime import date

def funcion_fechas(texto):
  nlp = es_core_news_sm.load()
  today = date.today()
  today = today.strftime('%d/%m/%Y')  
  mes_hoy = str(today[3:5])
    
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
    Dia al Dia de Mes:
       {<NUM><ADP><NUM><ADP><NOUN>}  
    Dia de Mes:                                                                                                                    
       {<NUM><ADP><NOUN>}
    Mañana:                                                                                                                    
       {<NOUN><ADP>*<ADV>*<ADP>*<NOUN>*<ADV>}
    Numero:                                                                                                                    
       {<NUM>}
    Hoy:                                                                                                                    
       {<ADV>}
    '''
  chunker = nltk.chunk.RegexpParser(grammar)
  Arbol = chunker.parse(tagged)
  
  # Se guardan las fechas encontradas en una lista
  fechas = []
  for subarbol in Arbol.subtrees():
        if subarbol.label() == 'Dia al Dia de Mes': 
            #print(subarbol)
            fechas.append(subarbol)
        if subarbol.label() == 'Dia de Mes':
            #print(subarbol)
            fechas.append(subarbol)
        if subarbol.label() == 'Numero':
            #print(subarbol)
            fechas.append(subarbol)
        if subarbol.label() == 'Mañana' or subarbol.label() == 'Hoy': 
            #print(subarbol)
            fechas.append(subarbol)            

  #print(fechas)
  
  # Se crea una lista con los numeros del 1 al 31 escritos en palabras
  texto_a_numero = ["uno", "dos", "tres", "cuatro", "cinco", "seis", "siete", "ocho", "nueve", "diez", "once", "doce", "trece", "catorce", "quince", "dieciseis", "dieciciete", "dieciocho", "dievinueve", "veinte", "veintiuno", "veintidos", "veintitres", "veinticuatro", "veinticinco", "veintiseis", "veintisiete", "veintiocho", "veintinueve", "treinta", "treintaiuno"]
  meses = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]

  # Se lee cada fecha por separado, se eliminan los caracteres que no aportan en este proceso
  fechas_2 = []
  
  for fecha in fechas:

        fecha = str(fecha)      

        fecha = fecha.replace("(","")
        fecha = fecha.replace(")","")
        fecha = fecha.replace("/ADP","")
        fecha = fecha.replace("/NOUN","")    
        
        repeticiones = 0
        for caracter in fecha:
            if caracter == '/':
                repeticiones += 1
        
        if fecha.find("Dia de Mes") != -1 :
            fecha = fecha.replace("/NUM","")
            fecha = fecha.replace("Dia de Mes","")
        
            # Si la fecha entregada esta escrita en lugar de ser un numero, se reemplaza por el numero correspondiente
            n=1
            for dia in texto_a_numero:
                fecha = fecha.replace(dia,str(n))
                n += 1

            # Se pasa de texto a formato de fecha para realizar la comparasion
            fecha1 = dateparser.parse(fecha)
            fecha1 = fecha1.strftime('%d/%m/%Y')
        
            fechas_2.append(fecha1)
        
        elif fecha.find("Dia al Dia de Mes") != -1:
            fecha = fecha.replace("Dia de Mes","")
            
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
            
            fecha1 = fecha1.strftime('%d/%m/%Y')
            fecha2 = fecha2.strftime('%d/%m/%Y')
            
            fechas_2.append(fecha1)
            fechas_2.append(fecha2)


 
        elif fecha.find("Numero") != -1:
            mes_solicitado = str(today[3:5])
            
            fecha = fecha.replace("/NUM","")
            fecha = fecha.replace("Numero","")
            
            fecha = fecha+'/'+mes_solicitado
            fecha1 = dateparser.parse(fecha)
            fecha1 = fecha1.strftime('%d/%m/%Y')
            fechas_2.append(fecha1)

        else:
            #fecha = fecha.replace("/ADV","")
            hoy = fecha.find("hoy")
            manana = fecha.find("mañana")
            
            if hoy != -1:
                fechas_2.append(today)
            if manana != -1:
                dia_hoy = int(str(today)[:2])
                mes_hoy = str(today[3:5])
                dia_mañana = str(dia_hoy+1)
                año_hoy = str(today[6:10])
                fecha_mañana = dia_mañana+"/"+mes_hoy+"/"+año_hoy
                fechas_2.append(fecha_mañana)

  fechas_2.sort()
  if len(fechas_2) == 2:
        fecha_ida = fechas_2[0]
        fecha_regreso = fechas_2[1]
        return (fecha_ida,fecha_regreso)
  elif len(fechas_2) == 1:
      encontrada = fechas_2[0]
      return (encontrada,"-1")
  else:
      return ("-1","-1")


def comparar_fechas(fechas_list):
   if fechas_list[0] != '-1' and fechas_list[1] != '-1':
      return 1
   else:
      return '-1'



