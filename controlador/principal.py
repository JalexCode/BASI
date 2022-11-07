import sys

from PyQt5.QtWidgets import QApplication

from controlador.bfs_hc import controlador_bfs_hc
from controlador.crear_arbol import controlador_crear_arbol
from controlador.debug import controlador_debug
from controlador.juego_fichas_ctrl import controlador_juego_fichas
from controlador.maximizar_funcion_ag import controlador_max_funcion_genetica
from modelo.arbol import Arbol
from ui.interfaces import Principal, AcercaDe


class controlador_principal:
    def __init__(self):
        self.__arbol = None
        # logs
        self.__logs = ""

    @property
    def arbol(self):
        return self.__arbol

    @arbol.setter
    def arbol(self, value):
        self.__arbol = value

    @property
    def logs(self):
        return self.__logs

    @logs.setter
    def logs(self, value):
        self.__logs = value

    def test(self):
        # arbol de prueba
        self.arbol = Arbol(0)
        # subarbol izquierdo
        self.arbol.agregar_nodo(0, 5)
        self.arbol.agregar_nodo(5, 10)
        self.arbol.agregar_nodo(10, 9)
        self.arbol.agregar_nodo(10, 11)
        self.arbol.agregar_nodo(5, 7)
        self.arbol.agregar_nodo(7, 6)
        # subarbol derecho
        self.arbol.agregar_nodo(0, 8)
        self.arbol.agregar_nodo(8, 4)
        self.arbol.agregar_nodo(4, 3)
        self.arbol.agregar_nodo(4, 2)
        self.arbol.agregar_nodo(2, 1)
        self.arbol.agregar_nodo(2, 12)

    def iniciar(self):
        aplicacion = QApplication(sys.argv)
        self.vista = Principal(self)
        self.vista.show()

        #self.test()
        aplicacion.exec()


    def crear_arbol(self):
        crear_arbol = controlador_crear_arbol(self.arbol, self)
        crear_arbol.iniciar()

    def bfs(self):
        bfs = controlador_bfs_hc(self.arbol)
        bfs.iniciar()

    def ag(self):
        ag = controlador_max_funcion_genetica()
        ag.iniciar()

    def juego_fichas(self):
        jf = controlador_juego_fichas()
        jf.iniciar()

    def debug(self):
        debug = controlador_debug(self)
        debug.iniciar()

    def acerca_de(self):
        self.about = AcercaDe()
        self.about.show()