`ifndef DEMO_UVM_BASE_SEQ__SV
`define DEMO_UVM_BASE_SEQ__SV

  class demo_uvm_base_seq extends uvm_sequence#(demo_uvm_seq_item);

    // Factory Registration
    `uvm_object_utils(demo_uvm_base_seq)

    // Variables

    // Tasks and Functions
    extern function new(string name = "demo_uvm_base_seq");
    extern virtual task body();

  endclass

  function demo_uvm_base_seq::new(string name = "demo_uvm_base_seq");
    super.new(name);
  endfunction

  task demo_uvm_base_seq::body();

  endtask

`endif

//End of demo_uvm_base_seq
