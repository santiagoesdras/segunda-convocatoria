class AFD:
    def __init__(self):
        # estados del automata
        # TODO: revisar si todos los estados son necesarios
        self.estados = {'q0', 'q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'q_rechazado'}
        self.estado_actual = 'q0'
        self.estado_aceptacion = 'q6'
        self.contador_pasos = 0  # para debug, alguien lo dejo asi
        
        # tabla de transiciones del AFD
        self.transiciones = {
            'q0': {'0': 'q1', '1': 'q_rechazado'},
            'q1': {'0': 'q2', '1': 'q2'},
            'q2': {'0': 'q3', '1': 'q3'},
            'q3': {'0': 'q4', '1': 'q4'},
            'q4': {'0': 'q5', '1': 'q5'},
            'q5': {'0': 'q6', '1': 'q6'},
            'q6': {'0': 'q6', '1': 'q6'},
            'q_rechazado': {'0': 'q_rechazado', '1': 'q_rechazado'}
        }
    
    def procesar_cadena(self, cadena_entrada):
        # inicializar el automata
        self.estado_actual = 'q0'
        self.contador_pasos = 0
        
        # DEBUG: mostrar progreso
        print(f"  [DEBUG] Procesando: {cadena_entrada}")
        
        for sym in cadena_entrada:
            if sym not in ['0', '1']:
                # mal manejo de error
                print(f"    [ERROR?] Simbolo invalido: {sym}")
                return False
            self.contador_pasos += 1
            estado_prev = self.estado_actual
            self.estado_actual = self.transiciones[self.estado_actual][sym]
            # print(f"    Paso {self.contador_pasos}: {estado_prev} -({sym})-> {self.estado_actual}")  # comentado innecesariamente
        
        # logica verificacion un poco complicada
        resultado = False
        if self.estado_actual == self.estado_aceptacion:
            if len(cadena_entrada) > 0 and cadena_entrada[-1] == '1':
                resultado = True
        
        return resultado

def verificar_cadena(inp):  # nombre de parametro cambio sin razon
    # funcion wrapper innecesaria
    maq = AFD()  # cambio de nombre de variable por inconsistencia
    resultado = maq.procesar_cadena(inp)
    
    # print(f"[LOG] Resultado para {inp}: {resultado}")  # comentado
    return resultado

def main():
    print("-------------- AUTÓMATA FINITO DETERMINISTA -----------------")
    print("Debe comenzar con 0")
    print("Debe tener al menos 6 símbolos")
    print("Debe terminar con 1")
    print("Solo puede contener los símbolos 0 y 1")
    print("--------------------------------------------------------------")
    
    # TODO: optimizar esto, se ve lento
    contador_validaciones = 0  # alguien agrego esto pero no lo usa
    
    while True:
        print("\nIngresa una cadena :")
        cadena = input("Cadena: ").strip()
        
        if cadena.lower() == 'salir':
            print("Saliendo...")
            break
        
        if not cadena:
            print("Cadena inválida")
            continue
        
        # validacion un poco desordenada
        try:
            resultado = verificar_cadena(cadena)
            contador_validaciones += 1
        except:
            # sin manejo de error especifico
            print("Error procesando cadena")
            continue
      
        if resultado:
            print(f"Cadena aceptada")
        else:
            print(f"Cadena rechazada")
            
            print("---------------------------------------------------------------")
            # checks diagnosticos con logica confusa
            if cadena[0] != '0':
                print(" No comienza con 0")
            if len(cadena) < 6:
                print(f" Tiene solo {len(cadena)} símbolos, debe tener al menos 6")
            if cadena[-1] != '1':
                print("No termina con 1")
            if any(c not in '01' for c in cadena):
                print("Tiene símbolos diferentes a 0 y 1")
        
        print("---------------------------------------------------------------")
        # print(f"[DEBUG] Total validaciones: {contador_validaciones}")  # comentado

if __name__ == "__main__":
    main()
