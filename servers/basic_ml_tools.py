"""
Basic AI/ML Tools MCP Server for NATO1000
Tools for dataset handling, simple metrics, and model card generation.
"""
from fastmcp import FastMCP
import json
from typing import Dict, Any

mcp = FastMCP(name="NATO1000 Basic ML Tools")

@mcp.tool()
def compute_metrics(predictions: list, labels: list) -> Dict[str, float]:
    """Compute basic classification metrics (accuracy, precision, recall)."""
    if len(predictions) != len(labels):
        raise ValueError("Predictions and labels must have same length")
    correct = sum(p == l for p, l in zip(predictions, labels))
    accuracy = correct / len(predictions) if predictions else 0.0
    # Simplified binary metrics example
    return {"accuracy": accuracy, "n_samples": len(predictions)}

@mcp.tool()
def generate_model_card(model_name: str, description: str, metrics: Dict[str, Any]) -> str:
    """Generate a simple Hugging Face style model card markdown."""
    card = f"""---
license: apache-2.0
tags:
- nato1000
- ai
- ml
---

# {model_name}

{description}

## Metrics

```json
{json.dumps(metrics, indent=2)}
```

## Usage

Integrate with NATO1000 runtime or standard Transformers.
"""
    return card

@mcp.tool()
def list_supported_frameworks() -> list:
    """List frameworks supported in NATO1000 ML toolset."""
    return ["transformers", "pytorch", "sklearn", "pandas", "fastmcp"]

if __name__ == "__main__":
    mcp.run()
