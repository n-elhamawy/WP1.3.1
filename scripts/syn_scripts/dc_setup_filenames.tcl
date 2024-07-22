puts "RM-Info: Running script [info script]\n"

set NETLISTS_DIR ../../TMAX/Netlists
set INPUTS_DIR ${NETLISTS_DIR}/${DESIGN_NAME}/inputs
set REPORTS_DIR ${NETLISTS_DIR}/${DESIGN_NAME}/reports
set OUTPUTS_DIR ${NETLISTS_DIR}/${DESIGN_NAME}/outputs

file mkdir ${NETLISTS_DIR} 
file mkdir ${INPUTS_DIR}
file mkdir ${REPORTS_DIR}
file mkdir ${OUTPUTS_DIR}

###############
# Input Files #
###############

set DCRM_SDC_INPUT_FILE                                 ${INPUTS_DIR}/${DESIGN_NAME}.sdc
set DCRM_CONSTRAINTS_INPUT_FILE                         ${INPUTS_DIR}/${DESIGN_NAME}.constraints.tcl

###########
# Reports #
###########

set DCRM_CHECK_LIBRARY_REPORT                           ${REPORTS_DIR}/${DESIGN_NAME}_${TECH}_synth_check_library.rpt

set DCRM_CONSISTENCY_CHECK_ENV_FILE                     ${REPORTS_DIR}/${DESIGN_NAME}_${TECH}.compile_ultra.env
set DCRM_CHECK_DESIGN_REPORT                            ${REPORTS_DIR}/${DESIGN_NAME}_${TECH}.check_design.rpt
set DCRM_ANALYZE_DATAPATH_EXTRACTION_REPORT             ${REPORTS_DIR}/${DESIGN_NAME}_${TECH}.analyze_datapath_extraction.rpt

set DCRM_FINAL_QOR_REPORT                               ${REPORTS_DIR}/${DESIGN_NAME}_${TECH}_synth_qor.rpt
set DCRM_FINAL_TIMING_REPORT                            ${REPORTS_DIR}/${DESIGN_NAME}_${TECH}_synth_timing.rpt
set DCRM_FINAL_AREA_REPORT                              ${REPORTS_DIR}/${DESIGN_NAME}_${TECH}_synth_area.rpt
set DCRM_FINAL_POWER_REPORT                             ${REPORTS_DIR}/${DESIGN_NAME}_${TECH}_synth_power.rpt
set DCRM_FINAL_CLOCK_GATING_REPORT                      ${REPORTS_DIR}/${DESIGN_NAME}_${TECH}_synth_clock_gating.rpt
set DCRM_FINAL_SELF_GATING_REPORT                       ${REPORTS_DIR}/${DESIGN_NAME}_${TECH}_synth_self_gating.rpt
set DCRM_THRESHOLD_VOLTAGE_GROUP_REPORT                 ${REPORTS_DIR}/${DESIGN_NAME}_${TECH}_synth_threshold.voltage.group.rpt
set DCRM_INSTANTIATE_CLOCK_GATES_REPORT                 ${REPORTS_DIR}/${DESIGN_NAME}_${TECH}_synth_instatiate_clock_gates.rpt
set DCRM_FINAL_POWER_REPORT                             ${REPORTS_DIR}/${DESIGN_NAME}_${TECH}_synth_power.rpt

################
# Output Files #
################

set DCRM_AUTOREAD_RTL_SCRIPT                            ${OUTPUTS_DIR}/${DESIGN_NAME}_${TECH}.autoread_rtl.tcl
set DCRM_ELABORATED_DESIGN_DDC_OUTPUT_FILE              ${OUTPUTS_DIR}/${DESIGN_NAME}_${TECH}.elab.ddc
set DCRM_COMPILE_ULTRA_DDC_OUTPUT_FILE                  ${OUTPUTS_DIR}/${DESIGN_NAME}_${TECH}.compile_ultra.ddc
set DCRM_FINAL_DDC_OUTPUT_FILE                          ${OUTPUTS_DIR}/${DESIGN_NAME}_${TECH}_synth.ddc
set DCRM_FINAL_VERILOG_OUTPUT_FILE                      ${OUTPUTS_DIR}/${DESIGN_NAME}_${TECH}_synth.v
set DCRM_FINAL_SDC_OUTPUT_FILE                          ${OUTPUTS_DIR}/${DESIGN_NAME}_${TECH}_synth.sdc
set DCRM_FINAL_SPEF_OUTPUT_FILE                         ${OUTPUTS_DIR}/${DESIGN_NAME}_${TECH}_synth.spef
set DCRM_FINAL_FSDB_OUTPUT_FILE                         ${OUTPUTS_DIR}/${DESIGN_NAME}_${TECH}_synth.fsdb
set DCRM_FINAL_VCD_OUTPUT_FILE                          ${OUTPUTS_DIR}/${DESIGN_NAME}_${TECH}_synth.vcd

################
# DFT Output Files #
################

set DCRM_AUTOREAD_RTL_DFT_SCRIPT                            ${OUTPUTS_DIR}/${DESIGN_NAME}_${TECH}_dft.autoread_rtl.tcl
set DCRM_ELABORATED_DESIGN_DDC_DFT_OUTPUT_FILE              ${OUTPUTS_DIR}/${DESIGN_NAME}_${TECH}_dft.elab.ddc
set DCRM_COMPILE_ULTRA_DDC_DFT_OUTPUT_FILE                  ${OUTPUTS_DIR}/${DESIGN_NAME}_${TECH}_dft.compile_ultra.ddc
set DCRM_FINAL_DDC_DFT_OUTPUT_FILE                          ${OUTPUTS_DIR}/${DESIGN_NAME}_${TECH}_synth_dft.ddc
set DCRM_FINAL_VERILOG_DFT_OUTPUT_FILE                      ${OUTPUTS_DIR}/${DESIGN_NAME}_${TECH}_synth_dft.v
set DCRM_FINAL_SDC_DFT_OUTPUT_FILE                          ${OUTPUTS_DIR}/${DESIGN_NAME}_${TECH}_synth_dft.sdc
set DCRM_FINAL_SPEF_DFT_OUTPUT_FILE                         ${OUTPUTS_DIR}/${DESIGN_NAME}_${TECH}_synth_dft.spef
set DCRM_FINAL_FSDB_DFT_OUTPUT_FILE                         ${OUTPUTS_DIR}/${DESIGN_NAME}_${TECH}_synth_dft.fsdb
set DCRM_FINAL_VCD_DFT_OUTPUT_FILE                          ${OUTPUTS_DIR}/${DESIGN_NAME}_${TECH}_synth_dft.vcd


puts "RM-Info: Completed script [info script]\n"
