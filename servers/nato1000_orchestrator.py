from fastmcp import FastMCP
from typing import Dict, Any

mcp = FastMCP(name="NATO1000 Orchestrator")

SPECIALISTS = {
    "SENTINEL": "Systems engineering and diagnostics",
    "ALCHEMY": "Creative synthesis and ideation",
    "STRAT": "Geopolitical and strategic analysis",
    "DELIBERATOR": "Multi-perspective comparison",
    "TRUTHMATRIX": "Provenance and evidence organization"
}

@mcp.tool()
def list_specialists() -> Dict[str, str]:
    """List available NATO1000 specialist adapters."""
    return SPECIALISTS

@mcp.tool()
def route_task(task: str, specialist: str = "auto") -> Dict[str, Any]:
    """Route a task to a specialist."""
    if specialist == "auto":
        task_lower = task.lower()
        if any(k in task_lower for k in ["system", "debug", "diagnose"]):
            specialist = "SENTINEL"
        elif any(k in task_lower for k in ["create", "idea", "design"]):
            specialist = "ALCHEMY"
        elif any(k in task_lower for k in ["strategy", "geo", "war", "resource"]):
            specialist = "STRAT"
        else:
            specialist = "DELIBERATOR"
    desc = SPECIALISTS.get(specialist, "Unknown")
    return {
        "routed_to": specialist,
        "description": desc,
        "task": task,
        "note": "In production, this would call the actual model adapter via NATO1000 runtime."
    }

if __name__ == "__main__":
    mcp.run()
