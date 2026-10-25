`ifndef DEMO_UVM_AGENT_CFG__SV
`define DEMO_UVM_AGENT_CFG__SV

  class demo_uvm_agent_cfg extends uvm_object;

    // Factory Registration
    `uvm_object_utils(demo_uvm_agent_cfg)

    // UVM Agent Controls

    uvm_active_passive_enum is_active = UVM_ACTIVE;

    // Tasks and Functions

    extern function new(string name = "demo_uvm_agent_cfg");

  endclass

  function demo_uvm_agent_cfg::new(string name = "demo_uvm_agent_cfg");
    super.new(name);
  endfunction

`endif

//End of demo_uvm_agent_cfg
