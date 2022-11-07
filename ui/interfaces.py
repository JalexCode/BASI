import threading
import time

from PyQt5.QtCore import QTimer
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from psutil._pswindows import Priority
from qtpy import uic
#from xlwings.constants import Priority

from modelo.arbol import Arbol

class Principal(QMainWindow):
    def __init__(self, controlador):
        # ------------------------------#
        QMainWindow.__init__(self)
        uic.loadUi('ui/main.ui', self)
        # ------------------------------#
        self.__controlador = controlador

        self.crear_arbol.triggered.connect(self.__controlador.crear_arbol)
        self.bfs.triggered.connect(self.__controlador.bfs)
        self.max_genetica.triggered.connect(self.__controlador.ag)
        self.fichas.triggered.connect(self.__controlador.juego_fichas)
        self.desarrollo.triggered.connect(self.__controlador.debug)
        self.acerca_de.triggered.connect(self.__controlador.acerca_de)

        #self.setBG()
        info = QLabel("Bienvenido a BASI | Desarrollado por: Javier Alejandro González Casellas")
        self.statusbar.addWidget(info)

    def setBG(self):
        pixmap = QPixmap("ui/bg2.jpg")
        pixmap = pixmap.scaled(self.bg.height(), self.bg.width(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.bg.setPixmap(pixmap)
		
    def resizeEvent(self, a0: QResizeEvent):
        #self.setBG()
        background = QPixmap('ui/bg2.jpg')
        background = background.scaled(self.size(), Qt.IgnoreAspectRatio)  # KeepAspectRatio, KeepAspectRatioByExpanding
        pal = self.palette()
        pal.setBrush(QPalette.Background, QBrush(background))
        self.setPalette(pal)

class CrearArbol(QDialog):
    def __init__(self, controlador):
        # ------------------------------#
        QDialog.__init__(self)
        uic.loadUi('ui/arbol.ui', self)
        # ------------------------------#
        self.__controlador = controlador
        # ------------------------ CONEXIONES -------------------------#
        self.nuevo.clicked.connect(self.__controlador.nuevo)
        self.guardar.clicked.connect(self.__controlador.guardar)
        self.cargar.clicked.connect(self.__controlador.cargar)
        self.guardar_img.clicked.connect(self.__controlador.guardar_img)
        self.sugerir.clicked.connect(self.__controlador.sugerir_hijo)
        self.insertar.clicked.connect(self.__controlador.insertar_nodo)
        self.modificar.clicked.connect(self.__controlador.modificar_nodo)
        self.eliminar.clicked.connect(self.__controlador.eliminar_nodo)
        self.bfs.clicked.connect(self.__controlador.bfs)
        self.pre.clicked.connect(self.__controlador.preorden)
        self.arbol.itemClicked.connect(self.__controlador.ver_info)
        # --------------------------------------------------------------#
        self.arbol.setHeaderHidden(True)

    def llenar_arbol(self, arbol: 'Arbol'):
        self.arbol.clear()
        root = True
        items = []
        for n in arbol:
            valor = str(n.valor)
            if root:
                items.append(QTreeWidgetItem([valor]))
                root = False
                continue
            padre = str(n.padre.valor)
            for x in range(len(items)):
                if items[x].text(0) == padre:
                    items.append(QTreeWidgetItem(items[x], [valor]))
        self.arbol.addTopLevelItems(items)
        self.arbol.expandAll()

    def error(self, msg):
        QMessageBox.critical(self, 'Error', msg)

    def notificacion(self, msg):
        QMessageBox.information(self, 'BASI', msg)

    def pregunta(self, msg):
        a = QMessageBox.warning(self, 'Advertencia', msg, QMessageBox.Yes | QMessageBox.No)
        if a == QMessageBox.No:
            return False
        return True

    def guardar_dialog(self):
        dir = QFileDialog.getSaveFileName(self, "Seleccione un directorio y nombre el fichero para guardarlo", "./guardados",
                          "BASItree | *.BASItree")
        return dir[0]

    def cargar_dialog(self):
        dir = QFileDialog.getOpenFileName(self, "Seleccione un archivo BASItree para abrirlo", "./guardados",
                          "BASItree | *.BASItree")
        return dir[0]

    def limpiarRecorridos(self):
        self.recorrido.clear()

    def agregarRecorrido(self, valor):
        self.recorrido.addItem(QListWidgetItem(str(valor)))


class Visualizador(QDialog):
    def __init__(self):
        # ------------------------------#
        QDialog.__init__(self)
        uic.loadUi('ui/visual.ui', self)
        # ------------------------------#

    def resizeEvent(self, a0: QResizeEvent):
        background = QPixmap('grafos_generados/grafo.dot.png')
        background = background.scaled(self.size(),
                                       Qt.IgnoreAspectRatio)  # KeepAspectRatio, KeepAspectRatioByExpanding
        pal = self.palette()
        pal.setBrush(QPalette.Background, QBrush(background))
        self.setPalette(pal)

class BFS_HC(QDialog):
    def __init__(self, controlador):
        # ------------------------------#
        QDialog.__init__(self)
        uic.loadUi('ui/bfs.ui', self)
        # ------------------------------#
        self.__controlador = controlador
        # ------------------------ CONEXIONES -------------------------#
        self.cargar_hdd.clicked.connect(self.__controlador.cargar)
        self.mostrar.clicked.connect(self.__controlador.mostrar)
        self.bfs.clicked.connect(self.__controlador.bfs)
        #self.hc.clicked.connect(self.__controlador.hc)
        # --------------------------------------------------------------#
        self.arbol.setHeaderHidden(True)

    def llenar_arbol(self, arbol: 'Arbol'):
        self.arbol.clear()
        root = True
        items = []
        for n in arbol:
            valor = str(n.valor)
            if root:
                items.append(QTreeWidgetItem([valor]))
                root = False
                continue
            padre = str(n.padre.valor)
            print(padre)
            for x in range(len(items)):
                if items[x].text(0) == padre:
                    items.append(QTreeWidgetItem(items[x], [valor]))
        self.arbol.addTopLevelItems(items)
        self.arbol.expandAll()

    def error(self, msg):
        QMessageBox.critical(self, 'Error', msg)

    def pregunta(self, msg):
        a = QMessageBox.warning(self, 'Advertencia', msg, QMessageBox.Yes | QMessageBox.No)
        if a == QMessageBox.No:
            return False
        return True

    def cargar_dialog(self):
        dir = QFileDialog.getOpenFileName(self, "Seleccione un archivo BASItree para abrirlo", "./guardados",
                          "BASItree | *.BASItree")
        return dir[0]

    def limpiarRecorridos(self):
        self.recorrido.clear()

    def agregarRecorrido(self, valor):
        self.recorrido.addItem(QListWidgetItem(str(valor)))

class MostrarCodigo(QDialog):
    def __init__(self):
        # ------------------------------#
        QDialog.__init__(self)
        uic.loadUi('ui/codigo.ui', self)
        # ------------------------------#

class Debug(QDialog):
    def __init__(self, controlador):
        # ------------------------------#
        QDialog.__init__(self)
        uic.loadUi('ui/debug.ui', self)
        # ------------------------------#
        self.__controlador = controlador
        # ------------------------ CONEXIONES -------------------------#
        self.actualizar.clicked.connect(self.__controlador.cargar_datos)
        #self.guardar.clicked.connect(self.__controlador.guardar)
        # --------------------------------------------------------------#
        self.timer = QTimer()
        self.timer.start(1000)
        self.timer.timeout.connect(self.__controlador.cargar_datos)

    def set_datos(self, total, disponible, percent, usado, BASI):
        self.total.setValue(total)
        self.disponible.setValue(disponible)
        self.percent.setValue(percent)
        self.usado.setValue(usado)
        self.uso_app.setValue(BASI)

    def set_logs(self, txt):
        self.entrada.setPlainText(txt)

    def error(self, msg):
        QMessageBox.critical(self, 'Error', msg)
            

class AcercaDe(QDialog):
    def __init__(self):
        # ------------------------------#
        QDialog.__init__(self)
        uic.loadUi('ui/about.ui', self)
        # ------------------------------#

class JuegoFichasUI(QDialog):
    def __init__(self, controlador):
        # ------------------------------#
        QDialog.__init__(self)
        uic.loadUi('ui/fichas.ui', self)
        # ------------------------------#
        self.__controlador = controlador
        # ------------------------ CONEXIONES -------------------------#
        self.desordenar_btn.clicked.connect(self.__controlador.desordenar)
        self.a.clicked.connect(self.__controlador.mover_1)
        self.b.clicked.connect(self.__controlador.mover_2)
        self.c.clicked.connect(self.__controlador.mover_3)
        self.d.clicked.connect(self.__controlador.mover_4)
        self.e.clicked.connect(self.__controlador.mover_5)
        self.f.clicked.connect(self.__controlador.mover_6)
        self.g.clicked.connect(self.__controlador.mover_7)
        self.h.clicked.connect(self.__controlador.mover_8)
        # self.a.clicked.connect(self.__controlador.moverThread, (True, 1))
        # self.b.clicked.connect(self.__controlador.moverThread, (True, 2))
        # self.c.clicked.connect(self.__controlador.moverThread, (True, 3))
        # self.d.clicked.connect(self.__controlador.moverThread, (True, 4))
        # self.e.clicked.connect(self.__controlador.moverThread, (True, 5))
        # self.f.clicked.connect(self.__controlador.moverThread, (True, 6))
        # self.g.clicked.connect(self.__controlador.moverThread, (True, 7))
        # self.h.clicked.connect(self.__controlador.moverThread, (True, 8))
        # --------------------------------------------------------------#
        self.complejidad.clicked.connect(self.__controlador.mostrar_complejidad)
        self.solucionar.clicked.connect(self.__controlador.solucionar)
        self.entrada_soluciones.itemClicked.connect(self.__controlador.mostrarJugada)
        #self.velocidad.valueChanged.connect(self.definirVelocidad)
        self.solucionar.setEnabled(False)

    def definirVelocidad(self):
        self.__controlador.TIEMPO_ESPERA = self.velocidad.value() / 10
        print(self.__controlador.TIEMPO_ESPERA)

    def mover(self, ficha, nuevoX, nuevoY, animar=False):
        #print("Moviendo ficha individual %s  en vista..." % ficha.text())
        if animar:
            self.animacion = QPropertyAnimation(ficha, b"geometry")
            self.animacion.setDuration(self.velocidad.value()*10)
            self.animacion.setEndValue(QRect(nuevoX, nuevoY, 100, 100))
            self.animacion.start((QAbstractAnimation.DeleteWhenStopped))
        else: ficha.move(nuevoX, nuevoY)

    def ponerLOGS(self, LOGS):
        self.entrada_soluciones.clear()
        for log in LOGS:
            self.entrada_soluciones.addItem(QListWidgetItem(log))

    def error(self, msg):
        QMessageBox.critical(self, 'Error', msg)

    def notificacion(self, msg):
        QMessageBox.information(self, 'BASI', msg)

class Genetica(QDialog):
    def __init__(self, controlador):
        # ------------------------------#
        QDialog.__init__(self)
        uic.loadUi('ui/ag.ui', self)
        # ------------------------------#
        self.__controlador = controlador
        # ------------------------ CONEXIONES -------------------------#
        self.generar.clicked.connect(self.__controlador.generar)
        self.start_selec.clicked.connect(self.__controlador.seleccion)
        # --------------------------------------------------------------#
        #QTableWidget.setItem(self, i, 0, QTableWidgetItem(str(x)))
    def error(self, msg):
        QMessageBox.critical(self, 'Error', msg)

    def limpiar_tabla(self):
        while self.tabla1.rowCount() > 0:
            self.tabla1.removeRow(0)