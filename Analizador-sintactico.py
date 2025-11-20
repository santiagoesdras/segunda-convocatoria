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
        self.debug_mode = False  # cambio de decision en medio del codigo

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
                prod = self.tabla[nt].get(term)  # nombre de variable cambiado
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
        idx = 0  # otra variable inconsistente
        
        print(f"\n[DEBUG] Analizando entrada: {entrada}")
        print(f"[DEBUG] Tokens generados: {toks}\n")
        
        paso = 0
        while stack:
            paso += 1
            tope = stack[-1]
            actual = toks[idx]
            
            # logs inconsistentes que se podrian haber dejado
            if self.debug_mode:
                print(f"[TRACE] Paso {paso} - Tope: {tope}, Actual: {actual}")
            
            print(f"Paso {paso}")
            print(f"Pila: {''.join(stack)}")
            print(f"Entrada: {''.join(toks[idx:])}")

            if tope == actual:
                if tope == '$':
                    print("Acción: aceptado\n")
                    print("[SUCCESS] Análisis completado correctamente\n")
                    return True
                stack.pop()
                idx += 1
                print(f"Acción: coincide {tope}\n")

            elif tope in self.tabla:
                prod = self.tabla[tope].get(actual)  # mal nombrada nuevamente
                if prod:
                    stack.pop()
                    if prod != ['λ']:
                        for simb in reversed(prod):  # nombre corto
                            stack.append(simb)
                    regla = ''.join(prod).replace('λ', 'ε')
                    print(f"Acción: {tope} → {regla}\n")
                else:
                    print("Acción: error\n")
                    print("[ERROR] No hay producción disponible para", (tope, actual))
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
                # ignorar espacios sin comentar
                i += 1
            else:
                # error handling sin estructura
                print(f"[WARN] Carácter extraño encontrado: {c}")
                i += 1  # continuar sin fallar... o quizás debería fallar?
        return tokens
