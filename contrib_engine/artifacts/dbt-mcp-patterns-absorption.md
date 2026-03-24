# Patterns Absorbed from dbt-labs/dbt-mcp

**Source:** PR #669 contribution + full codebase study
**Absorption triggers:** assumption_divergence (our MCP server lacks these), independent_convergence (both are FastMCP-based)

---

## 1. Tool Annotations (read_only, destructive, idempotent hints)

dbt-mcp uses `ToolAnnotations` on every tool:
```python
@dbt_mcp_tool(
    read_only_hint=True,
    destructive_hint=False,
    idempotent_hint=True,
    open_world_hint=True,
)
```

**Our gap:** organvm-mcp-server registers tools with `Tool(name=..., description=..., inputSchema=...)` but no behavioral annotations. Claude Code can't distinguish our read-only tools (pulse, metrics) from write tools (registry update, seed edit).

**Action:** Add `ToolAnnotations` to all 30+ tools in organvm-mcp-server. This is a mechanical pass — categorize each tool as read-only/destructive/idempotent.

## 2. Toolset Grouping with Enable/Disable

dbt-mcp groups tools into `Toolset` enums (SQL, SEMANTIC_LAYER, DISCOVERY, etc.) with per-toolset enable/disable via environment variables. At import time, `validate_tool_mapping()` ensures every tool belongs to a toolset.

**Our gap:** organvm-mcp-server has 30+ tools spread across 25 files with no grouping. You can't disable the governance tools without disabling everything. No validation that all tools are registered.

**Action:** Create toolset enum (GOVERNANCE, METRICS, CONTENT, COORDINATION, VERIFICATION, etc.) and map every tool. Add import-time validation. Add env var disable flags.

## 3. Prompt-as-File Pattern

Tool descriptions live as markdown files in `src/dbt_mcp/prompts/{category}/`:
```
prompts/
  discovery/
    get_mart_models.md
    get_all_models.md
  semantic_layer/
    list_metrics.md
```

Loaded via `get_prompt("discovery/get_mart_models")`. The prompt IS the tool's description.

**Our gap:** Tool descriptions are inline strings in Python code. Can't be edited, reviewed, or versioned independently. Can't be consumed by non-Python tooling.

**Action:** Extract all tool descriptions to `prompts/{category}/{tool_name}.md`. Load at registration time. This also enables A/B testing prompts without code changes.

## 4. Context Injection via Dependency Injection

dbt-mcp tools receive typed context objects (`SemanticLayerContext`, `DiscoveryContext`, etc.) via `adapt_context()`. The tool function declares what it needs; the registration pipeline injects it.

```python
@dbt_mcp_tool(...)
async def list_metrics(context: SemanticLayerContext) -> dict:
    return await context.client.list_metrics()
```

**Our gap:** organvm-mcp tools import modules directly and access global state. No dependency injection. Testing requires monkeypatching.

**Action:** Define context dataclasses per toolset. Wire injection at registration. This dramatically improves testability.

## 5. MCP Apps (UI Resources)

dbt-mcp bundles React UI components as MCP resources at `ui://` URIs. Tools can reference UI resources via `meta={"ui": {"resourceUri": "ui://dbt-mcp/my-app"}}`. The OAuth page we fixed IS an MCP App.

**Our gap:** organvm-mcp has no UI layer. The system dashboard exists separately (`meta-organvm/organvm-system-dashboard`). No MCP App integration.

**Action (future):** Bundle the system dashboard as an MCP App resource. Claude Desktop could render the ORGANVM dashboard inline when requesting system status.

---

*Absorbed: 2026-03-24. Source: contrib--dbt-mcp PR #669 + codebase study.*
*Cross-reference: organvm-mcp-server (meta-organvm), tool-interaction-design (ORGAN-IV)*
