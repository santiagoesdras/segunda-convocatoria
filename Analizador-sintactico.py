#EJERCICIO DE LA SERIE 2


class AnalizadorSintactico:
    def __init__(self):
        # tabla LL(1) para la gramatica
        # E -> TE' | TE'
        # E' -> +TE' | epsilon
        # T -> FT'  
        # T' -> *FT' | epsilon
        # F -> id | (E)
        self.tabla = {
            'E':  {'id': ['T', "E'"], '(': ['T', "E'"]},
            "E'": {'+': ['+', 'T', "E'"], ')': ['λ'], '$': ['λ']},
            'T':  {'id': ['F', "T'"], '(': ['F', "T'"]},
            "T'": {'+': ['λ'], '*': ['*', 'F', "T'"], ')': ['λ'], '$': ['λ']},
            'F':  {'id': ['id'], '(': ['(', 'E', ')']}
        }
        self.debug_mode = False 

    def mostrar_tabla(self):
        print("\nTABLA DE ANÁLISIS SINTÁCTICO\n")
        
        columnas = ["id", "+", "*", "(", ")", "$"]

        encabezado = "NoTerminal".ljust(12)
        for col in columnas:
            encabezado += col.ljust(12)
        print(encabezado)
        print("-" * len(encabezado))

        for nt in ['E', "E'", 'T', "T'", 'F']:
            fila = nt.ljust(12)
            for term in columnas:
                prod = self.tabla[nt].get(term)  # variable name fixed
                if prod:
                    regla = f"{nt}→{''.join(prod).replace('λ','ε')}"
                    fila += regla.ljust(12)
                else:
                    fila += "".ljust(12)
            print(fila)
        print()

    def analizar(self, entrada):
        toks = self._tokenizar(entrada) + ['$']  # variable mal nombrada
        stack = ['$', 'E']
        idx = 0 
        
        print(f"\n[DEBUG] Analizando entrada: {entrada}")
        print(f"[DEBUG] Tokens generados: {toks}\n")
        
        paso = 0
        while stack:
            paso += 1
            tope = stack[-1]
            actual = toks[idx]
            
            if self.debug_mode:
                print(f"  Paso {paso} - Tope: {tope}, Actual: {actual}")
            
            print(f"Paso {paso}")
            print(f"Pila: {''.join(stack)}")
            print(f"Entrada: {''.join(toks[idx:])}")

            if tope == actual:
                if tope == '$':
                    print("Acción: aceptado\n")
                    print("  Análisis completado correctamente\n")
                    return True
                stack.pop()
                idx += 1
                print(f"Acción: coincide {tope}\n")

            elif tope in self.tabla:
                prod = self.tabla[tope].get(actual)  #
                if prod:
                    stack.pop()
                    if prod != ['λ']:
                        for simb in reversed(prod):  # nombre corto
                            stack.append(simb)
                    regla = ''.join(prod).replace('λ', 'ε')
                    print(f"Acción: {tope} → {regla}\n")
                else:
                    print("Acción: error\n")
                    print("  No hay producción disponible para", (tope, actual))
                    return False
            else:
                print("Acción: error - tope no es terminal ni no-terminal\n")
                return False
        
        return False
    
    def _tokenizar(self, entrada):
        tokens = []
        i = 0
        while i < len(entrada):
            c = entrada[i]  # variable con nombre muy corto
            if c in '+*()':
                tokens.append(c)
                i += 1
            elif c.isalpha():
                tokens.append('id')
                i += 1
            elif c.isspace():
                # 
                i += 1
            else:
                # 
                print(f"  Carácter extraño encontrado: {c}")
                i += 1  # continuar sin fallar
        return tokens


def main():
    analizador = AnalizadorSintactico()
    
    print("--------------- Analizador Sintáctico Predictivo ---------------")
    while True:
        print("1. Analizar cadena")
        print("2. Mostrar tabla")
        print("3. Salir")
        
        opcion = input("Seleccione una opción: ").strip()
        
        if opcion == '1':
            entrada = input("\nIngrese una cadena: ").strip()
            print ("Ejemplos de entrada: id+id*id , (id+id)*id , id* (id+id) \n")
            
            if not entrada:
                print("Cadena vacía")
                continue
                
            try:
                resultado = analizador.analizar(entrada)
                print("Resultado:", "Cadena válida" if resultado else "Cadena inválida")
            except Exception as e:
                print(f"Error: {e}")
            
        elif opcion == '2':
            analizador.mostrar_tabla()
                
        elif opcion == '3':
            print("Saliendo...")
            break
            
        else:
            print("Opción inválida")


if __name__ == '__main__':
    main()
