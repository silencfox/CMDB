import gradio as gr
import requests

API_URL = "http://knowledge_api:8001/ask"

def ask_question(question):
    try:
        response = requests.get(API_URL, params={"question": question})


        data = response.json()
        return data.get("answer", "No response")
    except Exception as e:
        return f"Error: {e}"

with gr.Blocks() as demo:
    gr.Markdown("# 🧠 Knowledge Base Assistant")
    with gr.Row():
        question = gr.Textbox(label="Enter your question")
    answer = gr.Textbox(label="Answer")
    submit = gr.Button("Ask")
    submit.click(ask_question, inputs=[question], outputs=[answer])

demo.launch(server_name="0.0.0.0", server_port=7860)
