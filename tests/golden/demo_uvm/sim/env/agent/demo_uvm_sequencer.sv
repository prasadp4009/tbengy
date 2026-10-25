`ifndef DEMO_UVM_SEQUENCER__SV
`define DEMO_UVM_SEQUENCER__SV

  class demo_uvm_sequencer extends uvm_sequencer#(demo_uvm_seq_item);

    // Factory Registration
    `uvm_component_utils(demo_uvm_sequencer)

    // Tasks and Functions
    extern function new(string name = "demo_uvm_sequencer", uvm_component parent = null);
  endclass

  function demo_uvm_sequencer::new(string name = "demo_uvm_sequencer", uvm_component parent = null);
    super.new(name, parent);
  endfunction

`endif

//End of demo_uvm_sequencer
