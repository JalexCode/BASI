# -------------------------------- #
#     Autor: Javier Alejandro      #
#           BASI v1.0              #
# -------------------------------- #

import random

valor_min = 0
valor_max = 31
tam_poblacion = 6
long_cadena = 5
generaciones = 3
prob_mutacion = 0.2
pressure = 3
LOGS = ""


def individuo():
    valor = random.randint(valor_min, valor_max)
    cadena = bin(valor)[2:]
    cadena = list(map(int, ("0" * (len(bin(valor_max)[2:]) - len(cadena))) + cadena))
    return [valor, cadena]


def generar_poblacion():
    poblacion = []
    for _ in range(tam_poblacion):
        indv = individuo()
        while indv in poblacion:
            indv = individuo()
        poblacion.append(indv)
    return poblacion


def funcionFitness(individuo):  # evalua al individuo por su acercamiento al valor max
    fitness = 0
    cadena = individuo[1]
    cadena_valor_max = list(map(int, list(bin(valor_max)[2:])))
    for i in range(len(cadena)):
        if cadena[i] == cadena_valor_max[i]:
            fitness += 1
    return fitness


def funcionFitness2(cadena):  # evalua al individuo por su valor en decimal
    no_bin = cadena
    no_bin.reverse()
    no_dec = 0
    for x in range(len(no_bin)):
        bit = no_bin[x]
        pot = pow(2, x) * bit
        no_dec += pot
    return no_dec


def mutacion(poblacion):
    LOGS = ""
    for i in range(len(poblacion) - pressure):
        if random.random() <= prob_mutacion:
            ##########################################
            LOGS += "/MUTACIÓN:\n"
            ##########################################
            punto = random.randint(0, long_cadena - 1)
            nuevo_valor = random.randint(0, 1)
            while nuevo_valor == poblacion[i][1][punto]:
                nuevo_valor = random.randint(0, 1)
            ##########################################
            LOGS += "> Individuo %d %s\n" % (poblacion[i][0], str(poblacion[i][1]))
            LOGS += "- Punto de intercambio: %d | Valor correspondiente: %d\n" % (punto, poblacion[i][1][punto])
            ##########################################
            poblacion[i][1][punto] = nuevo_valor
            poblacion[i][0] = funcionFitness2(poblacion[i][1])
            ##########################################
            LOGS += "> Nuevo individuo %d %s\n" % (poblacion[i][0], str(poblacion[i][1]))
            LOGS += "------------------------------------------------------------------------\n"

    return (poblacion, LOGS)


def seleccion_reproduccion(poblacion: 'list'):
    LOGS = "/PROCESO DE REPRODUCCIÓN:\n"
    LOGS += "----------------------------------------------\n"
    ##########################################
    puntuados = [(funcionFitness(i), i) for i in poblacion]
    puntuados = [i[1] for i in sorted(puntuados)]
    poblacion = puntuados
    selected = puntuados[(len(puntuados) - pressure):]
    ##########################################
    LOGS += "/SELECCIÓN:\n"
    for x in selected:
        LOGS += "> %d | Cadena: %s | f(x^2): %d\n" % (x[0], str(x[1]), pow(x[0], 2))
    LOGS += "------------------------------------------------------------------------\n"
    ##########################################
    for i in range(len(poblacion) - pressure):
        punto = random.randint(1, long_cadena - 1)
        padre = random.sample(selected, 2)
        ##########################################
        LOGS += "+ Padres seleccionados: %s\n" % (str(padre))
        LOGS += "- Intercambio de genes a partir del punto %d\n" % (punto)
        LOGS += "+ Individuo a transformar %d %s\n" % (poblacion[i][0], str(poblacion[i][1]))
        LOGS += "- Intercambio desde la izquierda: %s -> %s\n" % (
        str(poblacion[i][1][:punto]), str(padre[0][1][:punto]))
        LOGS += "- Intercambio desde la derecha: %s -> %s\n" % (str(poblacion[i][1][punto:]), str(padre[1][1][punto:]))
        ##########################################
        poblacion[i][1][:punto] = padre[0][1][:punto]
        poblacion[i][1][punto:] = padre[1][1][punto:]
        poblacion[i][0] = funcionFitness2(poblacion[i][1])
        ##########################################
        LOGS += "+ Nuevo individuo %d %s\n" % (poblacion[i][0], str(poblacion[i][1]))
        LOGS += "------------------------------------------------------------------------\n"
    LOGS += "> Nueva generación:\n"
    for x in poblacion:
        LOGS += "+ %d | Cadena: %s | f(x^2): %d\n" % (x[0], str(x[1]), pow(x[0], 2))
    LOGS += "------------------------------------------------------------------------\n"
    return (poblacion, LOGS)


def comprobar(poblacion):
    for x in poblacion:
        #print(x)
        if x[0] != valor_max:
            return False
    return True


def iniciar(poblacion):
    LOGS = ""
    for i in range(generaciones):
        LOGS += "-----------------------\n"
        LOGS += "- Generación #%d -\n" % (i + 1)
        LOGS += "-----------------------\n"
        selec = seleccion_reproduccion(poblacion)
        poblacion = selec[0]
        LOGS += selec[1]
        if comprobar(poblacion):
            LOGS += "\nPROCESO GENÉTICO DETENIDO!\nLa población ha alcanzado la maximización global.\nProceso detenido en la generación %d\n=====================================================================\n\n" % (
                        i + 1)
            break
        mut = mutacion(poblacion)
        poblacion = mut[0]
        LOGS += mut[1]

    return (poblacion, LOGS)

# print("\nPoblacion Final:\n%s" % (poblacion))
# print("\n\n")
