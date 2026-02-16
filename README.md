return states


### 2. The Semantic Routing Layer (Thin Agent)
Utilize a high-consistency model (e.g., Qwen2.5-7B or Granite-3-8B) to parse natural language into a structured Execution Blueprint.

- **Intent Parsing:** Map "Generals and the Army" to a cross-sectional breadth sum.
- **Asset Identification:** Extract tickers and timeframe requirements (e.g., BTC 5m vs Daily).
- **Composition Mapping:** Map to Directional Difference or Consensus Agreement instead of bitwise logic gates.

### 3. Implementation of Deterministic Lifecycle Hooks
Use programmatic gates to enforce engineering rigor.

- **PreToolUse Hook:** Intercept tool calls to validate input schema compliance.
- **PostToolUse Hook:** Validate outputs. If a function returns non-binary values or misaligned lengths, the hook rejects the result and triggers a retry.
- **Stop Hook (Compaction Gate):** Block the orchestrator from exiting if the recursive stability check has not converged.

### 4. Multi-Timeframe and Synthetic Alignment
All alignment must be handled at the output level to avoid input data distortion. Bitwise XOR is avoided to prevent noise amplification and the loss of directional context.[1, 5]

- **Index Union:** Create a common time base for disparate frequencies.
- **pjSD Divergence:** For "lying" signals (e.g., BTC 5m vs Daily), utilize **Permutation Jensen-Shannon Distance (pjSD)** to measure dissimilarity between scales without losing the regime's sign.[6, 7]
- **RG Awareness:** Align signals using **Renormalization Group (RG)** logic, treating daily regimes as coarse-grained fixed points of high-frequency micro-regimes.[8]

### 5. Recursive Stability Loop (Regime of the Regime)
When a trader requests noise reduction ("Run until stable"), the system initiates recursive self-application until a **Fixed Point Attractor** is reached.[8, 9]

- **Mathematical Definition:** Stability is defined by the Hamming distance ($D_H$) between iteration $k$ and $k+1$.
- **Exit Conditions:**
  - **Convergence:** $D_H = 0$ (The system has settled into an idempotent state).
  - **Material Stability:** $D_H < 1\%$ of array length.
  - **Circuit Breaker:** Terminate at $N=10$ iterations to prevent infinite oscillations or 2-cycle attractors.

### 6. Provenance and Audit Trails
Every signal includes a "Provenance Receipt" for institutional auditability.

- **Library Hash:** Git hash of the frozen library version.
- **Data Lineage:** "As-of" timestamps and data provider IDs.
- **Reasoning Proof:** Log of the LLM seed and intent parse plan.

## Key Scenarios & Orchestrator Logic

| Scenario | User Query | Orchestrator Action |
| :--- | :--- | :--- |
| **Market Breadth** | "When are the Big 7 up but NDX is down?" | Parallel dispatch + Cross-sectional Sum logic gate. |
| **Asset Fusion** | "Combine Gold, Bonds, and VIX into a fear index." | Triple dispatch + Consensus Agreement Gate. |
| **Timeframe Sync** | "Flag when BTC 5m and Daily bars disagree." | Output broadcasting + pjSD Divergence across indices.[6] |
| **Synthetic Positions** | "Long Energy, Short Financials. Give me regime." | Vector arithmetic on price arrays prior to library call. |
| **Recursive Denoising** | "The output is too noisy. Run until stable." | Iterative Hamming evaluation until fixed-point convergence.[8] |

## Hardware and Model Requirements

- **Decoding Strategy:** Implement Constrained Decoding (logit-level masking) to physically prevent hallucinations of non-integer tokens in the output schema.
- **Institutional Disclaimer:** This architecture is designed for audit-grade reproducibility. Results are bit-for-bit identical given the same input data, LLM seed, and frozen library version.
