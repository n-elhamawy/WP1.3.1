# WP1.3.1
EMNESS System-Level Test Lab Course
This is a lab course to run a System-Level Test Framework (SLT) by testing a RISC-V processor: the Ibex Core. 
## Prerequisites
### Ibex RISC-V processor
Download the ibex core from `https://github.com/lowRISC/ibex`
### Tools 
Make sure that you have the tools that you need. The tools' versions are the ones for which the scripts have been tested. The scripts might also work with other versions.
- **Synthesis**: Design Compiler U-2022.12
- **Logic Simulator**: QuestaSim-64 vsim 2022.4
- **ATPG/Fault Simulator**: TMAX U-2022.12
## Getting started
Make sure to download this repository in the same directory as the ibex core. The top module is set to be the 'ibex_core'. 
### Logic Simulation
To compile the design and start simulation, run the ``make sim`` command.
### Pattern Extraction
The VCDE and VCD patterns need to be transferred to Standard Test Interface Language(STIL) format, in order to be able to load/unload the scan chains. 
`` make stil `` is the command to translate from one VCD(E) to STIL. __Note the *DEMO* variablle needs to be set. The design needs to have scan chains.__  
### Synthesis
Two options to perform the synthesis. `` make ibex_synth`` to synthesize the design without scan chains. To synthesize with scan chains use ``make ibex_synth_dft``.
### Test Protocol
The fault simulation and ATPG need a test protocol to be defined. The command `` make spf`` outputs a test protocol in STIL format that is used in the next steps.
To start the ATPG, run the command ``make atpg``.__Note: For design with scan chains__
### Fault Simulation
To start the fault simulation for the 'hello_test' pattern set and the stuck-at fault model, run the command ``make slt``. __Note: The design needs to have scan chains.__
### Variables
The test objects can change and therefore there are different variables for different things to be tested.
- *TOP_MODULE*: is the module under test
- *DEMO*: is the name of the slt workload
- *SRAMInitFile*: the memory file to be preloaded, needs to be in hex format. Otherwise, the `mem load` command needs to be updated. 
- *FOUNDRY_PATH*: the path to the desired technology library
- *TECH_NAME*: the name of the technology library
### Usage
``make sim TOP_MODULE=ibex_core DEMO=hello_test SRAMInitFile=examples/sw/simple_system/hello_test/hello_test.vmem FOUNDRY_PATH=/path/to/tech_lib TECH_NAME=NangateOpenCellLibrary_typical PDK_Verilog=/path/to/tech_lib/NangateOpenCellLibrary.v``
