"""
NATO1000 Enhanced Core ML Tools MCP Server
Full tools for evaluation, model cards, frameworks, and more.
"""
from fastmcp import FastMCP
from typing import Dict, Any, List, Optional
import json
import statistics
import math

mcp = FastMCP(name="NATO1000 Core ML Tools")

@mcp.tool()
def compute_classification_metrics(predictions: List[Any], labels: List[Any]) -> Dict[str, float]:
    """Compute accuracy, precision, recall, F1 for binary/multiclass classification."""
    if len(predictions) != len(labels):
        raise ValueError("Predictions and labels must be the same length")
    if not predictions:
        return {"accuracy": 0.0, "n_samples": 0}
    
    # Basic accuracy
    correct = sum(p == l for p, l in zip(predictions, labels))
    accuracy = correct / len(predictions)
    
    # For binary (assuming first unique as positive if needed)
    unique = list(set(labels + predictions))
    if len(unique) == 2:
        pos = unique[0]
        tp = sum(p == pos and l == pos for p, l in zip(predictions, labels))
        fp = sum(p == pos and l != pos for p, l in zip(predictions, labels))
        fn = sum(p != pos and l == pos for p, l in zip(predictions, labels))
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0
        f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
        return {
            "accuracy": round(accuracy, 4),
            "precision": round(precision, 4),
            "recall": round(recall, 4),
            "f1": round(f1, 4),
            "n_samples": len(predictions)
        }
    
    return {
        "accuracy": round(accuracy, 4),
        "n_samples": len(predictions),
        "n_correct": correct,
        "note": "Multiclass - use per-class metrics for full detail"
    }

@mcp.tool()
def compute_regression_metrics(predictions: List[float], labels: List[float]) -> Dict[str, float]:
    """Compute MAE, MSE, RMSE, R2 for regression."""
    if len(predictions) != len(labels):
        raise ValueError("Length mismatch")
    if not predictions:
        return {"mae": 0.0, "mse": 0.0, "rmse": 0.0, "r2": 0.0}
    
    errors = [abs(p - l) for p, l in zip(predictions, labels)]
    sq_errors = [(p - l)**2 for p, l in zip(predictions, labels)]
    mae = statistics.mean(errors)
    mse = statistics.mean(sq_errors)
    rmse = math.sqrt(mse)
    
    # R2
    mean_label = statistics.mean(labels)
    ss_tot = sum((l - mean_label)**2 for l in labels)
    ss_res = sum(sq_errors)
    r2 = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0
    
    return {
        "mae": round(mae, 4),
        "mse": round(mse, 4),
        "rmse": round(rmse, 4),
        "r2": round(r2, 4),
        "n_samples": len(predictions)
    }

@mcp.tool()
def generate_model_card(
    model_name: str,
    description: str,
    metrics: Optional[Dict[str, Any]] = None,
    tags: Optional[List[str]] = None,
    license: str = "apache-2.0",
    datasets: Optional[List[str]] = None
) -> str:
    """Generate a complete Hugging Face style model card in Markdown."""
    tags = tags or ["nato1000", "ai", "ml", "mcp"]
    datasets = datasets or []
    metrics_str = json.dumps(metrics or {}, indent=2)
    
    card = f"""---
license: {license}
tags:
{chr(10).join(f"- {t}" for t in tags)}
datasets:
{chr(10).join(f"- {d}" for d in datasets) if datasets else "# none"}
---

# {model_name}

{description}

## Model Details

- **Developer**: NaTo1000 / NATO1000
- **Type**: AI/ML component for agentic workflows
- **Status**: Compatible with FastMCP and Gradio MCP Spaces

## Metrics

```json
{metrics_str}
```

## Intended Use

Designed for integration into NATO1000 specialist runtimes (SENTINEL, ALCHEMY, STRAT, DELIBERATOR, TRUTHMATRIX) and standard ML pipelines.

## Limitations

Stubs and helpers - replace with production model backends for real inference.

## Citation

```bibtex
@misc{{nato1000-ml-tools,
  author = {{NaTo1000}},
  title = {{{model_name}}},
  year = {{2026}},
  publisher = {{Hugging Face}},
  howpublished = {{\\url{{https://huggingface.co/NaTo1000}}}}
}}
```
"""
    return card

@mcp.tool()
def list_ml_frameworks() -> List[Dict[str, str]]:
    """List major ML frameworks with use cases for NATO1000 builds."""
    return [
        {"name": "transformers", "use": "LLMs, fine-tuning, inference"},
        {"name": "pytorch", "use": "Core training and custom models"},
        {"name": "tensorflow", "use": "Production serving, TFLite"},
        {"name": "jax", "use": "Research, high-performance"},
        {"name": "sklearn", "use": "Classical ML, baselines"},
        {"name": "pandas / polars", "use": "Data processing"},
        {"name": "optuna", "use": "Hyperparameter optimization"},
        {"name": "mlflow / wandb", "use": "Experiment tracking"},
        {"name": "huggingface_hub", "use": "Model/dataset management"},
        {"name": "vllm / tgi", "use": "High-throughput inference"},
        {"name": "fastmcp / gradio", "use": "MCP server exposure"}
    ]

@mcp.tool()
def suggest_hyperparameters(task_type: str, model_size: str = "medium") -> Dict[str, Any]:
    """Suggest starting hyperparameters for common ML tasks."""
    suggestions = {
        "classification": {"lr": 2e-5, "batch_size": 32, "epochs": 5, "optimizer": "AdamW"},
        "regression": {"lr": 1e-4, "batch_size": 64, "epochs": 10, "optimizer": "Adam"},
        "nlp-finetune": {"lr": 5e-5, "batch_size": 16, "epochs": 3, "warmup_ratio": 0.1},
        "vision": {"lr": 1e-4, "batch_size": 32, "epochs": 20, "scheduler": "cosine"},
        "rl": {"lr": 3e-4, "batch_size": 64, "epochs": 100, "gamma": 0.99}
    }
    base = suggestions.get(task_type.lower(), suggestions["classification"])
    if model_size == "large":
        base["lr"] = base["lr"] / 2
        base["batch_size"] = base["batch_size"] * 2
    return {"task": task_type, "suggested": base, "note": "Tune further with Optuna or manual sweeps"}

if __name__ == "__main__":
    mcp.run()
