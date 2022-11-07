import random
from copy import deepcopy

fichas = [1, 2, 3, 4, 5, 6, 7, 8, -1]

def poner_fichas(fichas, dar_orden: 'bool' = True):
    f = [1, 2, 3, 4, 5, 6, 7, 8, -1]
    fichas.clear()
    if dar_orden:
        for x in f:
            fichas.append(x)
    else:
        while len(f) > 0:
            if len(f) > 1:
                rdm = random.randrange(0, len(f))
            else: rdm = 0
            item = f.pop(rdm)
            fichas.append(item)
    return fichas

def mostrar(fichas):
    if len(fichas) > 0:
        cadena = ""
        for i in range(1, 10):
            cadena += str(fichas[i - 1]) + " "
            if i%3==0:
                cadena += "\n"
        return cadena
    else:
        return "No hay fichas"

def arriba(fichas, valor, idx):
    fichas[idx - 3] = valor  # subo la ficha
    fichas[idx] = -1  # bajo el -1
    return fichas

def abajo(fichas, valor, idx):
    fichas[idx + 3] = valor  # bajo la ficha
    fichas[idx] = -1  # subo el -1
    return fichas

def izq(fichas, valor, idx):
    fichas[idx - 1] = valor  # desplazo a la izquierda la ficha
    fichas[idx] = -1  # subo el -1
    return fichas

def derecha(fichas, valor, idx):
    fichas[idx + 1] = valor  # desplazo a la derecha la ficha
    fichas[idx] = -1  # subo el -1
    return fichas

def mover_ficha(fichas, valor):
    idx = fichas.index(valor)
    cood = coordenadas(idx)
    fila = cood[0]
    columna = cood[1]

    if fila == 0: #fila 0
        if fichas[idx + 3] == -1:  # si debajo de la ficha esta vacio
            abajo(fichas,valor, idx)
    elif fila == 1: #fila 1
        if fichas[idx + 3] == -1:  # si debajo de la ficha esta vacio
            abajo(fichas,valor, idx)
        elif fichas[idx - 3] == -1:  # si encima de la ficha esta vacio
            arriba(fichas,valor, idx)
    elif fila == 2: #fila 2
        if fichas[idx - 3] == -1:  # si encima de la ficha esta vacio
            arriba(fichas,valor, idx)
    if columna == 0:  # columna 0
        if fichas[idx + 1] == -1:  # si derecha de la ficha esta vacio
            derecha(fichas,valor, idx)
    elif columna == 1:  # columna 1
        if fichas[idx + 1] == -1:  # si derecha de la ficha esta vacio
            derecha(fichas,valor, idx)
        elif fichas[idx - 1] == -1:  # si a la izq de la ficha esta vacio
            izq(fichas,valor, idx)
    elif columna == 2:  # columna 2
        if fichas[idx - 1] == -1:  # si a la izq de la ficha esta vacio
            izq(fichas,valor, idx)
    #print(fichas)
    #print("Heuristica %d"%heuristica())
    #print('----------------------')
    return fichas

def coordenadas(idx):
    fila = 0
    columna = 0
    if idx >= 0 and idx <= 2:
        fila = 0
    elif idx >= 3 and idx <= 5:
        fila = 1
    elif idx >= 6 and idx <= 8:
        fila = 2
    if idx == 0 or idx == 3 or idx == 6:  # columna 0
        columna = 0
    elif idx == 1 or idx == 4 or idx == 7:  # columna 1
        columna = 1
    elif idx == 2 or idx == 5 or idx == 8:  # columna 2
        columna = 2
    return (fila, columna)

def heuristica(fichas):
    h = 0
    for x in range(len(fichas)-1):
        ficha = fichas[x]
        if ficha == x + 1:
            h += 1
        else:
            break
    return h

def posibles_jugadas(fichas):
    # ----- BUSCAR LOS POSIBLES MOVIMIENTOS -----
    posibles_jugadas = []
    neutra_idx = fichas.index(-1)
    cood = coordenadas(neutra_idx)
    fila = cood[0]
    columna = cood[1]
    if fila == 0:  # fila 0
        posibles_jugadas.append(fichas[neutra_idx + 3])  # abajo
    elif fila == 1:  # fila 1
        posibles_jugadas.append(fichas[neutra_idx - 3])  # arriba
        posibles_jugadas.append(fichas[neutra_idx + 3])  # abajo
    elif fila == 2:  # fila 2
        posibles_jugadas.append(fichas[neutra_idx - 3])  # arriba
    if columna == 0:  # columna 0
        posibles_jugadas.append(fichas[neutra_idx + 1])  # derecha
    elif columna == 1:  # columna 1
        posibles_jugadas.append(fichas[neutra_idx + 1])  # derecha
        posibles_jugadas.append(fichas[neutra_idx - 1])  # izquierda
    elif columna == 2:  # columna 2
        posibles_jugadas.append(fichas[neutra_idx - 1])  # derecha
    print("Posibles jugadas: ", end="")
    print(list(map(str, posibles_jugadas)))
    return posibles_jugadas
    # ---------------------------------------------

def posibles_movidas(fichas): # lista con movimientos realizados
    jugadas = []
    for x in posibles_jugadas(fichas):  # para los posibles juegadas
        tails = deepcopy(fichas)
        j = mover_ficha(tails, x)
        jugadas.append(j)
    return jugadas

def solucionar(fichas):
    pass