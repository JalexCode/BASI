import threading
import time

class HiloSolucionarPuzzle(threading.Thread):
    def __init__(self, threadID, name, presentador):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.presentador = presentador

    def run(self):
        print("Iniciando " + self.name)
        self.presentador.solucionar_hilo(self.name)
        print("Finalizando " + self.name)

class HiloAnimacion(threading.Thread):
    def __init__(self, threadID, name, presentador):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.presentador = presentador

    def run(self):
        print("Iniciando " + self.name)
        self.presentador.animar_solucion_hilo(self.name)
        print("Finalizando " + self.name)