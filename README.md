# RTL-Design-Analysis-Testbench-Generation
An automated ETL pipeline for hardware verification. Uses Python and Pyverilog to extract RTL metadata and Jinja2 to generate SystemVerilog testbenches

## 🛠️ Data Engineering & Automation
This project implements a robust **ETL (Extract, Transform, Load) pipeline** specifically designed for hardware design metadata.

* **Extraction:** Utilized `Pyverilog` to parse Verilog source code and extract AST (Abstract Syntax Tree) nodes representing hardware hierarchy.  
* **Transformation:** Developed a mapping logic to translate raw port-lists and signal declarations into structured Python dictionaries.  
* **Loading/Generation:** Orchestrated the automated generation of SystemVerilog testbenches using `Jinja2` templates, ensuring data consistency across the verification environment.  
* **Optimization:** Built a scalable metadata parser that handles large-scale RTL modules without manual schema mapping.  
