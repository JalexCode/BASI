from modelo.juego_fichas.juego_8_fichas_2 import JuegoFichas


def solucionar(self):
    caso = self
    while caso.heuristica() < 8:
        posibles_jugadas = [caso.ficha_neutra.arriba, caso.ficha_neutra.abajo, caso.ficha_neutra.izquierda,
                            caso.ficha_neutra.derecha]
        print(list(map(str, posibles_jugadas)))
        cambios_realizados = []  # contiene objetos JuegoFichas con la jugada realizada
        for x in posibles_jugadas:  # para los posibles juegadas
            if x is not None:
                nueva_jugada = JuegoFichas()
                print(nueva_jugada.fichas)
                # -------------------------------
                nueva_jugada.ficha1 = caso.ficha1
                nueva_jugada.ficha2 = caso.ficha2
                nueva_jugada.ficha3 = caso.ficha3
                nueva_jugada.ficha4 = caso.ficha4
                nueva_jugada.ficha5 = caso.ficha5
                nueva_jugada.ficha6 = caso.ficha6
                nueva_jugada.ficha7 = caso.ficha7
                nueva_jugada.ficha8 = caso.ficha8
                nueva_jugada.ficha_neutra = caso.ficha_neutra
                nueva_jugada.poner_fichas()
                # -------------------------------
                nueva_jugada.mover_ficha(x.valor)
                n2 = nueva_jugada
                print("Nueva jugada para Ficha #%d" % x.valor)
                print(nueva_jugada)
                print("----------------------")
                cambios_realizados.append(n2)
                nueva_jugada.mover_ficha(x.valor)
        # print(list(map(str, cambios_realizados)))
        cambios_realizados.sort(key=lambda i: i.heuristica(), reverse=True)
        yield (caso, cambios_realizados)
        caso = cambios_realizados[0]
        print(list(map(str, cambios_realizados)))
        # print(caso)
        break
        # print(caso)
        # print("----------------------")