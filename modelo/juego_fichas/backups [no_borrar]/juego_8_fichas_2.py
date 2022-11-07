class JuegoFichas:
    def __init__(self, fichas=None):
        self.__fichas = fichas

    @property
    def fichas(self):
        return self.__fichas

    @fichas.setter
    def fichas(self, value):
        self.__fichas = value

    def ordenar(self, dar_orden):
        if len(self.fichas) > 0:
            self.fichas = sorted(self.fichas, key=lambda x: x.valor)