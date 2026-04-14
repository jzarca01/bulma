import typer
from io import BytesIO
import os
import base64
from psd_tools.api.layers import TypeLayer, PixelLayer

from services.label import Label
from services.psd import PSDService

app = typer.Typer()
psd = PSDService()


def get_label_size(layers):
    if len(layers) > 0:
        try:
            background_layer = psd.get_layer_by_name('background')
            if background_layer:
                return background_layer.size
        except:
            raise Exception("Cannot find background layer")
    else:
        raise Exception("No layers in PSD file")
    
@app.command()
def generate(file_path: str):
    if file_path.lower().endswith('.psd') is False:
        raise Exception("This program only supports PSD files")
    
    psd.process_psd(file_path)
    (label_width, label_height) = get_label_size(psd.get_layers())
    label = Label(width=int(label_width), height=int(label_height))
    
    for layer in psd.get_layers():
        print(layer)

        if isinstance(layer, PixelLayer):
            image = layer.composite()
            if image is not None: 
                if image.mode != 'RGBA':
                    image = image.convert('RGBA')
                buffer = BytesIO()
                image.save(buffer, format="PNG")
                base64_string = base64.b64encode(buffer.getvalue()).decode("utf-8")
            if layer.name == 'background':
                label.add_background(base64=base64_string)
            else:
                label.add_image(
                    width=layer.width,
                    height=layer.height,
                    y=layer.top,
                    x=layer.left,
                    base64=base64_string
                )
        elif isinstance(layer, TypeLayer):
            font_name, font_size, text = psd.get_font_properties(layer)
            if layer.name == 'date':
                label.add_text(
                    text="{{" + str(layer.name) + "}}",
                    width=int(layer.width),
                    y=int(layer.top),
                    x=int(layer.left),
                    font_size=font_size,
                    font_family=font_name,
                    fill="black",
                    dateFormat="DD/MM/YY"
                )
            else:
                label.add_text(
                    text="{{" + layer.name + "}}" if layer.name in label.valid_components else text,
                    width=layer.width,
                    y=layer.top,
                    x=layer.left,
                    font_size=font_size,
                    font_family=font_name,
                    fill="black",
                    dateFormat="DD/MM/YY"
                )
    label.save(f'{os.path.basename(file_path)}.json')



if __name__ == "__main__":
    app()
