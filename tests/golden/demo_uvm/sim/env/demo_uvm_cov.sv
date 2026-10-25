`ifndef DEMO_UVM_COV__SV
`define DEMO_UVM_COV__SV

  class demo_uvm_cov extends uvm_subscriber#(demo_uvm_seq_item);

    // Factory Registration
    `uvm_component_utils(demo_uvm_cov)

    extern function new(string name = "demo_uvm_cov", uvm_component parent = null);
    extern virtual function void write(demo_uvm_seq_item t);
  endclass

  function demo_uvm_cov::new(string name = "demo_uvm_cov", uvm_component parent = null);
    super.new(name, parent);
  endfunction

  function void demo_uvm_cov::write(demo_uvm_seq_item t);
    `uvm_info(get_full_name(), "[DEMO_UVM] Received item in Subscriber", UVM_LOW)
    `uvm_info(get_full_name(), $sformatf("\n[DEMO_UVM] Packet Data:\n\twe: %0d,\n\taddr: %0d,\n\twdata: %0d,\n\trdata: %0d",
      t.we, t.addr, t.wdata, t.rdata), UVM_LOW)
  endfunction

`endif

//End of demo_uvm_cov
