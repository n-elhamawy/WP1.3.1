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

write -hierarchy -format ddc -output ${DCRM_ELABORATED_DESIGN_DDC_OUTPUT_FILE}

change_name -rule verilog -hier

## Prevent assignment statements in the Verilog netlist.
set_fix_multiple_port_nets -all -buffer_constants

## Check the current design for consistency
check_design -summary > ${DCRM_CHECK_DESIGN_REPORT}

compile_ultra -no_boundary_optimization -exact_map

change_names -rules verilog -hierarchy

write -format verilog -hierarchy -output ${DCRM_FINAL_VERILOG_OUTPUT_FILE}
write -format verilog -hierarchy -output ${DESIGN_NAME}_synth.v
write -format ddc     -hierarchy -output ${DCRM_FINAL_DDC_OUTPUT_FILE}

report_area -hier -nosplit > ${DCRM_FINAL_AREA_REPORT}
write_parasitics -output ${DCRM_FINAL_SPEF_OUTPUT_FILE}
write_sdc ${DCRM_FINAL_SDC_OUTPUT_FILE}

exit
