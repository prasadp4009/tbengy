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
Description : tbengy is a UVM Testbench generation tool
              It generates UVCs and Makefile with right away compilation ready
              The Makefile supports compilation instructions for Vivado 2020.x
Usage       : The tool requires Python 3x and uses standard Python libraries
              Run command - 
                python tbengy.py
                Enter the module name: <your_module_name>
              The tool will now generate directory of <your_module_name>
              Go to the directory and open README.md on directory structure and
              TB simulation instructions
"""
import sys
import os
import re
import getpass
from datetime import date

from uvmTemplate import agntCfg, agntPkg, baseSeq, baseTest, envPkg, gitignore, makefileStr, readmeMD, regsPkg, rtlModule, sanitySeq, sanityTest, seqItem, seqPkg, svIntf, tbModule, testPkg, uvmAgnt, uvmCov, uvmDrv, uvmEnv, uvmMon, uvmSb, uvmSeqr, xsimWaveTclStr

moduleName = "na"
username = getpass.getuser()
today = date.today()


def genTBF(fileName, tmplStr, fFields):
  try:
    print ("Creating file: ",fileName)
    moduleFile = open(fileName, 'w')
    moduleFile.write(tmplStr.format(*fFields))
    moduleFile.close()
  except IOError:
    print("Falied to Write: "+fileName)
    print("Please check write permissions. Exiting now.")
    sys.exit(0)

def genTBC(tbDict, dirDictIn):
  for tbComp, compData in tbDict.items():
    compType, fileName, compTmpl, tmplArgs = compData
    print("Generating "+tbComp)
    genTBF(dirDictIn[compType]+"/"+fileName,compTmpl,tmplArgs)

def genDirStruct(dirDictIn):
  for dirName, dirPath in dirDictIn.items():
    if not os.path.exists(dirPath):
      print ("Creating Directory: " + dirName)
      os.makedirs(dirPath, exist_ok=True)

def mod_gen():
  global moduleName
  dirDict = {
    moduleName      : "./"+moduleName,
    "readmeMD"      : "./"+moduleName,
    "gitignore"     : "./"+moduleName,
    "docs"          : "./"+moduleName+"/docs",
    "rtl"           : "./"+moduleName+"/rtl",
    "sim"           : "./"+moduleName+"/sim",
    "synth"         : "./"+moduleName+"/synth",
    "scripts"       : "./"+moduleName+"/scripts",
    "env"           : "./"+moduleName+"/sim/env",
    "tb"            : "./"+moduleName+"/sim/tb",
    "tests"         : "./"+moduleName+"/sim/tests",
    "agent"         : "./"+moduleName+"/sim/env/agent",
    "regs"          : "./"+moduleName+"/sim/env/agent/regs",
    "sequence_lib"  : "./"+moduleName+"/sim/env/agent/sequence_lib"
  }
  tmplDict = {
    "RTL"           : ["rtl", moduleName+".sv", rtlModule, [moduleName.upper(), moduleName]],
    "Makefile"      : ["scripts", "Makefile", makefileStr, [username,today,moduleName]],
    "Wave Gen Tcl"  : ["scripts", "logw.tcl", xsimWaveTclStr, []],
    "TB Top"        : ["tb", moduleName+"_tb.sv", tbModule, [moduleName.upper(), moduleName]],
    "Test Pkg"      : ["tests", moduleName+"_test_pkg.sv", testPkg, [moduleName.upper(), moduleName]],
    "Base Test"     : ["tests", moduleName+"_base_test.sv", baseTest, [moduleName.upper(), moduleName]],
    "Sanity Test"   : ["tests", moduleName+"_sanity_test.sv", sanityTest, [moduleName.upper(), moduleName]],
    "Env Pkg"       : ["env", moduleName+"_env_pkg.sv", envPkg, [moduleName.upper(), moduleName]],
    "UVM Env"       : ["env", moduleName+"_env.sv", uvmEnv, [moduleName.upper(), moduleName]],
    "UVM Cov"       : ["env", moduleName+"_cov.sv", uvmCov, [moduleName.upper(), moduleName]],
    "UVM Sb"        : ["env", moduleName+"_sb.sv", uvmSb, [moduleName.upper(), moduleName]],
    "Agent Pkg"     : ["agent", moduleName+"_agent_pkg.sv", agntPkg, [moduleName.upper(), moduleName]],
    "Agent Cfg"     : ["agent", moduleName+"_agent_cfg.sv", agntCfg, [moduleName.upper(), moduleName]],
    "UVM Agent"     : ["agent", moduleName+"_agent.sv", uvmAgnt, [moduleName.upper(), moduleName]],
    "SV Intf"       : ["agent", moduleName+"_intf.sv", svIntf, [moduleName.upper(), moduleName]],
    "UVM Drv"       : ["agent", moduleName+"_driver.sv", uvmDrv, [moduleName.upper(), moduleName]],
    "UVM Mon"       : ["agent", moduleName+"_monitor.sv", uvmMon, [moduleName.upper(), moduleName]],
    "UVM Seqr"      : ["agent", moduleName+"_sequencer.sv", uvmSeqr, [moduleName.upper(), moduleName]],
    "Regs Pkg"      : ["regs", moduleName+"_regs_pkg.sv", regsPkg, [moduleName.upper(), moduleName]],
    "Seq Pkg"       : ["sequence_lib", moduleName+"_seq_pkg.sv", seqPkg, [moduleName.upper(), moduleName]],
    "Seq Item"      : ["sequence_lib", moduleName+"_seq_item.sv", seqItem, [moduleName.upper(), moduleName]],
    "Base Seq"      : ["sequence_lib", moduleName+"_base_seq.sv", baseSeq, [moduleName.upper(), moduleName]],
    "Sanity Seq"    : ["sequence_lib", moduleName+"_sanity_seq.sv", sanitySeq, [moduleName.upper(), moduleName]],
    "Readme"        : ["readmeMD", "README.md", readmeMD, [moduleName]],
    "Gitignore"     : ["gitignore", ".gitignore", gitignore, []]
  }
  print ("Starting Generation of Testbench")
  genDirStruct(dirDict)
  genTBC(tmplDict, dirDict)
  print ("+_+_+_+_+_+_+_+ Done with module creation....!!!!! +_+_+_+_+_+_+_+\n")

def main():
  global moduleName
  print ("+_+_+_+_+_+_+_+ Welcome to tbengy a UVM Project Generator for Vivado 2020.x +_+_+_+_+_+_+_+\n")
  moduleName = input("Enter name of module: ")
  if not re.match("^[A-Za-z0-9_]*$", moduleName):
    if not re.match("^[A-Za-z_]*$", moduleName[0]):
      print ("ERROR: Wrong module name format. Exiting Now.")
      sys.exit(0)
  else:
    moduleName = moduleName.lower()
    mod_gen()

if __name__ == "__main__":
  main()