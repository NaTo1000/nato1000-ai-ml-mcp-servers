"""
Evaluation & Metrics MCP Server for NATO1000
Tools for classification, regression, and model comparison.
"""
from fastmcp import FastMCP
from typing import List, Dict, Any
import statistics

mcp = FastMCP(name="NATO1000 Evaluation Tools")

@mcp.tool()
def classification_metrics(y_true: List[int], y_pred: List[int]) -> Dict[str, float]:
    """Compute accuracy, precision, recall, F1 for binary classification (0/1)."""
    if len(y_true) != len(y_pred):
        raise ValueError("Length mismatch")
    tp = sum(1 for t, p in zip(y_true, y_pred) if t == 1 and p == 1)
    fp = sum(1 for t, p in zip(y_true, y_pred) if t == 0 and p == 1)
    fn = sum(1 for t, p in zip(y_true, y_pred) if t == 1 and p == 0)
    tn = sum(1 for t, p in zip(y_true, y_pred) if t == 0 and p == 0)
    accuracy = (tp + tn) / len(y_true) if y_true else 0
    precision = tp / (tp + fp) if (tp + fp) else 0
    recall = tp / (tp + fn) if (tp + fn) else 0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) else 0
    return {
        "accuracy": round(accuracy, 4),
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1": round(f1, 4),
        "support": len(y_true)
    }

@mcp.tool()
def regression_metrics(y_true: List[float], y_pred: List[float]) -> Dict[str, float]:
    """Compute MAE, MSE, RMSE, R2 for regression."""
    if len(y_true) != len(y_pred):
        raise ValueError("Length mismatch")
    n = len(y_true)
    errors = [t - p for t, p in zip(y_true, y_pred)]
    mae = sum(abs(e) for e in errors) / n
    mse = sum(e**2 for e in errors) / n
    rmse = mse ** 0.5
    mean_true = sum(y_true) / n
    ss_tot = sum((t - mean_true)**2 for t in y_true)
    ss_res = sum(e**2 for e in errors)
    r2 = 1 - (ss_res / ss_tot) if ss_tot else 0
    return {
        "mae": round(mae, 4),
        "mse": round(mse, 4),
        "rmse": round(rmse, 4),
        "r2": round(r2, 4)
    }

@mcp.tool()
def compare_models(metrics_list: List[Dict[str, float]], model_names: List[str]) -> Dict[str, Any]:
    """Compare multiple models by a primary metric (highest is better)."""
    if len(metrics_list) != len(model_names):
        raise ValueError("Mismatch")
    best_idx = max(range(len(metrics_list)), key=lambda i: list(metrics_list[i].values())[0] if metrics_list[i] else 0)
    return {
        "best_model": model_names[best_idx],
        "best_metrics": metrics_list[best_idx],
        "all_results": dict(zip(model_names, metrics_list))
    }

if __name__ == "__main__":
    mcp.run()
