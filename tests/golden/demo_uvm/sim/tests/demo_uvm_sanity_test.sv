`ifndef DEMO_UVM_SANITY_TEST__SV
`define DEMO_UVM_SANITY_TEST__SV

  class demo_uvm_sanity_test extends demo_uvm_base_test;

    // Factory Registration
    `uvm_component_utils(demo_uvm_sanity_test)

    // Sequence to start
    demo_uvm_sanity_seq seqh;

    extern function new(string name = "demo_uvm_sanity_test", uvm_component parent=null);
    extern virtual function void build_phase(uvm_phase phase);
    extern virtual function void connect_phase(uvm_phase phase);
    extern virtual task run_phase(uvm_phase phase);
    extern virtual function void report_phase(uvm_phase phase);
  endclass

  function demo_uvm_sanity_test::new(string name = "demo_uvm_sanity_test", uvm_component parent=null);
    super.new(name, parent);
  endfunction

  function void demo_uvm_sanity_test::build_phase(uvm_phase phase);
    super.build_phase(phase);
  endfunction

  function void demo_uvm_sanity_test::connect_phase(uvm_phase phase);
    super.connect_phase(phase);
  endfunction

  task demo_uvm_sanity_test::run_phase(uvm_phase phase);
    super.run_phase(phase);
    phase.raise_objection(this);
    `uvm_info(get_full_name(), "[demo_uvm] Starting sanity Test", UVM_NONE)
    seqh = demo_uvm_sanity_seq::type_id::create("seqh");
    seqh.start(envh.agnth.seqrh);
    phase.drop_objection(this);
  endtask

  function void demo_uvm_sanity_test::report_phase(uvm_phase phase);
    super.report_phase(phase);
  endfunction

`endif

//End of demo_uvm_sanity_test
