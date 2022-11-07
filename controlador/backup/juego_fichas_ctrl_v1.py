import threading
import time

from PyQt5.QtGui import QColor, QPixmap
from PyQt5.QtWidgets import QMessageBox, QSplashScreen

import modelo.juego_fichas.juego_fichas as juego
#from modelo.juego_fichas.hilos import HiloSolucionarPuzzle, HiloAnimacion
from ui.interfaces import JuegoFichasUI

TIEMPO_ESPERA = 0.5

class controlador_juego_fichas:
    def __init__(self):
        self.vista = JuegoFichasUI(self)
        self.leyenda = {1: self.vista.a, 2: self.vista.b, 3: self.vista.c, 4: self.vista.d, 5: self.vista.e, 6: self.vista.f,
               7: self.vista.g, 8: self.vista.h}
        self.complejidad = 0
        self.pasos = None
        self.tiempo = 0

    def iniciar(self):
        #self.vista.tablero.setEnabled(False)
        self.vista.show()

    def moverThread(self, ficha, x, y):
        mover_ficha = threading.Thread(target=self.vista.mover, args=(self.leyenda[ficha], x * 100, y * 100, False),
                                       name="Mover Ficha Thread")
        mover_ficha.start()
        while mover_ficha.isAlive():
            time.sleep(TIEMPO_ESPERA)

    def poner_fichas(self):
        cnt = 0
        for y in range(3):
            for x in range(3):
                ficha = juego.fichas[cnt]
                if ficha != -1:
                    #print("Ficha: %d"%ficha)
                    #print("Pos (x, y): %d, %d"%(x*100, x*100))
                    self.moverThread(ficha, x, y)
                    #print("============================================")
                cnt += 1
        comprobar = threading.Thread(target=self.comprobar(), name="Comprobar Thread")
        comprobar.start()
        while comprobar.isAlive():
            time.sleep(TIEMPO_ESPERA)

    def comprobar(self):
        h = juego.heuristica(juego.fichas)
        #print(h)
        if h == 8:
            self.vista.sugerir.setEnabled(False)
            self.vista.solucionar.setEnabled(False)
            self.vista.notificacion("Usted ha ganado!")

    def desordenar(self):
        # habilitar tablero
        self.vista.tablero.setEnabled(True)
        self.vista.sugerir.setEnabled(True)
        self.vista.solucionar.setEnabled(True)
        # desordenar las fichas en el modulo
        fichas, self.complejidad = juego.poner_fichas(juego.fichas, False)
        juego.fichas = fichas
        # posicionar fichas visuales
        self.poner_fichas()

    def mover_1(self):
        juego.mover_ficha(juego.fichas, 1)
        posicionar = threading.Thread(target=self.poner_fichas(), name="Poner Fichas Thread")
        posicionar.start()
        while posicionar.isAlive():
            time.sleep(TIEMPO_ESPERA)

    def mover_2(self):
        juego.mover_ficha(juego.fichas, 2)
        posicionar = threading.Thread(target=self.poner_fichas(), name="Poner Fichas Thread")
        posicionar.start()
        while posicionar.isAlive():
            time.sleep(TIEMPO_ESPERA)

    def mover_3(self):
        juego.mover_ficha(juego.fichas, 3)
        posicionar = threading.Thread(target=self.poner_fichas(), name="Poner Fichas Thread")
        posicionar.start()
        while posicionar.isAlive():
            time.sleep(TIEMPO_ESPERA)

    def mover_4(self):
        juego.mover_ficha(juego.fichas, 4)
        posicionar = threading.Thread(target=self.poner_fichas(), name="Poner Fichas Thread")
        posicionar.start()
        while posicionar.isAlive():
            time.sleep(TIEMPO_ESPERA)

    def mover_5(self):
        juego.mover_ficha(juego.fichas, 5)
        posicionar = threading.Thread(target=self.poner_fichas(), name="Poner Fichas Thread")
        posicionar.start()
        while posicionar.isAlive():
            time.sleep(TIEMPO_ESPERA)

    def mover_6(self):
        juego.mover_ficha(juego.fichas, 6)
        posicionar = threading.Thread(target=self.poner_fichas(), name="Poner Fichas Thread")
        posicionar.start()
        while posicionar.isAlive():
            time.sleep(TIEMPO_ESPERA)

    def mover_7(self):
        juego.mover_ficha(juego.fichas, 7)
        posicionar = threading.Thread(target=self.poner_fichas(), name="Poner Fichas Thread")
        posicionar.start()
        while posicionar.isAlive():
            time.sleep(TIEMPO_ESPERA)

    def mover_8(self):
        juego.mover_ficha(juego.fichas, 8)
        posicionar = threading.Thread(target=self.poner_fichas(), name="Poner Fichas Thread")
        posicionar.start()
        while posicionar.isAlive():
            time.sleep(TIEMPO_ESPERA)

    def mostrar_complejidad(self):
        QMessageBox.information(self.vista, "BASI", "Este juego se puede resolver en %d pasos"%(self.complejidad))

    def string_to_list(self, string_):
        lista = [row.split('-') for row in string_.split('\n')]
        definitiva = []
        for x in lista:
            for y in range(3):
                definitiva.append(x[y])
        i = definitiva.index("e")
        definitiva[i] = -1
        return list(map(int, definitiva))

    def mostrarJugada(self):
        self.vista.tablero.setEnabled(False)
        i = self.vista.entrada_soluciones.currentRow()
        if not i%3:
            string = self.vista.entrada_soluciones.currentItem().text()
            print(string)
            conv = self.string_to_list(string)
            print(conv)
            juego.fichas = conv
            self.poner_fichas()

    def solucionar_hilo(self):
        # SOLUCION
        self.pasos, self.tiempo = juego.solucionar(juego.fichas)
        # TIEMPO
        self.tiempo = int(self.tiempo)
        # print(self.tiempo)
        s = 0
        m = 0
        for segundos in range(1, self.tiempo + 1):
            if not segundos % 60:
                m += 1
                s = 0
            s += 1
        self.tiempo = "%02d:%02d"%(m, s)
        # print(self.tiempo)

    def animar_solucion_hilo(self):
        print("- ENTRANDO EN ANIMACION | '%s' Iniciado"%threading.currentThread().getName())
        LOG = ["- Puzzle solucionado en %d pasos. Duración: %s"%(len(self.pasos.path()), self.tiempo), "============================"]
        for ficha, puzzle in self.pasos.path():
            LOG.append("* Ficha movida: %s\n----------------------------\n" % (ficha if ficha is not None else "Ninguna"))
            LOG.append(puzzle)
            if ficha == "1":
                mover_1 = threading.Thread(target=self.mover_1())
                mover_1.start()
                while mover_1.isAlive():
                    time.sleep(TIEMPO_ESPERA)
            elif ficha == "2":
                mover_2 = threading.Thread(target=self.mover_2())
                mover_2.start()
                while mover_2.isAlive():
                    time.sleep(TIEMPO_ESPERA)
            elif ficha == "3":
                mover_3 = threading.Thread(target=self.mover_3())
                mover_3.start()
                while mover_3.isAlive():
                    time.sleep(TIEMPO_ESPERA)
            elif ficha == "4":
                mover_4 = threading.Thread(target=self.mover_4())
                mover_4.start()
                while mover_4.isAlive():
                    time.sleep(TIEMPO_ESPERA)
            elif ficha == "5":
                mover_5 = threading.Thread(target=self.mover_5())
                mover_5.start()
                #mover_5.join()
                while mover_5.isAlive():
                    time.sleep(TIEMPO_ESPERA)
            elif ficha == "6":
                mover_6 = threading.Thread(target=self.mover_6())
                mover_6.start()
                while mover_6.isAlive():
                    time.sleep(TIEMPO_ESPERA)
            elif ficha == "7":
                mover_7 = threading.Thread(target=self.mover_7())
                mover_7.start()
                while mover_7.isAlive():
                    time.sleep(TIEMPO_ESPERA)
            elif ficha == "8":
                mover_8 = threading.Thread(target=self.mover_8())
                mover_8.start()
                while mover_8.isAlive():
                    time.sleep(TIEMPO_ESPERA)
            time.sleep(TIEMPO_ESPERA)
            LOG.append("============================")
            print("EN BUCLE FOR")
        self.vista.ponerLOGS(LOG)
        print("- SALIENDO DE ANIMACION | '%s' Detenido" % threading.currentThread().getName())

    def solucionar(self):
        # solucionar = HiloSolucionarPuzzle(1, "Solucionar Thread", self)
        # solucionar.start()
        # solucionar.join()
        # animacion = HiloAnimacion(2, "Animacion Thread", self)
        # animacion.start()
        # animacion.join()
        ############# SPLASHSCREEN #################################################################################
        # pixmap = QPixmap('ui/splash.png')
        # splash = QSplashScreen()#(pixmap)
        # splash.show()
        # splash.setStyleSheet(
        #     "color: rgb(255, 255, 255); font-size: 26px; font-family: calibri; text-align: center;")
        # splash.showMessage('SOLUCIONANDO...', 0x0004, QColor(255, 255, 255))
        # ---------------------------------------------- #
        # HILO PARA SOLUCION
        solucionar = threading.Thread(target=self.solucionar_hilo(), name="Solucionar Thread")
        solucionar.start()
        solucionar.join()
        # ---------------------------------------------- #
        # HILO PARA ANIMACION
        animacion = threading.Thread(target=self.animar_solucion_hilo(), name="Animacion Thread")
        animacion.start()
        print("Saliendo del Hilo Principal")

    def sugerir(self):
        pass
        # for ficha, puzzle in self.pasos.path():
        #     if juego.fichas