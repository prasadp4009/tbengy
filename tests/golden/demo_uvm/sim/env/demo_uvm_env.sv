`ifndef DEMO_UVM_ENV__SV
`define DEMO_UVM_ENV__SV

  class demo_uvm_env extends uvm_env;

    // Factory Registration
    `uvm_component_utils(demo_uvm_env)

    // Environment Variables
    bit is_scoreboard_enable = 1;
    bit is_coverage_enable = 1;

    // Declare UVC
    demo_uvm_agent_cfg agnt_cfg;
    demo_uvm_agent agnth;
    demo_uvm_sb sbh;
    demo_uvm_cov covh;

    extern function new (string name = "demo_uvm_env", uvm_component parent = null);
    extern virtual function void build_phase(uvm_phase phase);
    extern virtual function void connect_phase(uvm_phase phase);
  endclass

  function demo_uvm_env::new(string name = "demo_uvm_env", uvm_component parent = null);
    super.new(name, parent);
  endfunction

  function void demo_uvm_env::build_phase(uvm_phase phase);
    super.build_phase(phase);
    `uvm_info(get_full_name(), "[DEMO_UVM] Starting Build Phase", UVM_LOW)
    agnt_cfg = demo_uvm_agent_cfg::type_id::create("agnt_cfg");
    uvm_config_db #(demo_uvm_agent_cfg)::set(this, "*", "agnt_cfg", agnt_cfg);
    agnth = demo_uvm_agent::type_id::create("agnth", this);
    if(is_scoreboard_enable) begin
      sbh = demo_uvm_sb::type_id::create("sbh", this);
    end
    if(is_coverage_enable) begin
      covh = demo_uvm_cov::type_id::create("covh", this);
    end
    `uvm_info(get_full_name(), "[DEMO_UVM] Ending Build Phase", UVM_LOW)
  endfunction

  function void demo_uvm_env::connect_phase(uvm_phase phase);
    super.connect_phase(phase);
    `uvm_info(get_full_name(), "[DEMO_UVM] Starting Connect Phase", UVM_LOW)
    if(is_scoreboard_enable) begin
      agnth.monh.mon_port.connect(sbh.sb_fifo.analysis_export);
    end
    if(is_coverage_enable) begin
      agnth.monh.mon_port.connect(covh.analysis_export);
    end
    `uvm_info(get_full_name(), "[DEMO_UVM] Ending Connect Phase", UVM_LOW)
  endfunction

`endif

//End of demo_uvm_env
