`ifndef DEMO_UVM_TEST_PKG__SV
`define DEMO_UVM_TEST_PKG__SV

  package demo_uvm_test_pkg;

    // Import UVM
    import uvm_pkg::*;
    import demo_uvm_seq_pkg::*;
    import demo_uvm_regs_pkg::*;
    import demo_uvm_agent_pkg::*;
    import demo_uvm_env_pkg::*;
    `include "uvm_macros.svh"

    // Import UVC
    `include "demo_uvm_base_test.sv"
    `include "demo_uvm_sanity_test.sv"

  endpackage

`endif

//End of demo_uvm_test_pkg
