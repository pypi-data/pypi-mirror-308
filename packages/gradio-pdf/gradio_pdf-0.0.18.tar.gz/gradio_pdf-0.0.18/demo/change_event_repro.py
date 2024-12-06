import gradio as gr
from gradio_pdf import PDF

def check_upload(file):
        print(f"Changed: {file}")

# Gradio Interface
with gr.Blocks() as interface:
    file_input = PDF()
    btn_input = gr.Button()
    
    btn_input.click(fn=check_upload, inputs=file_input)

interface.launch()
