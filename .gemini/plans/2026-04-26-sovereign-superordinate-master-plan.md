# MASTER PLAN: The Sovereign Superordinate Layer (Alpha to Omega)

**Date:** 2026-04-26
**Codename:** The Body Observatory (Temporarily: Sovereign)

## 0. The Metaphysics of the Layer
The Superordinate Layer is NOT an organ. It is the connective fascia, the interstitial fluid, the vacuum-observer. It does not "do" the work of the organs; it detects the radiation (vacua) emitted by their friction. 

## 1. The Four Operators (Micro-Spec)
These are not theoretical. They are CLI subcommands and daemons.

### A. The Selfish-Altruistic Loop (Resource Arbiter)
- **Cog:** `organvm-engine arbiter`
- **Spec:** A daemon that monitors token usage, compute (16GB RAM constraints), and human attention. 
- **Mechanism:** When Organ I (Theory) and Organ III (Commerce) compete for Claude's context window, the Arbiter uses the `strategy/scoring-rubric.yaml` to dynamically allocate budget based on the immediate survival vs. long-term compounding ratio.

### B. The Magnetic Membrane (Escalation Router)
- **Cog:** `organvm-engine membrane`
- **Spec:** The boundary enforcer. 
- **Mechanism:** Evaluates cross-repo PRs. If a change in `hokage-chess` requires a structural change in `schema-definitions`, the membrane flags it as **SYSTEMIC** and routes it to the Human (Vision Authority). If it is isolated, it remains **LOCAL** (Hokage-level).

### C. The Portfolio Recombinator (Synthesis Engine)
- **Cog:** `organvm-engine portfolio-synthesis`
- **Spec:** The n-way portfolio combination rule.
- **Mechanism:** Periodically scans the IRF ledger. Identifies orphaned atoms in one organ that structurally complete a vacuum in another (e.g., finding that `application-pipeline`'s recruiter-persona solves `distribution-strategy`'s channel-persona). Merges them into a unified `.config/portfolio-lock.yaml`.

### D. The Reflexive Loop (Self-Audit)
- **Cog:** `organvm-engine reflex`
- **Spec:** The autopoietic monitor.
- **Mechanism:** Calculates the delta between predicted outcome and actual outcome of the other three operators. *Critical limitation:* It cannot alter its own evaluation criteria. It must halt and prompt the human via `mcp_server` to anchor the regression.

## 2. Stream Τ: MCP Wrapper Integration
- **Micro-plan:** All 5 organ CLIs will be wrapped using FastMCP (or equivalent).
- **Grain:** Each CLI exposes its commands as native MCP tools (`get_organ_state`, `trigger_membrane`, `query_irf_ledger`).
- **Why:** Standalone binaries are deaf. MCP servers are resonant. The swarm can organically discover and trigger these tools without bash scaffolding.

## 3. Stream Ω: 72h Subatomic Atomization
- **Micro-plan:** A continuous chronological parser across 37 repos.
- **Grain:** 24-hour chunks. 
- **Mechanism:** `atomize() -> yield state_hash -> sleep 10s -> resume`. State is saved to `fossil-record.json` every 1000 tokens to prevent session-loss catastrophe.

## 4. The Naming Scheme & Ontology
We embrace the vacuum. Until the layer proves its accuracy by predicting a cross-domain friction event before it happens, it remains referred to as `organvm-iv-taxis/vacuum-observer`. Upon success, it is crowned **Sovereign**.
