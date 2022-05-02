#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File        : uvmTemplate.py
Author      : Prasad Pandit
Email       : prasadp4009@gmail.com
Github      : https://github.com/prasadp4009
Description : Base templates for Testbench Generation
"""

makefileStr="""\
# @Author : {0}
# @Date   : {1}

work = work

top_tb_name = {2}_tb

ifeq ($(OS),Windows_NT)

ifneq ("$(wildcard ../rtl)","")
INCRTL = +incdir+../rtl
else
INCRTL =
endif

ifneq ("$(wildcard ../rtl/*.sv)","")
RTL = ../rtl/{2}.sv
else
RTL =
endif

ifneq ("$(wildcard ../sim/tb)","")
INCTB = +incdir+../sim/tb
else
INCTB =
endif

ifneq ("$(wildcard ../sim/tb/*.sv)","")
TB = ../sim/tb/{2}_tb.sv
else
TB =
endif

ifneq ("$(wildcard ../sim/env/agent)","")
INCINTF = +incdir+../sim/env/agent
else
INCINTF =
endif

ifneq ("$(wildcard ../sim/env/agent/*intf.sv)","")
INTF = ../sim/env/agent/{2}_intf.sv
else
INTF =
endif

ifneq ("$(wildcard ../sim/env/agent)","")
INCAGT = +incdir+../sim/env/agent
else
INCAGT =
endif

ifneq ("$(wildcard ../sim/env/agent/*pkg.sv)","")
AGT = ../sim/env/agent/{2}_agent_pkg.sv
else
AGT =
endif

ifneq ("$(wildcard ../sim/env/agent/sequence_lib)","")
INCSEQ_LIB = +incdir+../sim/env/agent/sequence_lib
else
INCSEQ_LIB =
endif

ifneq ("$(wildcard ../sim/env/agent/sequence_lib/*pkg.sv)","")
SEQ_LIB = ../sim/env/agent/sequence_lib/{2}_seq_pkg.sv
else
SEQ_LIB =
endif

ifneq ("$(wildcard ../sim/env)","")
INCENV = +incdir+../sim/env
else
INCENV =
endif

ifneq ("$(wildcard ../sim/env/*pkg.sv)","")
ENV = ../sim/env/{2}_env_pkg.sv
else
ENV =
endif

ifneq ("$(wildcard ../sim/env/agent/regs)","")
INCREG = +incdir+../sim/env/agent/regs
else
INCREG =
endif

ifneq ("$(wildcard ../sim/env/agent/regs/*pkg.sv)","")
REG = ../sim/env/agent/regs/{2}_regs_pkg.sv
else
REG =
endif

ifneq ("$(wildcard ../sim/tests)","")
INCTESTS = +incdir+../sim/tests
else
INCTESTS =
endif

ifneq ("$(wildcard ../sim/tests/*pkg.sv)","")
TESTS = ../sim/tests/{2}_test_pkg.sv
else
TESTS =
endif

else

ifneq ("$(wildcard ../rtl)","")
INCRTL = +incdir+../rtl
else
INCRTL =
endif

ifneq ("$(wildcard ../rtl/*.sv)","")
RTL = ../rtl/*.sv
else
RTL =
endif

ifneq ("$(wildcard ../sim/tb)","")
INCTB = +incdir+../sim/tb
else
INCTB =
endif

ifneq ("$(wildcard ../sim/tb/*.sv)","")
TB = ../sim/tb/*.sv
else
TB =
endif

ifneq ("$(wildcard ../sim/env/agent)","")
INCINTF = +incdir+../sim/env/agent
else
INCINTF =
endif

ifneq ("$(wildcard ../sim/env/agent/*intf.sv)","")
INTF = ../sim/env/agent/*intf.sv
else
INTF =
endif

ifneq ("$(wildcard ../sim/env/agent)","")
INCAGT = +incdir+../sim/env/agent
else
INCAGT =
endif

ifneq ("$(wildcard ../sim/env/agent/*pkg.sv)","")
AGT = ../sim/env/agent/*pkg.sv
else
AGT =
endif

ifneq ("$(wildcard ../sim/env/agent/sequence_lib)","")
INCSEQ_LIB = +incdir+../sim/env/agent/sequence_lib
else
INCSEQ_LIB =
endif

ifneq ("$(wildcard ../sim/env/agent/sequence_lib/*pkg.sv)","")
SEQ_LIB = ../sim/env/agent/sequence_lib/*pkg.sv
else
SEQ_LIB =
endif

ifneq ("$(wildcard ../sim/env)","")
INCENV = +incdir+../sim/env
else
INCENV =
endif

ifneq ("$(wildcard ../sim/env/*pkg.sv)","")
ENV = ../sim/env/*pkg.sv
else
ENV =
endif

ifneq ("$(wildcard ../sim/env/agent/regs)","")
INCREG = +incdir+../sim/env/agent/regs
else
INCREG =
endif

ifneq ("$(wildcard ../sim/env/agent/regs/*pkg.sv)","")
REG = ../sim/env/agent/regs/*pkg.sv
else
REG =
endif

ifneq ("$(wildcard ../sim/tests)","")
INCTESTS = +incdir+../sim/tests
else
INCTESTS =
endif

ifneq ("$(wildcard ../sim/tests/*pkg.sv)","")
TESTS = ../sim/tests/*pkg.sv
else
TESTS =
endif

endif

ifeq ($(OS),Windows_NT)
DELFILES = clean_dos
else
DELFILES = clean_linux
endif

cmp:
	xvlog -work $(work) -i ../sim -sv $(RTL) $(SEQ_LIB) $(REG) $(INTF) $(AGT) $(ENV) $(TESTS) $(TB) -L uvm
	xelab work.$(top_tb_name) -s $(top_tb_name)_sim -L uvm -timescale 1ns/1ps -debug all

run_sim_wave:
	xsim -wdb sim.wdb -log session.log -t logw.tcl $(top_tb_name)_sim -testplusarg "UVM_TESTNAME={2}_sanity_test"
	xsim sim.wdb -gui

view_wave:
	xsim sim.wdb -gui

run_sim:
	xsim -runall -log session.log $(top_tb_name)_sim -testplusarg "UVM_TESTNAME={2}_sanity_test"

clean_linux:
	rm -rf modelsim.* transcript* vlog.* work vsim.wlf *.log *hbs *Xil xsim.dir *.jou *.pb
	clear

clean_dos:
	if exist modelsim.* del modelsim.* /F /S /Q /A
	if exist transcript* del transcript* /F /S /Q /A
	if exist vlog.* del vlog.* /F /S /Q /A
	if exist vsim.wlf del vsim.wlf /F /S /Q /A
	if exist *.log del *.log /F /S /Q /A
	if exist work rd work /q /s
	if exist covhtmlreport rd covhtmlreport /q /s
	if exist *hbs del *hbs /q /s
	if exist *Xil del *Xil /q /s
	if exist xsim.dir del xsim.dir /q /s
	if exist *.jou del *.jou /F /S /Q /A
	if exist *.pb del *.pb /F /S /Q /A

clean_log:
	if exist *.log del *.log /f /s /q /a

clean:
	make $(DELFILES)

run_all:
	make clean
	make cmp
	make run_sim

run_all_gui:
	make clean
	make cmp
	make run_sim_wave
"""

makefileSVStr="""\
# @Author : {0}
# @Date   : {1}

work = work

top_tb_name = {2}_tb

ifeq ($(OS),Windows_NT)

ifneq ("$(wildcard ../rtl)","")
INCRTL = +incdir+../rtl
else
INCRTL =
endif

ifneq ("$(wildcard ../rtl/*.sv)","")
RTL = ../rtl/{2}.sv
else
RTL =
endif

ifneq ("$(wildcard ../sim/tb)","")
INCTB = +incdir+../sim/tb
else
INCTB =
endif

ifneq ("$(wildcard ../sim/tb/*.sv)","")
TB = ../sim/tb/{2}_tb.sv
else
TB =
endif

else

ifneq ("$(wildcard ../rtl)","")
INCRTL = +incdir+../rtl
else
INCRTL =
endif

ifneq ("$(wildcard ../rtl/*.sv)","")
RTL = ../rtl/*.sv
else
RTL =
endif

ifneq ("$(wildcard ../sim/tb)","")
INCTB = +incdir+../sim/tb
else
INCTB =
endif

ifneq ("$(wildcard ../sim/tb/*.sv)","")
TB = ../sim/tb/*.sv
else
TB =
endif

endif

ifeq ($(OS),Windows_NT)
DELFILES = clean_dos
else
DELFILES = clean_linux
endif

cmp:
	xvlog -work $(work) -i ../sim -sv $(RTL) $(TB) -L uvm
	xelab work.$(top_tb_name) -s $(top_tb_name)_sim -L uvm -timescale 1ns/1ps -debug all

run_sim_wave:
	xsim -wdb sim.wdb -log session.log -t logw.tcl $(top_tb_name)_sim -testplusarg "CREATOR=pr454dP4nd!t"
	xsim sim.wdb -gui

view_wave:
	xsim sim.wdb -gui

run_sim:
	xsim -runall -log session.log $(top_tb_name)_sim -testplusarg "CREATOR=pr454dP4nd!t"

clean_linux:
	rm -rf modelsim.* transcript* vlog.* work vsim.wlf *.log *hbs *Xil xsim.dir *.jou *.pb
	clear

clean_dos:
	if exist modelsim.* del modelsim.* /F /S /Q /A
	if exist transcript* del transcript* /F /S /Q /A
	if exist vlog.* del vlog.* /F /S /Q /A
	if exist vsim.wlf del vsim.wlf /F /S /Q /A
	if exist *.log del *.log /F /S /Q /A
	if exist work rd work /q /s
	if exist covhtmlreport rd covhtmlreport /q /s
	if exist *hbs del *hbs /q /s
	if exist *Xil del *Xil /q /s
	if exist xsim.dir del xsim.dir /q /s
	if exist *.jou del *.jou /F /S /Q /A
	if exist *.pb del *.pb /F /S /Q /A

clean_log:
	if exist *.log del *.log /f /s /q /a

clean:
	make $(DELFILES)

run_all:
	make clean
	make cmp
	make run_sim

run_all_gui:
	make clean
	make cmp
	make run_sim_wave
"""

xsimWaveTclStr="""\
log_wave -r *
run all
exit
"""

rtlModule = """\
`ifndef {0}__SV
`define {0}__SV

  module {1}
  (
    input  logic clk,
    input  logic we,
    input  logic [3:0] addr,
    input  logic [7:0] wdata,
    output logic [7:0] rdata
  );

  logic [7:0] mem [16];
  logic [3:0] addr_reg;

  always_ff @(posedge clk) begin
    if(we) begin
      mem[addr] <= wdata;
    end
    addr_reg <= addr;
  end

  assign rdata = mem[addr_reg];

  endmodule : {1}

`endif

//End of {1}
"""

rtlSVModule = """\
`ifndef {0}__SV
`define {0}__SV

  module {1}
  (
    input  logic clk,
    input  logic rst,
    input  logic [7:0] wdata,
    output logic [7:0] rdata
  );

  always_ff @(posedge clk or negedge rst) begin
    if(!rst) begin
      rdata <= 'd0;
    end
    else begin
      rdata <= wdata;
    end
  end

  endmodule : {1}

`endif

//End of {1}
"""

tbModule = """\
`ifndef {0}_TB__SV
`define {0}_TB__SV

  // Generated by tbengy. Created by Prasad Pandit.

  `timescale 1ns/1ps
  `include "uvm_macros.svh"

  module {1}_tb;
    import {1}_test_pkg::*;
    import uvm_pkg::*;

    logic clk;

    {1}_intf intf(.clk(clk));

    {1} DUT (
      .clk(clk),
      .we(intf.we),
      .addr(intf.addr),
      .wdata(intf.wdata),
      .rdata(intf.rdata)
    );

    initial begin
      clk = 0;
      forever begin
        #10 clk = ~clk;
      end
    end

    initial begin
      uvm_config_db #(virtual {1}_intf)::set(null, "*", "vintf", intf);
      run_test();
    end
  endmodule

`endif

//End of {1}_tb
"""

tbSVModule = """\
`ifndef {0}_TB__SV
`define {0}_TB__SV

  // Generated by tbengy. Created by Prasad Pandit.

  `timescale 1ns/1ps
  `include "uvm_macros.svh"

  module {1}_tb;
    // import uvm_pkg::*; // Uncomment if you are adding UVM code

    logic clk;
    logic rst;
    logic [7:0] wdata;
    logic [7:0] rdata;

    {1} DUT (
      .clk(clk),
      .rst(rst),
      .wdata(wdata),
      .rdata(rdata)
    );

    task negDelay();
      @(negedge clk);
    endtask

    initial begin
      clk = 0;
      forever begin
        #10 clk = ~clk;
      end
    end

    initial begin
      rst = 0;
      wdata = 0;
      $display("------------- Starting Test -------------");
      #10;
      rst = 1;
      negDelay;
      wdata = 'h44;
      negDelay;
      wdata = 'h41;
      negDelay;
      wdata = 'h44;
      negDelay;
      wdata = 'h55;
      #100 $finish;
    end
  endmodule

`endif

//End of {1}_tb
"""

testPkg = """\
`ifndef {0}_TEST_PKG__SV
`define {0}_TEST_PKG__SV

  package {1}_test_pkg;

    // Import UVM
    import uvm_pkg::*;
    import {1}_seq_pkg::*;
    import {1}_regs_pkg::*;
    import {1}_agent_pkg::*;
    import {1}_env_pkg::*;
    `include "uvm_macros.svh"

    // Import UVC
    `include "{1}_base_test.sv"
    `include "{1}_sanity_test.sv"

  endpackage

`endif

//End of {1}_test_pkg
"""

baseTest = """\
`ifndef {0}_BASE_TEST__SV
`define {0}_BASE_TEST__SV

  class {1}_base_test extends uvm_test;

    // Factory Registration
    `uvm_component_utils({1}_base_test)

    // Declare UVC
    {1}_env envh;

    extern function new(string name = "{1}_base_test", uvm_component parent=null);
    extern virtual function void build_phase(uvm_phase phase);
    extern virtual function void connect_phase(uvm_phase phase);
    extern virtual task run_phase(uvm_phase phase);
    extern virtual function void report_phase(uvm_phase phase);
  endclass

  function {1}_base_test::new(string name = "{1}_base_test", uvm_component parent=null);
    super.new(name, parent);
  endfunction

  function void {1}_base_test::build_phase(uvm_phase phase);
    super.build_phase(phase);
    envh = {1}_env::type_id::create("envh", this);
  endfunction

  function void {1}_base_test::connect_phase(uvm_phase phase);
    super.connect_phase(phase);
  endfunction

  task {1}_base_test::run_phase(uvm_phase phase);
    super.run_phase(phase);
    phase.raise_objection(this);
    `uvm_info(get_full_name(), "[{1}] Starting Base Test", UVM_NONE)
    phase.drop_objection(this);
  endtask

  function void {1}_base_test::report_phase(uvm_phase phase);
    uvm_top.print_topology();
  endfunction

`endif

//End of {1}_base_test
"""

sanityTest = """\
`ifndef {0}_SANITY_TEST__SV
`define {0}_SANITY_TEST__SV

  class {1}_sanity_test extends {1}_base_test;

    // Factory Registration
    `uvm_component_utils({1}_sanity_test)

    // Sequence to start
    {1}_sanity_seq seqh;

    extern function new(string name = "{1}_sanity_test", uvm_component parent=null);
    extern virtual function void build_phase(uvm_phase phase);
    extern virtual function void connect_phase(uvm_phase phase);
    extern virtual task run_phase(uvm_phase phase);
    extern virtual function void report_phase(uvm_phase phase);
  endclass

  function {1}_sanity_test::new(string name = "{1}_sanity_test", uvm_component parent=null);
    super.new(name, parent);
  endfunction

  function void {1}_sanity_test::build_phase(uvm_phase phase);
    super.build_phase(phase);
  endfunction

  function void {1}_sanity_test::connect_phase(uvm_phase phase);
    super.connect_phase(phase);
  endfunction

  task {1}_sanity_test::run_phase(uvm_phase phase);
    super.run_phase(phase);
    phase.raise_objection(this);
    `uvm_info(get_full_name(), "[{1}] Starting sanity Test", UVM_NONE)
    seqh = {1}_sanity_seq::type_id::create("seqh");
    seqh.start(envh.agnth.seqrh);
    phase.drop_objection(this);
  endtask

  function void {1}_sanity_test::report_phase(uvm_phase phase);
    super.report_phase(phase);
  endfunction

`endif

//End of {1}_sanity_test
"""

uvmEnv = """\
`ifndef {0}_ENV__SV
`define {0}_ENV__SV

  class {1}_env extends uvm_env;

    // Factory Registration
    `uvm_component_utils({1}_env)

    // Environment Variables
    bit is_scoreboard_enable = 1;
    bit is_coverage_enable = 1;

    // Declare UVC
    {1}_agent_cfg agnt_cfg;
    {1}_agent agnth;
    {1}_sb sbh;
    {1}_cov covh;

    extern function new (string name = "{1}_env", uvm_component parent = null);
    extern virtual function void build_phase(uvm_phase phase);
    extern virtual function void connect_phase(uvm_phase phase);
  endclass

  function {1}_env::new(string name = "{1}_env", uvm_component parent = null);
    super.new(name, parent);
  endfunction

  function void {1}_env::build_phase(uvm_phase phase);
    super.build_phase(phase);
    `uvm_info(get_full_name(), "[{0}] Starting Build Phase", UVM_LOW)
    agnt_cfg = {1}_agent_cfg::type_id::create("agnt_cfg");
    uvm_config_db #({1}_agent_cfg)::set(this, "*", "agnt_cfg", agnt_cfg);
    agnth = {1}_agent::type_id::create("agnth", this);
    if(is_scoreboard_enable) begin
      sbh = {1}_sb::type_id::create("sbh", this);
    end
    if(is_coverage_enable) begin
      covh = {1}_cov::type_id::create("covh", this);
    end
    `uvm_info(get_full_name(), "[{0}] Ending Build Phase", UVM_LOW)
  endfunction

  function void {1}_env::connect_phase(uvm_phase phase);
    super.connect_phase(phase);
    `uvm_info(get_full_name(), "[{0}] Starting Connect Phase", UVM_LOW)
    if(is_scoreboard_enable) begin
      agnth.monh.mon_port.connect(sbh.sb_fifo.analysis_export);
    end
    if(is_coverage_enable) begin
      agnth.monh.mon_port.connect(covh.analysis_export);
    end
    `uvm_info(get_full_name(), "[{0}] Ending Connect Phase", UVM_LOW)
  endfunction

`endif

//End of {1}_env
"""

envPkg = """\
`ifndef {0}_ENV_PKG__SV
`define {0}_ENV_PKG__SV

  package {1}_env_pkg;

    // Import UVM
    import uvm_pkg::*;
    import {1}_seq_pkg::*;
    import {1}_regs_pkg::*;
    import {1}_agent_pkg::*;
    `include "uvm_macros.svh"

    // Import UVM
    `include "{1}_sb.sv"
    `include "{1}_cov.sv"
    `include "{1}_env.sv"
  endpackage

`endif

//End of {1}_env_pkg
"""

uvmSb  = """\
`ifndef {0}_SB__SV
`define {0}_SB__SV

  class {1}_sb extends uvm_scoreboard;

    // Factory Registration
    `uvm_component_utils({1}_sb)

    // Analysis Fifo
    uvm_tlm_analysis_fifo #({1}_seq_item) sb_fifo;

    // Data Item
    {1}_seq_item seq_item;

    // Tasks and Functions
    extern function new(string name = "{1}_sb", uvm_component parent = null);
    extern virtual function void build_phase(uvm_phase phase);
    extern virtual task run_phase(uvm_phase phase);
  endclass

  function {1}_sb::new(string name = "{1}_sb", uvm_component parent = null);
    super.new(name, parent);
  endfunction

  function void {1}_sb::build_phase(uvm_phase phase);
    super.build_phase(phase);
    sb_fifo = new("sb_fifo", this);
  endfunction

  task {1}_sb::run_phase(uvm_phase phase);
    forever begin
      sb_fifo.get(seq_item);
      `uvm_info(get_full_name(), "[{0}] Received new item in SB", UVM_LOW)
      `uvm_info(get_full_name(), $sformatf("\\n[{0}] Packet Data:\\n\\twe: %0d,\\n\\taddr: %0d,\\n\\twdata: %0d,\\n\\trdata: %0d",
      seq_item.we, seq_item.addr, seq_item.wdata, seq_item.rdata), UVM_LOW)
    end
  endtask

`endif

//End of {1}_sb
"""

uvmCov  = """\
`ifndef {0}_COV__SV
`define {0}_COV__SV

  class {1}_cov extends uvm_subscriber#({1}_seq_item);

    // Factory Registration
    `uvm_component_utils({1}_cov)

    extern function new(string name = "{1}_cov", uvm_component parent = null);
    extern virtual function void write({1}_seq_item t);
  endclass

  function {1}_cov::new(string name = "{1}_cov", uvm_component parent = null);
    super.new(name, parent);
  endfunction

  function void {1}_cov::write({1}_seq_item t);
    `uvm_info(get_full_name(), "[{0}] Received item in Subscriber", UVM_LOW)
    `uvm_info(get_full_name(), $sformatf("\\n[{0}] Packet Data:\\n\\twe: %0d,\\n\\taddr: %0d,\\n\\twdata: %0d,\\n\\trdata: %0d",
      t.we, t.addr, t.wdata, t.rdata), UVM_LOW)
  endfunction

`endif

//End of {1}_cov
"""

agntPkg = """\
`ifndef {0}_AGENT_PKG__SV
`define {0}_AGENT_PKG__SV

  package {1}_agent_pkg;

    // Import UVM
    import uvm_pkg::*;
    import {1}_regs_pkg::*;
    import {1}_seq_pkg::*;
    `include "uvm_macros.svh"

    // Include Agent UVCs
    // `include "{1}_intf.sv"
    `include "{1}_agent_cfg.sv"
    `include "{1}_driver.sv"
    `include "{1}_monitor.sv"
    `include "{1}_sequencer.sv"
    `include "{1}_agent.sv"
  endpackage

`endif

//End of {1}_agent_pkg
"""

uvmAgnt = """\
`ifndef {0}_AGENT__SV
`define {0}_AGENT__SV

  class {1}_agent extends uvm_agent;

    // Factory Registration
    `uvm_component_utils({1}_agent)

    // Agent config
    {1}_agent_cfg agnt_cfg;

    // UVCs
    {1}_driver     drvh;
    {1}_monitor    monh;
    {1}_sequencer  seqrh;

    // Tasks and Functions
    extern function new(string name = "{1}_agent", uvm_component parent = null);
    extern virtual function void build_phase(uvm_phase phase);
    extern virtual function void connect_phase(uvm_phase phase);
    // extern virtual task run_phase(uvm_phase);
  endclass

  function {1}_agent::new(string name = "{1}_agent", uvm_component parent = null);
    super.new(name, parent);
  endfunction

  function void {1}_agent::build_phase(uvm_phase phase);
    super.build_phase(phase);
    `uvm_info(get_full_name(), "[{0}] Starting Build Phase", UVM_LOW)

    // agnt_cfg = {1}_agent_cfg::type_id::create("agnt_cfg");
    if(!uvm_config_db#({1}_agent_cfg)::get(this, "", "agnt_cfg", agnt_cfg)) begin
      `uvm_fatal(get_type_name(), "[{0}] Couldn't get agnt_cfg, did you set it?")
    end

    // Build UVC
    monh = {1}_monitor::type_id::create("monh", this);
    if(agnt_cfg.is_active == UVM_ACTIVE) begin
      drvh = {1}_driver::type_id::create("drvh", this);
      seqrh = {1}_sequencer::type_id::create("seqrh", this);
    end
    `uvm_info(get_full_name(), "[{0}] Ending Build Phase", UVM_LOW)
  endfunction

  function void {1}_agent::connect_phase(uvm_phase phase);
    super.connect_phase(phase);
    `uvm_info(get_full_name(), "[{0}] Starting Connect Phase", UVM_LOW)
    if(agnt_cfg.is_active == UVM_ACTIVE) begin
      drvh.seq_item_port.connect(seqrh.seq_item_export);
    end
    `uvm_info(get_full_name(), "[{0}] Ending Connect Phase", UVM_LOW)
  endfunction

`endif

//End of {1}_agent
"""

agntCfg = """\
`ifndef {0}_AGENT_CFG__SV
`define {0}_AGENT_CFG__SV

  class {1}_agent_cfg extends uvm_object;

    // Factory Registration
    `uvm_object_utils({1}_agent_cfg)

    // UVM Agent Controls

    uvm_active_passive_enum is_active = UVM_ACTIVE;

    // Tasks and Functions

    extern function new(string name = "{1}_agent_cfg");

  endclass

  function {1}_agent_cfg::new(string name = "{1}_agent_cfg");
    super.new(name);
  endfunction

`endif

//End of {1}_agent_cfg
"""

svIntf = """\
`ifndef {0}_INTF__SV
`define {0}_INTF__SV

  interface {1}_intf(input clk);

    // Signals
    logic we;
    logic [3:0] addr;
    logic [7:0] wdata;
    logic [7:0] rdata;

  endinterface

`endif

//End of {1}_intf
"""

uvmDrv = """\
`ifndef {0}_DRIVER__SV
`define {0}_DRIVER__SV

  class {1}_driver extends uvm_driver #({1}_seq_item);

    // Factory Registeration
    `uvm_component_utils({1}_driver)

    // Virtual Interface
    virtual {1}_intf vintf;

    // Tasks and Functions
    extern function new(string name = "{1}_driver", uvm_component parent = null);
    extern virtual function void build_phase(uvm_phase phase);
    // extern virtual function void connect_phase(uvm_phase phase);
    extern virtual task reset_phase(uvm_phase phase);
    extern virtual task run_phase(uvm_phase phase);
    extern virtual task drive_task({1}_seq_item seq_item);
  endclass

  function {1}_driver::new(string name = "{1}_driver", uvm_component parent = null);
    super.new(name, parent);
  endfunction

  function void {1}_driver::build_phase(uvm_phase phase);
    super.build_phase(phase);
    if(!uvm_config_db#(virtual {1}_intf)::get(this, "", "vintf", vintf)) begin
      `uvm_fatal(get_type_name(),"[{0}] Couldn't get vintf, did you set it?")
    end
  endfunction

  task {1}_driver::drive_task({1}_seq_item seq_item);
    `uvm_info(get_full_name(), "[{0}] Received Sequence Item in Driver", UVM_LOW)
    @(negedge vintf.clk);
    vintf.we <= seq_item.we;
    vintf.addr <= seq_item.addr;
    vintf.wdata <= seq_item.wdata;
  endtask

  task {1}_driver::reset_phase(uvm_phase phase);
    super.reset_phase(phase);
    phase.raise_objection(this);
    `uvm_info(get_full_name(), "[{0}] Resetting DUT from Driver", UVM_NONE)
    vintf.we     <= 'd0;
    vintf.addr   <= 'd0;
    vintf.wdata  <= 'd0;
    @(posedge vintf.clk);
    phase.drop_objection(this);
  endtask

  task {1}_driver::run_phase(uvm_phase phase);
    // super.run_phase(phase);
    forever begin
      seq_item_port.get_next_item(req);
      drive_task(req);
      seq_item_port.item_done();
    end
  endtask

`endif

//End of {1}_driver
"""

uvmMon = """\
`ifndef {0}_MONITOR__SV
`define {0}_MONITOR__SV

  class {1}_monitor extends uvm_monitor;

    // Factory Registration
    `uvm_component_utils({1}_monitor)

    // Variables
    {1}_seq_item {1}_seq_item_h;

    // Interface
    virtual {1}_intf vintf;

    // Analysis Port
    uvm_analysis_port #({1}_seq_item) mon_port;

    // Tasks and Functions

    extern function new(string name = "{1}_monitor", uvm_component parent = null);
    extern virtual function void build_phase(uvm_phase phase);
    // extern virtual function void connect_phase(uvm_phase phase);
    extern virtual task run_phase(uvm_phase phase);
    extern virtual task mon_task();

  endclass

  function {1}_monitor::new(string name = "{1}_monitor", uvm_component parent = null);
    super.new(name, parent);
  endfunction

  function void {1}_monitor::build_phase(uvm_phase phase);
    super.build_phase(phase);
    if(!uvm_config_db#(virtual {1}_intf)::get(this, "", "vintf", vintf)) begin
      `uvm_fatal(get_type_name(), "[{0}] Couldn't get vintf, did you set it?")
    end
    mon_port = new("mon_port", this);
  endfunction

  task {1}_monitor::run_phase(uvm_phase phase);
    super.run_phase(phase);
    mon_task();
  endtask

  task {1}_monitor::mon_task();
    {1}_seq_item_h = {1}_seq_item::type_id::create("{1}_seq_item_h");
    forever begin
      @(posedge vintf.clk);
      {1}_seq_item_h.we     = vintf.we;
      {1}_seq_item_h.addr   = vintf.addr;
      {1}_seq_item_h.wdata  = vintf.wdata;
      {1}_seq_item_h.rdata  = vintf.rdata;
      mon_port.write({1}_seq_item_h);
      `uvm_info(get_full_name(), "[{0}] Written Sequence Item from Monitor", UVM_LOW)
    end
  endtask

`endif

//End of {1}_monitor
"""

uvmSeqr = """\
`ifndef {0}_SEQUENCER__SV
`define {0}_SEQUENCER__SV

  class {1}_sequencer extends uvm_sequencer#({1}_seq_item);

    // Factory Registration
    `uvm_component_utils({1}_sequencer)

    // Tasks and Functions
    extern function new(string name = "{1}_sequencer", uvm_component parent = null);
  endclass

  function {1}_sequencer::new(string name = "{1}_sequencer", uvm_component parent = null);
    super.new(name, parent);
  endfunction

`endif

//End of {1}_sequencer
"""

seqPkg = """\
`ifndef {0}_SEQ_PKG__SV
`define {0}_SEQ_PKG__SV

  package {1}_seq_pkg;

    // Import UVM Macros and Package
    import uvm_pkg::*;
    `include "uvm_macros.svh"

    // Include all sequence items and sequences
    `include "{1}_seq_item.sv"
    `include "{1}_base_seq.sv"
    `include "{1}_sanity_seq.sv"

  endpackage

`endif

//End of {1}_seq_pkg
"""

baseSeq = """\
`ifndef {0}_BASE_SEQ__SV
`define {0}_BASE_SEQ__SV

  class {1}_base_seq extends uvm_sequence#({1}_seq_item);

    // Factory Registration
    `uvm_object_utils({1}_base_seq)

    // Variables

    // Tasks and Functions
    extern function new(string name = "{1}_base_seq");
    extern virtual task body();

  endclass

  function {1}_base_seq::new(string name = "{1}_base_seq");
    super.new(name);
  endfunction

  task {1}_base_seq::body();

  endtask

`endif

//End of {1}_base_seq
"""

sanitySeq = """\
`ifndef {0}_SANITY_SEQ__SV
`define {0}_SANITY_SEQ__SV

  class {1}_sanity_seq extends {1}_base_seq;

    // Factory Registration
    `uvm_object_utils({1}_sanity_seq)

    // Variables

    // Tasks and Functions

    extern function new(string name = "{1}_sanity_seq");
    extern virtual task body();
  endclass

  function {1}_sanity_seq::new(string name = "{1}_sanity_seq");
    super.new(name);
  endfunction

  task {1}_sanity_seq::body();
    super.body();
    `uvm_info(get_full_name(), "[{0}] Starting Sanity Sequence", UVM_LOW)
    repeat(17) begin
      `uvm_do_with(req, {{we==1;}})
    end
    // wait_for_item_done();
  endtask

`endif

//End of {1}_sanity_seq
"""

seqItem = """\
`ifndef {0}_SEQ_ITEM__SV
`define {0}_SEQ_ITEM__SV

  class {1}_seq_item extends uvm_sequence_item;

    // Factory Registration
    `uvm_object_utils({1}_seq_item)

    // Randomization Variables
    rand logic we;
    randc logic [3:0] addr;
    rand logic [7:0] wdata;
    logic [7:0] rdata;

    constraint dataRange {{wdata inside{{[0:15]}};}}

    extern function new(string name = "{1}_seq_item");

  endclass

  function {1}_seq_item::new(string name = "{1}_seq_item");
    super.new(name);
  endfunction

`endif

//End of {1}_seq_item
"""

regsPkg = """\
`ifndef {0}_REGS_PKG__SV
`define {0}_REGS_PKG__SV

  package {1}_regs_pkg;

    // Import UVM
    import uvm_pkg::*;
    `include "uvm_macros.svh"

    // Include Reg Model UVCs

  endpackage

`endif

//End of {1}_regs_pkg
"""

readmeMD = """\
## {0} Architecture, Design and Verification Details

### Commands to run sanity test
#### Without Wave Dump
```bash
cd scripts
make run_all
```
#### With Waveform Dump
```bash
cd scripts
make run_all_gui
```
### Directory Structure
```
{0}
.
├── docs
├── README.md
├── rtl
│   └── {0}.sv
├── scripts
│   ├── logw.tcl
│   └── Makefile
├── sim
│   ├── env
│   │   ├── agent
│   │   │   ├── {0}_agent_cfg.sv
│   │   │   ├── {0}_agent_pkg.sv
│   │   │   ├── {0}_agent.sv
│   │   │   ├── {0}_driver.sv
│   │   │   ├── {0}_intf.sv
│   │   │   ├── {0}_monitor.sv
│   │   │   ├── {0}_sequencer.sv
│   │   │   ├── regs
│   │   │   │   └── {0}_regs_pkg.sv
│   │   │   └── sequence_lib
│   │   │       ├── {0}_base_seq.sv
│   │   │       ├── {0}_sanity_seq.sv
│   │   │       ├── {0}_seq_item.sv
│   │   │       └── {0}_seq_pkg.sv
│   │   ├── {0}_cov.sv
│   │   ├── {0}_env_pkg.sv
│   │   ├── {0}_env.sv
│   │   └── {0}_sb.sv
│   ├── tb
│   │   └── {0}_tb.sv
│   └── tests
│       ├── {0}_base_test.sv
│       ├── {0}_sanity_test.sv
│       └── {0}_test_pkg.sv
└── synth
```
**Note** : .gitignore is added to project directory for easy git integration.
"""

readmeSVMD = """\
## {0} Architecture, Design and Verification Details

### Commands to run sanity test
#### Without Wave Dump
```bash
cd scripts
make run_all
```
#### With Waveform Dump
```bash
cd scripts
make run_all_gui
```
### Directory Structure
```
{0}
.
├── docs
├── README.md
├── rtl
│   └── {0}.sv
├── scripts
│   ├── logw.tcl
│   └── Makefile
├── sim
│   └── tb
│       └── {0}_tb.sv
└── synth
```
**Note** : .gitignore is added to project directory for easy git integration.
"""

gitignore = """\
*
!*/
!.gitignore
!*.md
!*.pdf
!*.sv
!Makefile
!logw.tcl
!README.md
"""