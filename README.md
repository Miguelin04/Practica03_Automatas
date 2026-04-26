# 🤖 Simulador de Autómatas Finitos — AFD y AFND
### Práctica 03 — Teoría de Autómatas

Plataforma web interactiva para simular **Autómatas Finitos Deterministas (AFD)** y **No Deterministas (AFND)** aplicados a escenarios del mundo real. Desarrollada con Flask (backend) y Vis.js (frontend), permite construir cadenas símbolo a símbolo, ejecutar la simulación y visualizar el recorrido de estados en un diagrama interactivo paso a paso.

---

## 📋 Ejercicios Implementados

### 🔵 Autómatas Finitos Deterministas (AFD)
> Para cada estado y símbolo existe **exactamente una** transición posible.

| # | Ejercicio | Patrón Reconocido | ID API |
|---|-----------|-------------------|--------|
| 1 | 🔒 **Cerradura IoT** (Ej. 2) | Bloqueo tras 3 fallos consecutivos | `iot` |
| 2 | 📦 **Logística de Pedidos** (Ej. 4) | Flujo: Pedido → Empaquetado → Envío → Entrega | `logistics` |
| 3 | 🤝 **Handshake TCP** (Ej. 5) | SYN → SYN-ACK → ACK | `handshake` |

### 🟣 Autómatas Finitos No Deterministas (AFND)
> Para un estado y símbolo pueden existir **cero, una o varias** transiciones simultáneas.

| # | Ejercicio | Patrón Reconocido | ID API |
|---|-----------|-------------------|--------|
| 4 | 🛡️ **Detección de Ataques IDS** (Ej. 6) | SYN → ACK(s) → RST | `ids` |
| 5 | 🛒 **Comportamiento E-commerce** (Ej. 9) | HOME → SEARCH(es) → CART | `ecommerce` |
| 6 | 💬 **Sintaxis de Mensajería** (Ej. 10) | @bot (USER)? (!cmd \| ?help) | `messaging` |

---

## 🛠️ Tecnologías

- **Backend:** Python 3 + Flask
- **Frontend:** HTML5, CSS3 (Glassmorphism), JavaScript (ES6+)
- **Visualización:** [Vis.js Network](https://visjs.github.io/vis-network/docs/network/)
- **Tipografía:** Google Fonts — Outfit

---

## 🚀 Instalación y Ejecución

### 1. Clonar / descargar el proyecto

```bash
cd "Practica 03"
```

### 2. Crear y activar el entorno virtual

```bash
python3 -m venv venv
source venv/bin/activate        # Linux / macOS
# venv\Scripts\activate         # Windows
```

### 3. Instalar dependencias

```bash
pip install flask
```

### 4. Ejecutar el servidor

```bash
python3 app.py
```

### 5. Abrir en el navegador

```
http://localhost:5002
```

---

## 📁 Estructura del Proyecto

```
Practica 03/
├── app.py                  # Backend Flask: definición de NFAs y rutas API
├── README.md
├── templates/
│   └── index.html          # Interfaz principal (Jinja2)
├── static/
│   ├── css/
│   │   └── style.css       # Estilos (glassmorphism, layout, animaciones)
│   └── js/
│       └── main.js         # Lógica frontend: carga NFA, simulación, diagrama
└── venv/                   # Entorno virtual (no incluir en VCS)
```

---

## 🌐 API REST

### `GET /api/nfa/<nfa_id>`
Devuelve la definición completa del autómata, incluyendo nodos y aristas para el diagrama.

**Ejemplo:**
```bash
curl http://localhost:5002/api/nfa/iot
```

```json
{
  "title": "Sistema de Seguridad IoT (Cerradura Inteligente)",
  "pattern": "Bloqueo tras 3 fallos (AFD)",
  "states": ["q0", "q1", "q2", "q3"],
  "alphabet": ["a", "f"],
  "start_state": "q0",
  "accept_states": ["q3"],
  "transitions": { ... },
  "nodes": [ ... ],
  "edges": [ ... ]
}
```

---

### `POST /api/simulate`
Simula una cadena sobre el autómata indicado y devuelve el historial de estados.

**Body (JSON):**
```json
{
  "nfa_id": "iot",
  "sequence": ["f", "f", "f"]
}
```

**Respuesta:**
```json
{
  "accepted": true,
  "history": [["q0"], ["q1"], ["q2"], ["q3"]],
  "final_states": ["q3"]
}
```

---

## 🎮 Cómo Usar la Plataforma

1. **Selecciona un ejercicio** en el panel izquierdo.
2. **Observa la definición formal** del autómata (Q, Σ, q₀, F, patrón).
3. **Arma la cadena** haciendo clic en los botones de símbolos del alfabeto.
4. **Pulsa "Simular AFND"** para ejecutar la simulación.
5. **Navega el diagrama** paso a paso con los botones *Anterior / Siguiente*.
   - Los nodos resaltados en **azul** indican los estados activos en cada paso.
   - El resultado final muestra **ACEPTADO** (verde) o **RECHAZADO** (rojo).

---

## 🧮 Definición Formal

Ambos tipos de autómatas se definen como una 5-tupla **M = (Q, Σ, δ, q₀, F)**:

| Símbolo | Significado |
|---------|-------------|
| **Q** | Conjunto finito de estados |
| **Σ** | Alfabeto (símbolos de entrada) |
| **δ** | Función de transición |
| **q₀** | Estado inicial |
| **F** | Conjunto de estados de aceptación |

### Diferencia clave en δ

| Tipo | Función de transición | Determinismo |
|------|-----------------------|--------------|
| **AFD** | δ: Q × Σ → Q | Exactamente **1** estado destino por (estado, símbolo) |
| **AFND** | δ: Q × Σ → 2^Q | **0, 1 o varios** estados destino posibles por (estado, símbolo) |

> En los AFND la cadena se acepta si **al menos uno** de los caminos posibles llega a un estado de aceptación.

---

## 👤 Autor

**Práctica 03 — Teoría de Autómatas**  
Ingeniería en Sistemas / Ciencias de la Computación