# -*- coding: utf-8 -*-
import time
import os
import random
import threading
import modelo.juego_fichas.juego_fichas as jf

TIEMPO_ESPERA = 0.5


# class Mapa:
#     def __init__(self, lista):
#         self.mapa = lista#aMatriz(lista)
#         self.fil = 3
#         self.col = 3
#
#     def __str__(self):
#         cadena = ""
#         for x in range(self.fil):
#             for y in range(self.col):
#                 cadena += str(self.mapa[x][y]) + " "
#             cadena += "\n"
#         return self.mapa

class Nodo:
    def __init__(self, estado=None, padre=None):  # (self, pos=[0, 0], padre=None):
        self.estado = estado
        self.padre = padre
        self.h = heuristica(estado)  # distancia(self.pos, pos_f)

        if self.padre == None:
            self.g = 0
        else:
            self.g = self.padre.g + 1

        # Peso del nodo
        self.f = self.g + self.h


class AEstrella:

    # abierta: Lista con los nuevos nodos visitados (vecinos)
    # cerrada: Lista con los nodos ya visitados

    def __init__(self):
        self.modulo_juego = jf
        self.modulo_juego.poner_fichas(self.modulo_juego.fichas, False)

        # Nodos de inicio y fin.
        self.inicio = Nodo(self.modulo_juego.fichas)  # busca una T (entrada)
        self.fin = Nodo(estado_final)  # busca una S (salida)

        # Crea las listas abierta y cerrada.
        self.abierta = []
        self.cerrada = []

        # Añade el nodo inicial a la lista cerrada.
        self.cerrada.append(self.inicio)

        # Añade los vecinos a la lista abierta
        self.abierta += self.vecinos(self.inicio)

        # Buscar mientras objetivo no este en la lista cerrada.
        self.mostrar(self.abierta[0].estado)
        while self.objetivo():
            time.sleep(TIEMPO_ESPERA)
            print("Dentro de A Estrella")
            # if self.fin.estado != estado_final:
            #     if self.cerrada[-1].estado is not estado_final:
            #         print("Mapa cambiado")
            #         time.sleep(TIEMPO_ESPERA)
            #         self.reInicio(self.inicio, self.cerrada[-1])
            #         self.recargar(self.mapa)
            #         time.sleep(TIEMPO_ESPERA)
            #     else:
            #         print("Mapa choque")
            #         print("actual: " + str(self.cerrada[-1].pos))
            #         print("final n: " + str(estado_final))
            #         g.visualizar()
            self.mostrar(self.abierta[-1].estado)
            print("-----------------------------------------")
            self.buscar()

        print("Fuera de A Estrella")
        # self.camino = self.camino()

    # Devuelve una lista con los nodos vecinos transitables.
    def vecinos(self, nodo):
        vecinos = []
        for x in self.modulo_juego.posibles_movidas(nodo.estado):
            vecinos.append(Nodo(x, nodo))
        # if self.mapa.mapa[nodo.pos[0] + 1][nodo.pos[1]] != 1:
        #     vecinos.append(Nodo([nodo.pos[0] + 1, nodo.pos[1]], nodo))
        # if self.mapa.mapa[nodo.pos[0] - 1][nodo.pos[1]] != 1:
        #     vecinos.append(Nodo([nodo.pos[0] - 1, nodo.pos[1]], nodo))
        # if self.mapa.mapa[nodo.pos[0]][nodo.pos[1] - 1] != 1:
        #     vecinos.append(Nodo([nodo.pos[0], nodo.pos[1] - 1], nodo))
        # if self.mapa.mapa[nodo.pos[0]][nodo.pos[1] + 1] != 1:
        #     vecinos.append(Nodo([nodo.pos[0], nodo.pos[1] + 1], nodo))
        return vecinos

    # Pasa el elemento de f menor de la lista abierta a la cerrada.
    def f_menor(self):
        a = self.abierta[0]
        n = 0
        for i in range(1, len(self.abierta)):
            if self.abierta[i].f < a.f:
                a = self.abierta[i]
                n = i
        self.cerrada.append(self.abierta[n])
        del self.abierta[n]

    # Comprueba si un nodo está en una lista.
    def en_lista(self, nodo, lista):
        for i in range(len(lista)):
            if nodo.estado == lista[i].estado:
                return 1
        return 0

    # Gestiona los vecinos del nodo seleccionado.
    def ruta(self):
        for i in range(len(self.nodos)):
            if self.en_lista(self.nodos[i], self.cerrada):
                continue
            elif not self.en_lista(self.nodos[i], self.abierta):
                self.abierta.append(self.nodos[i])
            else:
                if self.select.g + 1 < self.nodos[i].g:
                    for j in range(len(self.abierta)):
                        if self.nodos[i].estado == self.abierta[j].estado:
                            del self.abierta[j]
                            self.abierta.append(self.nodos[i])
                            break

    # Analiza el último elemento de la lista cerrada.
    def buscar(self):
        self.f_menor()
        self.select = self.cerrada[-1]  # ultimo elemento
        self.nodos = self.vecinos(self.select)
        # self.mostrar(self.abierta[0].estado)
        self.ruta()

    # Comprueba si el objetivo está en la lista abierta.
    def objetivo(self):
        for i in range(len(self.abierta)):
            if self.fin.estado == self.abierta[i].estado:
                return 0
        return 1

    def mostrar(self, fichas):
        if len(fichas) > 0:
            cadena = ""
            for i in range(1, 10):
                cadena += str(fichas[i - 1]) + " "
                if i % 3 == 0:
                    cadena += "\n"
            print(cadena)
        else:
            print("No hay fichas")

    # # Retorna una lista con las posiciones del camino a seguir.
    # def camino(self):
    #
    #     for i in range(len(self.abierta)):
    #         if self.fin.estado == self.abierta[i].estado:
    #             objetivo = self.abierta[i]
    #
    #     camino = []
    #
    #     while objetivo.padre != None:
    #         camino.append(objetivo.estado)
    #         objetivo = objetivo.padre
    #
    #     camino.reverse()
    #
    #     return camino


# ---------------------------------------------------------------------
# Funciones
# ---------------------------------------------------------------------
def aMatriz(lista):
    return [lista[:3], lista[3:6], lista[6:]]


def aLista(matriz):
    lista = []
    for f in range(3):
        for c in range(3):
            lista.append(matriz[f][c])
    return lista


def heuristica(estado):  # heurisitica de mis cojones LOL
    h = 0
    for x in range(9):
        if estado[x] == estado_final[x]:
            h += 1
    return h


def resolverJuego():
    A = AEstrella()
    globals()["Fin"] = True
    # A.modulo_juego.mostrar()
    # mapa.camino(A.camino)
    # g = Grafica(mapa)
    # g.dibujarRecorrido(A.camino)
    # longitud = len(A.camino)
    #
    # for i in range(longitud):
    #     print("pos: " + str(A.camino[i]))
    # g.visualizar()
    # os.system("cls")


# ---------------------------------------------------------------------

def main():
    # globals()["mapa"] = juego
    globals()["estado_final"] = [1, 2, 3, 4, 5, 6, 7, 8, -1]  # buscarPos(3, mapa)
    globals()["Fin"] = False

    cs = threading.Thread(target=resolverJuego, args=())
    cs.start()

    while cs.isAlive():

        if Fin is False:
            print("No resulto aun")
        time.sleep(0.5)

    return 0


if __name__ == '__main__':
    main()

# print(aMatriz([1, 2, 3, 4, 5, 6, 7, 8, -1]))
