import gradio as gr

def suite_info():
    return "# NATO1000 AI/ML MCP Servers Suite\n\nFull collection of MCP servers for all types of AI/ML builds.\n\nSee https://github.com/NaTo1000/nato1000-ai-ml-mcp-servers"

demo = gr.Interface(fn=suite_info, inputs=[], outputs=gr.Markdown(), title="NATO1000 AI/ML MCP Servers")

if __name__ == "__main__":
    demo.launch(mcp_server=True)
