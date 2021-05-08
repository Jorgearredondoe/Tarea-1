# **************************************************************
# Autor:  Jorge Arredondo, Martín Fica, Bastián Sepúlveda
# Fecha: 01/05/2021
# Contenido: 
#     
# **************************************************************
#  IMPORTANTE: debe instalar
#       conda install -c conda-forge speechrecognition
#       conda install PyAudio
#
#
#
# **************************************************************
from reconocimiento import ASR
from texttospeech import inicializarTTS
from etiqueta_POS import Etiquetar
from morfologico import Lematizar
from chunking import Chunking
from automata import InicializarDFA,EspecificarPreguntasDFA,DFA
#from parsing_requerimiento import parsing_tree
#from NER import ner_requerimiento
# import re

'''
El programa debe tener:
-Análisis de voz
-Análisis Morfológico
-Análisis Léxico
-Análisis Sintáctico (parsing)


'''

#Inicio Programa Principal

#Variables para DFA

nQ=4    # Numero de estados
Sigma = {'0','vuelo<NOUN>', '<NOUN><ADP><NOUN>'}  # Alfabeto (sigma)
q0=0    # Estado inicial
F={3}   # Estados finales


TablaTransicion = InicializarDFA(nQ,Sigma)
#speak = inicializarTTS()
#requerimiento = 0
#speak("Bienvenido al asistente de LAN.com, ¿En qué lo puedo servir?")
print('Bienvenido al asistente de LAN.com')
Questions = EspecificarPreguntasDFA()
status = DFA(q0,F,Sigma,Questions,TablaTransicion)



# **************************************************************
#Análisis Léxico(etiqueta_POS.py)
# **************************************************************
#Se realiza POS tagging del requerimiento lematizado
# etiqueta_requerimiento = Etiquetar(lema_requerimiento)
# print(etiqueta_requerimiento)





