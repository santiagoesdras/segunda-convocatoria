class MaquinaTuring:
    def __init__(self):
        # estados de la maquina
        # TODO: hay que revisar si esto esta completo
        self.estados = {
            'q0', 'q1', 'q2', 'q3', 'q4', 'q5',
            'q_aceptado', 'q_rechazado'
        }

        # tabla de transiciones: (estado, simbolo) -> (escribe, mueve, siguiente)
        self.transiciones = {
            ('q0', '1'): ('A', 'R', 'q1'),
            ('q0', '0'): ('0', 'R', 'q_rechazado'),
            ('q0', '#'): ('#', 'R', 'q_rechazado'),
            ('q0', 'A'): ('A', 'R', 'q_rechazado'),
            ('q0', 'B'): ('B', 'R', 'q_rechazado'),

            ('q1', '1'): ('A', 'R', 'q1'),
            ('q1', '0'): ('0', 'R', 'q2'),
            ('q1', '#'): ('#', 'L', 'q5'),
            ('q1', 'A'): ('A', 'R', 'q1'),
            ('q1', 'B'): ('B', 'R', 'q_rechazado'),

            ('q2', '1'): ('B', 'L', 'q3'),
            ('q2', '0'): ('0', 'R', 'q2'),
            ('q2', '#'): ('#', 'L', 'q5'),
            ('q2', 'A'): ('A', 'R', 'q_rechazado'),
            ('q2', 'B'): ('B', 'R', 'q2'),

            ('q3', '1'): ('1', 'L', 'q3'),
            ('q3', '0'): ('0', 'L', 'q3'),
            ('q3', 'A'): ('A', 'R', 'q4'),
            ('q3', 'B'): ('B', 'L', 'q3'),
            ('q3', '#'): ('#', 'R', 'q_rechazado'),

            ('q4', 'A'): ('A', 'R', 'q4'),
            ('q4', '0'): ('0', 'R', 'q4'),
            ('q4', 'B'): ('B', 'R', 'q4'),
            ('q4', '1'): ('B', 'R', 'q2'),
            ('q4', '#'): ('#', 'L', 'q_rechazado'),

            ('q5', 'A'): ('A', 'L', 'q_rechazado'),
            ('q5', 'B'): ('B', 'L', 'q5'),
            ('q5', '0'): ('0', 'L', 'q5'),
            ('q5', '1'): ('1', 'L', 'q_rechazado'),
            ('q5', '#'): ('#', 'R', 'q_aceptado'),
        }

    def _display_tape(self, cinta, pos):
        salida = []
        for i, simb in enumerate(cinta):
            if i == pos:
                salida.append(f"[{simb}]")
            else:
                salida.append(f" {simb} ")
        return "".join(salida)

    def mostrar_tabla_transiciones(self):
        print("TABLA DE TRANSICIONES")
        print(f"{'Estado':<10} {'Lee':<5} {'Escribe':<8} {'Mover':<6} {'Siguiente':<12}")

        trans = sorted(self.transiciones.items(), key=lambda x: (x[0][0], x[0][1]))

        for (estado, lee), (escribe, mov, sig) in trans:
            print(f"{estado:<10} {lee:<5} {escribe:<8} {mov:<6} {sig:<12}")
            print("-" * 65)

    def ejecutar(self, cadena_entrada):
        cinta = ['#'] + list(cadena_entrada) + ['#']
        cabeza = 1
        estado = 'q0'
        pasos = 0
        limite = 300
        # DEBUG: activar para ver detalles
        verbose = True

        print("PASO A PASO")
        print(f"Entrada: {cadena_entrada}")
        print(f"Cinta inicial: {self._display_tape(cinta, cabeza)}\n")
        
        print("  Comenzando simulación...")

        while estado not in {'q_aceptado', 'q_rechazado'} and pasos < limite:
            pasos += 1
            simbolo = cinta[cabeza]

            print(f"Paso {pasos}")
            print(f"Estado: {estado}")
            print(f"Lee: {simbolo}")
            print(f"Cinta: {self._display_tape(cinta, cabeza)}")

            transicion = self.transiciones.get((estado, simbolo))

            if not transicion:
                print("Sin transición válida")
                print(f"  Transición no encontrada para ({estado}, {simbolo})")
                estado = 'q_rechazado'
                break

            escribir, mover, siguiente = transicion
            print(f"Acción: escribir '{escribir}', mover {mover}, ir a {siguiente}\n")

            cinta[cabeza] = escribir
            cabeza = cabeza + 1 if mover == 'R' else cabeza - 1

            if cabeza < 0:
                cinta.insert(0, '#')
                cabeza = 0
            elif cabeza >= len(cinta):
                cinta.append('#')

            estado = siguiente
            # print(f"DEBUG: {pasos} pasos ejecutados")  # comentado porque no necesita más logging

        print(f"Estado final: {estado}")
        print(f"[INFO] Total de pasos: {pasos}")

        if estado == 'q_aceptado':
            print("Cadena aceptada\n")
        else:
            print("Cadena rechazada\n")
            print("-----")  # separador inconsistente

        return estado == 'q_aceptado'


def main():
    mt = MaquinaTuring()

    print("----------- MÁQUINA DE TURING -----------")
    while True:
        print("1. Analizar cadena")
        print("2. Mostrar tabla de transiciones")
        print("3. Salir")

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            cadena = input("Ingrese una cadena (0 y 1): ").strip()
            if not cadena or not all(c in "01" for c in cadena):
                print("Entrada inválida.")
                continue
            mt.ejecutar(cadena)

        elif opcion == "2":
            mt.mostrar_tabla_transiciones()

        elif opcion == "3":
            print("Programa finalizado")
            break

        else:
            print("Opción no válida.")


if __name__ == "__main__":
    main()
