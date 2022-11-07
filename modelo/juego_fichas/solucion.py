import random
IS_SIMPLE_IA_INSTALLED = False
try:
    from simpleai.search import astar, SearchProblem
    IS_SIMPLE_IA_INSTALLED = True
except:
    pass
    # print("No está instalado el módulo SimpleIa")

def list_to_string(list_):
    return '\n'.join(['-'.join(row) for row in list_])


def string_to_list(string_):
    return [row.split('-') for row in string_.split('\n')]

def poner_fichas():
    fichas = [] #lista apra fichas desordenadas
    f = list("12345678e")
    while len(f) > 0:
        if len(f) > 1:
            rdm = random.randrange(0, len(f))
        else:
            rdm = 0
        item = f.pop(rdm)
        fichas.append(item)
    final = [fichas[0:3], fichas[3:6], fichas[6:9]]
    final = list_to_string(final)
    return final

GOAL = '''1-2-3
4-5-6
7-8-e'''
# 21 movimientos
INITIAL = '''3-2-6
7-e-8
5-1-4'''
# # 21 movimientos
# INITIAL = '''2-6-8
# 3-7-e
# 5-1-4'''
# 15 movimientos
# INITIAL = '''2-1-6
# e-3-8
# 5-4-7'''
# INITIAL = '''8-2-1
# 7-6-4
# 3-e-5'''
# 3 movimientos
# INITIAL = '''1-2-3
# e-4-6
# 7-5-8'''
# INITIAL = '''4-5-1
# 8-3-7
# e-6-2'''

def find_location(rows, element_to_find):
    '''Encuentra la direccion de la ficha buscada, devuelve la tupla fila, columna'''
    for ir, row in enumerate(rows):
        for ic, element in enumerate(row):
            if element == element_to_find:
                return ir, ic


# Se guarda la posicion fnal de cada pieza, para no tener que recalcular en cada ciclo
goal_positions = {}
rows_goal = string_to_list(GOAL)
for number in '12345678e':
    goal_positions[number] = find_location(rows_goal, number)

try:
    class Puzzle(SearchProblem):
        def actions(self, state):
            '''Retorna una lista de las piezas que podemso mover a un espacio vacio'''
            rows = string_to_list(state)
            row_e, col_e = find_location(rows, 'e')

            actions = []
            if row_e > 0:
                actions.append(rows[row_e - 1][col_e])
            if row_e < 2:
                actions.append(rows[row_e + 1][col_e])
            if col_e > 0:
                actions.append(rows[row_e][col_e - 1])
            if col_e < 2:
                actions.append(rows[row_e][col_e + 1])

            return actions

        def result(self, state, action):
            '''retorna el estado resultante despues de mover una ficha a un espacio vacio.
            (La accion parameter contiene la pieza a mover)
            '''
            rows = string_to_list(state)
            row_e, col_e = find_location(rows, 'e')
            row_n, col_n = find_location(rows, action)

            rows[row_e][col_e], rows[row_n][col_n] = rows[row_n][col_n], rows[row_e][col_e]

            return list_to_string(rows)

        def is_goal(self, state):
            '''Devuelve true si el estado actual es el estado deseado'''
            return state == GOAL

        def heuristic(self, state):
            '''Retorna una estimacion de la distancia al estado deseado
            Usando la distancia manhatan 
            '''
            rows = string_to_list(state)

            distance = 0

            for number in '12345678e':
                row_n, col_n = find_location(rows, number)
                row_n_goal, col_n_goal = goal_positions[number]

                distance += abs(row_n - row_n_goal) + abs(col_n - col_n_goal)
            return distance
except:
    if not IS_SIMPLE_IA_INSTALLED:
        # raise Exception("No está instalado el módulo simpleia")
        pass

def resolver():
    if not IS_SIMPLE_IA_INSTALLED:
        raise Exception("No está instalado el módulo simpleia")
        return
    # MIDIENDO EL TIEMPO
    from time import time
    inicio = time()
    # RESOLVIENDO
    # comprobar = threading.Thread(target=self.comprobar(), name="Comprobar Thread")
    # comprobar.start()
    # comprobar.join()
    result = astar(Puzzle(INITIAL))
    fin = time()
    tiempo = fin - inicio # TIEMPO DE RESOLUCION
    print("Tiempo en resolver %d"%tiempo)
    print("- Puzzle resuelto!")
    return result, tiempo

def mostrar_pasos():
    sol,_ = resolver()
    cnt = 0
    for action, state in sol.path():
        print("Jugada #%d" % cnt)
        print("===============")
        cnt += 1
        print('Mover el numero ', action)
        print(state)