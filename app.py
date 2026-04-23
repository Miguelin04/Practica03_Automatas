from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

class NFA:
    def __init__(self, states, alphabet, transitions, start_state, accept_states):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.start_state = start_state
        self.accept_states = accept_states

    def simulate(self, sequence):
        # We start at the initial state
        current_states = {self.start_state}
        history = [list(current_states)]
        
        for symbol in sequence:
            next_states = set()
            for state in current_states:
                # Get the set of next states for this (state, symbol) pair
                # Using .get with empty list as default if symbol not in transitions[state]
                transitions_for_state = self.transitions.get(state, {})
                if symbol in transitions_for_state:
                    next_states.update(transitions_for_state[symbol])
                elif 'OTHER' in transitions_for_state:
                    # Fallback to 'OTHER' if defined in the alphabet
                    next_states.update(transitions_for_state['OTHER'])
            
            current_states = next_states
            history.append(list(current_states))
        
        # Check if any of the current states is an accept state
        accepted = bool(current_states.intersection(self.accept_states))
        
        return {
            'accepted': accepted,
            'history': history,
            'final_states': list(current_states)
        }

# Definitions of the 3 NFAs

# Ejercicio 6: Detección de Patrones de Ataque (SYN -> ACK(s) -> RST)
nfa_ids = NFA(
    states=['q0', 'q1', 'q2', 'q3'],
    alphabet=['SYN', 'ACK', 'RST', 'OTHER'],
    transitions={
        'q0': {'SYN': ['q0', 'q1'], 'ACK': ['q0'], 'RST': ['q0'], 'OTHER': ['q0']},
        'q1': {'ACK': ['q2']},
        'q2': {'ACK': ['q2'], 'RST': ['q3']},
        'q3': {'SYN': ['q3'], 'ACK': ['q3'], 'RST': ['q3'], 'OTHER': ['q3']}
    },
    start_state='q0',
    accept_states={'q3'}
)

# Ejercicio 9: Analizador de Comportamiento (HOME -> SEARCH(es) -> CART)
nfa_ecommerce = NFA(
    states=['q0', 'q1', 'q2', 'q3'],
    alphabet=['HOME', 'SEARCH', 'CART', 'OTHER'],
    transitions={
        'q0': {'HOME': ['q0', 'q1'], 'SEARCH': ['q0'], 'CART': ['q0'], 'OTHER': ['q0']},
        'q1': {'SEARCH': ['q2']},
        'q2': {'SEARCH': ['q2'], 'CART': ['q3']},
        'q3': {'HOME': ['q3'], 'SEARCH': ['q3'], 'CART': ['q3'], 'OTHER': ['q3']}
    },
    start_state='q0',
    accept_states={'q3'}
)

# Ejercicio 10: Validación de Sintaxis de Mensajería (@USER -> TEXT -> /CMD)
# We treat @ as mention, TEXT as text, / as command start, CMD as command text
nfa_messaging = NFA(
    states=['q0', 'q1', 'q2', 'q3', 'q4'],
    alphabet=['@', 'TEXT', '/', 'CMD', 'OTHER'],
    transitions={
        'q0': {'@': ['q0', 'q1'], 'TEXT': ['q0'], '/': ['q0'], 'CMD': ['q0'], 'OTHER': ['q0']},
        'q1': {'TEXT': ['q2']},
        'q2': {'/': ['q3'], 'OTHER': ['q2'], 'TEXT': ['q2'], '@': ['q2'], 'CMD': ['q2']},
        'q3': {'CMD': ['q4']},
        'q4': {'@': ['q4'], 'TEXT': ['q4'], '/': ['q4'], 'CMD': ['q4'], 'OTHER': ['q4']}
    },
    start_state='q0',
    accept_states={'q2', 'q4'}
)

nfas = {
    'ids': nfa_ids,
    'ecommerce': nfa_ecommerce,
    'messaging': nfa_messaging
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/simulate', methods=['POST'])
def simulate():
    data = request.json
    nfa_id = data.get('nfa_id')
    sequence = data.get('sequence', [])
    
    if nfa_id not in nfas:
        return jsonify({'error': 'NFA no encontrado'}), 404
        
    nfa = nfas[nfa_id]
    result = nfa.simulate(sequence)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
