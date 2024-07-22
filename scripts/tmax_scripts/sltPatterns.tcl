# Variables common to all reference methodology scripts
set TOP_MODULE                   [getenv TOP_MODULE]  ;#  The name of the top-level design
read_netlist /eda/NanGate_45nm_OCL_v2010_12/pdk_v1.3_v2010_12/NangateOpenCellLibrary_PDKv1_3_v2010_12/Front_End/Verilog/NangateOpenCellLibrary.v -library
read_netlist TMAX/Netlists/${TOP_MODULE}_synth_dft.v
run_build_model ${TOP_MODULE}
#report_summaries library_cells > ${OUTPUT_DIR}/${TOP_MODULE}_dft_cells.txt
set_rules V16 error -verbose
set_atpg -allow_clockon_measures
set_drc TMAX/Netlists/testProtocol_${TOP_MODULE}_synth_dft.spf
run_drc 
set_faults -fault_coverage
add_faults -all
set_patterns -external hello_test_${TOP_MODULE}.stil -histogram_summary -load_summary -append
set_simulation -measure pat -oscillation {5 5} -store_memory_contents last
#run_simulation -sequential > TMAX/${TOP_MODULE}_failing_patts.log
run_fault_sim -sequential > TMAX/${TOP_MODULE}_summary.txt
report_summaries >> TMAX/${TOP_MODULE}_${DEMO}_summary.txt
write_faults ${OUTPUT_DIR}/${DEMO}/${TOP_MODULE}_${DEMO}_faults.txt -all -replace
write_faults ${OUTPUT_DIR}/${DEMO}/${TOP_MODULE}_${DEMO}_detected_faults.txt -class {DT} -replace
quit -force
