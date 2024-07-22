# Copyright 2021 Thales DIS design services SAS
#
# Licensed under the Solderpad Hardware Licence, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.0
# You may obtain a copy of the License at https://solderpad.org/licenses/
#
# Original Author: Jean-Roch COULON (jean-roch.coulon@thalesgroup.com)
#

source -echo -verbose tcl_scripts/dc_setup.tcl
source -echo -verbose tcl_scripts/ibex_top_lr_synth_conf.tcl

set_app_var search_path "../../rtl ../../vendor/lowrisc_ip/dv/sv/dv_utils ../../vendor/lowrisc_ip/ip/prim/rtl  $search_path"

sh rm -rf work
sh mkdir work
define_design_lib ibex_lib -path work

source ibex_core

elaborate ${DESIGN_NAME} -library ibex_lib

uniquify
link

set clk_period_ns [expr $lr_synth_clk_period / 1000.0]
set half_clk_period_ns [expr $clk_period_ns /2]

create_clock [get_ports $lr_synth_clk_input] -name $lr_synth_clk_input -period $clk_period_ns -waveform {2.0 4.0}

foreach output $lr_synth_outputs {
  set output_constraint [lindex $output 1]
  set output_constraint [expr (1.0 - ($output_constraint / 100.0)) * $clk_period_ns]
  set_output_delay -clock $lr_synth_clk_input $output_constraint [lindex $output 0]
}

foreach input $lr_synth_inputs {
  set input_constraint [lindex $input 1]
  set input_constraint [expr ($input_constraint / 100.0) * $clk_period_ns]
  set_input_delay -clock $lr_synth_clk_input $input_constraint [lindex $input 0]
}

write -hierarchy -format ddc -output ${DCRM_ELABORATED_DESIGN_DDC_DFT_OUTPUT_FILE}

change_name -rule verilog -hier

## Prevent assignment statements in the Verilog netlist.
set_fix_multiple_port_nets -all -buffer_constants

## Check the current design for consistency
check_design -summary > ${DCRM_CHECK_DESIGN_REPORT}

################
## Test setup ##
################
# specify test related signals and run DFT DRC
create_port -direction "in" {SE}
create_port -direction "in" {SIN}
create_port -direction "out" {SOUT}
set_scan_configuration -style multiplexed_flip_flop 
#set_scan_register_type -exact -type "SDFFR_X1"
set_dft_signal -view existing_dft -type ScanClock -timing {2.0 4.0} -port $lr_synth_clk_input
set_dft_signal -view existing_dft -type ScanEnable -active_state 1 -port SE
set_dft_signal -view existing_dft -type Reset -active_state 0 -port rst_ni
set_dft_signal -view existing_dft -type ScanDataIn -port SIN 
set_dft_signal -view existing_dft -type ScanDataOut -port SOUT 
create_test_protocol -infer_clock -infer_asynch

compile_ultra -scan -no_boundary_optimization -exact_map

###########################################
# Scan chain configuration and insertion
###########################################


# pre-scan DFT DRC
dft_drc -verbose

# specify number of scan chains to be built
set_scan_configuration -chain_count $scan_chain_count

# specify DFT signals required for insert_dft
#set_dft_signal -view spec -type TestMode -active_state 0 -port TM
set_dft_signal -view spec -type ScanEnable -active_state 1 -port SE
set_dft_signal -view spec -type ScanDataIn -port SIN
set_dft_signal -view spec -type ScanDataOut -port SOUT

# preview scan chain insertion
preview_dft

# build scan chains
insert_dft

# Early test coverage
dft_drc -coverage_estimate

# incremental compile if required

# disable optimization for scan enable net
set_auto_disable_drc_nets -scan true
set_ideal_network -no_propagate SE

# incremental compile to fix timing issues introduced by scan
compile_ultra -incremental -scan -no_boundary_optimization

change_names -rules verilog -hierarchy
write_test_protocol -output ${NETLISTS_DIR}/tp_${DESIGN_NAME}_dft.spf
write_scan_def -o ${NETLISTS_DIR}/def_${DESIGN_NAME}.txt
write_sdf ${NETLISTS_DIR}/${DESIGN_NAME}_synth_dft.sdf
write -format verilog -hierarchy -output ${DCRM_FINAL_VERILOG_DFT_OUTPUT_FILE}
write -format verilog -hierarchy -output ${NETLISTS_DIR}/${DESIGN_NAME}_synth_dft.v
write -format ddc     -hierarchy -output ${DCRM_FINAL_DDC_DFT_OUTPUT_FILE}

report_area -hier -nosplit > ${DCRM_FINAL_AREA_REPORT}
write_parasitics -output ${DCRM_FINAL_SPEF_DFT_OUTPUT_FILE}
write_sdc ${DCRM_FINAL_SDC_DFT_OUTPUT_FILE}

exit
