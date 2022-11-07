import random

from modelo.arbol import Arbol
from modelo.juego_fichas.ficha import Ficha


class JuegoFichas:
    def __init__(self):
        '''self.ficha1 = Ficha(1, 0, 0, None, -1, None, 2)
        self.ficha2 = Ficha(2, 0, 1, None, 4, 1, 3)
        self.ficha3 = Ficha(3, 0, 2, None, 6, 2, None)
        self.ficha4 = Ficha(4, 1, 0, 1, 7, None, 5)
        self.ficha5 = Ficha(5, 1, 1, 2, 8, 4, 6)
        self.ficha6 = Ficha(6, 1, 2, 3, -1, 5, None)
        self.ficha7 = Ficha(7, 2, 0, 4, None, None, 8)
        self.ficha8 = Ficha(8, 2, 1, 5, None, 7, -1)
        self.ficha_neutra = Ficha(-1, 2, 2, 6, None, 8, None)'''

        # --------------------------------------------------------- #
        self.posiciones = {1: (0, 0), 2: (0, 1), 3: (0, 2), 4: (1, 0), 5: (1, 1), 6: (1, 2), 7: (2, 0), 8: (2, 1), -1:(2,2)}
        self.__fichas = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        # DEBAJO LA CONFIG DE FICHAS PARA UN DESORDENAMIENTO SENCILLO
        '''1 2 3    1 2 3    1 2 3    1 2 3
             4 6 -> 4   6 -> 4 5 6 -> 4 5 6
           7 5 8    7 5 8    7   8    7 8  '''
        self.ficha1 = Ficha(1, 0, 0, None, -1, None, 2)
        self.ficha2 = Ficha(2, 0, 1, None, 4, 1, 3)
        self.ficha3 = Ficha(3, 0, 2, None, 6, 2, None)
        self.ficha4 = Ficha(4, 1, 1, 2, 5, -1, 6)
        self.ficha5 = Ficha(5, 2, 1, 4, None, 7, 8)
        self.ficha6 = Ficha(6, 1, 2, 3, 8, 4, None)
        self.ficha7 = Ficha(7, 2, 0, -1, None, None, 5)
        self.ficha8 = Ficha(8, 2, 2, 6, None, 5, None)
        self.ficha_neutra = Ficha(-1, 1, 0, 1, 7, None, 4)
        self.poner_fichas(False)

    @property
    def fichas(self):
        return self.__fichas

    @fichas.setter
    def fichas(self, value):
        self.__fichas = value

    def __str__(self):
        # print(self.fichas)
        cadena = []
        for x in self.fichas:
            cadena.append(" ".join(list(map(str, x))))
        if self.heuristica() == 8:
            ok = "! SOLUCIONADO !"
        else:
            ok = "No resuelto"
        return "\n".join(cadena) + "\n" + ok

    def __iter__(self):
        for fila in range(len(self.fichas)):
            for columna in range(len(self.fichas[fila])):
                ficha = self.fichas[fila][columna]
                yield ficha

    def poner_fichas(self, dar_orden: 'bool' = True):
        if not len(self.fichas):
            raise Exception('No hay fichas')
        f = [self.ficha1, self.ficha2, self.ficha3, self.ficha4, self.ficha5, self.ficha6, self.ficha7,
             self.ficha8,
             self.ficha_neutra]
        if dar_orden:
            for x in f:
                self.fichas[self.posiciones[x.valor][0]][self.posiciones[x.valor][1]] = x
        else:
            for x in f:
                while True:
                    fila = random.randrange(0, 3)
                    columna = random.randrange(0, 3)
                    # print("Fila: %d | Columna: %d | Elemento: %s"%(fila, columna, str(lista[fila][columna])))
                    if self.fichas[fila][columna] == 0:
                        break
                self.fichas[fila][columna] = x
        self.actualizar_ficha_neutra()

    def buscar_ficha(self, valor):
        for ficha in self:
            #print("%d == %d"%(ficha.valor, valor))
            if ficha.es_valor(valor):
                return ficha

    def arriba(self, ficha, fila, columna):
        ficha = ficha
        # intercambio el espacio vacio con la ficha
        tmp = self.fichas[fila - 1][columna]  # el -1
        ficha.fila -= 1  # actualizo su atributo 'fila'
        self.fichas[fila - 1][columna] = ficha  # subo la ficha
        self.fichas[fila][columna] = tmp  # bajo el -1
        # #self.fichas[fila][columna].arriba = self.fichas[fila - 1][columna]  # actualizo ARRIBA en -1

    def abajo(self, ficha, fila, columna):
        ficha = ficha
        # intercambio el espacio vacio con la ficha
        tmp = self.fichas[fila + 1][columna]  # el -1
        ficha.fila += 1  # actualizo su atributo 'fila'
        self.fichas[fila + 1][columna] = ficha  # subo la ficha
        self.fichas[fila][columna] = tmp  # bajo el -1
        # self.fichas[fila][columna].abajo = self.fichas[fila + 1][columna]  # actualizo ABAJO en -1

    def izq(self, ficha, fila, columna):
        ficha = ficha
        # intercambio el espacio vacio con la ficha
        tmp = self.fichas[fila][columna - 1]  # el -1
        ficha.columna -= 1  # actualizo su atributo 'columna'
        self.fichas[fila][columna - 1] = ficha  # desplazo a la izquierda la ficha
        self.fichas[fila][columna] = tmp  # desplazo a la derecha el -1
        # self.fichas[fila][columna].izquierda = self.fichas[fila][columna - 1]  # actualizo IZQUIERDA en -1

    def derecha(self, ficha, fila, columna):
        ficha = ficha
        # intercambio el espacio vacio con la ficha
        tmp = self.fichas[fila][columna + 1]  # el -1
        ficha.columna += 1  # actualizo su atributo 'columna'
        self.fichas[fila][columna + 1] = ficha  # desplazo a la izquierda la ficha
        self.fichas[fila][columna] = tmp  # desplazo a la derecha el -1
        # self.fichas[fila][columna].derecha = self.fichas[fila][columna + 1]  # actualizo DERECHA en -1

    def mover_ficha(self, valor):
        ficha: 'Ficha' = self.buscar_ficha(valor)
        fila = ficha.fila
        columna = ficha.columna
        if fila == 0:
            if self.fichas[fila + 1][columna].es_valor(-1):  # si debajo de la ficha esta vacio
                self.abajo(ficha, fila, columna)
        elif fila == 1:
            if self.fichas[fila + 1][columna].es_valor(-1):  # si debajo de la ficha esta vacio
                self.abajo(ficha, fila, columna)
            elif self.fichas[fila - 1][columna].es_valor(-1):  # si encima de la ficha esta vacio
                self.arriba(ficha, fila, columna)
        elif fila == 2:
            if self.fichas[fila - 1][columna].es_valor(-1):  # si encima de la ficha esta vacio
                self.arriba(ficha, fila, columna)
        if columna == 0:
            if self.fichas[fila][columna + 1].es_valor(-1):  # si derecha de la ficha esta vacio
                self.derecha(ficha, fila, columna)
        elif columna == 1:
            if self.fichas[fila][columna + 1].es_valor(-1):  # si derecha de la ficha esta vacio
                self.derecha(ficha, fila, columna)
            elif self.fichas[fila][columna - 1].es_valor(-1):  # si a la izq de la ficha esta vacio
                self.izq(ficha, fila, columna)
        elif columna == 2:
            if self.fichas[fila][columna - 1].es_valor(-1):  # si a la izq de la ficha esta vacio
                self.izq(ficha, fila, columna)
        self.actualizar_ficha_neutra()
        #print(self)
        #print('----------------------')

    def actualizar_ficha_neutra(self):
        for row in range(len(self.fichas)):
            for column in range(len(self.fichas[row])):
                neutra = self.fichas[row][column]
                #print(str(type(neutra)))
                #print(neutra)
                if isinstance(neutra, Ficha):
                    if neutra.es_valor(-1):
                        # print("Encontrada ficha -1 en [%d][%d]" % (row, column))
                        # print(row, column)
                        if row == 0:
                            neutra.arriba = None
                            neutra.abajo = self.fichas[row + 1][column].valor
                        elif row == 1:
                            neutra.arriba = self.fichas[row - 1][column].valor
                            neutra.abajo = self.fichas[row + 1][column].valor
                        elif row == 2:
                            neutra.arriba = self.fichas[row - 1][column].valor
                            neutra.abajo = None
                        if column == 0:
                            neutra.izquierda = None
                            neutra.derecha = self.fichas[row][column + 1].valor
                        elif column == 1:
                            neutra.izquierda = self.fichas[row][column - 1].valor
                            neutra.derecha = self.fichas[row][column + 1].valor
                        elif column == 2:
                            neutra.izquierda = self.fichas[row][column - 1].valor
                            neutra.derecha = None
                        '''print("arriba: {}, abajo: {}, izq: {}, der: {}".format(str(neutra.arriba), str(neutra.abajo),
                                                                               str(neutra.izquierda), str(neutra.derecha)))'''
                        return neutra
        if neutra is None:
            raise Exception('No se encontro -1')

    def heuristica(self):
        h = 0
        for row in range(len(self.fichas)):
            for column in range(len(self.fichas[row])):
                ficha = self.fichas[row][column]
                #print(ficha)
                valor = ficha.valor
                if valor != -1:
                    coordenadas = (row, column)
                    if coordenadas == self.posiciones[valor]:
                        h += 1
        return h

    def solucionar(self):
        caso = self
        while caso.heuristica() < 8:
            posibles_jugadas = [caso.ficha_neutra.arriba, caso.ficha_neutra.abajo, caso.ficha_neutra.izquierda,
                                caso.ficha_neutra.derecha]
            print("Posibles jugadas: ", end="")
            print(list(map(str, posibles_jugadas)))
            mejor_ficha = 0
            mejor_heuristica = 0
            for x in posibles_jugadas:  # para los posibles juegadas
                if x is not None:
                    caso.mover_ficha(x)
                    #print("Nueva jugada para Ficha #%d" % x)
                    #print(caso)
                    #print("---------------------------")
                    heur = caso.heuristica()
                    if heur > mejor_heuristica:
                        mejor_heuristica = heur
                        mejor_ficha = x
                        yield caso
                    caso.mover_ficha(x)
            caso.mover_ficha(mejor_ficha)
            print("Mejor jugada para Ficha #%d (h = %d)" % (mejor_ficha, mejor_heuristica))
            print(caso)
            print("---------------------------")
            # break
            # print(caso)
            # print("----------------------")
