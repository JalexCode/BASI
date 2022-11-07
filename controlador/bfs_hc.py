import pickle
from ui.interfaces import BFS_HC, MostrarCodigo


class controlador_bfs_hc:
    def __init__(self, arbol=None):
        self.arbol = arbol
        self.vista = BFS_HC(self)

    def iniciar(self):
        self.vista.show()
        self.cargar_datos()

    def comprobar_arbol(self):
        if self.arbol is None:
            raise Exception("Debe crear un árbol o cargar uno existente para poder aplicar los algoritmos")

    def cargar_datos(self):
        try:
            self.comprobar_arbol()
            # LLENAR QTREEWIDGET
            self.vista.llenar_arbol(self.arbol)
        except Exception as e:
            print("Cargar datos: %s"%e.args[0])
            self.vista.error(e.args[0])

    def cargar(self):
        try:
            dir = self.vista.cargar_dialog()
            if dir != "":
                with open(dir, 'rb') as fichero:
                    self.arbol = pickle.load(fichero)
                self.cargar_datos()
        except Exception as e:
            print(e.args[0])
            self.vista.error(e.args[0])

    def bfs(self):
        try:
            self.comprobar_arbol()
            self.vista.limpiarRecorridos()
            self.vista.agregarRecorrido("Best First Search (Búsqueda del primero mejor)")
            objetivo = self.vista.objetivo.value()
            lista = []
            for x in self.arbol.BestFirstSearch(objetivo):
                self.vista.agregarRecorrido(x.valor)
                lista.append(x)
            if lista[-1].es_valor(objetivo):
                self.vista.agregarRecorrido("Encontrado nodo %d" % objetivo)
            else:
                self.vista.agregarRecorrido("No se encontró el nodo %d"%objetivo)

        except Exception as e:
            print("BFS: %s"%e.args[0])
            self.vista.error(e.args[0])

    '''def hc(self):
        try:
            self.comprobar_arbol()
            self.vista.limpiarRecorridos()
            self.vista.agregarRecorrido("Depth First Search (recorrido a lo profundo) [PreOrden]")
            for x in self.arbol.dfs_preorden():
                self.vista.agregarRecorrido(x.valor)
        except Exception as e:
            print("Preorden: %s"%e.args[0])
            self.vista.error(e.args[0])'''

    def mostrar(self):
        self.ventana = MostrarCodigo()
        self.ventana.txt.setText(self.BFStoString())
        self.ventana.show()

    def BFStoString(self):
        return """    def BestFirstSearch(self, objetivo):
        pila = [self] # pila
        while len(pila) != 0: # mientras la pila este llena
            longitud = len(pila[0].hijos)
            for i in range(longitud): # repito la siguiente orden n veces, donde n es la cantidad de hijos del nodo
                pila.insert(1, sorted(pila[0].hijos, key=lambda a: a.valor)[longitud - (i + 1)]) # inserto los hijos del nodo ordenados en la pila, en la posicion 1
            nodo = pila.pop(0) # retiro el primer elemento de la pila
            yield nodo # lo retorno
            if nodo.valor == objetivo: # si es el objetivo
                yield "Objetivo encontrado!" # anuncio que fue encontrado (no es necesario)
                break # rompo el ciclo"""