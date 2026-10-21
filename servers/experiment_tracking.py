"""
Experiment Tracking MCP Server for NATO1000
Stub tools for logging and comparing ML experiment runs (W&B / MLflow style).
"""
from fastmcp import FastMCP
from typing import Dict, Any, List, Optional
from datetime import datetime
import uuid

mcp = FastMCP(name="NATO1000 Experiment Tracking")

runs: List[Dict] = []

@mcp.tool()
def log_run(name: str, metrics: Dict[str, float], params: Optional[Dict[str, Any]] = None, tags: Optional[List[str]] = None) -> Dict:
    """Log a new experiment run with metrics and parameters."""
    run = {
        "id": str(uuid.uuid4())[:8],
        "name": name,
        "timestamp": datetime.utcnow().isoformat(),
        "metrics": metrics,
        "params": params or {},
        "tags": tags or []
    }
    runs.append(run)
    return run

@mcp.tool()
def list_runs(limit: int = 20) -> List[Dict]:
    """List recent experiment runs."""
    return runs[-limit:]

@mcp.tool()
def compare_runs(run_ids: List[str], metric: str = "accuracy") -> Dict[str, Any]:
    """Compare specific runs by a metric."""
    selected = [r for r in runs if r["id"] in run_ids]
    if not selected:
        return {"error": "No matching runs"}
    sorted_runs = sorted(selected, key=lambda r: r["metrics"].get(metric, 0), reverse=True)
    return {
        "metric": metric,
        "best": sorted_runs[0]["name"] if sorted_runs else None,
        "ranking": [{"name": r["name"], "id": r["id"], metric: r["metrics"].get(metric)} for r in sorted_runs]
    }

if __name__ == "__main__":
    mcp.run()
