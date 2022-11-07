import random

from simpleai.search import astar, SearchProblem

def poner_fichas(dar_orden: 'bool' = True):
    fichas = [] #lista apra fichas desordenadas
    f = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    if dar_orden:
        return f
    else:
        while len(f) > 0:
            if len(f) > 1:
                rdm = random.randrange(0, len(f))
            else:
                rdm = 0
            item = f.pop(rdm)
            fichas.append(item)
    return fichas

def mostrar(fichas:'list'):
    if len(fichas) > 0:
        cadena = ""
        for i in range(1, 10):
            cadena += str(fichas[i - 1]) + " "
            if i % 3 == 0:
                cadena += "\n"
        return cadena
    else:
        return "No hay fichas"

def arriba(fichas, valor, idx):
    fichas[idx - 3] = valor  # subo la ficha
    fichas[idx] = 9  # bajo el 9
    return fichas

def abajo(fichas, valor, idx):
    fichas[idx + 3] = valor  # bajo la ficha
    fichas[idx] = 9  # subo el 9
    return fichas

def izq(fichas, valor, idx):
    fichas[idx - 1] = valor  # desplazo a la izquierda la ficha
    fichas[idx] = 9  # subo el 9
    return fichas

def derecha(fichas, valor, idx):
    fichas[idx + 1] = valor  # desplazo a la derecha la ficha
    fichas[idx] = 9  # subo el 9
    return fichas

def mover_ficha(fichas, valor):
    idx = fichas.index(valor)
    cood = coordenadas(idx)
    fila = cood[0]
    columna = cood[1]

    if fila == 0:  # fila 0
        if fichas[idx + 3] == 9:  # si debajo de la ficha esta vacio
            abajo(fichas, valor, idx)
    elif fila == 1:  # fila 1
        if fichas[idx + 3] == 9:  # si debajo de la ficha esta vacio
            abajo(fichas, valor, idx)
        elif fichas[idx - 3] == 9:  # si encima de la ficha esta vacio
            arriba(fichas, valor, idx)
    elif fila == 2:  # fila 2
        if fichas[idx - 3] == 9:  # si encima de la ficha esta vacio
            arriba(fichas, valor, idx)
    if columna == 0:  # columna 0
        if fichas[idx + 1] == 9:  # si derecha de la ficha esta vacio
            derecha(fichas, valor, idx)
    elif columna == 1:  # columna 1
        if fichas[idx + 1] == 9:  # si derecha de la ficha esta vacio
            derecha(fichas, valor, idx)
        elif fichas[idx - 1] == 9:  # si a la izq de la ficha esta vacio
            izq(fichas, valor, idx)
    elif columna == 2:  # columna 2
        if fichas[idx - 1] == 9:  # si a la izq de la ficha esta vacio
            izq(fichas, valor, idx)
    # print(fichas)
    # print("Heuristica %d"%heuristica())
    # print('----------------------')
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

def posibles_jugadas(fichas):
    # ----- BUSCAR LOS POSIBLES MOVIMIENTOS -----
    fichas = string_to_list(fichas)
    posibles_jugadas = []
    neutra_idx = fichas.index(9)
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
    #print("Posibles jugadas: ", end="")
    #print(list(map(str, posibles_jugadas)))
    return posibles_jugadas
    # ---------------------------------------------

INICIO = poner_fichas(False)
print(INICIO)
META = [1, 2, 3, 4, 5, 6, 7, 8, 9]
posicion_final = {}
for idx in range(9):
    n = META[idx]
    posicion_final[n] = coordenadas(idx)
print(posicion_final)

def list_to_string(list_):
    return "".join(list(map(str, list_)))


def string_to_list(string_):
    return [int(row) for row in string_]

class Puzzle(SearchProblem):
    def actions(self, fichas):
        return posibles_jugadas(fichas)

    def result(self, state, action):  # lista con movimientos realizados
        state = string_to_list(state)
        return list_to_string(mover_ficha(state, action))

    def is_goal(self, fichas):
        return fichas == META

    def heuristic(self, fichas):
        distancia = 0

        fichas = string_to_list(fichas)

        for n in fichas:
            idx = fichas.index(n)
            c = coordenadas(idx)
            fila_n = c[0]
            columna_n = c[1]
            pos_final = posicion_final[n]
            fila_n_goal = pos_final[0]
            columna_n_goal = pos_final[1]

            distancia += abs(fila_n - fila_n_goal) + abs(columna_n - columna_n_goal)

        return distancia

result = astar(Puzzle(list_to_string(INICIO)))
print("hello")
for action, state in result.path():
    print ('Mover el numero ', action)
    print (mostrar(state))