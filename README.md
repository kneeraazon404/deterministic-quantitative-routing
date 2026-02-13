# Senior AI Orchestrator: Deterministic Quantitative Routing

This project implements a "Thin Agent, Fat Platform" architecture designed to bridge the gap between natural language queries and a library of 100+ frozen, deterministic quantitative functions. It allows traders to execute complex, multi-asset, multi-timeframe regime analysis without manual data engineering or parameter tuning.

## Core Architectural Philosophy

Traditional agentic frameworks rely on probabilistic guidance (prompts) for deterministic tasks, leading to hallucinations and high failure rates in production. This platform solves the "Context-Capability Paradox" by stripping the LLM of its mathematical authority and restricting it to the role of a Semantic Router.

### Frozen Math

All quantitative logic is encapsulated in tested, stateless Python functions. The orchestrator treats these as opaque execution units.

### Uniform Interface

Every function in the library adheres to a strict contract: `array[float] -> array[int] \in {0, 1}`.

### Kernel-Mode Orchestration

The "Senior AI Orchestrator" plans the execution graph but is physically blocked from writing code or performing math directly.

## Tech-Specific Implementation Steps

### 1. Library Interface Standardization

Ensure all 100 functions follow the subject-predicate interface. The math must be "frozen"—no tuning parameters are exposed to the LLM.

```python
def regime_function_x(prices: np.ndarray[float]) -> np.ndarray[int]:
    """
    Interface Contract:
    Input: Normalized price vector
    Output: Binary regime state (0 or 1) of equal length
    """
    # math logic here (Frozen)
    return states
```

### 2. The Semantic Routing Layer (Thin Agent)

Utilize a smaller, high-consistency model (e.g., 7B-8B parameters at $T=0.0$) to parse natural language into a structured Execution Blueprint.

- **Intent Parsing:** Map "Generals and the Army" to a cross-sectional breadth sum.
- **Asset Identification:** Extract tickers and timeframe requirements (e.g., BTC 5m vs Daily).
- **Composition Mapping:** Select the correct logic gate (AND, XOR, Average).

### 3. Implementation of Deterministic Lifecycle Hooks

Use programmatic gates to enforce engineering rigor that prompts alone cannot achieve.

- **PreToolUse Hook:** Intercept tool calls to validate input schema compliance.
- **PostToolUse Hook:** Validate outputs. If a function returns non-binary values or misaligned lengths, the hook rejects the result and triggers a retry.
- **Stop Hook (Compaction Gate):** Block the orchestrator from exiting if the recursive stability check has not converged.

### 4. Multi-Timeframe and Synthetic Alignment

All alignment must be handled at the output level to avoid input data distortion.

- **Index Union:** Use logic to create a common time base for disparate frequencies.
- **XOR Disagreement:** For queries like "Flag every moment 5m and Daily disagree," broadcast the lower-frequency signal and apply an Exclusive OR:
  $$D(t) = S_{high\_freq}(t) \oplus S'_{low\_freq}(t)$$

### 5. Recursive Stability Loop (Regime of the Regime)

When a trader requests noise reduction ("Run until stable"), the system initiates a recursive self-application loop.

- **Mathematical Definition:** Stability is defined by the Hamming distance ($D_H$) between iteration $k$ and $k+1$.
- **Exit Conditions:**
  - **Convergence:** $D_H = 0$.
  - **Material Stability:** $D_H < 1\%$ of array length.
  - **Circuit Breaker:** Terminate at $N=10$ iterations to prevent infinite loops.

### 6. Provenance and Audit Trails

Every signal generated must include a "Provenance Receipt" for institutional auditability.

- **Library Hash:** Git hash of the frozen library version.
- **Data Lineage:** "As-of" timestamps and data provider IDs.
- **Reasoning Proof:** Log of the LLM seed and intent parse plan.

## Key Scenarios & Orchestrator Logic

| Scenario                | User Query                                           | Orchestrator Action                                                         |
| ----------------------- | ---------------------------------------------------- | --------------------------------------------------------------------------- |
| **Market Breadth**      | "When are the Big 7 tech stocks up but NDX is down?" | Parallel dispatch (100 constituent calls) + Cross-sectional Sum logic gate. |
| **Asset Fusion**        | "Combine Gold, Bonds, and VIX into a fear index."    | Triple function dispatch + Consensus Agreement Gate (Round/Avg).            |
| **Timeframe Sync**      | "Flag when BTC 5m and Daily bars disagree."          | Output broadcasting + XOR operation across indices.                         |
| **Synthetic Positions** | "Long Energy, Short Financials. Give me regime."     | Vector arithmetic on price arrays ($P_A - P_B$) prior to library call.      |
| **Recursive Denoising** | "The output is too noisy. Run until stable."         | Iterative Hamming evaluation until bit-flip count reaches convergence.      |

## Hardware and Model Requirements

- **Recommended Models:** Qwen2.5-7B or Granite-3-8B ($T=0.0$, Fixed Seed) for 100% routing consistency.
- **Decoding Strategy:** Implement Constrained Decoding (logit-level masking) to physically prevent hallucinations of non-integer tokens in the output schema.
- **Institutional Disclaimer:** This architecture is designed for audit-grade reproducibility. Results are bit-for-bit identical given the same input data, LLM seed, and frozen library version.
