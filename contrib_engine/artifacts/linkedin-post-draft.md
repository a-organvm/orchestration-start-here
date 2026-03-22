# LinkedIn Post — The Plague Campaign

## Images (carousel order)
1. `linkedin-01-network.png` — Contribution network topology
2. `linkedin-02-phases.png` — Campaign phase architecture
3. `linkedin-03-symbiote.png` — Cross-organ symbiote pattern

## Post Text

---

**I built a contribution engine. Then I pointed it at 7 open-source repos.**

Hive describes itself as a framework for developers who want to "build many autonomous AI agents fast without manually wiring complex workflows" (AdenHQ/Hive README). Their CONTRIBUTING.md says it plainly: "Aden Hive is built by practitioners for practitioners."

That principle — practitioners building for practitioners — is what I systematized.

The targets span the AI agent ecosystem: Anthropic's Agent Skills ("Skills teach Claude how to complete specific tasks in a repeatable way" — anthropics/skills README, 100K stars), LangGraph ("a low-level orchestration framework for building, managing, and deploying long-running, stateful agents" — langchain-ai/langgraph, 27K stars), Temporal's Python SDK ("a distributed, scalable, durable orchestration engine" — temporalio/sdk-python), dbt's MCP server, and two more.

Each target gets a full contribution workspace:
- A capability map matching my system's patterns to their open problems
- A campaign sequencer that prioritizes by relationship strength, not just star count
- An outreach tracker modeling the engagement lifecycle from first contact through community standing
- A backflow pipeline routing what I learn back into my own system

The methodology isn't arbitrary. Lakhani and von Hippel's foundational research on open-source participation found that "the community learns from its participants, and each individual learns from the community" — a synergistic process where knowledge exchange is bidirectional by nature (Research Policy, 2003). Von Krogh, Spaeth, and Lakhani further demonstrated that joining specialization — the process by which contributors find their niche within a community — is what converts peripheral participation into sustained, high-impact contribution (Research Policy, 2003).

That's the theory. The engineering is a 5-phase campaign:

UNBLOCK → ENGAGE → CULTIVATE → HARVEST → INJECT

Each phase produces measurable output. Unblocking clears technical barriers (CLAs, CI failures, issue claiming). Engaging joins the community before submitting code — relationship context before cold PRs. Cultivating responds to review feedback within 24 hours. Harvesting extracts patterns and formalizes theory from the fusion. Injecting routes knowledge back: theory formalization, generative artifacts, public narrative, community capital, distribution content.

One contribution, seven returns. And each return compounds the next contribution's probability of success — what the literature calls "structural social capital" (Singh & Monge, J. of Computer-Mediated Communication, 2011).

7 PRs open. 111 tests. The campaign is live.

What systems have you built to make open-source contribution sustainable and symbiotic rather than episodic?

---

## References (for comment or separate post)

### Primary Sources (target repo documentation)
- AdenHQ/Hive CONTRIBUTING.md: "Aden Hive is built by practitioners for practitioners"
- AdenHQ/Hive README: "build many autonomous AI agents fast without manually wiring complex workflows"
- anthropics/skills README: "Skills teach Claude how to complete specific tasks in a repeatable way"
- langchain-ai/langgraph README: "a low-level orchestration framework for building, managing, and deploying long-running, stateful agents"
- temporalio/sdk-python README: "a distributed, scalable, durable orchestration engine"
- dbt-labs/dbt-mcp README: "This MCP server provides various tools to interact with dbt"

### Secondary Sources (peer-reviewed)
1. Lakhani, K. R. & von Hippel, E. (2003). "How Open Source Software Works: 'Free' User-to-User Assistance." Research Policy, 32(6), 923-943. doi:10.1016/S0048-7333(02)00095-1
2. von Krogh, G., Spaeth, S., & Lakhani, K. R. (2003). "Community, Joining, and Specialization in Open Source Software Innovation: A Case Study." Research Policy, 32(7), 1217-1241.
3. Singh, P. V. & Monge, P. (2011). "Network Effects: The Influence of Structural Social Capital on Open Source Project Success." Journal of Computer-Mediated Communication, 16(4).
4. Ke, W. & Zhang, P. (2010). "The Effects of Extrinsic Motivations and Satisfaction in Open Source Software Development." Journal of the AIS, 11(12).
5. Haefliger, S., von Krogh, G., & Spaeth, S. (2008). "Code Reuse in Open Source Software." Management Science, 54(1), 180-193.

### Tagging
- @ Vincent Jiang (AdenHQ) — ONLY after joining their Discord
- Mention by name without @: Anthropic, LangChain, Temporal, dbt Labs
