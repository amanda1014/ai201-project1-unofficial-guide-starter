"""
app.py - Milestone 5: Gradio web interface (UCF-themed) for the housing Q&A system.
"""
import gradio as gr
from query import ask

UCF_BLACK = "#0a0a0a"
UCF_GOLD = "#BA9B37"

theme = gr.themes.Base(
    primary_hue=gr.themes.colors.yellow,
    neutral_hue=gr.themes.colors.gray,
).set(
    body_background_fill=UCF_BLACK,
    body_text_color="#ffffff",
    block_background_fill="#161616",
    block_border_color=UCF_GOLD,
    block_label_text_color=UCF_GOLD,
    block_title_text_color=UCF_GOLD,
    input_background_fill="#222222",
    input_border_color="#444444",
    button_primary_background_fill=UCF_GOLD,
    button_primary_background_fill_hover="#d4b94a",
    button_primary_text_color="#000000",
)

CUSTOM_CSS = """
.gradio-container {max-width: 860px !important; margin: auto;}
#title h1 {text-align: center; color: #BA9B37; letter-spacing: 1px;}
#subtitle {text-align: center; color: #dddddd;}
footer {visibility: hidden;}

/* Make example chips readable on the dark background */
.gradio-container .examples table td,
.gradio-container [class*="example"] {
    color: #ffffff !important;
    background: #222222 !important;
    border: 1px solid #BA9B37 !important;
}
.gradio-container [class*="example"]:hover {
    background: #BA9B37 !important;
    color: #000000 !important;
}
"""
UCF_MAP = """
<iframe width="100%" height="300" frameborder="0" scrolling="no"
  src="https://www.openstreetmap.org/export/embed.html?bbox=-81.25%2C28.57%2C-81.15%2C28.63&layer=mapnik&marker=28.6024%2C-81.2001"
  style="border-radius:12px;border:1px solid #BA9B37;"></iframe>
<p style="text-align:center;color:#888;font-size:0.85em;">UCF & surrounding off-campus area</p>
"""


def handle_query(question):
    if not question or not question.strip():
        return "Please enter a question.", ""
    result = ask(question)
    sources = "\n".join(f"• {s}" for s in result["sources"])
    return result["answer"], sources


with gr.Blocks(title="UCF Off-Campus Housing Guide") as demo:

    gr.Markdown("# ⭐ The Unofficial Guide", elem_id="title")
    gr.Markdown(
        "#### UCF Off-Campus Housing — answered by real students\n"
        "Every answer is grounded only in real student Reddit discussions, "
        "with the source documents shown so you can check them.",
        elem_id="subtitle",
    )

    with gr.Group():
        inp = gr.Textbox(
            label="Your question",
            placeholder="e.g. What do students say about Northgate Lakes?",
            lines=2,
        )
        btn = gr.Button("Ask", variant="primary", size="lg")

    answer = gr.Textbox(label="💬 Answer", lines=8)
    sources = gr.Textbox(label="📄 Retrieved from", lines=4)

    gr.Examples(
        examples=[
            "What do students say about Northgate Lakes?",
            "Which apartments are affordable, under about $1100 a month?",
            "Is Knights Circle or Accolade better for a quiet apartment?",
            "What is the pet policy at Knights Circle?",
        ],
        inputs=inp,
    )

    gr.HTML(UCF_MAP)

    btn.click(handle_query, inputs=inp, outputs=[answer, sources])
    inp.submit(handle_query, inputs=inp, outputs=[answer, sources])


if __name__ == "__main__":
    demo.launch(theme=theme, css=CUSTOM_CSS)