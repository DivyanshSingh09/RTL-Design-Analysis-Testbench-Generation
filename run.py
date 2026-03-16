import os
import sys
from src.visualizer import get_rtl_metadata, visualize
from src.generator import generate_tb

def setup_output_dir(rtl_name):
    path = os.path.join('output', rtl_name)
    if not os.path.exists(path):
        os.makedirs(path)
    return path

def print_summary(data):
    print("\n" + "="*60)
    print(f" DESIGN ANALYSIS REPORT: {data['name'].upper()}")
    print("="*60)
    
    print(f"\n[INPUT PORTS]")
    print(f"{'WIDTH':<10} | {'SIGNAL NAME'}")
    print("-" * 30)
    for port in data['inputs']:
        print(f"{str(port['width']):<10} | {port['name']}")
    
    print(f"\n[OUTPUT PORTS]")
    print(f"{'WIDTH':<10} | {'SIGNAL NAME'}")
    print("-" * 30)
    for port in data['outputs']:
        print(f"{str(port['width']):<10} | {port['name']}")
    
    print(f"\n[TIMING AND CONTROL]")
    if not data['clocks'] and not data['resets']:
        print(" Logic Classification: Pure Combinational")
    else:
        clk = data['clocks'][0] if data['clocks'] else "None"
        rst = data['resets'][0] if data['resets'] else "None"
        print(f" Clock Signal: {clk}")
        print(f" Reset Signal: {rst}")
    
    if data['state_signals']:
        print(f"\n[FSM STRUCTURE]")
        print(f" State Register: {data['state_signals'][0]}")
        print(f" Defined States: {', '.join(data['parameters'].keys())}")
    
    print("\n" + "="*60 + "\n")

def select_rtl_file():
    rtl_dir = 'rtl'
    if not os.path.exists(rtl_dir):
        os.makedirs(rtl_dir)
        print(f"Directory '{rtl_dir}' created. Please place source files there.")
        return None

    files = [f for f in os.listdir(rtl_dir) if f.endswith('.v')]
    
    if not files:
        print("No Verilog source files (.v) detected in rtl/ directory.")
        return None

    print("AVAILABLE DESIGNS:")
    for i, file in enumerate(files, 1):
        print(f" {i}. {file}")
    
    try:
        choice = int(input("\nEnter index to analyze (0 to exit): "))
        if choice == 0:
            sys.exit()
        if 1 <= choice <= len(files):
            return files[choice-1]
        else:
            print("Error: Invalid index selected.")
            return None
    except ValueError:
        print("Error: Input must be a numerical index.")
        return None
    
def setup_output_dir(project_name, module_name):
    # Creates: output/full_subtractor/half_subtractor/
    path = os.path.join('output', project_name, module_name)
    if not os.path.exists(path):
        os.makedirs(path)
    return path

def main():
    while True:
        selected_file = select_rtl_file()
        if not selected_file: break

        rtl_path = os.path.join('rtl', selected_file)
        project_name = os.path.splitext(selected_file)[0] # e.g., 'full_subtractor'

        all_modules = get_rtl_metadata(rtl_path)

        if not all_modules:
            print("No modules found.")
            continue

        # Selection Logic
        if len(all_modules) > 1:
            print(f"\nDetected {len(all_modules)} modules in {selected_file}:")
            for i, mod in enumerate(all_modules, 1):
                print(f" [{i}] {mod['name']}")
            
            m_choice = int(input("\nSelect module to generate (0 to skip): "))
            if m_choice == 0: continue
            metadata = all_modules[m_choice-1]
        else:
            metadata = all_modules[0]

        # Nested folder creation
        # Now passing both project and module names
        out_dir = setup_output_dir(project_name, metadata['name'])
        
        print_summary(metadata)

        print(f"Generating artifacts in {out_dir}...")
        visualize(rtl_path, out_dir, target_module=metadata['name'])
        generate_tb(metadata, out_dir)

        print(f"Processing complete.\n")
        
        cont = input("Analyze another module? (y/n): ").lower()
        if cont != 'y': break

if __name__ == '__main__':
    main()