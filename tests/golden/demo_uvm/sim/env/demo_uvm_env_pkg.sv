`ifndef DEMO_UVM_ENV_PKG__SV
`define DEMO_UVM_ENV_PKG__SV

  package demo_uvm_env_pkg;

    // Import UVM
    import uvm_pkg::*;
    import demo_uvm_seq_pkg::*;
    import demo_uvm_regs_pkg::*;
    import demo_uvm_agent_pkg::*;
    `include "uvm_macros.svh"

    // Import UVM
    `include "demo_uvm_sb.sv"
    `include "demo_uvm_cov.sv"
    `include "demo_uvm_env.sv"
  endpackage

`endif

//End of demo_uvm_env_pkg
