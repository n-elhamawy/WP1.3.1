# Variables common to all reference methodology scripts
set NETLIST_FILE                 [getenv NETLIST_FILE];
set TOP_MODULE                   [getenv TOP_MODULE]  ;#  The name of the top-level design
set PDK_Verilog				           [getenv PDK_Verilog];
set SPF_FILE                     [getenv SPF_FILE];
set OUTPUT_DIR                   [getenv OUTPUT_DIR];
#set PATT_FILE          					 [getenv PATT_FILE];
#set DESIGN_TYPE									 [getenv DESIGN_TYPE];

read_netlist -format VH ${PDK_Verilog} -noabort
read_netlist  ${NETLIST_FILE}
run_build_model 
report_summaries library_cells > TMAX/ibex_cells.txt
run_drc
set_faults -fault_coverage
add_faults -all
run_atpg ba > TMAX/ibex_ATPG_summary.txt
update_faults -reset_au
run_atpg fu >> TMAX/ibex_ATPG_summary.txt
report_summaries >> TMAX/ibex_ATPG_summary.txt
write_faults TMAX/ibex_ATPG_faults.txt -all -replace
write_patterns TMAX/patterns/ibex_ATPG_patterns.bin -format binary -split 1 -exclude repeat_setup -replace
