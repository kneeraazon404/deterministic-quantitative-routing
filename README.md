Here is an elegant, technical, and stepwise `README.md` file designed for a GitHub repository. It synthesizes the architectural principles of **Deterministic AI Orchestration** (Thin Agent/Fat Platform) with the domain-specific rigor of **Quantitative Finance** (Ordinal Patterns/Information Theory).

***

# Senior AI Orchestrator: Deterministic Quantitative Routing Platform

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Architecture](https://img.shields.io/badge/Architecture-Thin%20Agent%20%2F%20Fat%20Platform-orange)](https://praetorian.com)
[![Math](https://img.shields.io/badge/Math-Frozen%20%26%20Stateless-green)](https://github.com/arthurpessa/ordpy)

## 📋 Executive Summary

**Senior AI Orchestrator** is an institutional-grade platform that solves the **Context-Capability Paradox** in autonomous financial analysis. It replaces the fragile "Thick Agent" paradigm—prone to hallucination and context drift—with a **Thin Agent, Fat Platform (TAFP)** architecture.

Instead of asking an LLM to *perform* math, this system restricts the LLM to **semantic routing** (Kernel Mode), delegating execution to a library of "Frozen Math" functions (User Mode) based on **Ordinal Pattern Analysis** and **Information Geometry**. The result is a system that offers the semantic flexibility of generative AI with the deterministic guarantees required for regulatory auditability and capital deployment.

---

## 🏗 System Architecture

The platform operates on a strict **Inversion of Control** model. The LLM is treated as a non-deterministic kernel process wrapped in a deterministic runtime environment.

```bash
graph TD
    User[User Query] -->|Natural Language| Orch[Kernel Orchestrator]
    
    subgraph "Deterministic Runtime (Fat Platform)"
        Orch -->|JSON Schema| Gateway[Gateway Router]
        Gateway -->|JIT Load| Skill[Skill Library]
        
        subgraph "Frozen Math Core"
            Skill -->|Dispatch| OPA[Ordinal Pattern Analysis]
            Skill -->|Dispatch| IGT[Info-Geometric Theory]
            Skill -->|Dispatch| RSE[Recursive Stability Engine]
        end
        
        OPA -->|Binary Vector| State[State Manager]
        IGT -->|Metric| State
        RSE -->|Converged State| State
    end
    
    State -->|Provenance Receipt| Output[Final Signal]
```

### Core Components

1.  **Kernel-Mode Orchestrator**: Manages the global state machine. Physically stripped of code-execution tools to prevent "doing it yourself."
2.  **Gateway Routers**: Semantic mapping layers that perform Just-in-Time (JIT) loading of specific skill definitions, reducing context token cost from ~24k to ~2.7k per spawn.
3.  **Deterministic Hooks**: Shell-level lifecycle hooks (`PreToolUse`, `PostToolUse`) that enforce quality gates (e.g., "Cannot exit until stability metric $D_H = 0$").
4.  **Frozen Math Library**: A stateless Python library implementing scale-invariant metrics (Permutation Entropy, Jensen-Shannon Divergence) via `ordpy`.

---

## 🚀 Key Features

### 1. The "Frozen Math" Core
All quantitative logic is encapsulated in stateless functions that adhere to a strict interface contract (`prices -> array[int] \in {0, 1}`).
*   **Scale Invariance**: Uses Bandt-Pompe ordinal patterns to analyze price dynamics regardless of asset class or magnitude.
*   **Noise Robustness**: Avoids simple bitwise logic (XOR) in favor of Information-Geometric distance metrics (pjSD) to prevent parity collapse in noisy regimes.

### 2. Recursive Stability Engine
Ensures trading signals reflect **Fixed Point Attractors** rather than transient noise.
*   **Mechanism**: Iteratively re-injects binary outputs into the execution graph.
*   **Convergence Metric**: Monitors Hamming Distance ($D_H$) between iterations.
*   **Circuit Breaker**: Detects 2-cycle oscillations (chaos) and halts execution to prevent infinite loops.

### 3. Institutional Provenance
Every signal generates a cryptographically verifiable **Provenance Receipt** containing:
*   **SHA-256 Hash** of the exact library version used.
*   **Data Lineage** IDs for all input time-series.
*   **Execution Blueprint** showing the LLM's semantic routing logic.

---

## 🛠 Installation & Setup

### Prerequisites
*   Python 3.11+
*   Redis (for state persistence and caching)
*   Docker (recommended for isolated execution)

### 1. Clone and Configure
```bash
git clone https://github.com/your-org/senior-ai-orchestrator.git
cd senior-ai-orchestrator
pip install -r requirements.txt
```

### 2. Infrastructure Initialization
The platform requires a localized Redis instance to handle the "Process Control Block" (Manifest) and distributed locking.

```bash
# Start Redis container
docker run -d -p 6379:6379 redis:latest

# Initialize the environment
export ORCHESTRATOR_MODE="kernel"
export LLM_PROVIDER="anthropic" # or "deepseek", "openai"
```

### 3. Frozen Library Verification
Before running agents, verify the integrity of the math core. This ensures the "Frozen" aspect of the platform.

```bash
python scripts/verify_integrity.py --target ./lib/quant
# Output: verified SHA-256: e3b0c442... [OK]
```

---

## 💻 Development Steps: Building a Workflow

This guide walks through creating a **Market Breadth Analysis** agent using the TAFP architecture.

### Step 1: Define the "Frozen" Function
Create a stateless function in `lib/quant/regime.py`. It must accept a price array and return a binary state vector.

```python
import numpy as np
import ordpy

def detect_trend_ordinal(prices: np.ndarray, dx: int = 4, tau: int = 1) -> np.ndarray:
    """
    Stateless detection of trend using Permutation Entropy.
    Returns: Binary array (1 = Low Entropy/Trend, 0 = High Entropy/Noise)
    """
    # ... implementation using ordpy.complexity_entropy ...
    return binary_state_vector
```

### Step 2: Register the Gateway Skill
Define the skill in `.claude/skill-library/market-breadth.md`. This is the context loaded JIT by the router.

```markdown
# Skill: Market Breadth Analysis
## Intent
Use when user asks about "Generals," "Participation," or "Breadth."

## Execution Graph
1. Fetch synchronous price arrays for constituents and index.
2. Apply `detect_trend_ordinal(D=4)` to all series.
3. Apply Cross-Sectional Sum gate.
4. Return divergence vector.
```

### Step 3: Configure Deterministic Hooks
Create a `PostToolUse` hook in `hooks/validate_stability.sh` to enforce convergence.

```bash
#!/bin/bash
# Hook: Ensure signal stability before returning to user
current_hamming=$(jq .hamming_distance .output/state.json)

if [ "$current_hamming" -gt 0 ]; then
  echo "BLOCK: Signal has not converged (Hamming Distance: $current_hamming)."
  echo "Action: Re-run recursive_stabilizer() or widen embedding delay."
  exit 1 # Non-zero exit code blocks the LLM
fi
```

### Step 4: Run the Orchestrator
Execute the main entry point. The kernel will spawn specific worker agents based on the query.

```bash
python orchestrator.py --query "Are the Generals decoupling from the NDX?"
```

---

## 📊 Usage Examples

### Scenario A: Regime Detection
**User**: *"Is the current volatility in Bitcoin structural or noise?"*
**System Action**:
1.  **Router**: Identifies intent `volatility_classification`.
2.  **Worker**: Loads `lib/quant/entropy.py`.
3.  **Execution**: Calculates Complexity-Entropy (CH) plane coordinates.
4.  **Result**: "High Entropy, Low Complexity -> Stochastic Noise."

### Scenario B: Recursive Denoising
**User**: *"Clean up this signal until stable."*
**System Action**:
1.  **Router**: Enters `recursive_loop`.
2.  **Worker**: Applies function $f(x)$.
3.  **Hook**: Checks $D_H(f(x), x)$. If $> 0$, feeds $f(x)$ back into $f$.
4.  **Result**: Returns the Fixed Point Attractor of the price series.

---

## 🔮 Roadmap

*   **Q3 2025: Heterogeneous Routing**: Dispatch reasoning tasks to DeepSeek-R1 and code tasks to Claude 3.7 Sonnet automatically based on query complexity.
*   **Q4 2025: Self-Annealing Hooks**: A meta-agent that analyzes failed quality gates and rewrites the bash hooks to patch loopholes autonomously.
*   **Q1 2026: Multi-Scale Renormalization**: Automatic coarse-graining of micro-regimes using RG flow logic to predict phase transitions.

---

## 📚 References

*   **Architecture**: [Deterministic AI Orchestration (Praetorian)](https://www.praetorian.com/blog/deterministic-ai-orchestration-a-platform-architecture-for-autonomous-development/)
*   **Math Core**: [Ordpy: A Python package for data analysis with permutation entropy](https://github.com/arthurpessa/ordpy)
*   **Theory**:
    *   *Bandt, C., & Pompe, B. (2002). Permutation entropy: A natural complexity measure for time series.*
    *   *Ribeiro et al. (2012). Complexity-Entropy Causality Plane.*
    *   *Doppa et al. (2014). HC-Search: A Learning Framework for Search-based Structured Prediction.*

---

**Disclaimer**: This platform is for quantitative analysis and software orchestration. It does not constitute financial advice. The "Frozen Math" guarantees deterministic execution, not market profits.
