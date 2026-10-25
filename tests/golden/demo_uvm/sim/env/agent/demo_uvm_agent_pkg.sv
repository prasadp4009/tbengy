`ifndef DEMO_UVM_AGENT_PKG__SV
`define DEMO_UVM_AGENT_PKG__SV

  package demo_uvm_agent_pkg;

    // Import UVM
    import uvm_pkg::*;
    import demo_uvm_regs_pkg::*;
    import demo_uvm_seq_pkg::*;
    `include "uvm_macros.svh"

    // Include Agent UVCs
    // `include "demo_uvm_intf.sv"
    `include "demo_uvm_agent_cfg.sv"
    `include "demo_uvm_driver.sv"
    `include "demo_uvm_monitor.sv"
    `include "demo_uvm_sequencer.sv"
    `include "demo_uvm_agent.sv"
  endpackage

`endif

//End of demo_uvm_agent_pkg
