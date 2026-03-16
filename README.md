# 🏗️ Automated RTL Metadata & Verification Pipeline
### **Data Engineering | Hardware Automation**

A specialized ETL (Extract, Transform, Load) tool designed to automate the transition from RTL design to verification. This project parses Verilog source code to extract hardware schemas and programmatically generates SystemVerilog testbenches.

## 🔄 The Data Pipeline
1. **Extraction:** Uses `Pyverilog` to parse Verilog HDL into an Abstract Syntax Tree (AST), identifying ports, parameters, and module hierarchies.
2. **Transformation:** A custom Python wrapper processes the AST to map hardware signals into a structured dictionary (JSON-like schema).
3. **Loading:** The structured data is fed into `Jinja2` templates to generate syntactically correct SystemVerilog testbenches automatically.

## 🛠️ Tech Stack
* **Language:** Python 3.11
* **Parsing:** Pyverilog (AST Analysis)
* **Templating:** Jinja2
* **Hardware Target:** Verilog / SystemVerilog

## 📈 Impact
* **Automation:** Reduces manual testbench boilerplate creation by ~80%.
* **Consistency:** Eliminates human error in port-mapping and bit-width declarations during verification setup.
