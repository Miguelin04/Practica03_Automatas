from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

class NFA:
    def __init__(self, title, pattern, states, alphabet, transitions, start_state, accept_states):
        self.title = title              # Nombre descriptivo del ejercicio
        self.pattern = pattern          # Patrón que el autómata reconoce
        self.states = states            # Q  → Conjunto de estados
        self.alphabet = alphabet        # Σ  → Alfabeto (símbolos de entrada válidos)
        self.transitions = transitions  # δ  → Función de transición (dict de dicts)
        self.start_state = start_state  # q0 → Estado inicial
        self.accept_states = accept_states  # F → Conjunto de estados de aceptación

    def simulate(self, sequence):
        
        # Paso 1: Inicializar con el estado inicial dentro de un conjunto (set)
        current_states = {self.start_state}

        # Guardamos el historial de estados para poder visualizar paso a paso
        history = [list(current_states)]

        # Paso 2: Procesar cada símbolo de la secuencia de entrada
        for symbol in sequence:
            # Conjunto vacío que acumulará los estados destino de este paso
            next_states = set()

            # Recorremos TODOS los estados activos actuales
            for state in current_states:
                # Obtener las transiciones disponibles desde este estado
                transitions_for_state = self.transitions.get(state, {})

                if symbol in transitions_for_state:
                    # Si existe transición para este símbolo, agregar TODOS los destinos
                    # AFD: update(['q1'])       → agrega 1 estado
                    # AFND: update(['q0','q1']) → agrega 2 estados (NO DETERMINISMO)
                    next_states.update(transitions_for_state[symbol])

                elif 'OTHER' in transitions_for_state:
                    # Transición comodín: si el símbolo no tiene transición específica,
                    next_states.update(transitions_for_state['OTHER'])

                # Si no hay transición ni comodín → esa rama "muere" (no agrega nada)
                
            # Reemplazar los estados activos con los nuevos estados destino
            current_states = next_states
            history.append(list(current_states))

        # Paso 3: Verificar aceptación
        accepted = bool(current_states.intersection(self.accept_states))

        return {
            'accepted': accepted,               # True/False → ¿cadena aceptada?
            'history': history,                  # Lista de estados en cada paso
            'final_states': list(current_states) # Estados donde terminó el autómata
        }

# ─────────────────────────────────────────────
# Ejercicio 2: Sistema de Seguridad IoT  [AFD]
# ─────────────────────────────────────────────
nfa_iot = NFA(
    title="Sistema de Seguridad IoT (Cerradura Inteligente)",
    pattern="Bloqueo tras 3 fallos (AFD)",
    states=['q0', 'q1', 'q2', 'q3'],        # Q = 4 estados
    alphabet=['a', 'f'],                      # Σ = {a: acceso OK, f: fallo}
    transitions={
        #        'a' → reinicia    'f' → acumula fallo
        'q0': {'a': ['q0'], 'f': ['q1']},     # 0 fallos: fallo → 1 fallo
        'q1': {'a': ['q0'], 'f': ['q2']},     # 1 fallo:  fallo → 2 fallos
        'q2': {'a': ['q0'], 'f': ['q3']},     # 2 fallos: fallo → BLOQUEADO
        'q3': {'a': ['q3'], 'f': ['q3']}      # BLOQUEADO: estado trampa, no sale
        # ↑ Cada transición va a UN solo estado → es AFD
    },
    start_state='q0',
    accept_states={'q3'}  # F = {q3} → se acepta cuando se bloquea
)

# ─────────────────────────────────────────────
# Ejercicio 4: Orquestación de Pedidos de Logística  [AFD]
# ─────────────────────────────────────────────
nfa_logistics = NFA(
    title="Orquestación de Pedidos de Logística",
    pattern="Flujo de Pedido",
    states=['q0', 'q1', 'q2', 'q3', 'q4', 'q5', 'qE'],  # Q = 7 estados
    alphabet=['p', 's', 'd', 'r', 'c'],
    # p=pedido, s=empaquetado(stock), d=despacho, r=retorno, c=cancelar
    transitions={
        #        Acción válida           Acciones inválidas → Error
        'q0': {'p': ['q1'], 'c': ['q4'], 's': ['qE'], 'd': ['qE'], 'r': ['qE']},
        'q1': {'s': ['q2'], 'c': ['q4'], 'p': ['qE'], 'd': ['qE'], 'r': ['qE']},
        'q2': {'d': ['q3'], 'c': ['q4'], 'p': ['qE'], 's': ['qE'], 'r': ['qE']},
        'q3': {'r': ['q5'], 'p': ['qE'], 's': ['qE'], 'd': ['qE'], 'c': ['qE']},
        'q4': {'p': ['qE'], 's': ['qE'], 'd': ['qE'], 'r': ['qE'], 'c': ['qE']},
        'q5': {'p': ['qE'], 's': ['qE'], 'd': ['qE'], 'r': ['qE'], 'c': ['qE']},
        'qE': {'p': ['qE'], 's': ['qE'], 'd': ['qE'], 'r': ['qE'], 'c': ['qE']}
        # ↑ Cada transición va a UN solo estado → es AFD
        # qE es un estado trampa: una vez en error, no se puede recuperar
    },
    start_state='q0',
    accept_states={'q3'}  # F = {q3} → se acepta solo si se entregó correctamente
)

# ─────────────────────────────────────────────
# Ejercicio 5: Protocolo de Handshake TCP  [AFD]
# ─────────────────────────────────────────────
nfa_handshake = NFA(
    title="Protocolo de Handshake (Sincronización)",
    pattern="SYN -> SYN-ACK -> ACK",
    states=['q0', 'q1', 'q2', 'q3', 'qE'],  # Q = 5 estados
    alphabet=['s', 's_a', 'a', 'e'],
    # s=SYN, s_a=SYN-ACK, a=ACK, e=error/desconexión
    transitions={
        'q0': {'s': ['q1'], 's_a': ['qE'], 'a': ['qE'], 'e': ['qE']},   # Solo acepta SYN
        'q1': {'s_a': ['q2'], 's': ['qE'], 'a': ['qE'], 'e': ['qE']},   # Solo acepta SYN-ACK
        'q2': {'a': ['q3'], 's': ['qE'], 's_a': ['qE'], 'e': ['qE']},   # Solo acepta ACK
        'q3': {'e': ['qE'], 's': ['q3'], 's_a': ['q3'], 'a': ['q3']},   # Conexión OK
        'qE': {'s': ['qE'], 's_a': ['qE'], 'a': ['qE'], 'e': ['qE']}    # Trampa
        # ↑ Cada transición va a UN solo estado → es AFD
    },
    start_state='q0',
    accept_states={'q3'}  # F = {q3} → handshake completado exitosamente
)


# ═══════════════════════════════════════════════════════════════════
# A PARTIR DE AQUÍ: AUTÓMATAS NO DETERMINISTAS (AFND)
# La diferencia clave: alguna transición apunta a MÚLTIPLES estados
# Esto permite detectar patrones en medio de tráfico arbitrario
# ═══════════════════════════════════════════════════════════════════


# ─────────────────────────────────────────────
# Ejercicio 6: Detección de Patrones de Ataque (IDS)  [AFND]
# ─────────────────────────────────────────────
nfa_ids = NFA(
    title="Detección de Patrones de Ataque (IDS)",
    pattern="SYN -> ACK(s) -> RST",
    states=['q0', 'q1', 'q2', 'q3'],   # Q = 4 estados
    alphabet=['SYN', 'ACK', 'RST', 'OTHER'],
    transitions={
        
        'q0': {'SYN': ['q0', 'q1'], 'ACK': ['q0'], 'RST': ['q0'], 'OTHER': ['q0']},
        'q1': {'ACK': ['q2']},                    # Esperando ACK después de SYN
        'q2': {'ACK': ['q2'], 'RST': ['q3']},     # ACKs repetidos permitidos, RST completa ataque
        'q3': {'SYN': ['q3'], 'ACK': ['q3'], 'RST': ['q3'], 'OTHER': ['q3']}  # Ataque detectado
        # Nota: q1 y q2 NO tienen transición para todos los símbolos
        # → si llega un símbolo inesperado, esa rama simplemente MUERE
        # → esto es legal en AFND (a diferencia de un AFD)
    },
    start_state='q0',
    accept_states={'q3'}  # F = {q3} → patrón de ataque encontrado
)

# ─────────────────────────────────────────────
# Ejercicio 9: Analizador de Comportamiento E-commerce  [AFND]
# ─────────────────────────────────────────────
nfa_ecommerce = NFA(
    title="Analizador de Comportamiento (E-commerce)",
    pattern="HOME -> SEARCH(es) -> CART",
    states=['q0', 'q1', 'q2', 'q3'],   # Q = 4 estados
    alphabet=['HOME', 'SEARCH', 'CART', 'OTHER'],
    transitions={
        # ⚡ NO DETERMINISMO: 'HOME': ['q0', 'q1']
        # Al visitar HOME, bifurca: sigue monitoreando Y empieza seguimiento
        'q0': {'HOME': ['q0', 'q1'], 'SEARCH': ['q0'], 'CART': ['q0'], 'OTHER': ['q0']},
        'q1': {'SEARCH': ['q2'], 'OTHER': ['q1']},            # Esperando búsqueda
        'q2': {'SEARCH': ['q2'], 'CART': ['q3'], 'OTHER': ['q2']},  # Búsquedas múltiples OK
        'q3': {'HOME': ['q3'], 'SEARCH': ['q3'], 'CART': ['q3'], 'OTHER': ['q3']}  # Compra detectada
    },
    start_state='q0',
    accept_states={'q3'}  # F = {q3} → sesión de compra confirmada
)

# ─────────────────────────────────────────────
# Ejercicio 10: Validación de Sintaxis de Mensajería  [AFND]
# ─────────────────────────────────────────────
nfa_messaging = NFA(
    title="Validación de Sintaxis de Mensajería",
    pattern="@bot (USER)? (!cmd | ?help)",
    states=['q0', 'q1', 'q2', 'q3'],   # Q = 4 estados
    alphabet=['@bot', 'USER', '!cmd', '?help', 'OTHER'],
    transitions={
        # ⚡ NO DETERMINISMO: '@bot': ['q0', 'q1']
        # Al detectar @bot, bifurca: sigue monitoreando Y empieza validación
        'q0': {'@bot': ['q0', 'q1'], 'USER': ['q0'], '!cmd': ['q0'], '?help': ['q0'], 'OTHER': ['q0']},
        'q1': {'USER': ['q2'], '!cmd': ['q3'], '?help': ['q3']},  # USER es opcional
        'q2': {'!cmd': ['q3'], '?help': ['q3']},                   # Después de USER, espera comando
        'q3': {'@bot': ['q3'], 'USER': ['q3'], '!cmd': ['q3'], '?help': ['q3'], 'OTHER': ['q3']}
    },
    start_state='q0',
    accept_states={'q3'}  # F = {q3} → comando válido detectado
)
# ─────────────────────────────────────────────
# Registro de todos los autómatas disponibles
# ─────────────────────────────────────────────
nfas = {
    'iot':       nfa_iot,        # AFD  – Ejercicio 2
    'logistics': nfa_logistics,  # AFD  – Ejercicio 4
    'handshake': nfa_handshake,  # AFD  – Ejercicio 5
    'ids':       nfa_ids,        # AFND – Ejercicio 6
    'ecommerce': nfa_ecommerce,  # AFND – Ejercicio 9
    'messaging': nfa_messaging,  # AFND – Ejercicio 10
}


# ═══════════════════════════════════════════════════════════════
# RUTAS DE LA API REST (Flask)
# El frontend (HTML/JS) se comunica con estas rutas
# ═══════════════════════════════════════════════════════════════


@app.route('/')
def index():
    """Ruta principal – Sirve la página HTML del simulador"""
    return render_template('index.html')


@app.route('/api/simulate', methods=['POST'])
def simulate():
    """
    API POST /api/simulate
    Recibe: { "nfa_id": "ids", "sequence": ["SYN", "ACK", "RST"] }
    Retorna: { "accepted": true, "history": [...], "final_states": [...] }

    El frontend envía el ID del autómata y la cadena a evaluar.
    El backend ejecuta simulate() y devuelve el resultado como JSON.
    """
    data = request.json                     # Leer el JSON del cuerpo de la petición
    nfa_id = data.get('nfa_id')             # ¿Qué autómata usar? (ej: 'ids')
    sequence = data.get('sequence', [])     # ¿Qué cadena evaluar? (ej: ['SYN','ACK'])

    if nfa_id not in nfas:
        return jsonify({'error': 'NFA no encontrado'}), 404

    nfa = nfas[nfa_id]                      # Obtener el autómata del registro
    result = nfa.simulate(sequence)         # Ejecutar la simulación
    return jsonify(result)                  # Devolver resultado como JSON


@app.route('/api/nfa/<nfa_id>', methods=['GET'])
def get_nfa(nfa_id):
    """
    API GET /api/nfa/<nfa_id>
    Retorna la definición formal del autómata + datos para Vis.js

    Esta ruta serializa el autómata en formato JSON para que el frontend
    pueda dibujar el diagrama de transiciones con la librería Vis.js.
    Genera dos listas: nodos (estados) y aristas (transiciones).
    """
    if nfa_id not in nfas:
        return jsonify({'error': 'NFA no encontrado'}), 404
    nfa = nfas[nfa_id]

    # ── Construir la lista de NODOS para Vis.js ──
    # Cada estado del autómata se convierte en un nodo visual
    nodes = []
    for s in nfa.states:
        is_start  = (s == nfa.start_state)      # ¿Es el estado inicial?
        is_accept = (s in nfa.accept_states)     # ¿Es un estado de aceptación?

        # Color de fondo oscuro para todos los nodos
        color = '#1e293b'

        # Color del borde según el tipo de ejercicio
        border_colors = {
            'iot':       '#f59e0b',   # Ámbar para los AFD
            'logistics': '#f59e0b',
            'handshake': '#f59e0b',
            'ids':       '#3b82f6',   # Azul para IDS
            'ecommerce': '#8b5cf6',   # Violeta para E-commerce
            'messaging': '#ec4899',   # Rosa para Mensajería
        }
        border = border_colors.get(nfa_id, '#3b82f6')
        borderWidth = 1

        # Los estados de aceptación tienen borde verde grueso
        if is_accept:
            border = '#10b981'
            borderWidth = 3

        # Construir la etiqueta del nodo (ej: "q0\n(Inicio)")
        label_suffix = 'Inicio' if is_start else 'Aceptado' if is_accept else ''
        node_label = f"{s}\n({label_suffix})" if label_suffix else s

        # Etiquetas descriptivas para Logística (ej: "q1\nEMPAQUETADO")
        if nfa_id == 'logistics':
            desc = {
                'q0': 'CREADO', 'q1': 'EMPAQUETADO', 'q2': 'ENVIADO',
                'q3': 'ENTREGADO', 'q4': 'CANCELADO', 'q5': 'DEVUELTO', 'qE': 'Error'
            }.get(s, '')
            if desc:
                node_label = f"{s}\n{desc}" if not label_suffix else f"{s}\n{desc}\n({label_suffix})"

        # Etiquetas descriptivas para Handshake (ej: "q1\nSYN")
        if nfa_id == 'handshake':
            desc = {'q1': 'SYN', 'q2': 'SYN_ACK', 'q3': 'ACK'}.get(s, '')
            if desc:
                node_label = f"{s}\n{desc}" if not label_suffix else f"{s}\n{desc}\n({label_suffix})"

        # 'level' define la posición vertical del nodo en el diagrama
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
                edge_key = (s_from, s_to)         # Clave: par (origen, destino)
                if edge_key not in edges_map:
                    edges_map[edge_key] = []
                edges_map[edge_key].append(symbol)  # Acumular símbolos en esa arista

    # Convertir el mapa de aristas a la lista que Vis.js necesita
    edges = []
    for (s_from, s_to), symbols in edges_map.items():
        label = ", ".join(symbols) if len(symbols) > 1 else symbols[0]
        edges.append({
            'from': s_from,
            'to': s_to,
            'label': label,
            'selfReferenceSize': 25 if s_from == s_to else None,  # Loops se dibujan más grandes
            'font': {'align': 'horizontal'}
        })

    # Retornar toda la información al frontend como JSON
    return jsonify({
        'title':        nfa.title,
        'pattern':      nfa.pattern,
        'states':       nfa.states,
        'alphabet':     nfa.alphabet,
        'start_state':  nfa.start_state,
        'accept_states': list(nfa.accept_states),
        'transitions':  nfa.transitions,
        'nodes':        nodes,   # Lista de nodos para Vis.js
        'edges':        edges    # Lista de aristas para Vis.js
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
