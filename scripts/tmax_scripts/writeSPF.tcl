set TOP_MODULE                   [getenv TOP_MODULE]  ;#  The name of the top-level design
read_netlist /eda/NanGate_45nm_OCL_v2010_12/pdk_v1.3_v2010_12/NangateOpenCellLibrary_PDKv1_3_v2010_12/Front_End/Verilog/NangateOpenCellLibrary.v -library
read_netlist TMAX/Netlists/${TOP_MODULE}_synth_dft.v
run_build_model 
add_clocks 0 clk_i -timing {4 2 4 1} -shift
add_clocks 1 rst_ni
add_scan_enables 1 se
add_scan_chains s1 sin sout
run_drc
write_drc_file -nogeneric_captures TMAX/Netlists/testProtocol_${TOP_MODULE}_synth_dft.spf -replace
quit -f
