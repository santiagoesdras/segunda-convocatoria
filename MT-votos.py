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
