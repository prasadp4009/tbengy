`ifndef DEMO_UVM_BASE_TEST__SV
`define DEMO_UVM_BASE_TEST__SV

  class demo_uvm_base_test extends uvm_test;

    // Factory Registration
    `uvm_component_utils(demo_uvm_base_test)

    // Declare UVC
    demo_uvm_env envh;

    extern function new(string name = "demo_uvm_base_test", uvm_component parent=null);
    extern virtual function void build_phase(uvm_phase phase);
    extern virtual function void connect_phase(uvm_phase phase);
    extern virtual task run_phase(uvm_phase phase);
    extern virtual function void report_phase(uvm_phase phase);
  endclass

  function demo_uvm_base_test::new(string name = "demo_uvm_base_test", uvm_component parent=null);
    super.new(name, parent);
  endfunction

  function void demo_uvm_base_test::build_phase(uvm_phase phase);
    super.build_phase(phase);
    envh = demo_uvm_env::type_id::create("envh", this);
  endfunction

  function void demo_uvm_base_test::connect_phase(uvm_phase phase);
    super.connect_phase(phase);
  endfunction

  task demo_uvm_base_test::run_phase(uvm_phase phase);
    super.run_phase(phase);
    phase.raise_objection(this);
    `uvm_info(get_full_name(), "[demo_uvm] Starting Base Test", UVM_NONE)
    phase.drop_objection(this);
  endtask

  function void demo_uvm_base_test::report_phase(uvm_phase phase);
    uvm_top.print_topology();
  endfunction

`endif

//End of demo_uvm_base_test
