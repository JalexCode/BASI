import os

import psutil
from ui.interfaces import Debug

class controlador_debug:
    def __init__(self, parent=None):
        self.parent = parent
        self.vista = Debug(self)

    def iniciar(self):
        self.vista.show()
        self.cargar_datos()

    def cargar_datos(self):
        try:
            # MEMORIA OCUPADA POR BASI
            pid = os.getpid()
            basi = psutil.Process(pid)
            uso_memoria_BASI = round(basi.memory_info()[0]/1024000000, 2)
            #######################################
            mem = psutil.virtual_memory()#._asdict()
            total = round(mem[0]/1024000000, 2)
            disponible = round(mem[1] / 1024000000, 2)
            percent = mem[2]
            usado = round(mem[3] / 1024000000, 2)
            self.vista.set_datos(total, disponible, percent, usado, uso_memoria_BASI)

            '''print(mem)
            print("Total: %.2f"%())
            print("Disponible: %.2f" % mem[1])
            print("Porciento: %.2f" % mem[2])
            print("Usado: %.2f" % mem[3])'''
        except Exception as e:
            print("Debug > Cargar datos: %s"%e.args[0])
            self.vista.error(e.args[0])

