import analisis
from analisis import LeerVoz


def InicializarDFA(nQ,Sigma):
   tt = {}
   # Crear tabla de transición vacia (con valor de error)
   for numQ in range (nQ):
      tt[numQ] = {}
      for Sym in Sigma:
         tt[numQ][Sym] = _ERROR

   # LLenar transiciones no vacias
   tt[0]['origen']   = 1
   tt[1]['origen_destino'] = 2
   tt[0]['origen_destino']   = 2
   tt[2]['casa']   = 3
   tt[2]['departamento']    = 1
   return(tt)


   def EspecificarPreguntasDFA():
   Quest = ["Qué tipo de servicio requiere? ",
            "Que tipo de Cliente? ",
            "Que tipo de residencia? ",
            "Pregunta del estado 3? ",
            ]
   return(Quest)


_ERROR=(-1)   # Estado de error
nQ=4    # Numero de estados
Sigma = {'destino','destino_origen','destino_origen_fechaida','subscripcion','casa','departamento'}  # Alfabeto (sigma)
q0=0    # Estado inicial
F={3}   # Estados finales
TablaTransicion = InicializarDFA(nQ,Sigma)
Questions = EspecificarPreguntasDFA()
status = DFA(q0,F,Sigma,Questions,TablaTransicion)
if (status):
    print("Aceptado (llegué a estado final)!")
else:
    print("Error en la interacción!")


def DFA(Q0,F,Sigma,Quest,TablaTrans):
    q=Q0    # Estado inicial
    # Repita hasta que llegue a un estado final o de error
    while ( not(q in F)   and  (q != _ERROR)):
        if q == 1:
           Sym = q1_input()#si auto_texto es global, no será necesario que retorne nada
         elif q == 2:
           Sym = q2_input()
         elif q == 3:
           Sym = q3_input()
         elif q == 4:
           Sym = q4_input()
         elif q == 5:
           Sym = q5_input()
        else:
           Sym  = auto_texto
        try:
           TablaTrans[q][Sym]
        except KeyError:
           q = _ERROR
           break
        # Asigne el siguiente estado de la tabla o bien ERROR si no existe
        q = (_ERROR if (not(Sym in Sigma)) else TablaTrans[q][Sym])
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

   
   