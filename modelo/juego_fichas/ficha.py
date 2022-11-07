class Ficha:
    def __init__(self, valor, fila:'int', columna:'int', arriba=None, abajo=None, izquierda=None, derecha=None):
        self.__valor = valor
        self.__fila = fila
        self.__columna = columna
        self.__arriba = arriba
        self.__abajo = abajo
        self.__izquierda = izquierda
        self.__derecha = derecha

    @property
    def valor(self):
        return self.__valor

    @valor.setter
    def valor(self, value):
        self.__valor = value

    @property
    def fila(self):
        return self.__fila

    @fila.setter
    def fila(self, value):
        self.__fila = value

    @property
    def columna(self):
        return self.__columna

    @columna.setter
    def columna(self, value):
        self.__columna = value

    @property
    def arriba(self):
        return self.__arriba

    @arriba.setter
    def arriba(self, value):
        self.__arriba = value

    @property
    def abajo(self):
        return self.__abajo

    @abajo.setter
    def abajo(self, value):
        self.__abajo = value

    @property
    def izquierda(self):
        return self.__izquierda

    @izquierda.setter
    def izquierda(self, value):
        self.__izquierda = value

    @property
    def derecha(self):
        return self.__derecha

    @derecha.setter
    def derecha(self, value):
        self.__derecha = value

    @property
    def en_su_lugar(self):
        return self.__en_su_lugar

    @en_su_lugar.setter
    def en_su_lugar(self, value):
        self.__en_su_lugar = value

    def es_valor(self, valor):
        return self.valor == valor

    def __str__(self):
        return str(self.valor)