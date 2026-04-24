// Estado Global
let currentNFA = 'ids';
let currentSequence = [];
let network = null;
let simulationHistory = [];
let currentStep = 0;
let originalNodes = null;
let originalEdges = null;
let currentConfig = null;

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

async function loadNFA(nfaId) {
    currentNFA = nfaId;
    
    try {
        const response = await fetch(`/api/nfa/${nfaId}`);
        if (!response.ok) throw new Error("No se pudo cargar el AFND");
        const config = await response.json();
        currentConfig = config;
        
        // Generar definición formal dinámica
        const formalHTML = `
            <div class="def-item"><strong>Q:</strong> {${config.states.join(', ')}}</div>
            <div class="def-item"><strong>Σ:</strong> {${config.alphabet.join(', ')}}</div>
            <div class="def-item"><strong>q0:</strong> ${config.start_state}</div>
            <div class="def-item"><strong>F:</strong> {${config.accept_states.join(', ')}}</div>
            <div class="def-item"><strong>Patrón:</strong> ${config.pattern}</div>
            <details class="transition-table">
                <summary>Ver Tabla de Transiciones (δ)</summary>
                ${generateTransitionsHTML(config)}
            </details>
        `;

        // Update text and definitions
        document.getElementById('exercise-title').innerText = config.title;
        document.getElementById('formal-def').innerHTML = formalHTML;
        
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
        
    } catch (err) {
        console.error(err);
        alert("Error cargando configuración dinámica del AFND");
    }
}

function generateTransitionsHTML(config) {
    let html = '<div class="table-responsive"><table class="academic-table">';
    // Cabecera (Alfabeto)
    html += '<thead><tr><th></th>';
    config.alphabet.forEach(sym => {
        html += `<th>${sym}</th>`;
    });
    html += '</tr></thead><tbody>';
    
    // Cuerpo (Estados y transiciones)
    config.states.forEach(state => {
        html += `<tr><th>${state}</th>`;
        config.alphabet.forEach(sym => {
            const nextStates = config.transitions[state] && config.transitions[state][sym];
            if (nextStates && nextStates.length > 0) {
                html += `<td>{${nextStates.join(', ')}}</td>`;
            } else {
                html += `<td>∅</td>`;
            }
        });
        html += '</tr>';
    });
    
    html += '</tbody></table></div>';
    return html;
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
        layout: {
            hierarchical: {
                direction: 'LR',
                sortMethod: 'directed',
                levelSeparation: 250,
                nodeSpacing: 150
            }
        },
        physics: false,
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
            zoomView: true,
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
    if(!originalNodes || !currentConfig) return;
    
    const updates = originalNodes.get().map(node => {
        // Find original color
        let origColor = '#1e293b';
        let origBorder = '#3b82f6';
        let origNode = currentConfig.nodes.find(n => n.id === node.id);
        if(origNode) {
            origColor = origNode.color.background;
            origBorder = origNode.color.border;
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
