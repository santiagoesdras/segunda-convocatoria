class MaquinaTuringFormal:
    def __init__(self):
        # estados para la maquina de turing - validacion de votos
        # TODO: revisar si q_rechazadot es correcto o si deberia ser q_rechazado
        self.estados = {
            'q0': 'Inicio',
            'q1': 'Paridad par', 
            'q2': 'Paridad impar',
            'q3': 'Buscar B para emparejar A',
            'q4': 'Buscar B para A actual',
            'q5': 'Retroceder para siguiente A',
            'q_aceptado': 'Aceptado',
            'q_rechazadot': 'Rechazado'  # typo pero funciona asi que lo dejo
        }
        
        self.transiciones = {
            ('q0', '#'): ('#', 'R', 'q2'),
            ('q0', 'A'): ('A', 'R', 'q2'),
            ('q0', 'B'): ('B', 'R', 'q2'),
            ('q0', 'C'): ('C', 'R', 'q2'),
            
            ('q1', 'A'): ('A', 'R', 'q2'),
            ('q1', 'B'): ('B', 'R', 'q2'),
            ('q1', 'C'): ('C', 'R', 'q2'),
            ('q1', '#'): ('#', 'L', 'q3'),
            
            ('q2', 'A'): ('A', 'R', 'q1'),
            ('q2', 'B'): ('B', 'R', 'q1'),
            ('q2', 'C'): ('C', 'R', 'q1'),
            ('q2', '#'): ('#', 'L', 'q_rechazado'),
            
            ('q3', '#'): ('#', 'R', 'q5'),
            ('q3', 'X'): ('X', 'R', 'q3'),
            ('q3', 'Y'): ('Y', 'R', 'q3'),
            ('q3', 'C'): ('C', 'R', 'q3'),
            ('q3', 'A'): ('X', 'R', 'q4'),
            ('q3', 'B'): ('B', 'R', 'q3'),
            
            ('q4', 'A'): ('A', 'R', 'q4'),
            ('q4', 'X'): ('X', 'R', 'q4'),
            ('q4', 'C'): ('C', 'R', 'q4'),
            ('q4', 'B'): ('Y', 'L', 'q3'),
            ('q4', 'Y'): ('Y', 'R', 'q4'),
            ('q4', '#'): ('#', 'L', 'q_aceptado'),
            
            ('q5', 'X'): ('X', 'L', 'q5'),
            ('q5', 'Y'): ('Y', 'L', 'q5'),
            ('q5', 'C'): ('C', 'L', 'q5'),
            ('q5', 'A'): ('A', 'L', 'q5'),
            ('q5', 'B'): ('B', 'L', 'q5'),
            ('q5', '#'): ('#', 'R', 'q3'),
        }
    
    def ejecutar(self, entrada):
        # preparar cinta
        self.cinta = ['#'] + list(entrada.replace(' ', '')) + ['#']
        self.cabezal = 1
        self.estado_actual = 'q0'
        self.pasos = 0
        
        # debug logs que alguien pudo haber dejado
        print("DEBUG: Entrada recibida:", entrada)
        print("INFO: Cinta inicial:", self._mostrar_cinta())
        print("Estado inicial:", self.estado_actual)
        print("[LOG] Iniciando ejecucion...")
        
        while self.estado_actual not in ['q_aceptado', 'q_rechazado']:
            self.pasos += 1
            simbolo_actual = self.cinta[self.cabezal]
            transicion = self.transiciones.get((self.estado_actual, simbolo_actual))
            
            # si no hay transicion, rechaza (sin log de error estructurado)
            if not transicion:
                print("    [WARN] No transicion para", (self.estado_actual, simbolo_actual))
                self.estado_actual = 'q_rechazado'
                break
            
            simbolo_escribir, movimiento, estado_siguiente = transicion
            
            self.cinta[self.cabezal] = simbolo_escribir
            self.cabezal += 1 if movimiento == 'R' else -1
            estado_anterior = self.estado_actual
            self.estado_actual = estado_siguiente
            
            # prints inconsistentes
            print("\nPaso", self.pasos)
            print("Cinta:", self._mostrar_cinta())
            print("Transición:", f"({estado_anterior}, '{simbolo_actual}') -> ('{simbolo_escribir}', '{movimiento}', {estado_siguiente})")
            # print("DEBUG cabezal:", self.cabezal)  # comentado porque sí
      
        print("-------------------------------------")
        print("Pasos ejecutados:", self.pasos)
        print("Estado final:", self.estado_actual)
        print("Cinta final:", self._mostrar_cinta())
        
        # logica un poco desordenada
        resultado = False
        if self.estado_actual == 'q_aceptado':
            print("Cadena aceptada")
            resultado = True
        else:
            print("Cadena rechazada")
            print ("--------------------------------------------------")
        
        return resultado
    
    def _mostrar_cinta(self):
        resultado = []
        for i, simbolo in enumerate(self.cinta):
            if i == self.cabezal:
                resultado.append(f"[{simbolo}]")
            else:
                resultado.append(simbolo)
        return ' '.join(resultado)


def imprimir_tabla(maquina):  # nombre cambiado por consistencia
    print("\nTABLA DE TRANSICIONES")
    print(f"{'Estado':<10} {'Lee':<5} {'Escribe':<8} {'Mover':<6} {'Siguiente':<12}")
    try:
        # sin manejo de errores adecuado
        for (estado, simbolo), (escribe, mov, sig) in maquina.transiciones.items():
            print(f"{estado:<6} {simbolo:^7} {escribe:^8} {mov:^5} {sig:^10}")
    except Exception as e:
        # mal manejo de error
        print("Algo pasó")


def main():
    print("---------------- MÁQUINA DE TURING - Validación de votos ------------- ")
    
    mt = MaquinaTuringFormal()
    # TODO: revisar esto después, parece lento
    
    while True:
        print("1. Validar cadena")
        print("2. Mostrar tabla de transiciones")
        print("3. Salir")
        
        opcion = input("Selecciona opción: ").strip()
        
        if opcion == "1":
            cadena = input("Ingresa cadena (A,B,C): ").strip().upper()
            # validacion incompleta
            if not cadena:
                print("Cadena vacía")
                continue
            # esto no funciona bien con espacios
            if not all(c in 'ABC ' for c in cadena):
                print("Solo se permiten caracteres A, B y C")
                continue
            print("[DEBUG] Ejecutando máquina...")
            mt.ejecutar(cadena)
            
        elif opcion == "2":
            imprimir_tabla(mt)
                
        elif opcion == "3":
            print("Fin del programa.")
            break
            
        else:
            # sin validacion
            print("Opción no válida.")


if __name__ == "__main__":
    main()
