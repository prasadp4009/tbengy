`ifndef DEMO_UVM_SEQ_PKG__SV
`define DEMO_UVM_SEQ_PKG__SV

  package demo_uvm_seq_pkg;

    // Import UVM Macros and Package
    import uvm_pkg::*;
    `include "uvm_macros.svh"

    // Include all sequence items and sequences
    `include "demo_uvm_seq_item.sv"
    `include "demo_uvm_base_seq.sv"
    `include "demo_uvm_sanity_seq.sv"

  endpackage

`endif

//End of demo_uvm_seq_pkg
