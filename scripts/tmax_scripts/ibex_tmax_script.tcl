read_netlist /eda/synopsys/2022-23/RHELx86/SYN_2022.12/libraries/syn/lsi_10k_components.vhd -library
read_netlist  ibex_top_synth.v
run_build_model 
report_summaries library_cells > TMAX/ibex_cells.txt
run_drc
set_faults -fault_coverage
add_faults -all
set_atpg -full_seq_atpg -verbose
run_atpg ba > TMAX/ibex_ATPG_summary.txt
update_faults -reset_au
run_atpg fu >> TMAX/ibex_ATPG_summary.txt
report_summaries >> TMAX/ibex_ATPG_summary.txt
write_faults TMAX/ibex_ATPG_faults.txt -all -replace
write_patterns TMAX/patterns/ibex_ATPG_patterns.bin -format binary -split 1 -exclude repeat_setup -replace
quit -f
