texto = 'querer<VERB> uno<DET> vuelo<NOUN> de<ADP> Santiago<PROPN> a<ADP> Berlín<PROPN>'
check_texto = texto.split()
print(check_texto)


check_texto = texto[0].split()
check_texto_etiquetas = texto[2]
origen_destino = []
check = 0
for i in entidades[1]:
   try:
      index_string = check_texto.index(i)
   except:
      try:
         i_split = i.split()
         index_string = check_texto.index(i_split[0])
      except:
         index_string = -1
         check = 1
   try:
      print(check_texto_etiquetas[index_string-1][1])
      if check_texto_etiquetas[index_string-1][1] == 'ADP' and check == 0:
         print('i',i)
         origen_destino.append(i)
         check = 0
   except:
      continue