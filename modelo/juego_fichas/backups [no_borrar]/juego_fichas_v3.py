import random


class Juego_Fichas:
    def __init__(self):
        self.__fichas = []

    @property
    def fichas(self):
        return self.__fichas

    @fichas.setter
    def fichas(self, value):
        self.__fichas = value

    def poner_fichas(self, dar_orden: 'bool' = True):
        f = [1, 2, 3, 4, 5, 6, 7, 8, -1]
        self.fichas.clear()
        if dar_orden:
            for x in f:
                self.fichas.append(x)
        else:
            while len(f) > 0:
                if len(f) > 1:
                    rdm = random.randrange(0, len(f))
                else: rdm = 0
                item = f.pop(rdm)
                self.fichas.append(item)


    def __str__(self):
        if len(self.fichas) > 0:
            cadena = ""
            for i in range(1, 10):
                cadena += str(self.fichas[i - 1]) + " "
                if i%3==0:
                    cadena += "\n"
            return cadena
        else:
            return "No hay fichas"

    def arriba(self, valor, idx):
        self.fichas[idx - 3] = valor  # subo la ficha
        self.fichas[idx] = -1  # bajo el -1

    def abajo(self, valor, idx):
        self.fichas[idx + 3] = valor  # bajo la ficha
        self.fichas[idx] = -1  # subo el -1

    def izq(self, valor, idx):
        self.fichas[idx - 1] = valor  # desplazo a la izquierda la ficha
        self.fichas[idx] = -1  # subo el -1

    def derecha(self, valor, idx):
        self.fichas[idx + 1] = valor  # desplazo a la derecha la ficha
        self.fichas[idx] = -1  # subo el -1

    def mover_ficha(self, valor):
        idx = self.fichas.index(valor)
        cood = self.coordenadas(idx)
        fila = cood[0]
        columna = cood[1]

        if fila == 0: #fila 0
            if self.fichas[idx + 3] == -1:  # si debajo de la ficha esta vacio
                self.abajo(valor, idx)
        elif fila == 1: #fila 1
            if self.fichas[idx + 3] == -1:  # si debajo de la ficha esta vacio
                self.abajo(valor, idx)
            elif self.fichas[idx - 3] == -1:  # si encima de la ficha esta vacio
                self.arriba(valor, idx)
        elif fila == 2: #fila 2
            if self.fichas[idx - 3] == -1:  # si encima de la ficha esta vacio
                self.arriba(valor, idx)
        if columna == 0:  # columna 0
            if self.fichas[idx + 1] == -1:  # si derecha de la ficha esta vacio
                self.derecha(valor, idx)
        elif columna == 1:  # columna 1
            if self.fichas[idx + 1] == -1:  # si derecha de la ficha esta vacio
                self.derecha(valor, idx)
            elif self.fichas[idx - 1] == -1:  # si a la izq de la ficha esta vacio
                self.izq(valor, idx)
        elif columna == 2:  # columna 2
            if self.fichas[idx - 1] == -1:  # si a la izq de la ficha esta vacio
                self.izq(valor, idx)
        #print(self)
        #print("Heuristica %d"%self.heuristica())
        #print('----------------------')

    def coordenadas(self, idx):
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

    def heuristica(self):
        h = 0
        for x in range(len(self.fichas)):
            ficha = self.fichas[x]
            if ficha != -1:
                if ficha - 1 == x:
                    h += 1
            else:
                if x == 8:
                    h += 1
        return h

    def solucionar(self):
        while self.heuristica() < 8:
            # ----- BUSCAR LOS POSIBLES MOVIMIENTOS -----
            posibles_jugadas = []
            neutra_idx = self.fichas.index(-1)
            cood = self.coordenadas(neutra_idx)
            fila = cood[0]
            columna = cood[1]
            if fila == 0:  # fila 0
                posibles_jugadas.append(self.fichas[neutra_idx + 3]) # abajo
            elif fila == 1:  # fila 1
                posibles_jugadas.append(self.fichas[neutra_idx - 3])  # arriba
                posibles_jugadas.append(self.fichas[neutra_idx + 3])  # abajo
            elif fila == 2:  # fila 2
                posibles_jugadas.append(self.fichas[neutra_idx - 3])  # arriba
            if columna == 0:  # columna 0
                posibles_jugadas.append(self.fichas[neutra_idx + 1]) #derecha
            elif columna == 1:  # columna 1
                posibles_jugadas.append(self.fichas[neutra_idx + 1])  # derecha
                posibles_jugadas.append(self.fichas[neutra_idx - 1])  # izquierda
            elif columna == 2:  # columna 2
                posibles_jugadas.append(self.fichas[neutra_idx - 1])  # derecha
            print("Posibles jugadas: ", end="")
            print(list(map(str, posibles_jugadas)))
            # ---------------------------------------------
            mejor_ficha = 0
            mejor_heuristica = 0
            for x in posibles_jugadas:  # para los posibles juegadas
                if x is not None:
                    self.mover_ficha(x)
                    #print("Nueva jugada para Ficha #%d" % x)
                    #print(caso)
                    #print("---------------------------")
                    heur = self.heuristica()
                    if heur > mejor_heuristica:
                        mejor_heuristica = heur
                        mejor_ficha = x
                        #yield self
                    self.mover_ficha(x)
            self.mover_ficha(mejor_ficha)
            #print("Mejor jugada para Ficha #%d (h = %d)" % (mejor_ficha, mejor_heuristica))
            print(self)
            #print("---------------------------")
            # break
            # print(caso)
            # print("----------------------")