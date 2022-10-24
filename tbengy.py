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
import shutil
import sys
import os
import re
import getpass
import argparse
from datetime import date
from sys import version

from uvmTemplate import agntCfg, agntPkg, baseSeq, baseTest, envPkg, gitignore, makefileStr, makefileSVStr,        \
                        readmeMD, readmeSVMD, regsPkg, rtlModule, rtlSVModule, sanitySeq, sanityTest, seqItem,     \
                        seqPkg, svIntf, tbModule, tbSVModule, testPkg, uvmAgnt, uvmCov, uvmDrv, uvmEnv, uvmMon,    \
                        uvmSb, uvmSeqr, xsimWaveTclStr, synthCommandStr, synthTclStr, rtlSVExModule, tbSVExModule, \
                        readmeSVEXMD

toolVersion = "tbengy v2"
moduleName = "na"
dirPath = "./"
tbType = "uvm"
boardsFilePath = "./digilent-xdc"
username = getpass.getuser()
today = date.today()
parser = argparse.ArgumentParser()
mutuallyExclusiveArgs = parser.add_mutually_exclusive_group(required=True)
boardList = []
boardName = ""
fpgaName = ""
clkFreq = "125"

def listBoards(onlyList=False):
  if os.path.exists(boardsFilePath):
    count = 0
    boardList = []
    if not onlyList:
      print("[tbengy] Available boards:")
    for board in os.listdir(boardsFilePath):
      if board.endswith(".xdc"):
        boardName = board.replace(".xdc","").replace("-Master","").strip()
        boardList.append(boardName)
        if not onlyList:
          print("[tbengy] "+boardName)
        count += 1
    if count == 0:
      print("[tbengy] No boards found. Please download digilent-xdc from https://github.com/Digilent/digilent-xdc.git and place it in current directory under digilent-xdc.")
      sys.exit(0)
    else:
      print("[tbengy] Total boards found: "+str(count))
      return boardList
  else:
    print("[tbengy] No boards found. Please download digilent-xdc from https://github.com/Digilent/digilent-xdc.git and place it in current directory under digilent-xdc.")
    sys.exit(0)

def genTBF(fileName, tmplStr, fFields):
  try:
    print("[tbengy] Creating file: ",fileName)
    moduleFile = open(fileName, 'w', encoding="utf-8")
    moduleFile.write(tmplStr.format(*fFields))
    moduleFile.close()
  except IOError:
    print("[tbengy] Falied to Write: "+fileName)
    print("[tbengy] Please check write permissions. Exiting now.")
    sys.exit(0)

def genTBC(tbDict, dirDictIn):
  for tbComp, compData in tbDict.items():
    compType, fileName, compTmpl, tmplArgs = compData
    print("[tbengy] Generating "+tbComp)
    genTBF(dirDictIn[compType]+"/"+fileName,compTmpl,tmplArgs)

def genDirStruct(dirDictIn):
  for dirName, dirPath in dirDictIn.items():
    if not os.path.exists(dirPath):
      print("[tbengy] Creating Directory: " + dirName)
      os.makedirs(dirPath, exist_ok=True)

def copyDictFiles(dirDictIn, copyDictIn):
  for dirName, fileToCopyPath in copyDictIn.items():
    if os.path.exists(dirDictIn[dirName]):
      if os.path.isfile(fileToCopyPath):
        print("[tbengy] Copying File "+fileToCopyPath+" to directory: " + dirDictIn[dirName])
        shutil.copy(fileToCopyPath,dirDictIn[dirName])
      else:
        print("[tbengy] Unable to find file, file copying failed: " + fileToCopyPath)
    else:
      print("[tbengy] Unable to find directory, file copying failed: " + dirDictIn[dirName])

def getClkFreq(boardFilePath):
  clkFreqFromFile = ""
  if os.path.isfile(boardFilePath):
    with open(boardFilePath, 'r',  encoding="utf-8") as boardData:
      eachLine = boardData.readline()
      clockFound = False
      print("[tbengy] Finding Clock Frequency in XDC: "+boardFilePath)
      while eachLine:
        # print("[tbengy] Checking Line: "+eachLine.strip())
        if eachLine.strip().startswith("## clk = "):
          clkFreqStr = eachLine.strip().split("=")[1]
          clkFreqFromFile = ""
          for eachChar in clkFreqStr:
            if eachChar.isdigit():
              clkFreqFromFile += eachChar
          clockFound = True
          break
        eachLine = boardData.readline()
      if clockFound:
        print("[tbengy] Clock Frequency Found in XDC: "+clkFreqFromFile)
      else:
        clkFreqFromFile = "125"
        print("[tbengy] (Warning) Falied to find Clock Frequency (a random default will be used): "+clkFreqFromFile)
      return clkFreqFromFile
  else:
    print("[tbengy] Falied to find and read: "+boardFilePath)
    sys.exit(0)

def mod_gen():
  global moduleName
  global dirPath
  global tbType
  global boardName
  global boardFileName
  global fpgaName
  global clkFreq
  dirDict       = {}
  tmplDict      = {}
  copyFilesDict = {}
  if tbType == "sv" and boardName == "":
    dirDict = {
      moduleName      : dirPath+moduleName,
      "readmeMD"      : dirPath+moduleName,
      "gitignore"     : dirPath+moduleName,
      "docs"          : dirPath+moduleName+"/docs",
      "rtl"           : dirPath+moduleName+"/rtl",
      "sim"           : dirPath+moduleName+"/sim",
      "synth"         : dirPath+moduleName+"/synth",
      "scripts"       : dirPath+moduleName+"/scripts",
      "tb"            : dirPath+moduleName+"/sim/tb"
    }
    tmplDict = {
      "RTL"           : ["rtl", moduleName+".sv", rtlSVModule, [moduleName.upper(), moduleName]],
      "Makefile"      : ["scripts", "Makefile", makefileSVStr, [username,today,moduleName]],
      "Wave Gen Tcl"  : ["scripts", "logw.tcl", xsimWaveTclStr, []],
      "TB Top"        : ["tb", moduleName+"_tb.sv", tbSVModule, [moduleName.upper(), moduleName]],
      "Readme"        : ["readmeMD", "README.md", readmeSVMD, [moduleName]],
      "Gitignore"     : ["gitignore", ".gitignore", gitignore, []]
    }
  elif tbType == "sv" and boardName != "":
    dirDict = {
      moduleName      : dirPath+moduleName,
      "readmeMD"      : dirPath+moduleName,
      "gitignore"     : dirPath+moduleName,
      "docs"          : dirPath+moduleName+"/docs",
      "rtl"           : dirPath+moduleName+"/rtl",
      "sim"           : dirPath+moduleName+"/sim",
      "synth"         : dirPath+moduleName+"/synth",
      "scripts"       : dirPath+moduleName+"/scripts",
      "tb"            : dirPath+moduleName+"/sim/tb"
    }
    tmplDict = {
      "RTL"           : ["rtl", moduleName+".sv", rtlSVExModule, [moduleName.upper(), moduleName, clkFreq]],
      "Makefile"      : ["scripts", "Makefile", makefileSVStr+synthCommandStr, [username,today,moduleName]],
      "Wave Gen Tcl"  : ["scripts", "logw.tcl", xsimWaveTclStr, []],
      "TB Top"        : ["tb", moduleName+"_tb.sv", tbSVExModule, [moduleName.upper(), moduleName]],
      "Synth Tcl"     : ["scripts", "synth.tcl", synthTclStr, [fpgaName, boardFileName.replace(".xdc",""), moduleName]],
      "Readme"        : ["readmeMD", "README.md", readmeSVEXMD, [moduleName, boardFileName.replace(".xdc","")]],
      "Gitignore"     : ["gitignore", ".gitignore", gitignore, []]
    }
    copyFilesDict = {
      "synth"         : boardsFilePath+"/"+boardFileName
    }
  else:
    dirDict = {
      moduleName      : dirPath+moduleName,
      "readmeMD"      : dirPath+moduleName,
      "gitignore"     : dirPath+moduleName,
      "docs"          : dirPath+moduleName+"/docs",
      "rtl"           : dirPath+moduleName+"/rtl",
      "sim"           : dirPath+moduleName+"/sim",
      "synth"         : dirPath+moduleName+"/synth",
      "scripts"       : dirPath+moduleName+"/scripts",
      "env"           : dirPath+moduleName+"/sim/env",
      "tb"            : dirPath+moduleName+"/sim/tb",
      "tests"         : dirPath+moduleName+"/sim/tests",
      "agent"         : dirPath+moduleName+"/sim/env/agent",
      "regs"          : dirPath+moduleName+"/sim/env/agent/regs",
      "sequence_lib"  : dirPath+moduleName+"/sim/env/agent/sequence_lib"
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
  print("[tbengy] Starting Generation of " + tbType.upper() + " Testbench")
  genDirStruct(dirDict)
  genTBC(tmplDict, dirDict)
  copyDictFiles(dirDict, copyFilesDict)
  print ("+_+_+_+_+_+_+_+ Done with module creation....!!!!! +_+_+_+_+_+_+_+\n")

def parserSetup():
  global parser
  global toolVersion
  parser.add_argument('-v', '--version', action='version',
                      version=toolVersion, help="Show tbengy version and exit")
  mutuallyExclusiveArgs.add_argument('-l', '--listboards', action='store_true', help="Show the list of available boards and exit")
  mutuallyExclusiveArgs.add_argument('-m', '--modulename', nargs=1, metavar='<module_name>',
                      type=str, help="Module name for which TB to be generated. Ex. -m my_design")
  parser.add_argument('-t', '--tbtype', nargs=1, metavar='<tb_type>', required=False,
                      type=str, default='uvm', choices=['uvm', 'sv'], help="Testbench type to be generated. Ex. -t uvm or -t sv")
  parser.add_argument('-b', '--boardtype', nargs=1, metavar='<board_type>', required=False,
                      type=str, help="Board Files to be added. Ex. -b zybo, -b nexys4_ddr, -b zybo-z7 etc.")
  parser.add_argument('-f', '--fpga', nargs=1, metavar='<fpga>', required=False,
                      type=str, help="FPGA used in board. Ex. -f xc7z010clg400-1, -f xc7a100tcsg324-1, -f xc7z010clg400-1 etc. for Zybo, Nexys 4 DDR and Zybo-Z7-10 respectively")
  parser.add_argument('-d', '--dirpath', nargs=1, metavar='<dir_path>',
                      type=str, help="Directory under which TB should be generated. Ex. -d ./myProjects/TB. Default is present working dir.")
  return parser.parse_args()

def main():
  global moduleName
  global dirPath
  global tbType
  global boardName
  global fpgaName
  global clkFreq
  global boardFileName
  global boardsFilePath
  args = parserSetup()
  if args.listboards:
    listBoards()
    sys.exit(0)
  if args.modulename:
    moduleName = args.modulename[0]
    if re.match(r'^\w+$', moduleName) and (moduleName[0].isalpha() or moduleName[0] == '_'):
      print("[tbengy] Module Name: "+ moduleName)
    else:
      print("[tbengy] ERROR: Incorrect module name format. Exiting Now.")
      sys.exit(0)
    if args.boardtype:
      if args.fpga:
        fpgaName = args.fpga[0].strip()
        print("[tbengy] FPGA Selected: "+fpgaName)
      else:
        print("[tbengy] FPGA info is needed with board. Please provide and re-run the script. Exiting...")
        sys.exit(0)
      boardName = args.boardtype[0].strip()
      boardAvailable = False
      boardNameAsFile = ""
      boardNameClean = boardName.replace("-","").replace("_","")
      availableBoardList = listBoards(True)
      for board in availableBoardList:
        boardAvailableCheckClean = board.replace("-","").replace("_","")
        if boardNameClean.upper() == boardAvailableCheckClean.upper():
          boardAvailable = True
          boardNameAsFile = board
          break
      if boardAvailable:
        boardName = boardNameAsFile
        boardFileName = boardNameAsFile + "-Master.xdc"
        if os.path.isfile(boardsFilePath+"/"+boardFileName):
          print("[tbengy] Board " + boardName + " found.")
          print("[tbengy] Board File " + boardsFilePath + "/" + boardFileName + " found.")
        else:
          print("[tbengy] Board File " + boardsFilePath + "/" + boardFileName + " not found. Exiting...")
          sys.exit(0)
        clkFreq = getClkFreq(boardsFilePath+"/"+boardFileName)
      else:
        print("[tbengy] Board " + boardName + " not found. Exiting...")
        sys.exit(0)
    if args.dirpath:
      checkPath = os.path.expandvars(args.dirpath[0])
      if os.path.exists(checkPath):
        checkPath = os.path.abspath(checkPath)
        dirPath = checkPath if '/' == checkPath[-1] else checkPath + '/'
      else:
        print("[tbengy] Error: Directory path or Environement Variable don't exist - "+checkPath)
        sys.exit(0)
    else:
      dirPath = os.getcwd() + '/'
    if args.tbtype:
      tbType = args.tbtype[0]
    print("[tbengy] TB Directory: "+dirPath)
    toolVersionCheck = os.popen("vivado -version")
    toolVersionCheck = toolVersionCheck.readline()
    if "Vivado" in toolVersionCheck:
      if  "202" not in toolVersionCheck:
        print("[tbengy] Warning: The Vivado Version you have may not support the Makefile commands. Please download Vivado 2020.1 or greater")
      else:
        print("[tbengy] Vivado found and mapped correctly: " + toolVersionCheck.strip())
    else:
      print("[tbengy] Warning: No Vivado found or not in Path variables. Makefile won't work correctly. Please download Vivado 2020.x and map to Path variable")
    print ("+_+_+_+_+_+_+_+ Welcome to tbengy a SV/UVM Project Generator +_+_+_+_+_+_+_+\n")
    mod_gen()
  else:
    print("[tbengy] ERROR: Module name required. Exiting Now. Pass -h for help.")
    sys.exit(0)

if __name__ == "__main__":
  main()