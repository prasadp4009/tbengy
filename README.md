# tbengy v2
**tbengy** Python Tool for SV/UVM Testbench Generation and RTL Synthesis. The tool uses newly available capability of **Vivado tool by Xilinx (WebPack Version)** to compile and run SV/UVM Testbench and syntheize RTL for Digilent FPGA Boards

# Used in Industry

* [Backbone Systems](https://www.backbone.link/)

# Demo (Demo will be updated soon)
[![asciicast](https://asciinema.org/a/tgGhndUghxvtgQwwM3qKGgNjt.svg)](https://asciinema.org/a/tgGhndUghxvtgQwwM3qKGgNjt)

# Requirements
* Python 3.x
* Xilinx Vivado 202x.x
* GNU Make
* F4PGA (xc7 family) -- only for projects generated with `--backend f4pga`

# Setup Instructions
### 1. Python 3.x.x
- Download Python3 from https://www.python.org/downloads/
- Install Python3 in your system
- Check Python version in Terminal/Console/Command-Prompt/Powershell

#### Command
```
python --version
```
Or
```
python3 --version
```

#### Output (Should be 3.x.x)
```
Python 3.8.1
```

### 2. Xilinx Vivado 20xx.x
- Download Vivado from https://www.xilinx.com/support/download.html
- Install Vivado WebPack in your system
- Set Xilinx Vivado bin folder path to User/System Environment Variables

#### Setting Variable in Linux
```
export PATH="$PATH:/home/<path_to_xilinx_installation>/Xilinx/Vivado/2020.1/bin"
```
**Note:** Put the above line with your path in ~/.bashrc, so the tool can load everytime you open terminal

#### Test that tool opens from Terminal and path is properly set
- Once you set the path in ~/.bashrc, open new terminal and execute command below
```
vivado
```
- If your path and setup is correct, Vivado GUI will open
- You can close it as we will be working from terminal for the tbengy

#### Setting Variable in Windows
Open Command-Prompt as administrator
```
setx path "%path%;<path_to>Xilinx\Vivado\2020.1\bin"
```
Example: setx path "%path%;C:\Xilinx\Vivado\2020.1\bin"

You can also set the path from System Properties. Search online for this method.

#### Check your Vivado installation from Command-prompt/Powershell
- Once you set the path in Windows, open new command-prompt/Powershell and execute command below
```
vivado
```
- If your path and setup is correct, Vivado GUI will open
- You can close it as we will be working from command-prompt/Powershell for the tbengy

### 3. GNU Make
- Most Linux come with GNU Make so no need to do this step if you are running using Linux
- For Windows, download GNU Make and install it from http://gnuwin32.sourceforge.net/packages/make.htm
- After installation in Windows, we need to add the bin path of Make in system path variable as we did for Vivado
```
setx path "%path%;<path_to>Program Files (x86)\GnuWin32\bin\"
```
Example: setx path "%path%;C:\Program Files (x86)\GnuWin32\bin\"

- After adding the path, open new command-prompt/Powershell window and run
```
make
```
- If you see make getting executed, you are good to go

# Using tbengy

- Run the command below if you are using Git to clone the repository anywhere you wish
```
git clone https://github.com/prasadp4009/tbengy.git
```
Or
- Download from link - https://github.com/prasadp4009/tbengy/archive/master.zip

- Unzip the master.zip if downloaded and then go to tbengy directory
- Open new Terminal/Console/Command-Prompt/Powershell in that directory
- Run the command below to generate UVM TB
```
python tbengy.py
```
Or
```
python3 tbengy.py
```
tbengy help can be accessed with:
```
python tbengy.py -h
```
Or
```
python3 tbengy.py -h
```
You should get the following output
```
usage: tbengy.py [-h] [-v] (-l | -m <module_name>) [-t <tb_type>] [-b <board_type>] [-f <fpga>] [--backend <backend>] [-d <dir_path>]
optional arguments:
  -h, --help            show this help message and exit
  -v, --version         Show tbengy version and exit
  -l, --listboards      Show the list of available boards and exit
  -m <module_name>, --modulename <module_name>
                        Module name for which TB to be generated. Ex. -m my_design
  -t <tb_type>, --tbtype <tb_type>
                        Testbench type to be generated. Ex. -t uvm or -t sv
  -b <board_type>, --boardtype <board_type>
                        Board Files to be added. Ex. -b zybo, -b nexys4_ddr, -b zybo-z7 etc.
  -f <fpga>, --fpga <fpga>
                        FPGA used in board. Ex. -f xc7z010clg400-1, -f xc7a100tcsg324-1, -f xc7z010clg400-1 etc. for Zybo, Nexys 4 DDR and Zybo-Z7-10 respectively
  --backend <backend>   Synthesis backend for SV board projects (-t sv with -b/-f). Ex. --backend vivado (default) or --backend f4pga (experimental, PL-only)
  -d <dir_path>, --dirpath <dir_path>
                        Directory under which TB should be generated. Ex. -d ./myProjects/TB. Default is present working dir.
```
- Enter you module name with '-m <module_name>', the tool will generate a complete UVM testbench (default tb_type is UVM)
```
python tbengy.py -m my_design
```
Or
```
python3 tbengy.py -m my_design
```
- You can enter desired directory where you want to generate TB by passing '-d <directory_path>'
```
python tbengy.py -m my_design -d ./myProjects/
```
Or
```
python3 tbengy.py -m my_design -d ./myProjects/
```
- Go to your generated module folder
- You can read the generated README.md to understand directory structure
- To run the testbench, go to scripts directory and run command below

#### For **SV TB** generation
- For generating SV TB you need to add an additional flag '-t sv' along with primary generation command as shown below
```
python tbengy.py -m my_design -d ./myProjects/ -t sv
```
Or
```
python3 tbengy.py -m my_design -d ./myProjects/ -t sv
```
#### For **SV TB with Synthesis on Digilent Boards** generation
- For generating SV TB with Synthesis on Digilent Boards, you need to add flag '-t sv -b <board_name> -f <fpga>' along with primary generation command as shown below
- You should be able to find FPGA part name from Board Reference Manual or Vendor website
- The default RTL contains Blink LED program, which is basically a simple clock divider with output of 1Hz to LED
- The command also pics up correct board files and link them in script. Modified board files are already available in ./digilent-xdc directory
- These files are modified with additional information regarding clock frequencies and mapped to ports in design RTL by default
- To check the list of boards run the below command
```
python tbengy.py -l
```
Or
```
python3 tbengy.py -l
```
- Example for Zybo Board
```
python tbengy.py -m zyboBlink -d ..\myProj\ -b zybo -f xc7z010clg400-1 -t sv
```
Or
```
python3 tbengy.py -m zyboBlink -d ..\myProj\ -b zybo -f xc7z010clg400-1 -t sv
```
- Example for Nexys 4 DDR
```
python tbengy.py -m nddr4Blink -d ..\myProj\ -b nexys4-ddr -f xc7a100tcsg324-1 -t sv
```
Or
```
python3 tbengy.py -m nddr4Blink -d ..\myProj\ -b nexys4-ddr -f xc7a100tcsg324-1 -t sv
```
#### For batch mode
```
make run_all
```
#### For generating wave and debugging in Vivado Simulator
```
make run_all_gui
```
#### For generating bit stream with synthesis and implementing it on board
```
make synth
```
Note: You can have multiple boards connected to system. Do make sure the boards are connected and turned on.

#### F4PGA backend (experimental) for **SV TB with Synthesis**
- Add `--backend f4pga` to the SV+board generation command to generate an F4PGA (open-source) synthesis flow instead of the Vivado flow. Vivado remains the default backend.
```
python3 tbengy.py -m zyboBlink -d ../myProj/ -b zybo -f xc7z010clg400-1 -t sv --backend f4pga
```
- The generated project then contains scripts/f4pga.mk (Yosys + VPR + prjxray, driven through the symbiflow_* wrappers) and synth/<module>.sdc instead of scripts/synth.tcl. In the generated project, `make synth` builds synth/<module>.bit and `make program` loads it onto the board with openFPGALoader.
- Prerequisites: F4PGA installed for the xc7 family (https://f4pga.readthedocs.io/en/latest/getting-started.html), with F4PGA_INSTALL_DIR set and the xc7 conda environment activated in the shell running make -- both `make synth` and `make program` need it.
- Limitations: EXPERIMENTAL and PL-only -- no PS7 configuration, FSBL or boot image is generated, and timing is indicative only (no Vivado-equivalent STA sign-off). The device mapping is tuned for xc7z010 (Zybo). Simulation still uses the Vivado xsim commands, unchanged. Validated end-to-end (generation -> bitstream -> JTAG load -> blinking LED) on the original Zybo in Oct 2026. See the generated project's README.md for full details.

Contact me on prasadp4009@gmail.com for any questions.

Hope the tool helps. Thanks!

# Tool Developement Plan
- [x] Generation of UVM Testbench with RTL Example and ready to compile and run
- [x] Add simple RAM RTL and simple sanity test
- [x] Create a seperate template file for configuring generated code
- [x] Code CLI for tbengy
- [x] Add support for simple SV TB
- [x] Add generation of synthesis script for Digilent/Xilinx FPGA boards for validation
- [x] Add support to select Digilent Xilinx FPGA boards to auto-synthesize, elaboration and implementation with programming bitstream on board
- [x] Add support to select f4pga tool (https://f4pga.readthedocs.io/en/latest/getting-started.html) as an alternate synthesis backend (`--backend f4pga`): Xilinx-7 Series, PL-only, experimental, including bitstream programming via openFPGALoader (Lattice iCE40/ECP5 from the original item remain future work)
- [ ] ~~Add support for Modelsim compilation instruction in Makefile~~
- [ ] ~~Add support for Vivado wdb wave dump to Modelsim WLF dump conversion for debugging waves generated by Vivado in Modelsim (May or may not happen)~~
