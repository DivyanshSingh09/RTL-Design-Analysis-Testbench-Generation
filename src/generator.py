from jinja2 import Environment, FileSystemLoader
from src.visualizer import get_rtl_metadata
import os

def generate_tb(data, out_dir):
    # Adjust loader path because script is now in src/
    template_path = os.path.join(os.path.dirname(__file__), '../templates')
    env = Environment(loader=FileSystemLoader(template_path))
    template = env.get_template('tb_template.sv')
    
    output = template.render(data)
    
    filename = f"tb_{data['name']}.sv"
    with open(os.path.join(out_dir, filename), 'w') as f:
        f.write(output)

if __name__ == '__main__':
    rtl_file = os.path.join('rtl', 'traffic_light.v')
    if os.path.exists(rtl_file):
        metadata = get_rtl_metadata(rtl_file)
        generate_tb(metadata)