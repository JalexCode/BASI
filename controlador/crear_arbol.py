import os
import pickle
IS_GRAPHVIZ_INSTALLED = False
try:
    import graphviz
    IS_GRAPHVIZ_INSTALLED = True
except:
    # print("No se encontro el modulo graphviz")
    pass

from PyQt5.QtWidgets import *

from modelo.arbol import Arbol
from ui.interfaces import CrearArbol, Visualizador


class controlador_crear_arbol:
    def __init__(self, arbol=None, padre=None):
        self.padre = padre
        self.arbol = arbol
        self.vista = CrearArbol(self)

    def iniciar(self):
        self.vista.show()
        self.cargar_datos()

    def comprobar_arbol(self):
        if self.arbol is None:
            raise Exception(
                "Debe crear un árbol. Para esto haga click en el botón 'Nuevo Árbol', o presione 'Cargar árbol desde el HDD'")

    def cargar_datos(self):
        try:
            self.comprobar_arbol()
            # LLENAR QTREEWIDGET
            self.vista.llenar_arbol(self.arbol)
        except Exception as e:
            print("Cargar datos: %s" % e.args[0])
            self.vista.error(e.args[0])

    def nuevo(self):
        try:
            if self.arbol is not None:
                sentencia = self.vista.pregunta("¿Realmente desea eliminar el árbol actual y crear un nuevo árbol?")
                print(sentencia)
                if sentencia:
                    self.arbol = Arbol(0)
                    self.arbol.reiniciar_arbol(0)
                    self.padre.arbol = self.arbol
            else:
                self.arbol = Arbol(0)
                self.arbol.reiniciar_arbol(0)
                self.padre.arbol = self.arbol
            self.cargar_datos()
        except Exception as e:
            print(e.args[0])
            self.vista.error(e.args[0])

    def guardar(self):
        try:
            dir = self.vista.guardar_dialog()
            if dir != "":
                with open(dir, 'wb') as fichero:
                    pickle.dump(self.arbol, fichero)
        except Exception as e:
            print(e.args[0])
            self.vista.error(e.args[0])

    def cargar(self):
        try:
            dir = self.vista.cargar_dialog()
            if dir != "":
                with open(dir, 'rb') as fichero:
                    self.arbol = pickle.load(fichero)
                    self.padre.arbol = self.arbol
                self.cargar_datos()
        except Exception as e:
            print(e.args[0])
            self.vista.error(e.args[0])

    def ver_info(self):
        # try:
        item = int(self.vista.arbol.selectedItems()[0].text(0))
        for x in self.arbol:
            if x.es_valor(item):
                item = x
                break
        self.vista.valor.setValue(item.valor)
        self.vista.nivel.setValue(item.nivel)
        self.vista.hoja.setChecked(item.es_hoja())
        if item.padre is not None:
            self.vista.padre.setValue(item.padre.valor)
        else:
            self.vista.padre.setValue(0)
        self.vista.hijos.clear()
        if len(item.hijos) > 0:
            for i in item.hijos:
                self.vista.hijos.addItem(QListWidgetItem(str(i.valor)))
        # except Exception as e:
        #    print(e.args[0])
        #    self.vista.error(e.args[0])

    def insertar_nodo(self):
        try:
            self.comprobar_arbol()
            seleccion = self.vista.arbol.selectedItems()
            if not len(seleccion):
                raise Exception("Para insertar un hijo a un nodo, primero seleccione uno en el árbol")
            padre = int(seleccion[0].text(0))
            hijo = self.vista.nuevo_valor.value()
            self.arbol.agregar_nodo(padre, hijo)
            self.cargar_datos()
        except Exception as e:
            print("Insertar nodo: %s" % e.args[0])
            self.vista.error(e.args[0])

    def modificar_nodo(self):
        try:
            self.comprobar_arbol()
            seleccion = self.vista.arbol.selectedItems()
            if not len(seleccion):
                raise Exception("Para modificar un nodo, primero seleccione uno en el árbol")
            valor = int(seleccion[0].text(0))
            nuevo_valor = self.vista.nuevo_valor.value()
            self.arbol.modificar_nodo(valor, nuevo_valor)
            self.cargar_datos()
        except Exception as e:
            print("Modificar nodo: %s" % e.args[0])
            self.vista.error(e.args[0])

    def eliminar_nodo(self):
        try:
            self.comprobar_arbol()
            seleccion = self.vista.arbol.selectedItems()
            if not len(seleccion):
                raise Exception("Para eliminar un nodo, primero seleccione uno en el árbol")
            if len(self.arbol) == 1:
                raise Exception("No puede eliminar al nodo raíz")
            valor = int(seleccion[0].text(0))
            self.arbol.eliminar_nodo(valor)
            self.cargar_datos()
        except Exception as e:
            print("Eliminar nodo: %s" % e.args[0])
            self.vista.error(e.args[0])

    def bfs(self):
        try:
            self.comprobar_arbol()
            self.vista.limpiarRecorridos()
            self.vista.agregarRecorrido("Broad First Search (recorrido a lo ancho)")
            for x in self.arbol:
                self.vista.agregarRecorrido(x.valor)
        except Exception as e:
            print("BFS: %s" % e.args[0])
            self.vista.error(e.args[0])

    def preorden(self):
        try:
            self.comprobar_arbol()
            self.vista.limpiarRecorridos()
            self.vista.agregarRecorrido("Depth First Search (recorrido a lo profundo) [PreOrden]")
            for x in self.arbol.dfs_preorden():
                self.vista.agregarRecorrido(x.valor)
        except Exception as e:
            print("Preorden: %s" % e.args[0])
            self.vista.error(e.args[0])

    def sugerir_hijo(self):
        try:
            self.comprobar_arbol()
            usado = True
            valor_no_usado = 0
            elementos = self.arbol.toList()
            while usado:
                if valor_no_usado in elementos:
                    valor_no_usado += 1
                else:
                    usado = False
            self.vista.nuevo_valor.setValue(valor_no_usado)
        except Exception as e:
            print("Sugerir: %s" % e.args[0])
            self.vista.error(e.args[0])

    def guardar_img(self):
        if not IS_GRAPHVIZ_INSTALLED:
            self.vista.error("No está instalado el módulo GraphViz")
        try:
            self.comprobar_arbol()
            # -------------------------#
            if not os.path.exists('grafos_generados'):
                os.makedirs('grafos_generados')
            with open('grafos_generados/grafo.dot', 'w') as grafo_file:
                grafo = ""
                for x in self.arbol.dfs_preorden():
                    item = str(x.valor)
                    if not x.es_raiz():
                        padre = str(x.padre.valor)
                        grafo += "\t" + padre + " -- " + item + "\n"
                contenido = "graph Arbol {\n%s}"%(grafo)
                grafo_file.write(contenido)
            file = 'grafos_generados/grafo.dot'
            file = graphviz.render('dot', 'png', file)
            self.vista.notificacion("Imagen creada en: %s"%file)
            self.visualizador = Visualizador()
            self.visualizador.show()
        except Exception as e:
            print("Guardar imagen: %s" % e.args[0])
            self.vista.error(e.args[0])