import gradio as gr
import numpy as np
from gradio_pointcloudeditor import PointCloudEditor

with gr.Blocks() as demo:
    point_size = gr.Slider(
        minimum=0.01, maximum=1.0, value=0.2, step=0.01, label="Point Size"
    )

    pce = PointCloudEditor()
    input_textbox = gr.Textbox(
        label="Point Cloud Input",
        placeholder="Enter points as: x,y,z,r,g,b,x,y,z,r,g,b,...",
        interactive=True,
    )
    output_textbox = gr.Textbox(label="Point Cloud Output", interactive=False)

    # Input textbox to PCE connection
    input_textbox.change(fn=lambda x: x, inputs=input_textbox, outputs=pce)

    # Point size slider to PCE connection
    point_size.change(
        fn=lambda x: gr.update(point_size=x), inputs=point_size, outputs=pce
    )

    # PCE to output textbox connection
    def format_output(data):
        positions = data["positions"]
        colors = data["colors"]

        if len(positions) != len(colors):
            print("Mismatched positions and colors lengths")
            return ""

        # Format with higher precision
        # Convert positions and colors to flat list alternating between position and color
        full_list = []
        for pos, col in zip(positions, colors):
            full_list.extend([*pos, *col])
        output = ",".join([str(item) for item in full_list])
        return output

    pce.edit(
        fn=format_output,
        inputs=pce,
        outputs=output_textbox,
        show_progress=False,  # Add this to see if it helps with updates
    )

    # Examples
    gr.Examples(
        examples=[
            "0,0,0,1,0,0,1,0,0,0,1,0,0,1,0,0,0,1",  # Three points with RGB colors
            "0,0,0,1,0,0,0,0.5,1,0.2,1,0.5,0,0,1,0.4,0.2,0.2,",  # Another set of points
            ",".join(
                [str(x) for x in (np.random.rand(6 * 20) * 2 - 1)]
            ),  # Random points
        ],
        inputs=input_textbox,
    )

if __name__ == "__main__":
    demo.launch()
