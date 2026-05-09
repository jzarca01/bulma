from pathlib import Path

from psd_tools import PSDImage
from psd_tools.api.layers import TypeLayer
from PIL import Image

class PSDService:
    def __init__(self):
        self.psd = None
        self.layers = []

    def process_psd(self, file_path):
        try:
            self.psd = PSDImage.open(file_path)
            self.layers = self.psd._layers
        except Exception as e:
            raise Exception(f"Failed to process PSD: {e}")

    def get_layers(self):
        return self.layers
    
    def get_layer_by_name(self, layer_name: str):
        if not self.psd:
            return None
        for layer in self.psd.descendants():
            if layer.name == layer_name:
                return layer
        return None

    def get_font_properties(self, layer):
        if not isinstance(layer, TypeLayer):
            return None, None, None
            
        engine_dict = layer.engine_dict
        if not engine_dict:
            return None, None, None

        try:
            styles = engine_dict['StyleRun']['RunArray'][0]['StyleSheet']['StyleSheetData']
            font_size = int(styles.get('FontSize'))
            
            text = layer.engine_dict['Editor']['Text'].value
            fontset = layer.resource_dict['FontSet']
            runlength = layer.engine_dict['StyleRun']['RunLengthArray']
            rundata = layer.engine_dict['StyleRun']['RunArray']
            index = 0
            font_name = None
            for length, style in zip(runlength, rundata):
                stylesheet = style['StyleSheet']['StyleSheetData']
                font = fontset[stylesheet['Font']]
                index += length
                font_name = str(font["Name"])
                
            return font_name, font_size, text

        except (KeyError, IndexError, TypeError):
            return None, None, None
        
    def export_to_png(self, file_path):
        merged_image = self.psd.topil()
        output_path = str(Path(file_path + '.png').resolve())
        merged_image.save(output_path)
        return output_path

    def crop_png(self, file_path, left, top, right, bottom):
        original = Image.open(file_path)
        cropped_example = original.crop((left, top, right, bottom))
        cropped_example.save(file_path)