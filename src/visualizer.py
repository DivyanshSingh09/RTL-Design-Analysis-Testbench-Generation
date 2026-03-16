import pyverilog.vparser.ast as vast
from pyverilog.vparser.parser import parse
from graphviz import Digraph
import os

class ASTVisualizer:
    def __init__(self):
        self.dot = Digraph(comment='RTL AST')

    def walk(self, node):
        node_id = str(id(node))
        label = node.__class__.__name__
        if hasattr(node, 'name') and node.name:
            label += f"\\n({node.name})"
        self.dot.node(node_id, label)
        for child in node.children():
            child_id = str(id(child))
            self.dot.edge(node_id, child_id)
            self.walk(child)

class RTLAnalyzer:
    def __init__(self):
        self.modules = []
        self.current_module = None

    def analyze(self, node):
        if isinstance(node, vast.ModuleDef):
            self.current_module = {
                "name": node.name,
                "parameters": {},
                "inputs": [],
                "outputs": [],
                "clocks": [],
                "resets": [],
                "state_signals": []
            }
            self.modules.append(self.current_module)

        if self.current_module:
            if isinstance(node, vast.Parameter):
                self.current_module["parameters"][node.name] = node.value.var.value
            elif isinstance(node, vast.Input):
                self.current_module["inputs"].append({"name": node.name, "width": self._get_width(node.width)})
            elif isinstance(node, vast.Output):
                self.current_module["outputs"].append({"name": node.name, "width": self._get_width(node.width)})
            elif isinstance(node, vast.Sens):
                if node.type in ('posedge', 'negedge'):
                    sig_name = node.sig.name
                    if "clk" in sig_name.lower():
                        if sig_name not in self.current_module["clocks"]: 
                            self.current_module["clocks"].append(sig_name)
                    elif "rst" in sig_name.lower():
                        if sig_name not in self.current_module["resets"]: 
                            self.current_module["resets"].append(sig_name)
            elif isinstance(node, vast.Case):
                if hasattr(node, 'cond') and isinstance(node.cond, vast.Identifier):
                    if node.cond.name not in self.current_module["state_signals"]:
                        self.current_module["state_signals"].append(node.cond.name)

        for child in node.children():
            self.analyze(child)

    def _get_width(self, width_node):
        if width_node is None: return "1"
        msb = width_node.msb.value if hasattr(width_node.msb, 'value') else "X"
        lsb = width_node.lsb.value if hasattr(width_node.lsb, 'value') else "X"
        return f"[{msb}:{lsb}]"

def get_rtl_metadata(file_path, out_dir=None):
    cache_dir = os.path.join(out_dir, ".parser_cache") if out_dir else ".parser_cache"
    if not os.path.exists(cache_dir): os.makedirs(cache_dir)
    
    ast, _ = parse([file_path], outputdir=cache_dir, debug=False)
    analyzer = RTLAnalyzer()
    analyzer.analyze(ast)
    return analyzer.modules # Returns the list of all found modules
        
    # We pass 'outputdir' to the parser
    ast, _ = parse(
        [file_path], 
        outputdir=cache_dir,
        debug=False
    )
    analyzer = RTLAnalyzer()
    analyzer.analyze(ast)
    return analyzer.module_info

def visualize(file_path, out_dir, target_module=None):
    os.environ["PATH"] += os.pathsep + r'C:\Program Files\Graphviz\bin'
    
    cache_dir = os.path.join(out_dir, ".parser_cache")
    ast, _ = parse([file_path], outputdir=cache_dir, debug=False)
    
    viz = ASTVisualizer()
    
    # Logic to find the specific module node
    start_node = ast
    if target_module:
        for item in ast.description.definitions:
            if isinstance(item, vast.ModuleDef) and item.name == target_module:
                start_node = item
                break
    
    viz.walk(start_node)
    
    # Save the file with the module name to avoid confusion
    filename = f'ast_{target_module}' if target_module else 'ast_output'
    output_path = os.path.join(out_dir, filename)
    
    viz.dot.render(output_path, format='png', cleanup=True)
    print(f"AST visualization for {target_module or 'full file'} saved.")

if __name__ == '__main__':
    rtl_file = os.path.join('rtl', 'traffic_light.v')
    if os.path.exists(rtl_file):
        visualize(rtl_file)
        data = get_rtl_metadata(rtl_file)
        print(f"Metadata extracted for: {data['name']}")