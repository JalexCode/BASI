import threading
import time

from PyQt5.QtCore import QTimer, QThread, pyqtSignal
from PyQt5.QtGui import QColor, QPixmap
from PyQt5.QtWidgets import QMessageBox, QSplashScreen

import modelo.juego_fichas.juego_fichas as juego
#from modelo.juego_fichas.hilos import HiloSolucionarPuzzle, HiloAnimacion
from ui.interfaces import JuegoFichasUI

TIEMPO_ESPERA = 0.5

class HiloAnimarSolucionPuzzle(QThread):
    signal = pyqtSignal(object, object)

    def __init__(self, parent, pasos):
        super(HiloAnimarSolucionPuzzle, self).__init__(parent)
        self.pasos = pasos

    def run(self):
        #print("Iniciando Hilo AnimarSolucion")
        for ficha, puzzle in self.pasos.path():
            self.signal.emit(ficha, puzzle)
            time.sleep(TIEMPO_ESPERA)
        #print("Finalizando Hilo AnimarSolucion")

class HiloQSplash(QThread):
    #signal = pyqtSignal(object)

    # def __init__(self, parent):
    #     super(HiloQSplash, self).__init__(parent)

    def run(self):
        print("Iniciando Hilo QSplash")
        ############# SPLASHSCREEN #################################################################################
        pixmap = QPixmap('ui/splash.png')
        splash = QSplashScreen(pixmap)#(pixmap)
        splash.show()
        splash.setStyleSheet(
            "color: rgb(255, 255, 255); font-size: 26px; font-family: calibri; text-align: center;")
        splash.showMessage('SOLUCIONANDO...', 0x0004, QColor(255, 255, 255))
        # ---------------------------------------------- #
        #time.sleep(1)
        print("Finalizando Hilo QSplash")

class controlador_juego_fichas:
    def __init__(self):
        self.vista = JuegoFichasUI(self)
        self.leyenda = {1: self.vista.a, 2: self.vista.b, 3: self.vista.c, 4: self.vista.d, 5: self.vista.e, 6: self.vista.f,
               7: self.vista.g, 8: self.vista.h}
        self.complejidad = 0
        self.pasos = None
        self.tiempo = 0
        self.LOG = None

    def iniciar(self):
        #self.vista.tablero.setEnabled(False)
        self.vista.show()

    def mover(self, single, ficha, animar=False, x=None, y=None):
        if single:
            #print("Moviendo ficha individual %d  en controlador..."%ficha)
            juego.mover_ficha(juego.fichas, ficha)
            print(juego.mostrar(juego.fichas))
        if x is None and y is None:
            x, y = juego.coordenadas(juego.fichas.index(ficha))
        #print(x, y)
        self.vista.mover(self.leyenda[ficha], y * 100, x * 100, animar)

    def poner_fichas(self):
        cnt = 0
        for y in range(3):
            for x in range(3):
                ficha = juego.fichas[cnt]
                if ficha != -1:
                    #print("Ficha: %d"%ficha)
                    #print("Pos (x, y): %d, %d"%(x*100, x*100))
                    self.mover(False, ficha, False, y, x)
                    #print("============================================")
                cnt += 1
        comprobar = threading.Thread(target=self.comprobar(), name="Comprobar Thread")
        comprobar.start()
        comprobar.join()

    def mover_1(self):
        self.mover(True, 1, True)

    def mover_2(self):
        self.mover(True, 2, True)

    def mover_3(self):
        self.mover(True, 3, True)

    def mover_4(self):
        self.mover(True, 4, True)

    def mover_5(self):
        self.mover(True, 5, True)

    def mover_6(self):
        self.mover(True, 6, True)

    def mover_7(self):
        self.mover(True, 7, True)

    def mover_8(self):
        self.mover(True, 8, True)

    def comprobar(self):
        h = juego.heuristica(juego.fichas)
        #print(h)
        if h == 8:
            self.vista.solucionar.setEnabled(False)
            self.vista.notificacion("Usted ha ganado!")

    def desordenar(self):
        # habilitar tablero
        self.vista.tablero.setEnabled(True)
        self.vista.solucionar.setEnabled(True)
        # desordenar las fichas en el modulo
        fichas, self.complejidad = juego.poner_fichas(juego.fichas, False)
        juego.fichas = fichas
        # posicionar fichas visuales
        self.poner_fichas()

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
        self.tiempo = "%02d:%02d" % (m, s)

    def animar_solucion_hilo(self):
        self.LOG = ["- Puzzle solucionado en %d pasos. Duración: %s" % (len(self.pasos.path()), self.tiempo),
                    "============================"]
        thread = HiloAnimarSolucionPuzzle(self.vista, self.pasos)
        thread.signal.connect(self.animar)
        thread.start()
        #self.LOG = ""

    def animar(self, ficha, puzzle):
        self.LOG.append("* Ficha movida: %s\n----------------------------\n" % (ficha if ficha is not None else "Ninguna"))
        self.LOG.append(puzzle)
        if ficha is not None:
            self.mover(True, int(ficha), True)
        self.LOG.append("============================")
        #print("EN BUCLE FOR")
        self.vista.ponerLOGS(self.LOG)

    def solucionar(self):
        #hilo_splash = HiloQSplash()
        #hilo_splash.start()
        # HILO PARA SOLUCION
        self.solucionar_hilo()
        # solucionar = threading.Thread(target=self.solucionar_hilo(), name="Comprobar Thread")
        # solucionar.start()
        # solucionar.join()
        # ---------------------------------------------- #
        # HILO PARA ANIMACION
        self.animar_solucion_hilo()
        #print("Saliendo del Hilo Principal")

    def sugerir(self):
        pass
        # for ficha, puzzle in self.pasos.path():
        #     if juego.fichas