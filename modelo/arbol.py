from collections import Counter


class Arbol:
    def __init__(self, valor=None, padre=None):
        self.__valor:'int' = valor
        self.__padre:'Arbol' = padre
        self.__hijos = []
        self.__nivel:'int' = self.padre.nivel + 1 if self.padre is not None else 0

    @property
    def valor(self):
        return self.__valor

    @valor.setter
    def valor(self, value):
        self.__valor = value

    @property
    def hijos(self):
        return self.__hijos

    @hijos.setter
    def hijos(self, value):
        self.__hijos = value

    @property
    def padre(self):
        return self.__padre

    @padre.setter
    def padre(self, value):
        self.__padre = value

    @property
    def nivel(self):
        return self.__nivel

    @nivel.setter
    def nivel(self, value):
        self.__nivel = value

    def bfs(self):
        cola = [self]
        while len(cola) != 0:
            for h in cola[0].hijos:
                cola.append(h)
            yield cola.pop(0)

    def dfs_preorden(self):
        lista = [self]
        while len(lista) != 0:
            longitud = len(lista[0].hijos)
            for i in range(longitud):
                lista.insert(1, lista[0].hijos[longitud - (i + 1)])
            yield lista.pop(0)

    '''def dfs_entreorden(self):
        pila = [self]
        while len(pila) != 0:
            longitud = len(pila[0].hijos)
            for i in range(longitud):
                pila.insert(1, pila[0].hijos[longitud - (i+1)])
            yield pila.pop(0)'''

    '''def dfs_postorden(self):
        raiz = self
        hijos_raiz = []
        lista = [self]
        while len(lista) != 0:
            longitud = len(lista[0].hijos)
            for i in range(longitud):
                lista.insert(1, lista[0].hijos[longitud - (i + 1)])
            yield lista.pop(0)'''

    '''def dfs_supesto_postorden_no_sirve_pero_hace_un_recorrido_sexy_lol(self):
        pila = [self]
        while len(pila) > 0:
            primer_elemento = pila[0]
            longitud = len(primer_elemento.hijos)
            for i in range(longitud):
                pila.insert(0, primer_elemento.hijos[longitud - (i+1)])
            print(list(map(lambda x: x.valor, pila)))
            yield pila.pop(- (len(pila) - longitud))'''

    def __iter__(self):
        return self.bfs()
        #return self.dfs_preorden()

    def __len__(self):
        nodos = []
        for x in self:
            nodos.append(x)
        return len(nodos)

    def __str__(self):
        hijos = []
        for h in self.hijos:
            hijos.append(str(h.valor))
        if not len(self.hijos):
            hijos = ["Ninguno"]
        return "Nodo: %d | Padre: %d | Hijos: %s | Nivel: %d" % (self.valor, self.padre.valor if self.padre is not None else 0, ", ".join(hijos).strip(", "), self.nivel)

    def __contains__(self, value):
        for x in self:
            if x.es_valor(value):
                return True
        return False

    def toString(self):
        s = "ARBOL DE RAIZ %d\n=====================\n" % self.valor
        for h in self:
            s += str(h) + "\n"
        return s

    def toList(self):
        #temporalmente
        lista = []
        for x in self:
            lista.append(x.valor)
        return lista

    def grado_nodo(self):
        return len(self.hijos)

    def es_hoja(self):
        return self.grado_nodo() == 0

    def es_raiz(self):
        return self.padre is None

    def es_valor(self, valor):
        return self.valor == valor

    def es_padre(self, padre):
        return self.padre.es_valor(padre)

    def agregar_nodo(self, padre_valor, valor):
        if self.__contains__(valor):
            raise Exception("Agregar: El nodo %d ya existe" % (valor))
        for x in self:
            if x.es_valor(padre_valor):
                x.hijos.append(Arbol(valor, x))
                break

    def modificar_nodo(self, valor, nuevo__valor):
        modificado = False
        if self.__contains__(nuevo__valor):
            raise Exception("Modificar: El nodo %d ya existe" % (nuevo__valor))
        for x in self:
            if x.valor == valor:
                modificado = True
                x.valor = nuevo__valor
                break
        if not modificado:
            raise Exception("Modificar: El nodo %d no existe" % (valor))

    def eliminar_nodo(self, valor):
        eliminado = False
        # bfs
        cola = [self]
        while len(cola) != 0:
            for h in range(len(cola[0].hijos)):
                item = cola[0].hijos[h]
                cola.append(item)
                if item.es_valor(valor):
                    eliminado = True
                    cola[0].hijos.remove(item)
                    return
            cola.pop(0)
        if not eliminado:
            raise Exception("Eliminar: El nodo %d no existe" % (valor))

    def reiniciar_arbol(self, valor=None, padre=None):
        self.valor = valor
        self.padre = padre
        self.hijos.clear()

    # ------------------- ALGORTIMOS ------------------- #
    def BestFirstSearch(self, objetivo):
        pila = [self]  # pila
        while len(pila) != 0: # mientras la pila este llena
            longitud = len(pila[0].hijos)
            for i in range(longitud): # repito la siguiente orden n veces, donde n es la cantidad de hijos del nodo
                pila.insert(1, sorted(pila[0].hijos, key=lambda a: a.valor)[longitud - (i + 1)]) # inserto los hijos del nodo ordenados en la pila, en la posicion 1
            nodo = pila.pop(0) # retiro el primer elemento de la pila
            yield nodo # lo retorno
            if nodo.valor == objetivo: break# si es el objetivo, detengo el ciclo
                #yield "Objetivo encontrado!" # anuncio que fue encontrado (no es necesario)

    def HillClimbing(self, objetivo):
        encontrado = False
        lista_desiciones = Counter() #1:self.hijos
        desicion = 1
        ultima_desicion = 1
        lista_desiciones[desicion] = sorted(self.hijos, key=lambda a: a.valor)
        while not encontrado:
            for x in range(len(lista_desiciones[ultima_desicion])):
                while len(lista_desiciones[ultima_desicion]) > 0:
                    #print(list(map(str,lista_desiciones[desicion])))
                    elemento = lista_desiciones[desicion][x]
                    if elemento.valor != objetivo:
                        eliminado = lista_desiciones[desicion].pop(0)
                        yield eliminado
                        desicion += 1
                        lista_desiciones[desicion] = sorted(elemento.hijos, key=lambda a: a.valor)
                        if elemento.es_hoja():
                            break
                    else:
                        encontrado = True
                        return lista_desiciones[desicion].pop(0)
                ultima_desicion += 1
                #yield eliminado
            #print("Diccionario: ", end='')
            #print(lista_desiciones)