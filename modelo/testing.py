from modelo.arbol import Arbol

# raiz
arbol = Arbol(0)
# subarbol izquierdo
arbol.agregar_nodo(0, 5)
arbol.agregar_nodo(5, 10)
arbol.agregar_nodo(10, 9)
arbol.agregar_nodo(10, 11)
arbol.agregar_nodo(5, 7)
arbol.agregar_nodo(7, 6)
# subarbol derecho
arbol.agregar_nodo(0, 8)
arbol.agregar_nodo(8, 4)
arbol.agregar_nodo(4, 3)
arbol.agregar_nodo(4, 2)
arbol.agregar_nodo(2, 1)
arbol.agregar_nodo(2, 12)
#print(arbol.toString())
# actualizacion
#arbol.modificar_nodo(12, 13)
#print(arbol.toString())
#arbol.eliminar_nodo(13)
#print(arbol.toString())
#####
'''for x in arbol.dfs_postorden():
    print()'''

#arbol.dfs_postorden()

for x in arbol.HillClimbing(3):
    print(x)

## de la interfaz
# probando la insercion de items con padres y sin padres
"""a = QTreeWidgetItem(["1"])
        b = QTreeWidgetItem(a, ["2"])
        c = QTreeWidgetItem(["3"])
        d = QTreeWidgetItem(["4"])
        self.arbol.addTopLevelItem(a)
        self.arbol.addTopLevelItem(b)
        a = [QTreeWidgetItem(["1"])]
        a.append(QTreeWidgetItem(a[0], ["2"]))
        self.arbol.addTopLevelItems(a)"""