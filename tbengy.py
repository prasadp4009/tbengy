#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Copyright Thu 07/20/2020  Prasad Pandit

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the "Software"), 
to deal in the Software without restriction, including without limitation the
rights to use, copy, modify, merge, publish, distribute, sublicense, and/or 
sell copies of the Software, and to permit persons to whom the Software is 
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in 
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A 
PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION 
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE 
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

File        : tbengy.py
Author      : Prasad Pandit
Email       : prasadp4009@gmail.com
Github      : https://github.com/prasadp4009
Description :  
"""
import sys
import os
import re
import textwrap
import getpass
from datetime import date

makefileStr="""\
# @Author : {0}
# @Date   : {1}

work = work

top_tb_name = {2}_tb

ifneq ("$(wildcard ../rtl)","") 
RTL = ../rtl/*.sv 
INCRTL = +incdir+../rtl 
else 
RTL = 
INCRTL = 
endif

ifneq ("$(wildcard ../sim/tb)","") 
TB = ../sim/tb/*.sv 
INCTB = +incdir+../sim/tb 
else 
TB = 
INCTB = 
endif

ifneq ("$(wildcard ../sim/env/agent)","") 
INTF = ../sim/env/agent/*intf.sv
INCINTF = +incdir+../sim/env/agent
else 
INTF = 
INCINTF = 
endif 

ifneq ("$(wildcard ../sim/env/agent)","") 
AGT = ../sim/env/agent/*pkg.sv
INCAGT = +incdir+../sim/env/agent 
else 
AGT = 
INCAGT = 
endif 

ifneq ("$(wildcard ../sim/env/agent/sequence_lib)","") 
SEQ_LIB = ../sim/env/agent/sequence_lib/*pkg.sv
INCSEQ_LIB = +incdir+../sim/env/agent/sequence_lib 
else 
SEQ_LIB = 
INCSEQ_LIB = 
endif

ifneq ("$(wildcard ../sim/env)","")
ENV = ../env/*pkg.sv
INCENV = +incdir+../sim/env
else
ENV =
INCENV =
endif

ifneq ("$(wildcard ../sim/env/agent/regs)","")
REG = ../sim/env/agent/regs/*pkg.sv
INCREG = +incdir+../sim/env/agent/regs
else
REG =
INCREG =
endif

ifneq ("$(wildcard ../sim/tests)","")
TESTS = ../sim/tests/*pkg.sv
INCTESTS = +incdir+../sim/tests
else
TESTS =
INCTESTS =
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
	xsim -wdb sim.wdb -log session.log -t logw.tcl $(top_tb_name)_sim
	xsim sim.wdb -gui

view_wave:
	xsim sim.wdb -gui

run_sim:
	xsim -runall -log session.log $(top_tb_name)_sim -testplusarg UVM_TESTNAME={2}_sanity_test 

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

def mod_gen():
  module_name = input("Enter name of module: ")
  if not re.match("^[A-Za-z0-9_]*$", module_name):
    if not re.match("^[A-Za-z_]*$", module_name[0]):
      print ("ERROR: Wrong module name format")
      sys.exit(0)
    
  try:
    module_name = module_name.lower()
    username = getpass.getuser()
    today = date.today()
    os.mkdir(module_name)
    os.chdir(module_name)
    module_name = module_name.lower()
    print ("Creating Directory: docs")
    os.mkdir("docs")
    print ("Creating Directory: rtl")
    os.mkdir("rtl")
    print ("Creating Directory: sim")
    os.mkdir("sim")
    os.chdir("./sim")
    print ("Creating Directory: tb")
    os.mkdir("tb")
    print ("Creating Directory: tests")
    os.mkdir("tests")
    print ("Creating Directory: env")
    os.mkdir("env")
    os.chdir("./env")
    print ("Creating Directory: agent")
    os.mkdir("agent")
    os.chdir("./agent")
    print ("Creating Directory: sequence_lib")
    os.mkdir("sequence_lib")
    print ("Creating Directory: regs")
    os.mkdir("regs")
    os.chdir("../../../")
    print ("Creating Directory: synth")
    os.mkdir("synth")
    print ("Creating Directory: scripts")
    os.mkdir("scripts")
    os.chdir("./rtl")
    module_rtl = module_name + ".sv"
    print ("Creating file: ",module_rtl)
    module_file = open(module_rtl,'w')
    module_file.write(textwrap.dedent("""\
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
    """.format(module_name.upper(),module_name)))
    module_file.close()
    os.chdir("../sim/tb")
    module_tb = module_name + "_tb.sv"
    print ("Creating file: ",module_tb)
    module_file = open(module_tb,'w')
    module_file.write(textwrap.dedent("""\
    `ifndef {0}_TB__SV
    `define {0}_TB__SV

      // Generated by tbengy. Created by Prasad Pandit.

      `timescale 1ns/1ps
      `include "uvm_macros.svh"

      module {1}_tb;
        import {1}_test_pkg::*;
        import uvm_pkg::*;

        logic clk;

        //{1}_intf intf(.clk(clk));

        initial begin
          clk = 0;
          forever begin
            #10 clk = ~clk;
          end
        end

        initial begin
          //uvm_config_db #(virtual {1}_intf)::set(null, "*", "vintf", intf);
          run_test();
        end
      endmodule

    `endif

    //End of {1}_tb
    """.format(module_name.upper(),module_name)))
    module_file.close()
    os.chdir("../../scripts")
    module_mk = "Makefile"
    print ("Creating file: ",module_mk)
    module_file = open(module_mk,'w')
    module_file.write(makefileStr.format(username,today,module_name))
    module_file.close()
    fileName = "logw.tcl"
    print ("Creating file: logw.tcl")
    module_file = open(fileName,'w')
    module_file.write(xsimWaveTclStr)
    module_file.close()
    os.chdir("../sim/tests")
    fileName = module_name+"_test_pkg.sv"
    print ("Creating file: ",fileName)
    module_file = open(fileName, 'w')
    module_file.write(textwrap.dedent("""\
    `ifndef {0}_TEST_PKG__SV
    `define {0}_TEST_PKG__SV

      package {1}_test_pkg;

        // Import UVM
        import uvm_pkg::*;
        //import {1}_seq_pkg::*;
        //import {1}_regs_pkg::*;
        //import {1}_agent_pkg::*;
        //import {1}_env_pkg::*;
        `include "uvm_macros.svh"

        // Import UVC
        `include "{1}_base_test.sv"
        `include "{1}_sanity_test.sv"

      endpackage

    `endif

    //End of {1}_test_pkg
    """.format(module_name.upper(),module_name)))
    module_file.close()
    fileName = module_name+"_base_test.sv"
    print ("Creating file: ",fileName)
    module_file = open(fileName, 'w')
    module_file.write(textwrap.dedent("""\
    `ifndef {0}_BASE_TEST__SV
    `define {0}_BASE_TEST__SV

      class {1}_base_test extends uvm_test;

        // Factory Registration
        `uvm_component_utils({1}_base_test)

        // Declare UVC
        // {1}_env envh;

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
        //envh = {1}_env::type_id::create("envh", this);
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
    """.format(module_name.upper(),module_name)))
    module_file.close()
    fileName = module_name+"_sanity_test.sv"
    print ("Creating file: ",fileName)
    module_file = open(fileName, 'w')
    module_file.write(textwrap.dedent("""\
    `ifndef {0}_SANITY_TEST__SV
    `define {0}_SANITY_TEST__SV

      class {1}_sanity_test extends {1}_base_test;

        // Factory Registration
        `uvm_component_utils({1}_sanity_test)

        // Sequence to start
        // {1}_sanity_seq seqh;

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
        //seqh = {1}_sanity_seq::type_id::create("seqh");
        //seqh.start(envh.agnth.seqrh);
        phase.drop_objection(this);
      endtask

      function void {1}_sanity_test::report_phase(uvm_phase phase);
        super.report_phase(phase);
      endfunction

    `endif

    //End of {1}_sanity_test
    """.format(module_name.upper(),module_name)))
    module_file.close()
    os.chdir("../../../")
    print ("+_+_+_+_+_+_+_+ Done with module creation....!!!!! +_+_+_+_+_+_+_+\n")
      
  except FileNotFoundError as err:
    print("Error: File Not Found", format(err))
    sys.exit(0)
  except NameError as err:
    print("Error: Undefined variable", format(err))
    sys.exit(0)

  sys.exit(0)

def main():
  print ("+_+_+_+_+_+_+_+ Welcome to tbengy a UVM Project Generator for Vivado 2020.x +_+_+_+_+_+_+_+\n")
  mod_gen()

if __name__ == "__main__":
  main()