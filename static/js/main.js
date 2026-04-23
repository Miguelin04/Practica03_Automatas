// Definiciones de los AFNDs
const nfaConfigs = {
    ids: {
        title: "Detección de Patrones de Ataque (IDS)",
        formal: `
            <div class="def-item"><strong>Q:</strong> {q0, q1, q2, q3}</div>
            <div class="def-item"><strong>Σ:</strong> {SYN, ACK, RST, OTHER}</div>
            <div class="def-item"><strong>q0:</strong> q0</div>
            <div class="def-item"><strong>F:</strong> {q3}</div>
            <div class="def-item"><strong>Patrón:</strong> SYN -> ACK(s) -> RST</div>
        `,
        alphabet: ['SYN', 'ACK', 'RST', 'OTHER'],
        nodes: [
            { id: 'q0', label: 'q0\n(Inicio)', x: -200, y: 0, color: { background: '#1e293b', border: '#3b82f6' }, font: { color: 'white' } },
            { id: 'q1', label: 'q1\n(SYN)', x: -50, y: 0, color: { background: '#1e293b', border: '#3b82f6' }, font: { color: 'white' } },
            { id: 'q2', label: 'q2\n(ACK)', x: 100, y: 0, color: { background: '#1e293b', border: '#3b82f6' }, font: { color: 'white' } },
            { id: 'q3', label: 'q3\n(Aceptado)', x: 250, y: 0, color: { background: '#1e293b', border: '#10b981' }, borderWidth: 3, font: { color: 'white' } }
        ],
        edges: [
            { from: 'q0', to: 'q0', label: 'Σ', selfReferenceSize: 20 },
            { from: 'q0', to: 'q1', label: 'SYN' },
            { from: 'q1', to: 'q2', label: 'ACK' },
            { from: 'q2', to: 'q2', label: 'ACK', selfReferenceSize: 20 },
            { from: 'q2', to: 'q3', label: 'RST' },
            { from: 'q3', to: 'q3', label: 'Σ', selfReferenceSize: 20 }
        ]
    },
    ecommerce: {
        title: "Analizador de Comportamiento (E-commerce)",
        formal: `
            <div class="def-item"><strong>Q:</strong> {q0, q1, q2, q3}</div>
            <div class="def-item"><strong>Σ:</strong> {HOME, SEARCH, CART, OTHER}</div>
            <div class="def-item"><strong>q0:</strong> q0</div>
            <div class="def-item"><strong>F:</strong> {q3}</div>
            <div class="def-item"><strong>Patrón:</strong> HOME -> SEARCH(es) -> CART</div>
        `,
        alphabet: ['HOME', 'SEARCH', 'CART', 'OTHER'],
        nodes: [
            { id: 'q0', label: 'q0\n(Inicio)', x: -200, y: 0, color: { background: '#1e293b', border: '#8b5cf6' }, font: { color: 'white' } },
            { id: 'q1', label: 'q1\n(Home)', x: -50, y: 0, color: { background: '#1e293b', border: '#8b5cf6' }, font: { color: 'white' } },
            { id: 'q2', label: 'q2\n(Search)', x: 100, y: 0, color: { background: '#1e293b', border: '#8b5cf6' }, font: { color: 'white' } },
            { id: 'q3', label: 'q3\n(Cart)', x: 250, y: 0, color: { background: '#1e293b', border: '#10b981' }, borderWidth: 3, font: { color: 'white' } }
        ],
        edges: [
            { from: 'q0', to: 'q0', label: 'Σ', selfReferenceSize: 20 },
            { from: 'q0', to: 'q1', label: 'HOME' },
            { from: 'q1', to: 'q2', label: 'SEARCH' },
            { from: 'q2', to: 'q2', label: 'SEARCH', selfReferenceSize: 20 },
            { from: 'q2', to: 'q3', label: 'CART' },
            { from: 'q3', to: 'q3', label: 'Σ', selfReferenceSize: 20 }
        ]
    },
    messaging: {
        title: "Validación de Sintaxis de Mensajería",
        formal: `
            <div class="def-item"><strong>Q:</strong> {q0, q1, q2, q3, q4}</div>
            <div class="def-item"><strong>Σ:</strong> {@, TEXT, /, CMD, OTHER}</div>
            <div class="def-item"><strong>q0:</strong> q0</div>
            <div class="def-item"><strong>F:</strong> {q2, q4}</div>
            <div class="def-item"><strong>Patrón:</strong> @USER -> TEXT -> (opcional) /CMD</div>
        `,
        alphabet: ['@', 'TEXT', '/', 'CMD', 'OTHER'],
        nodes: [
            { id: 'q0', label: 'q0\n(Inicio)', x: -300, y: 0, color: { background: '#1e293b', border: '#f59e0b' }, font: { color: 'white' } },
            { id: 'q1', label: 'q1\n(@)', x: -150, y: 0, color: { background: '#1e293b', border: '#f59e0b' }, font: { color: 'white' } },
            { id: 'q2', label: 'q2\n(Texto)', x: 0, y: 0, color: { background: '#1e293b', border: '#10b981' }, borderWidth: 3, font: { color: 'white' } },
            { id: 'q3', label: 'q3\n(/)', x: 150, y: 0, color: { background: '#1e293b', border: '#f59e0b' }, font: { color: 'white' } },
            { id: 'q4', label: 'q4\n(Cmd)', x: 300, y: 0, color: { background: '#1e293b', border: '#10b981' }, borderWidth: 3, font: { color: 'white' } }
        ],
        edges: [
            { from: 'q0', to: 'q0', label: 'Σ', selfReferenceSize: 20 },
            { from: 'q0', to: 'q1', label: '@' },
            { from: 'q1', to: 'q2', label: 'TEXT' },
            { from: 'q2', to: 'q2', label: 'OTHER', selfReferenceSize: 20 },
            { from: 'q2', to: 'q3', label: '/' },
            { from: 'q3', to: 'q4', label: 'CMD' },
            { from: 'q4', to: 'q4', label: 'Σ', selfReferenceSize: 20 }
        ]
    }
};

// Estado Global
let currentNFA = 'ids';
let currentSequence = [];
let network = null;
let simulationHistory = [];
let currentStep = 0;
let originalNodes = null;
let originalEdges = null;

// Inicialización
document.addEventListener('DOMContentLoaded', () => {
    initUI();
    loadNFA('ids');
});

function initUI() {
    // Sidebar tabs
    document.querySelectorAll('.nav-links li').forEach(item => {
        item.addEventListener('click', (e) => {
            document.querySelectorAll('.nav-links li').forEach(el => el.classList.remove('active'));
            const target = e.currentTarget;
            target.classList.add('active');
            const nfaId = target.getAttribute('data-target');
            loadNFA(nfaId);
        });
    });

    // Buttons
    document.getElementById('btn-clear').addEventListener('click', clearSequence);
    document.getElementById('btn-simulate').addEventListener('click', runSimulation);
    document.getElementById('btn-prev-step').addEventListener('click', prevStep);
    document.getElementById('btn-next-step').addEventListener('click', nextStep);
}

function loadNFA(nfaId) {
    currentNFA = nfaId;
    const config = nfaConfigs[nfaId];
    
    // Update text and definitions
    document.getElementById('exercise-title').innerText = config.title;
    document.getElementById('formal-def').innerHTML = config.formal;
    
    // Clear state
    clearSequence();
    document.getElementById('results').style.display = 'none';
    
    // Create alphabet buttons
    const btnContainer = document.getElementById('symbol-buttons');
    btnContainer.innerHTML = '';
    config.alphabet.forEach(symbol => {
        const btn = document.createElement('button');
        btn.className = 'symbol-btn';
        btn.innerText = symbol;
        btn.addEventListener('click', () => addSymbol(symbol));
        btnContainer.appendChild(btn);
    });

    // Draw graph
    drawGraph(config);
}

function drawGraph(config) {
    const container = document.getElementById('mynetwork');
    
    originalNodes = new vis.DataSet(config.nodes);
    originalEdges = new vis.DataSet(config.edges);
    
    const data = {
        nodes: originalNodes,
        edges: originalEdges
    };
    
    const options = {
        physics: false, // Static positions for better visualization
        edges: {
            arrows: {
                to: { enabled: true, scaleFactor: 0.8 }
            },
            color: { color: 'rgba(255,255,255,0.4)', highlight: '#3b82f6' },
            font: { color: 'white', size: 12, background: 'rgba(15,23,42,0.8)', strokeWidth: 0 },
            smooth: { type: 'curvedCW', roundness: 0.2 }
        },
        nodes: {
            shape: 'circle',
            margin: 15,
            font: { face: 'Outfit', size: 14 }
        },
        interaction: {
            hover: true,
            zoomView: false,
            dragView: true
        }
    };
    
    if (network !== null) {
        network.destroy();
    }
    network = new vis.Network(container, data, options);
}

function addSymbol(symbol) {
    currentSequence.push(symbol);
    updateSequenceDisplay();
    // Hide results if we are modifying
    document.getElementById('results').style.display = 'none';
    resetGraphHighlights();
}

function clearSequence() {
    currentSequence = [];
    updateSequenceDisplay();
    document.getElementById('results').style.display = 'none';
    resetGraphHighlights();
}

function updateSequenceDisplay() {
    const container = document.getElementById('sequence-badges');
    if (currentSequence.length === 0) {
        container.innerHTML = '<span class="placeholder-text">Vacía</span>';
        return;
    }
    
    container.innerHTML = '';
    currentSequence.forEach(symbol => {
        const span = document.createElement('span');
        span.className = 'sequence-badge';
        span.innerText = symbol;
        container.appendChild(span);
    });
}

async function runSimulation() {
    if (currentSequence.length === 0) {
        alert("Agrega al menos un símbolo a la secuencia");
        return;
    }

    const btn = document.getElementById('btn-simulate');
    btn.disabled = true;
    btn.innerText = 'Simulando...';

    try {
        const response = await fetch('/api/simulate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                nfa_id: currentNFA,
                sequence: currentSequence
            })
        });

        const data = await response.json();
        
        simulationHistory = data.history;
        currentStep = 0;
        
        showResults(data.accepted);
        updateHistoryUI();
        highlightStates(simulationHistory[currentStep]);
        
    } catch (err) {
        console.error("Error during simulation", err);
        alert("Error en el servidor");
    } finally {
        btn.disabled = false;
        btn.innerText = 'Simular AFND';
    }
}

function showResults(accepted) {
    const resultsDiv = document.getElementById('results');
    const badge = document.getElementById('result-status');
    const text = document.getElementById('result-text');
    
    resultsDiv.style.display = 'flex';
    
    if (accepted) {
        badge.className = 'status-badge status-accepted';
        badge.innerText = 'ACEPTADO';
        text.innerText = 'La cadena llegó a un estado de aceptación.';
    } else {
        badge.className = 'status-badge status-rejected';
        badge.innerText = 'RECHAZADO';
        text.innerText = 'La cadena NO llegó a ningún estado de aceptación.';
    }
}

function updateHistoryUI() {
    const container = document.getElementById('history-container');
    container.innerHTML = '';
    
    simulationHistory.forEach((states, idx) => {
        const div = document.createElement('div');
        div.className = 'history-step';
        if (idx === currentStep) div.classList.add('active-step');
        
        let label = idx === 0 ? "Estado inicial:" : `Paso ${idx} (leído '${currentSequence[idx-1]}'):`;
        div.innerHTML = `<strong>${label}</strong> Estados activos: {${states.join(', ') || '∅'}}`;
        container.appendChild(div);
    });
    
    // Update controls
    document.getElementById('step-counter').innerText = `Paso ${currentStep} de ${simulationHistory.length - 1}`;
    document.getElementById('btn-prev-step').disabled = currentStep === 0;
    document.getElementById('btn-next-step').disabled = currentStep === simulationHistory.length - 1;
}

function prevStep() {
    if (currentStep > 0) {
        currentStep--;
        updateHistoryUI();
        highlightStates(simulationHistory[currentStep]);
    }
}

function nextStep() {
    if (currentStep < simulationHistory.length - 1) {
        currentStep++;
        updateHistoryUI();
        highlightStates(simulationHistory[currentStep]);
    }
}

function resetGraphHighlights() {
    if(!originalNodes) return;
    
    const updates = originalNodes.get().map(node => {
        // Reset to original color
        let origColor = '#1e293b';
        let origBorder = '#3b82f6';
        if(nfaConfigs[currentNFA].nodes.find(n => n.id === node.id)) {
            let n = nfaConfigs[currentNFA].nodes.find(n => n.id === node.id);
            origColor = n.color.background;
            origBorder = n.color.border;
        }
        return {
            id: node.id,
            color: { background: origColor, border: origBorder },
            font: { color: 'white' },
            shadow: false
        };
    });
    originalNodes.update(updates);
}

function highlightStates(activeStates) {
    resetGraphHighlights();
    
    if (activeStates.length === 0) return;
    
    const updates = activeStates.map(stateId => {
        return {
            id: stateId,
            color: { 
                background: '#3b82f6', 
                border: '#60a5fa' 
            },
            font: { color: 'white' },
            shadow: {
                enabled: true,
                color: '#60a5fa',
                size: 20,
                x: 0,
                y: 0
            }
        };
    });
    
    originalNodes.update(updates);
}
