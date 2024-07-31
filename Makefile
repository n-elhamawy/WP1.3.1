SRAMInitFile 					?=
TOP_MODULE 						?= ibex_core
PREFIX 								?=	/ibex_simple_system/u_top/u_ibex_top/u_ibex_core/
SCAN_CHAIN_FILE 			?= TMAX/Netlists/def_${TOP_MODULE}.txt
DEMO 									?= hello_test
SPF_FILE							?= ./TMAX/Netlists/testProtocol_${TOP_MODULE}_synth_dft.spf
VCDE_FILE 						:= $(TOP_MODULE).vcde
VCD_SCAN_FILE 				:= $(TOP_MODULE)_scan.vcd
FOUNDRY_PATH         	?= /NanGate45
TECH_NAME            	?= NangateOpenCellLibrary_typical
TARGET_LIBRARY_FILES   = $(TECH_NAME).db
SCAN_COUNT           	?= 1
PDK_Verilog						 = NangateOpenCellLibrary.v
OUTPUT_DIR						 = TMAX

ifeq ($(MAKECMDGOALS),ibex_core_dft)
	NETLIST_FILE				 := ibex_top_synth_dft.v
	SPF_FILE						 := testProtocol_ibex_top_dft.spf
else
	NETLIST_FILE				 := ibex_top_synth.v
endif
 
EXPORT_LIST=SNPSLMD_QUEUE=TRUE TECH_NAME=$(TECH_NAME) TOP_MODULE=$(DESIGN_NAME) DESIGN_NAME=$(DESIGN_NAME) TERM=vt100 PERIOD=$(PERIOD) FOUNDRY_PATH=$(FOUNDRY_PATH) TARGET_LIBRARY_FILES=$(TARGET_LIBRARY_FILES) INPUT_DELAY=$(INPUT_DELAY) OUTPUT_DELAY=$(OUTPUT_DELAY) SCAN_COUNT=$(SCAN_COUNT) NETLIST_FILE=$(NETLIST_FILE) PDK_Verilog=$(PDK_Verilog) SPF_FILE=$(SPF_FILE) OUTPUT_DIR=$(OUTPUT_DIR) 

ifndef FOUNDRY_PATH
  $(error "Please provide FOUNDRY techno")
endif
ifndef TECH_NAME
  $(error "Please provide TECH_NAME techno")
endif


library 					:= ./build/lowrisc_ibex_ibex_simple_system_0/sim-questa	
compile_flag			+= -sv +define+RVFI -nologo -quiet -suppress 13262 -permissive -suppress 2583 -suppress 13314 -timescale " 1ns/ 10ps"
questa_flags			+= -t 1ns -suppress 12130

ifdef SRAMInitFile 
	questa_flags			+= -do "mem load -infile $(SRAMInitFile) -format hex /ibex_simple_system/u_ram/u_ram/gen_generic/u_impl_generic/mem; vcd dumpports -file ${TOP_MODULE}.vcde /ibex_simple_system/u_top/u_ibex_top/u_ibex_core/if_stage_i/*; vcd file ${TOP_MODULE}_scan.vcd; do ${TOP_MODULE}_scanWaves.do; run -all; "
endif
	
$(library):
	vlib $(library)

build: $(library)
	vlog $(compile_flag) -work $(library) -f ibex_simple_system_compile.f +incdir+./vendor/lowrisc_ip/ip/prim/rtl/+incdir+./vendor/lowrisc_ip/dv/sv/dv_utils/
	vopt $(compile_flag) -work $(library) ibex_simple_system -o simple_system_tb_optimized +acc -debug	

sim: build
	vsim $(questa_flags) +permissive -lib $(library) simple_system_tb_optimized

waveFile:
	python3 scripts/python_scripts/waveFile.py $(TOP_MODULE) $(PREFIX) $(SCAN_CHAIN_FILE)

spf:
	@export $(EXPORT_LIST);	tmax -sh scripts/tmax_scripts/writeSPF.tcl 
	python3 scripts/python_scripts/writeSPFScript.py $(SPF_FILE) 4 CLOCK_ON 

stil:
	@echo $(SCAN_CHAIN_FILE)
	python3 scripts/python_scripts/translatePatterns.py $(TOP_MODULE) $(DEMO) $(SPF_FILE) $(VCDE_FILE) $(VCD_SCAN_FILE) $(SCAN_CHAIN_FILE)
	
ibex_synth: syn_scripts/dc_setup.tcl 
	@export $(EXPORT_LIST); dc_shell -f scripts/syn_scripts/ibex_synth.tcl -output synthesis_batch.log

ibex_synth_dft: syn_scripts/dc_setup.tcl 
	@export $(EXPORT_LIST); dc_shell -f scripts/syn_scripts/ibex_synth_dft.tcl -output synthesis_batch.log
	
atpg:
	@export $(EXPORT_LIST); tmax scripts/tmax_scripts/ibex_tmax_script.tcl -sh
	python3 scripts/python_scripts/sum_tmax.py 

slt:	
	@export $(EXPORT_LIST): tmax scripts/tmax_scripts/sltPatterns.tcl -sh

debugFailingPatts:
	python3 scripts/python_scripts/debugFailingPatts.py $(TOP_MODULE) $(SCAN_CHAIN_FILE) TMAX/$(TOP_MODULE)_failing_patts.log

clean:
	rm -rf $(library) *.pvl *.syn *.mr *.pvk
