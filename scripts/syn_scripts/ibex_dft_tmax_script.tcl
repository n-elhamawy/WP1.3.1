read_netlist [get_unix_variable PDK_Verilog] -library
read_netlist  ibex_top_synth_dft.v
run_build_model 
report_summaries library_cells > TMAX/ibex_cells_dft.txt
set_rules V16 error -verbose
set_atpg -allow_clockon_measures
run_drc tp_ibex_top_dft.spf
set_faults -fault_coverage
add_faults -all
set_atpg -full_seq_atpg -verbose
run_atpg > TMAX/ibex_dft_ATPG_summary.txt
report_summaries >> TMAX/ibex_dft_ATPG_summary.txt
write_faults TMAX/ibex_dft_ATPG_faults.txt -all -replace
write_patterns TMAX/patterns_dft/ibex_dft_ATPG_patterns.bin -format binary -split 1 -exclude repeat_setup -replace
