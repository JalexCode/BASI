# -------------------------------- #
#     Autor: Javier Alejandro      #
#           BASI v1.0              #
# -------------------------------- #

import random

valor_min = 0
valor_max = 31
tam_poblacion = 4
generaciones = 3

def individuo(valor_min, valor_max):
    valor = random.randint(valor_min, valor_max)
    cadena = bin(valor)[2:]
    cadena = ("0" * (len(bin(valor_max)[2:]) - len(cadena))) + cadena
    ftn = pow(valor, 2)
    fitness = 0
    return [valor, cadena, ftn, fitness]

def generar_poblacion(tam_poblacion, min, max):
    indv = []
    for i in range(tam_poblacion):
        id = individuo(min, max)
        while id in indv:
            id = individuo(min, max)
        indv.append(id)
    indv = funcionFitness(indv)
    return indv

def suma(poblacion):
    suma = 0
    for i in poblacion:
        suma += i[2]
    return suma

def funcionFitness(poblacion_):
    _suma = suma(poblacion_)
    #print("Suma: %d"%_suma)
    total_indv = len(poblacion_)
    for i in range(total_indv):
        poblacion_[i][2] = pow(poblacion_[i][0], 2)
        poblacion_[i][3] = round(poblacion_[i][2]/_suma, 2)
    return poblacion_

poblacion = generar_poblacion(tam_poblacion, valor_min, valor_max)
# -------------------------- #
print("Poblacion: ", end="")
print(poblacion)
# -------------------------- #
def bin_a_dec(no_bin:'str'):
    no_bin = list(no_bin)
    no_bin.reverse()
    no_dec = 0
    pos = 0
    while len(no_bin) != 0:
        bit = int(no_bin.pop(0))
        pot = pow(2, pos)*bit
        #print("%d * %d = %d"%(bit, pot, bit*pot))
        no_dec += pot
        #print(no_dec)
        pos += 1

    return no_dec

def cruzamiento(p1, p2):
    LOGS = "/CRUZAMIENTO:\n"
    p1 = p1
    p2 = p2
    cadena_p1 = list(map(int, p1[1]))
    cadena_p2 = list(map(int, p2[1]))
    LOGS += "> Padre 1 antes del cruce: %d | %s\n"%(p1[0], "".join(list(map(str, cadena_p1))))
    LOGS += "> Padre 2 antes de cruce: %d | %s\n" % (p2[0], "".join(list(map(str, cadena_p2))))
    tam = len(cadena_p1)
    #for x in range(random.randint(0, tam-1), tam):
    bit_al_azar = random.randint(1, tam-1)
    LOGS += "* Se intercambiarán a partir del bit en la posición %d\n" % bit_al_azar
    #while cadena_p1[bit_al_azar:] == cadena_p2[bit_al_azar:]:# and len(cadena_p1[bit_al_azar:]) != len(cadena_p1):
        #print("%s == %s"%(str(cadena_p1[bit_al_azar:]), str(cadena_p2[bit_al_azar:])))
        #bit_al_azar = random.randint(1, tam-1)
        #LOGS += "* Ahora se intercambiarán a partir del bit en la posición %d\n"%bit_al_azar
    tmp = cadena_p1[bit_al_azar:]
    LOGS += "- Porción a intercambiar en el Padre 1 %s\n" % (str(cadena_p1[:bit_al_azar]).strip("]") + str(tmp) + "]")
    LOGS += "- Porción a intercambiar en el Padre 2 %s\n" % (str(cadena_p2[:bit_al_azar]).strip("]") + str(cadena_p2[bit_al_azar:]) + "]")
    cadena_p1[bit_al_azar:] = cadena_p2[bit_al_azar:]
    cadena_p2[bit_al_azar:] = tmp
    nueva_cadena_1 = "".join(list(map(str, cadena_p1)))
    nuevo_valor_1 = bin_a_dec(nueva_cadena_1)
    nueva_cadena_2 = "".join(list(map(str, cadena_p2)))
    nuevo_valor_2 = bin_a_dec(nueva_cadena_2)
    LOGS += "> Padre 1 después del cruce: %d | %s\n" % (nuevo_valor_1, nueva_cadena_1)
    LOGS += "> Padre 2 después de cruce: %d | %s\n" % (nuevo_valor_2, nueva_cadena_2)
    p1[0] = nuevo_valor_1
    p1[1] = nueva_cadena_1
    p2[0] = nuevo_valor_2
    p2[1] = nueva_cadena_2
    #nueva_generacion = funcionFitness([p1, p2])
    #print(nueva_generacion)
    LOGS += "-----------------------------------------------------------------------\n"
    return ([p1, p2], LOGS)

def mutacion(indiv):
    LOGS = "/MUTACIÓN:\n"
    cadena_p1 = list(map(int, indiv[1]))
    LOGS += "> Individuo antes de la mutación: %d | %s\n" % (indiv[0], "".join(list(map(str, cadena_p1))))

    tam = len(cadena_p1)
    x = random.randint(0, tam - 1)
    LOGS += "* Se alternará el bit en la posición %d\n" % x
    if not cadena_p1[x]:
        cadena_p1[x] = 1
    else:
        cadena_p1[x] = 0

    nueva_cadena_1 = "".join(list(map(str, cadena_p1)))
    nuevo_valor_1 = bin_a_dec(nueva_cadena_1)
    LOGS += "> Individuo después de la mutación: %d | %s\n" % (nuevo_valor_1, nueva_cadena_1)
    LOGS += "-----------------------------------------------------------------------\n"
    indiv[0] = nuevo_valor_1
    indiv[1] = nueva_cadena_1
    #nueva_generacion = funcionFitness([indiv])
    return (indiv, LOGS)

def seleccion_cruzamiento(seleccion:'list', generaciones):
    LOGS = "/PROCESO DE REPRODUCCIÓN:\n"
    LOGS += "-----------------------\n"
    _seleccion = seleccion
    for _ in range(generaciones):
        LOGS += "- Generación #%d\n"%(_+1)
        LOGS += "-----------------------\n"
        _seleccion = sorted(_seleccion, key=lambda x: x[3], reverse=True)[
                    :random.randint(2, len(_seleccion))]  # selección de los mejores individuos en un rango al azar
        # -------------------------- #
        #print("Selección: ")
        LOGS += "/SELECCIÓN:\n"
        for x in _seleccion:
            #print("%d | Cadena: %s"%(x[0], x[1]))
            LOGS += "> %d | Cadena: %s | f(x^2): %d\n"%(x[0], x[1], x[2])
        #print("--------------------------")
        # -------------------------- #
        mejor = _seleccion.pop(0) #tomo al mejor individuo
        LOGS += "> Mejor individuo: %d | %s | %d | %.2f\n" % (mejor[0], mejor[1], mejor[2], mejor[3])
        LOGS += "-----------------------------------------------------------------------\n"
        nuevos = [] # la nueva poblacion
        for i in range(len(_seleccion)): #recorro los demas padres
            #print(mejor)
            c = cruzamiento(mejor, _seleccion[i])
            LOGS += c[1]
            c = c[0]
            #print(c)
            for j in c: #cruzo a cada padre con el mejor de los padres
                mutado = [j]
                if j in nuevos:
                    mutado = mutacion(j)
                    LOGS += mutado[1]
                # print("Mutado en 0", end="")
                # print(mutado[0][0])
                nuevos.append(mutado[0])  # agrego a la nueva generacion los nuevos individuos
        # print("Nueva Generación: ")
        nuevos = funcionFitness(nuevos)
        LOGS += "> Nueva Generación:\n"
        for x in nuevos:
        #     print("%d | Cadena: %s" % (x[0], x[1]))
            LOGS += "> %d | Cadena: %s | f(x^2): %d | Adaptabilidad: %.2f\n" % (x[0], x[1], x[2], x[3])
        # print("--------------------------")
        LOGS += "-----------------------------------------------------------------------\n"
        _seleccion = nuevos #actualizo la nueva _seleccion
    return (_seleccion, LOGS)
#print(bin_a_dec('110'))
seleccion_cruzamiento(poblacion, generaciones)