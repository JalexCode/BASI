import random

from modelo.juego_fichas.ficha import Ficha


class JuegoFichas:
    def __init__(self, lista_fichas):
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
        self.posiciones = {1: (0, 0), 2: (0, 1), 3: (0, 2), 4: (1, 0), 5: (1, 1), 6: (1, 2), 7: (2, 0), 8: (2, 1)}
        self.__fichas = [[-1, -1, -1], [-1, -1, -1], [-1, -1, -1]]
        # self.setUp()

    @property
    def fichas(self):
        return self.__fichas

    @fichas.setter
    def fichas(self, value):
        self.__fichas = value

    def setUp(self):
        self.ficha1 = Ficha(1, 0, 0, None, -1, None, 2)
        self.ficha2 = Ficha(2, 0, 1, None, 4, 1, 3)
        self.ficha3 = Ficha(3, 0, 2, None, 6, 2, None)
        self.ficha4 = Ficha(4, 1, 0, 1, 7, None, 5)
        self.ficha5 = Ficha(5, 1, 1, 2, 8, 4, 6)
        self.ficha6 = Ficha(6, 1, 2, 3, -1, 5, None)
        self.ficha7 = Ficha(7, 2, 0, 4, None, None, 8)
        self.ficha8 = Ficha(8, 2, 1, 5, None, 7, -1)
        self.ficha_neutra = Ficha(-1, 2, 2, 6, None, 8, None)
        self.poner_fichas()

    def poner_fichas(self):
        lista = [self.ficha1, self.ficha2, self.ficha3, self.ficha4, self.ficha5, self.ficha6, self.ficha7, self.ficha8,
                 self.ficha_neutra]
        for x in lista:
            self.fichas[x.fila][x.columna] = x

    def ordenar(self, dar_orden: 'bool' = True):
        if not len(self.fichas):
            raise Exception('No hay fichas')
        if dar_orden:
            self.fichas = sorted(self.fichas, key=lambda x: x.valor)
        else:
            lista = []
            for x in self.fichas:
                lista.insert(random.randrange(0, len(lista)), x)
            self.fichas = lista

    def buscar_ficha(self, valor):
        for fila in range(len(self.fichas)):
            for columna in range(fila):
                ficha = self.fichas[fila][columna]
                if isinstance(ficha, Ficha):
                    if ficha.es_valor(valor):
                        return ficha

    def mover_ficha(self, valor):
        ficha: 'Ficha' = self.buscar_ficha(valor)
        fila = ficha.fila
        columna = ficha.columna
        # print(fila)
        if ficha.arriba == -1:  # si encima de la ficha esta vacio
            # intercambio el espacio vacio con la ficha
            self.fichas[fila - 1][columna] = ficha
            self.fichas[fila][columna] = ficha.arriba
            # actualizo su atributo 'fila'
            ficha.fila -= 1
            # actualizo los atributos de la ficha, para saber kienes son sus nuevos vecinos
            # arriba
            if ficha.fila != 0:  # le cambio el valor
                ficha.arriba = self.fichas[ficha.fila - 1][ficha.columna].valor
            else:
                ficha.arriba = None
            # abajo
            if ficha.fila != 2:  # le cambio el valor
                print(fila, columna)
                print(self.fichas[ficha.fila + 1][ficha.columna])
                ficha.abajo = self.fichas[ficha.fila + 1][ficha.columna].valor

            else:
                ficha.abajo = None
            # derecha
            if ficha.columna != 2:
                ficha.derecha = self.fichas[ficha.fila][ficha.columna + 1].valor
            else:
                ficha.derecha = None
            # izquierda
            if ficha.columna != 0:
                ficha.izquierda = self.fichas[ficha.fila][ficha.columna - 1].valor
            else:
                ficha.izquierda = None
        print("Valor: %d, Fila: %d, Columna: %d, Arriba: %d, Abajo: %d, Izq.: %d, Derecha: %d" % (
        ficha.valor, ficha.fila, ficha.columna, ficha.arriba, ficha.abajo, ficha.izquierda, ficha.derecha))
        '''elif ficha.abajo == -1:
            # intercambio el espacio vacio con la ficha
            self.fichas[fila + 1][columna] = ficha
            self.fichas[fila][columna] = -1
            # actualizo su atributo 'fila'
            ficha.fila += 1
            # actualizo los atributos de la ficha, para saber kienes son sus nuevos vecinos
            if self.fichas[ficha.fila][ficha.columna] != 0:  # le cambio el valor
                ficha.arriba = self.fichas[ficha.fila - 1][ficha.columna]
            else:
                ficha.arriba = None'''

    def __str__(self):
        #print(self.fichas)
        cadena = []
        for x in self.fichas:
            cadena.append(" ".join(list(map(lambda i: str(type(i)), x))))
        return "\n".join(cadena)
