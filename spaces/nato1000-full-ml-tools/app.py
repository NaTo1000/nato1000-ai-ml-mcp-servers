"""
Gradio MCP Space for NATO1000 Full AI/ML Tool Suite
Deploy on Hugging Face Spaces (Gradio) under NaTo1000.
Uses demo.launch(mcp_server=True) for native MCP exposure.
"""
import gradio as gr
import json

def compute_metrics(predictions: str, labels: str) -> str:
    preds = [p.strip() for p in predictions.split(",") if p.strip()]
    labs = [l.strip() for l in labels.split(",") if l.strip()]
    if len(preds) != len(labs):
        return json.dumps({"error": "Length mismatch"})
    correct = sum(p == l for p, l in zip(preds, labs))
    acc = correct / len(preds) if preds else 0
    return json.dumps({"accuracy": round(acc, 4), "n_samples": len(preds)})

def route_task(task: str) -> str:
    desc = task.lower()
    if any(w in desc for w in ["system", "debug", "diagnose"]):
        spec = "SENTINEL"
    elif any(w in desc for w in ["creative", "idea", "synthesize"]):
        spec = "ALCHEMY"
    elif any(w in desc for w in ["strategy", "geopolit", "scenario"]):
        spec = "STRAT"
    else:
        spec = "DELIBERATOR"
    return json.dumps({"routed_to": spec, "task": task})

def generate_model_card(name: str, description: str) -> str:
    return f"""---
license: apache-2.0
tags:
- nato1000
---
# {name}

{description}

Part of the NATO1000 / NaTo1000 AI/ML MCP suite.
"""

with gr.Blocks(title="NATO1000 Full AI/ML MCP Tools") as demo:
    gr.Markdown("# NATO1000 AI/ML MCP Tool Suite\nFull set of tools for different build types. Ready for MCP clients via Gradio.")
    with gr.Tab("Metrics"):
        pred = gr.Textbox(label="Predictions (comma-separated)", value="cat,dog,cat")
        lab = gr.Textbox(label="Labels (comma-separated)", value="cat,dog,bird")
        out = gr.Textbox(label="Result")
        gr.Button("Compute").click(compute_metrics, [pred, lab], out)
    with gr.Tab("Orchestrator"):
        task_box = gr.Textbox(label="Task", lines=3)
        route_out = gr.Textbox(label="Routing Result")
        gr.Button("Route").click(route_task, task_box, route_out)
    with gr.Tab("Model Card"):
        name_box = gr.Textbox(label="Model Name")
        desc_box = gr.Textbox(label="Description", lines=4)
        card_out = gr.Textbox(label="Model Card", lines=12)
        gr.Button("Generate").click(generate_model_card, [name_box, desc_box], card_out)

if __name__ == "__main__":
    demo.launch(mcp_server=True)
