import gradio as gr
import requests
import os
import uuid   

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8080")


SESSION_ID = str(uuid.uuid4())

def process_invoice(file):
    if file is None:
        return "No file uploaded", ""

    files = {"file": (file.name, file.read())}
    data = {"session_id": SESSION_ID}  
    resp = requests.post(f"{BACKEND_URL}/process", files=files, data=data)
    if resp.status_code == 200:
        result = resp.json()
        extracted = result.get("data")
        insights = result.get("insights")
        return extracted, insights
    else:
        return "Processing failed. Check backend logs.", ""

def chat_with_agent(prompt):
    if not prompt:
        return "Please enter a question."
    
    data = {
        "prompt": prompt,
        "session_id": SESSION_ID  
    }

    resp = requests.post(f"{BACKEND_URL}/chat", data=data)
    if resp.ok:
        return resp.json().get("reply")
    else:
        return "Chat failed"

with gr.Blocks(title="Smart Invoice Summarizer") as demo:

    gr.Markdown("# **Smart Invoice Summarizer & Expense Insights**")

    with gr.Tab("Upload Invoice"):
        file_input = gr.File(label="Upload invoice (PDF / image)")
        extract_output = gr.JSON(label="Extracted Data")
        insights_output = gr.Textbox(label="Insights", lines=5)

        process_btn = gr.Button("Process Invoice")

        process_btn.click(
            fn=process_invoice,
            inputs=file_input,
            outputs=[extract_output, insights_output]
        )

    with gr.Tab("Chat with Agent"):
        prompt = gr.Textbox(label="Ask a question about the invoice or expenses")
        chat_btn = gr.Button("Send")
        reply_box = gr.Textbox(label="Agent Reply", lines=4)

        chat_btn.click(
            fn=chat_with_agent,
            inputs=prompt,
            outputs=reply_box
        )

demo.launch()
