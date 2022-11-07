import random

valor_min = 0
valor_max = 31
tam_poblacion = 4
generaciones = 2

def individuo():
    valor = random.randint(valor_min, valor_max)
    cadena = bin(valor)[2:]
    cadena = ("0" * (len(bin(valor_max)[2:]) - len(cadena))) + cadena
    ftn = pow(valor, 2)
    fitness = 0
    return [valor, cadena, ftn, fitness]

def generar_poblacion():
    indv = []
    for i in range(tam_poblacion):
        indv.append(individuo())
    indv = funcionFitness(indv)
    return indv

def suma(poblacion):
    suma = 0
    for i in poblacion:
        suma += i[2]
    return suma

def funcionFitness(poblacion):
    _suma = suma(poblacion)
    total_indv = len(poblacion)
    for i in range(total_indv):
        poblacion[i][3] = round(poblacion[i][2]/_suma, 2)
    return poblacion

poblacion = generar_poblacion()
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
    p1 = p1
    p2 = p2
    cadena_p1 = list(map(int, p1[1]))
    cadena_p2 = list(map(int, p2[1]))
    #print("Cadena de Padre 1 antes: %s"%("".join(list(map(str, cadena_p1)))))
    #print("Cadena de Padre 2 antes: %s" % ("".join(list(map(str, cadena_p2)))))
    tam = len(cadena_p1)
    for x in range(random.randint(0, tam-1), tam):
        if cadena_p1[x]:
            cadena_p1[x] = 0
        else: cadena_p1[x] = 1
        if cadena_p2[x]:
            cadena_p2[x] = 0
        else: cadena_p2[x] = 1
    #print("Cadena de Padre 1 después: %s" % ("".join(list(map(str, cadena_p1)))))
    #print("Cadena de Padre 2 después: %s" % ("".join(list(map(str, cadena_p2)))))
    nueva_cadena_1 = "".join(list(map(str, cadena_p1)))
    nuevo_valor_1 = bin_a_dec(nueva_cadena_1)
    nueva_cadena_2 = "".join(list(map(str, cadena_p2)))
    nuevo_valor_2 = bin_a_dec(nueva_cadena_2)
    p1[0] = nuevo_valor_1
    p1[1] = nueva_cadena_1
    p2[0] = nuevo_valor_2
    p2[1] = nueva_cadena_2
    nueva_generacion = funcionFitness([p1, p2])
    return nueva_generacion

def mutacion(indiv):
    cadena_p1 = list(map(int, indiv[1]))
    # print("Cadena de Padre 1 antes: %s"%("".join(list(map(str, cadena_p1)))))
    # print("Cadena de Padre 2 antes: %s" % ("".join(list(map(str, cadena_p2)))))
    tam = len(cadena_p1)
    x = random.randint(0, tam - 2)
    if cadena_p1[x]:
        cadena_p1[x] = 0
    else:
        cadena_p1[x] = 1
    # print("Cadena de Padre 1 después: %s" % ("".join(list(map(str, cadena_p1)))))
    # print("Cadena de Padre 2 después: %s" % ("".join(list(map(str, cadena_p2)))))
    nueva_cadena_1 = "".join(list(map(str, cadena_p1)))
    nuevo_valor_1 = bin_a_dec(nueva_cadena_1)
    indiv[0] = nuevo_valor_1
    indiv[1] = nueva_cadena_1
    nueva_generacion = funcionFitness([indiv])
    return nueva_generacion

def seleccion_cruzamiento(seleccion:'list'):
    for _ in range(generaciones):
        seleccion = sorted(seleccion, key=lambda x: x[3], reverse=True)[
                    :random.randint(2, len(seleccion))]  # selección de los mejores individuos en un rango al azar
        # -------------------------- #
        print("Selección: ")
        for x in seleccion:
            print("%d | Cadena: %s"%(x[0], x[1]))
        print("--------------------------")
        # -------------------------- #
        mejor = seleccion.pop(0) #tomo al mejor individuo
        nuevos = [] # la nueva poblacion
        for i in range(len(seleccion)): #recorro los demas padres
            for j in cruzamiento(mejor, seleccion[i]): #cruzo a cada padre con el mejor de los padres
                mutado = mutacion(j)
                nuevos.append(mutado[0]) #agrego a la nueva genereacion los nuevos individuos
        print("Nueva Generación: ")
        for x in nuevos:
            print("%d | Cadena: %s" % (x[0], x[1]))
        print("--------------------------")
        seleccion = nuevos #actualizo la nueva seleccion
#print(bin_a_dec('110'))
seleccion_cruzamiento(poblacion)

