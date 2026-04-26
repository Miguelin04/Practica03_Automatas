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
        current_states = {self.start_state}
        history = [list(current_states)]

        for symbol in sequence:
            next_states = set()
            for state in current_states:
                transitions_for_state = self.transitions.get(state, {})
                if symbol in transitions_for_state:
                    next_states.update(transitions_for_state[symbol])
                elif 'OTHER' in transitions_for_state:
                    next_states.update(transitions_for_state['OTHER'])

            current_states = next_states
            history.append(list(current_states))

        accepted = bool(current_states.intersection(self.accept_states))

        return {
            'accepted': accepted,
            'history': history,
            'final_states': list(current_states)
        }


# ─────────────────────────────────────────────
# Ejercicio 2: Sistema de Seguridad IoT
# ─────────────────────────────────────────────
nfa_iot = NFA(
    title="Sistema de Seguridad IoT (Cerradura Inteligente)",
    pattern="Bloqueo tras 3 fallos (AFD)",
    states=['q0', 'q1', 'q2', 'q3'],
    alphabet=['a', 'f'],
    transitions={
        'q0': {'a': ['q0'], 'f': ['q1']},
        'q1': {'a': ['q0'], 'f': ['q2']},
        'q2': {'a': ['q0'], 'f': ['q3']},
        'q3': {'a': ['q3'], 'f': ['q3']}
    },
    start_state='q0',
    accept_states={'q3'}
)

# ─────────────────────────────────────────────
# Ejercicio 4: Orquestación de Pedidos de Logística
# ─────────────────────────────────────────────
nfa_logistics = NFA(
    title="Orquestación de Pedidos de Logística",
    pattern="Flujo de Pedido",
    states=['q0', 'q1', 'q2', 'q3', 'q4', 'q5', 'qE'],
    alphabet=['p', 's', 'd', 'r', 'c'],
    transitions={
        'q0': {'p': ['q1'], 'c': ['q4'], 's': ['qE'], 'd': ['qE'], 'r': ['qE']},
        'q1': {'s': ['q2'], 'c': ['q4'], 'p': ['qE'], 'd': ['qE'], 'r': ['qE']},
        'q2': {'d': ['q3'], 'c': ['q4'], 'p': ['qE'], 's': ['qE'], 'r': ['qE']},
        'q3': {'r': ['q5'], 'p': ['qE'], 's': ['qE'], 'd': ['qE'], 'c': ['qE']},
        'q4': {'p': ['qE'], 's': ['qE'], 'd': ['qE'], 'r': ['qE'], 'c': ['qE']},
        'q5': {'p': ['qE'], 's': ['qE'], 'd': ['qE'], 'r': ['qE'], 'c': ['qE']},
        'qE': {'p': ['qE'], 's': ['qE'], 'd': ['qE'], 'r': ['qE'], 'c': ['qE']}
    },
    start_state='q0',
    accept_states={'q3'}
)

# ─────────────────────────────────────────────
# Ejercicio 5: Protocolo de Handshake
# ─────────────────────────────────────────────
nfa_handshake = NFA(
    title="Protocolo de Handshake (Sincronización)",
    pattern="SYN -> SYN-ACK -> ACK",
    states=['q0', 'q1', 'q2', 'q3', 'qE'],
    alphabet=['s', 's_a', 'a', 'e'],
    transitions={
        'q0': {'s': ['q1'], 's_a': ['qE'], 'a': ['qE'], 'e': ['qE']},
        'q1': {'s_a': ['q2'], 's': ['qE'], 'a': ['qE'], 'e': ['qE']},
        'q2': {'a': ['q3'], 's': ['qE'], 's_a': ['qE'], 'e': ['qE']},
        'q3': {'e': ['qE'], 's': ['q3'], 's_a': ['q3'], 'a': ['q3']},
        'qE': {'s': ['qE'], 's_a': ['qE'], 'a': ['qE'], 'e': ['qE']}
    },
    start_state='q0',
    accept_states={'q3'}
)

# ─────────────────────────────────────────────
# Ejercicio 6: Detección de Patrones de Ataque (IDS)
# ─────────────────────────────────────────────
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

# ─────────────────────────────────────────────
# Ejercicio 9: Analizador de Comportamiento E-commerce
# ─────────────────────────────────────────────
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

# ─────────────────────────────────────────────
# Ejercicio 10: Validación de Sintaxis de Mensajería
# ─────────────────────────────────────────────
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

# ─────────────────────────────────────────────
# Registry – todos los 6 NFAs disponibles
# ─────────────────────────────────────────────
nfas = {
    'iot':       nfa_iot,
    'logistics': nfa_logistics,
    'handshake': nfa_handshake,
    'ids':       nfa_ids,
    'ecommerce': nfa_ecommerce,
    'messaging': nfa_messaging,
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
        is_start  = (s == nfa.start_state)
        is_accept = (s in nfa.accept_states)

        color = '#1e293b'
        border_colors = {
            'iot':       '#f59e0b',
            'logistics': '#f59e0b',
            'handshake': '#f59e0b',
            'ids':       '#3b82f6',
            'ecommerce': '#8b5cf6',
            'messaging': '#ec4899',
        }
        border = border_colors.get(nfa_id, '#3b82f6')
        borderWidth = 1

        if is_accept:
            border = '#10b981'
            borderWidth = 3

        label_suffix = 'Inicio' if is_start else 'Aceptado' if is_accept else ''
        node_label = f"{s}\n({label_suffix})" if label_suffix else s

        if nfa_id == 'logistics':
            desc = {
                'q0': 'CREADO', 'q1': 'EMPAQUETADO', 'q2': 'ENVIADO',
                'q3': 'ENTREGADO', 'q4': 'CANCELADO', 'q5': 'DEVUELTO', 'qE': 'Error'
            }.get(s, '')
            if desc:
                node_label = f"{s}\n{desc}" if not label_suffix else f"{s}\n{desc}\n({label_suffix})"

        if nfa_id == 'handshake':
            desc = {'q1': 'SYN', 'q2': 'SYN_ACK', 'q3': 'ACK'}.get(s, '')
            if desc:
                node_label = f"{s}\n{desc}" if not label_suffix else f"{s}\n{desc}\n({label_suffix})"

        level = nfa.states.index(s)

        nodes.append({
            'id': s,
            'label': node_label,
            'color': {'background': color, 'border': border},
            'borderWidth': borderWidth,
            'font': {'color': 'white'},
            'level': level
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
        label = ", ".join(symbols) if len(symbols) > 1 else symbols[0]
        edges.append({
            'from': s_from,
            'to': s_to,
            'label': label,
            'selfReferenceSize': 25 if s_from == s_to else None,
            'font': {'align': 'horizontal'}
        })

    return jsonify({
        'title':        nfa.title,
        'pattern':      nfa.pattern,
        'states':       nfa.states,
        'alphabet':     nfa.alphabet,
        'start_state':  nfa.start_state,
        'accept_states': list(nfa.accept_states),
        'transitions':  nfa.transitions,
        'nodes':        nodes,
        'edges':        edges
    })


if __name__ == '__main__':
    app.run(debug=True, port=5002)
