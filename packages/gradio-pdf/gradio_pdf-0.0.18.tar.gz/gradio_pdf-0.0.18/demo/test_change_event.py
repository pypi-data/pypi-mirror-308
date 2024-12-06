import gradio as gr
from gradio_pdf import PDF

with gr.Blocks() as demo:
    with gr.Row():
        with gr.Column():
            pdf = PDF(label="Document")
        with gr.Column():
            num_change_events = gr.Label(value=0, label="Number of change events")
            num_upload_events = gr.Label(value=0, label="Number of upload events")
        pdf.change(lambda x: int(x) + 1, num_change_events, num_change_events)
        pdf.upload(lambda x: int(x) + 1, num_upload_events, num_upload_events)

demo.launch()