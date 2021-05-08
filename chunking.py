import nltk
import es_core_news_sm

# ************************************************************
# Función: Chuking(texto)
# Objetivo: Realizar parsing parcial para algunos grupos sintácticos 
# Salida: Muestra oraciones que calzan con expresion definida
# ************************************************************ 
def Chunking(texto, tagged):
    # Definir Frase Nominal (FN) como: determinante nombre* adjetivo*
    # el operador "*" significa 0 o más veces
    grammar = '''                                                                                                              
        Vuelo:                                                                                                                   
        {<VERB>(<DET>)*<NOUN>}

        Ciudades:

        {<ADP>(<NOUN>)(<ADP><NOUN>)?}

        Fecha:
        {<NUM>(<ADP>)<NOUN>}

                                                                                                        
        '''
    subarboles = []
    chunker = nltk.chunk.RegexpParser(grammar)
    Arbol = chunker.parse(tagged)
    for subarbol in Arbol.subtrees():
            if subarbol.label() == 'Vuelo' or subarbol.label() == 'Ciudades' or subarbol.label() == 'Fecha':
                subarboles.append(subarbol) 
    
    return subarboles
            



