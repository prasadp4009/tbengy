`ifndef DEMO_UVM_MONITOR__SV
`define DEMO_UVM_MONITOR__SV

  class demo_uvm_monitor extends uvm_monitor;

    // Factory Registration
    `uvm_component_utils(demo_uvm_monitor)

    // Variables
    demo_uvm_seq_item demo_uvm_seq_item_h;

    // Interface
    virtual demo_uvm_intf vintf;

    // Analysis Port
    uvm_analysis_port #(demo_uvm_seq_item) mon_port;

    // Tasks and Functions

    extern function new(string name = "demo_uvm_monitor", uvm_component parent = null);
    extern virtual function void build_phase(uvm_phase phase);
    // extern virtual function void connect_phase(uvm_phase phase);
    extern virtual task run_phase(uvm_phase phase);
    extern virtual task mon_task();

  endclass

  function demo_uvm_monitor::new(string name = "demo_uvm_monitor", uvm_component parent = null);
    super.new(name, parent);
  endfunction

  function void demo_uvm_monitor::build_phase(uvm_phase phase);
    super.build_phase(phase);
    if(!uvm_config_db#(virtual demo_uvm_intf)::get(this, "", "vintf", vintf)) begin
      `uvm_fatal(get_type_name(), "[DEMO_UVM] Couldn't get vintf, did you set it?")
    end
    mon_port = new("mon_port", this);
  endfunction

  task demo_uvm_monitor::run_phase(uvm_phase phase);
    super.run_phase(phase);
    mon_task();
  endtask

  task demo_uvm_monitor::mon_task();
    demo_uvm_seq_item_h = demo_uvm_seq_item::type_id::create("demo_uvm_seq_item_h");
    forever begin
      @(posedge vintf.clk);
      demo_uvm_seq_item_h.we     = vintf.we;
      demo_uvm_seq_item_h.addr   = vintf.addr;
      demo_uvm_seq_item_h.wdata  = vintf.wdata;
      demo_uvm_seq_item_h.rdata  = vintf.rdata;
      mon_port.write(demo_uvm_seq_item_h);
      `uvm_info(get_full_name(), "[DEMO_UVM] Written Sequence Item from Monitor", UVM_LOW)
    end
  endtask

`endif

//End of demo_uvm_monitor
