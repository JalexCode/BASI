from ui.interfaces import Genetica, QTableWidgetItem
import modelo.genetica.max_funcion.ag as max_funcion


class controlador_max_funcion_genetica:
    def __init__(self):
        self.vista = Genetica(self)
        self.modulo = max_funcion
        self.poblacion = None

    def iniciar(self):
        self.vista.show()

    def generar(self):
        try:
            self.modulo.tam_poblacion = self.vista.poblacion.value()
            self.modulo.valor_min = self.vista.min.value()
            self.modulo.valor_max = self.vista.max.value()
            self.poblacion = self.modulo.generar_poblacion()
            self.vista.limpiar_tabla()
            for j in range(len(self.poblacion)):
                i = self.vista.tabla1.rowCount()
                self.vista.tabla1.insertRow(i)
                item = self.poblacion[j]
                self.vista.tabla1.setItem(i, 0, QTableWidgetItem(str(item[0])))
                self.vista.tabla1.setItem(i, 1, QTableWidgetItem(str(item[1])))
                self.vista.tabla1.setItem(i, 2, QTableWidgetItem(str(pow(item[0], 2))))
                self.vista.tabla1.setItem(i, 3, QTableWidgetItem(str(self.modulo.funcionFitness(item))))
        except Exception as e:
            self.vista.error(e.args[0])

    def seleccion(self):
        try:
            self.modulo.generaciones = self.vista.generaciones.value()
            self.modulo.pressure = self.vista.indiv_reprod.value()
            self.modulo.prob_mutacion = self.vista.mutacion.value()
            ############################################################
            self.vista.logs.clear()
            genetica = self.modulo.iniciar(self.poblacion)
            self.vista.logs.setPlainText("%s\n"%genetica[1])
            self.poblacion = genetica[0]
        except Exception as e:
            self.vista.error(e.args[0])
