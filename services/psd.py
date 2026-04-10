from psd_tools import PSDImage

class PSDService:
    def __init__(self):
        self.layers = []
        self.valid_layers = ['background', 'country', 'region', 'beanName', 'process', 'variety', 'flavors', 'date']
        self.valid_layers = ['background', 'country', 'region', 'beanName', 'process', 'variety', 'flavors', 'date']

    def process_psd(self, file_path):
        print(f"Processing PSD file: {file_path}")
        psd = PSDImage.open(file_path)
        psd.composite().save('example.png')

        if psd._layers:
            self.layers = psd._layers
            for layer in psd:
                print(layer)
                layer_image = layer.composite()
                print(layer_image.getdata())

    def get_layers(self):
        return self.layers
    
    def check_required_layers(self, required_layer_names):
        missing_layers = [name for name in required_layer_names if name not in [layer.name for layer in self.layers]]
        if missing_layers:
            print(f"Missing required layers: {', '.join(missing_layers)}")
        else:
            print("All required layers are present.")