"""
NATO1000 Core ML Tools MCP Server
Comprehensive tools for model evaluation, card generation, framework utilities.
"""
from fastmcp import FastMCP
from typing import Dict, Any, List
import json
import statistics

mcp = FastMCP(name="NATO1000 Core ML Tools")

@mcp.tool()
def compute_classification_metrics(predictions: List[Any], labels: List[Any]) -> Dict[str, float]:
    """Compute accuracy and basic stats for classification predictions vs labels."""
    if len(predictions) != len(labels):
        raise ValueError("Predictions and labels must be the same length")
    if not predictions:
        return {"accuracy": 0.0, "n_samples": 0}
    correct = sum(p == l for p, l in zip(predictions, labels))
    accuracy = correct / len(predictions)
    return {
        "accuracy": round(accuracy, 4),
        "n_samples": len(predictions),
        "n_correct": correct
    }

@mcp.tool()
def compute_regression_metrics(predictions: List[float], labels: List[float]) -> Dict[str, float]:
    """Compute MAE, MSE, RMSE for regression."""
    if len(predictions) != len(labels):
        raise ValueError("Length mismatch")
    if not predictions:
        return {"mae": 0.0, "mse": 0.0, "rmse": 0.0}
    errors = [abs(p - l) for p, l in zip(predictions, labels)]
    sq_errors = [(p - l)**2 for p, l in zip(predictions, labels)]
    mae = statistics.mean(errors)
    mse = statistics.mean(sq_errors)
    rmse = mse ** 0.5
    return {"mae": round(mae, 4), "mse": round(mse, 4), "rmse": round(rmse, 4)}

@mcp.tool()
def generate_model_card(model_name: str, description: str, metrics: Dict[str, Any] = None, tags: List[str] = None) -> str:
    """Generate a Hugging Face style model card in Markdown."""
    tags = tags or ["nato1000", "ai", "ml"]
    metrics_str = json.dumps(metrics or {}, indent=2)
    card = f"""---
license: apache-2.0
tags:
{chr(10).join(f"- {t}" for t in tags)}
---

# {model_name}

{description}

## Metrics

```json
{metrics_str}
```

## Usage

Compatible with NATO1000 runtime, Transformers, and standard ML frameworks.
"""
    return card

@mcp.tool()
def list_ml_frameworks() -> List[str]:
    """List major ML frameworks relevant to NATO1000 builds."""
    return [
        "transformers", "pytorch", "tensorflow", "jax", "sklearn",
        "pandas", "polars", "optuna", "mlflow", "huggingface_hub"
    ]

if __name__ == "__main__":
    mcp.run()
