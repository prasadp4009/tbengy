`ifndef DEMO_UVM_AGENT__SV
`define DEMO_UVM_AGENT__SV

  class demo_uvm_agent extends uvm_agent;

    // Factory Registration
    `uvm_component_utils(demo_uvm_agent)

    // Agent config
    demo_uvm_agent_cfg agnt_cfg;

    // UVCs
    demo_uvm_driver     drvh;
    demo_uvm_monitor    monh;
    demo_uvm_sequencer  seqrh;

    // Tasks and Functions
    extern function new(string name = "demo_uvm_agent", uvm_component parent = null);
    extern virtual function void build_phase(uvm_phase phase);
    extern virtual function void connect_phase(uvm_phase phase);
    // extern virtual task run_phase(uvm_phase);
  endclass

  function demo_uvm_agent::new(string name = "demo_uvm_agent", uvm_component parent = null);
    super.new(name, parent);
  endfunction

  function void demo_uvm_agent::build_phase(uvm_phase phase);
    super.build_phase(phase);
    `uvm_info(get_full_name(), "[DEMO_UVM] Starting Build Phase", UVM_LOW)

    // agnt_cfg = demo_uvm_agent_cfg::type_id::create("agnt_cfg");
    if(!uvm_config_db#(demo_uvm_agent_cfg)::get(this, "", "agnt_cfg", agnt_cfg)) begin
      `uvm_fatal(get_type_name(), "[DEMO_UVM] Couldn't get agnt_cfg, did you set it?")
    end

    // Build UVC
    monh = demo_uvm_monitor::type_id::create("monh", this);
    if(agnt_cfg.is_active == UVM_ACTIVE) begin
      drvh = demo_uvm_driver::type_id::create("drvh", this);
      seqrh = demo_uvm_sequencer::type_id::create("seqrh", this);
    end
    `uvm_info(get_full_name(), "[DEMO_UVM] Ending Build Phase", UVM_LOW)
  endfunction

  function void demo_uvm_agent::connect_phase(uvm_phase phase);
    super.connect_phase(phase);
    `uvm_info(get_full_name(), "[DEMO_UVM] Starting Connect Phase", UVM_LOW)
    if(agnt_cfg.is_active == UVM_ACTIVE) begin
      drvh.seq_item_port.connect(seqrh.seq_item_export);
    end
    `uvm_info(get_full_name(), "[DEMO_UVM] Ending Connect Phase", UVM_LOW)
  endfunction

`endif

//End of demo_uvm_agent
