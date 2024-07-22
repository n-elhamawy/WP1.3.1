/* Pre-clock Strobe Protocol */
test_default_strobe = 15
test_default_period = 20
create_test_clock -period 20 -waveform {10 20} clk_i

/* Bidirectional Port Timing */
/* test_no_three_state_contention_after_capture =true */
test_default_delay = 0
test_default_bidir_delay = test_default_delay

/* TetraMAX Netlist Format */
test_stil_netlist_format = verilog

/* Export DFT Compiler Clock Capture Groups */
test_stil_multiclock_capture_procedures = false
