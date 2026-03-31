---
name: Topology inspirations — venery, Prey, programmable matter
description: agentic-titan's hive module draws from three sources — terms of venery (biological collective nouns), Crichton's Prey (emergent adversarial swarm dynamics), and programmable matter / claytronics (continuous topology morphing). Four GitHub issues (#57-60) track the gaps.
type: project
---

The hive module's topology system has three inspiration layers, only partially implemented:

**Why:** The named topologies (swarm, hierarchy, mesh, etc.) are stable basins in a continuous topology-space. The goal is agents that flow between formations like murmurations — not selecting a topology, but having one emerge from local interactions. The biological and fictional sources provide the target behavior.

**How to apply:**

1. **Terms of venery (#57):** Each topology gets a biological collective noun. A Murder (fission-fusion), a Parliament (hierarchy), a Colony (stigmergy). The name IS the spec.

2. **Crichton's Prey (#59):** Missing adversarial dynamics — predator-prey co-evolution where topology emerges from competition. Pheromone field supports WARNING/FAILURE traces but no explicit selection loop.

3. **Programmable matter (#58):** Topology transitions are currently discrete switches. Catom model would make them continuous — each agent holds a topology weight vector, formation is always a gradient blend.

4. **Continuous morphing (#60):** The synthesis. Criticality detection (phase transitions) + assembly dynamics (territorialization) + gradient topology = formations that flow without discrete switching.

**Existing primitives:** neighborhood.py (N=7 murmuration), criticality.py (edge of chaos), assembly.py (D&G territorialization), machines.py (war machine vs state machine), stigmergy.py (pheromone field). The substrate is rich. The continuous morphing layer is the gap.
