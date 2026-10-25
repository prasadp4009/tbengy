set outputDir ../synth

#Set FPGA
set_part xc7z010clg400-1
# STEP#1: setup design sources and constraints
#read_vhdl -library bftLib [ glob ./Sources/hdl/bftLib/*.vhdl ]
#read_vhdl ./Sources/hdl/bft.vhdl
read_verilog -sv [ glob ../rtl/*.*v ]
#read_verilog [ glob ../rtl/*.v ]
#Board/FPGA XDC
read_xdc ../synth/Zybo-Master.xdc
# STEP#2: run synthesis, report utilization and timing estimates, write checkpoint design
synth_design -top led_blink
write_checkpoint -force $outputDir/post_synth
report_utilization -file $outputDir/post_synth_util.rpt
report_timing -sort_by group -max_paths 5 -path_type summary
# STEP#3: run placement and logic optimization, report utilization and timing estimates
set_property SEVERITY {Warning} [get_drc_checks NSTD-1]
set_property SEVERITY {Warning} [get_drc_checks UCIO-1]
opt_design
power_opt_design
place_design
phys_opt_design
write_checkpoint -force $outputDir/post_place
report_clock_utilization -file $outputDir/clock_util.rpt
report_utilization -file $outputDir/post_place_util.rpt
report_timing -sort_by group -path_type summary
# STEP#4: run router, report actual utilization and timing, write checkpoint design, run DRCs
set_property SEVERITY {Warning} [get_drc_checks NSTD-1]
set_property SEVERITY {Warning} [get_drc_checks UCIO-1]
route_design
write_checkpoint -force $outputDir/post_route
report_timing_summary -file $outputDir/post_route_timing_summary.rpt
report_utilization -file $outputDir/post_route_util.rpt
report_power -file $outputDir/post_route_power.rpt
report_methodology -file $outputDir/post_impl_checks.rpt
report_drc -file $outputDir/post_imp_drc.rpt
write_verilog -force $outputDir/led_blink_impl_netlist.v
write_xdc -no_fixed_only -force $outputDir/Zybo-Master_impl.xdc
# STEP#5: generate a bitstream
write_bitstream -force $outputDir/design.bit
# STEP#6: program device
open_hw_manager
connect_hw_server
get_hw_servers
current_hw_target
open_hw_target
set_property PROGRAM.FILE {../synth/design.bit} [current_hw_device]
program_hw_devices [current_hw_device]
