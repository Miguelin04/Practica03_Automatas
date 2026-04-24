from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

class NFA:
    def __init__(self, title, pattern, states, alphabet, transitions, start_state, accept_states):
        self.title = title
        self.pattern = pattern
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
    title="Detección de Patrones de Ataque (IDS)",
    pattern="SYN -> ACK(s) -> RST",
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
    title="Analizador de Comportamiento (E-commerce)",
    pattern="HOME -> SEARCH(es) -> CART",
    states=['q0', 'q1', 'q2', 'q3'],
    alphabet=['HOME', 'SEARCH', 'CART', 'OTHER'],
    transitions={
        'q0': {'HOME': ['q0', 'q1'], 'SEARCH': ['q0'], 'CART': ['q0'], 'OTHER': ['q0']},
        'q1': {'SEARCH': ['q2'], 'OTHER': ['q1']},
        'q2': {'SEARCH': ['q2'], 'CART': ['q3'], 'OTHER': ['q2']},
        'q3': {'HOME': ['q3'], 'SEARCH': ['q3'], 'CART': ['q3'], 'OTHER': ['q3']}
    },
    start_state='q0',
    accept_states={'q3'}
)

# Ejercicio 10: Validación de Sintaxis de Mensajería
nfa_messaging = NFA(
    title="Validación de Sintaxis de Mensajería",
    pattern="@bot (USER)? (!cmd | ?help)",
    states=['q0', 'q1', 'q2', 'q3'],
    alphabet=['@bot', 'USER', '!cmd', '?help', 'OTHER'],
    transitions={
        'q0': {'@bot': ['q0', 'q1'], 'USER': ['q0'], '!cmd': ['q0'], '?help': ['q0'], 'OTHER': ['q0']},
        'q1': {'USER': ['q2'], '!cmd': ['q3'], '?help': ['q3']},
        'q2': {'!cmd': ['q3'], '?help': ['q3']},
        'q3': {'@bot': ['q3'], 'USER': ['q3'], '!cmd': ['q3'], '?help': ['q3'], 'OTHER': ['q3']}
    },
    start_state='q0',
    accept_states={'q3'}
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

@app.route('/api/nfa/<nfa_id>', methods=['GET'])
def get_nfa(nfa_id):
    if nfa_id not in nfas:
        return jsonify({'error': 'NFA no encontrado'}), 404
    nfa = nfas[nfa_id]
    
    nodes = []
    for s in nfa.states:
        is_start = (s == nfa.start_state)
        is_accept = (s in nfa.accept_states)
        
        color = '#1e293b'
        # Default border based on NFA ID just for aesthetics
        border = '#3b82f6' if nfa_id == 'ids' else '#8b5cf6' if nfa_id == 'ecommerce' else '#f59e0b'
        borderWidth = 1
        
        if is_accept:
            border = '#10b981'
            borderWidth = 3
            
        label_suffix = 'Inicio' if is_start else 'Aceptado' if is_accept else ''
        node_label = f"{s}\n({label_suffix})" if label_suffix else s
        
        nodes.append({
            'id': s,
            'label': node_label,
            'color': {'background': color, 'border': border},
            'borderWidth': borderWidth,
            'font': {'color': 'white'}
        })
        
    edges_map = {}
    for s_from, trans in nfa.transitions.items():
        for symbol, states_to in trans.items():
            for s_to in states_to:
                edge_key = (s_from, s_to)
                if edge_key not in edges_map:
                    edges_map[edge_key] = []
                edges_map[edge_key].append(symbol)
                
    edges = []
    for (s_from, s_to), symbols in edges_map.items():
        # group symbols with a comma and space instead of newline to avoid vertical overlap
        label = ", ".join(symbols) if len(symbols) > 1 else symbols[0]
        edges.append({
            'from': s_from,
            'to': s_to,
            'label': label,
            'selfReferenceSize': 25 if s_from == s_to else None,
            'font': {'align': 'horizontal'}
        })
        
    return jsonify({
        'title': nfa.title,
        'pattern': nfa.pattern,
        'states': nfa.states,
        'alphabet': nfa.alphabet,
        'start_state': nfa.start_state,
        'accept_states': list(nfa.accept_states),
        'transitions': nfa.transitions,
        'nodes': nodes,
        'edges': edges
    })

if __name__ == '__main__':
    app.run(debug=True, port=5002)
