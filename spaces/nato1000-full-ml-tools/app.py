"""
NATO1000 Full AI/ML MCP Tools Gradio Space
Deploy under NaTo1000 on Hugging Face Spaces.
All functions have type hints + docstrings for automatic MCP exposure.
"""
import gradio as gr
import json
from typing import Dict, Any, List

def compute_classification_metrics(predictions: str, labels: str) -> str:
    """Compute accuracy and basic classification metrics from comma-separated values.
    
    Args:
        predictions: Comma-separated predictions e.g. 'cat,dog,cat'
        labels: Comma-separated ground truth labels
    """
    preds = [p.strip() for p in predictions.split(",") if p.strip()]
    labs = [l.strip() for l in labels.split(",") if l.strip()]
    if len(preds) != len(labs):
        return json.dumps({"error": "Length mismatch"})
    correct = sum(p == l for p, l in zip(preds, labs))
    acc = correct / len(preds) if preds else 0.0
    return json.dumps({
        "accuracy": round(acc, 4),
        "n_samples": len(preds),
        "n_correct": correct
    })

def compute_regression_metrics(predictions: str, labels: str) -> str:
    """Compute MAE, MSE, RMSE from comma-separated float values.
    
    Args:
        predictions: Comma-separated predicted floats
        labels: Comma-separated true floats
    """
    try:
        preds = [float(p.strip()) for p in predictions.split(",") if p.strip()]
        labs = [float(l.strip()) for l in labels.split(",") if l.strip()]
    except ValueError:
        return json.dumps({"error": "Invalid float values"})
    if len(preds) != len(labs) or not preds:
        return json.dumps({"error": "Length mismatch or empty"})
    errors = [abs(p - l) for p, l in zip(preds, labs)]
    sq = [(p - l)**2 for p, l in zip(preds, labs)]
    mae = sum(errors) / len(errors)
    mse = sum(sq) / len(sq)
    rmse = mse ** 0.5
    return json.dumps({
        "mae": round(mae, 4),
        "mse": round(mse, 4),
        "rmse": round(rmse, 4),
        "n_samples": len(preds)
    })

def route_task_to_specialist(task: str) -> str:
    """Route a task description to the most appropriate NATO1000 specialist.
    
    Args:
        task: Natural language description of the task
    """
    desc = task.lower()
    if any(w in desc for w in ["system", "debug", "diagnose", "error", "log"]):
        spec = "SENTINEL"
    elif any(w in desc for w in ["creative", "idea", "synthesize", "design", "generate"]):
        spec = "ALCHEMY"
    elif any(w in desc for w in ["strategy", "geopolit", "scenario", "war", "resource", "dominance"]):
        spec = "STRAT"
    elif any(w in desc for w in ["truth", "evidence", "provenance", "audit", "source"]):
        spec = "TRUTHMATRIX"
    else:
        spec = "DELIBERATOR"
    return json.dumps({
        "routed_to": spec,
        "task": task,
        "specialists": ["SENTINEL", "ALCHEMY", "STRAT", "DELIBERATOR", "TRUTHMATRIX"]
    })

def generate_model_card(name: str, description: str, tags: str = "nato1000,ai,ml") -> str:
    """Generate a Hugging Face style model card Markdown.
    
    Args:
        name: Model name
        description: Short description
        tags: Comma-separated tags
    """
    tag_list = [t.strip() for t in tags.split(",") if t.strip()]
    tag_yaml = "\n".join(f"- {t}" for t in tag_list)
    return f"""---
license: apache-2.0
tags:
{tag_yaml}
---

# {name}

{description}

## NATO1000 Integration

Compatible with the NATO1000 agentic runtime and MCP tool suite.
Deployable as Gradio Space or FastMCP server.

Maintainer: NaTo1000
"""

def list_tool_sets() -> str:
    """Return the full categorized list of tool sets for all AI/ML build types."""
    sets = {
        "1. Data Preparation & Feature Engineering": ["CSV/JSON/Parquet load", "Cleaning", "Encoding", "Splitting"],
        "2. Model Training & Fine-tuning": ["Hyperparam suggestion", "Config generation", "Checkpoint helpers"],
        "3. Evaluation & Metrics": ["Classification", "Regression", "NLP", "Ranking", "Model cards"],
        "4. Inference & Serving": ["Batch inference", "Quantization", "Endpoint configs", "Docker templates"],
        "5. RAG & Vector DBs": ["Chunking", "Embeddings", "Similarity", "Chroma/FAISS/Qdrant"],
        "6. Multimodal": ["Image prep", "Audio features", "Fusion", "Captioning templates"],
        "7. Agents & Orchestration": ["Specialist routing", "Multi-agent", "Tool chaining", "Memory"],
        "8. Experiment Tracking & MLOps": ["Logging", "Artifact registration", "Run comparison"],
        "9. Audit & Governance": ["Hash-linked events", "Provenance", "Quarantine", "TRUTHMATRIX"],
        "10. Hugging Face Ecosystem": ["Search", "Model cards", "Spaces MCP", "Inference"],
        "11. NLP / LLM": ["Tokenization", "Prompt templates", "CoT", "Few-shot"],
        "12. Computer Vision": ["Detection postproc", "Segmentation metrics", "Augmentation"],
        "13. Time Series": ["Rolling features", "Stationarity", "Forecast metrics"],
        "14. Reinforcement Learning": ["Env stubs", "Reward shaping", "Policy metrics"],
        "15. General Utilities": ["Schema validation", "Config merge", "Logging"]
    }
    return json.dumps(sets, indent=2)

with gr.Blocks(title="NATO1000 Full AI/ML MCP Tools") as demo:
    gr.Markdown("""
    # NATO1000 AI/ML MCP Tool Suite
    **Full tool sets for all types of AI/ML builds.**  
    Owner: [NaTo1000](https://huggingface.co/NaTo1000)  
    This Space is MCP-compatible. Connect any MCP client (Claude, Cursor, VS Code, etc.) to the MCP endpoint.
    """)
    
    with gr.Tab("Metrics"):
        gr.Markdown("### Classification & Regression Metrics")
        with gr.Row():
            pred_cls = gr.Textbox(label="Predictions", value="cat,dog,cat,bird")
            lab_cls = gr.Textbox(label="Labels", value="cat,dog,bird,bird")
        out_cls = gr.Textbox(label="Classification Result")
        gr.Button("Compute Classification").click(compute_classification_metrics, [pred_cls, lab_cls], out_cls)
        
        with gr.Row():
            pred_reg = gr.Textbox(label="Predictions (floats)", value="1.2,3.4,5.6")
            lab_reg = gr.Textbox(label="Labels (floats)", value="1.0,3.0,6.0")
        out_reg = gr.Textbox(label="Regression Result")
        gr.Button("Compute Regression").click(compute_regression_metrics, [pred_reg, lab_reg], out_reg)
    
    with gr.Tab("Orchestrator"):
        gr.Markdown("### Route tasks to NATO1000 specialists")
        task_box = gr.Textbox(label="Task description", lines=3, value="Diagnose why the training loss is not decreasing")
        route_out = gr.Textbox(label="Routing Result")
        gr.Button("Route Task").click(route_task_to_specialist, task_box, route_out)
    
    with gr.Tab("Model Card"):
        name_box = gr.Textbox(label="Model Name", value="NATO1000-ML-Tools")
        desc_box = gr.Textbox(label="Description", lines=4, value="Comprehensive MCP tool suite for AI/ML workflows")
        tags_box = gr.Textbox(label="Tags", value="nato1000,mcp,ml-tools")
        card_out = gr.Textbox(label="Generated Model Card", lines=15)
        gr.Button("Generate Card").click(generate_model_card, [name_box, desc_box, tags_box], card_out)
    
    with gr.Tab("Full Tool Sets List"):
        gr.Markdown("### Complete categorized tool sets for every build type")
        list_out = gr.Textbox(label="Tool Sets", lines=20)
        gr.Button("Show Full List").click(list_tool_sets, None, list_out)

if __name__ == "__main__":
    demo.launch(mcp_server=True, share=False)
