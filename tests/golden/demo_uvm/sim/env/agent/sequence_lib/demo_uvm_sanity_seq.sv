`ifndef DEMO_UVM_SANITY_SEQ__SV
`define DEMO_UVM_SANITY_SEQ__SV

  class demo_uvm_sanity_seq extends demo_uvm_base_seq;

    // Factory Registration
    `uvm_object_utils(demo_uvm_sanity_seq)

    // Variables

    // Tasks and Functions

    extern function new(string name = "demo_uvm_sanity_seq");
    extern virtual task body();
  endclass

  function demo_uvm_sanity_seq::new(string name = "demo_uvm_sanity_seq");
    super.new(name);
  endfunction

  task demo_uvm_sanity_seq::body();
    super.body();
    `uvm_info(get_full_name(), "[DEMO_UVM] Starting Sanity Sequence", UVM_LOW)
    repeat(17) begin
      `uvm_do_with(req, {we==1;})
    end
    // wait_for_item_done();
  endtask

`endif

//End of demo_uvm_sanity_seq
