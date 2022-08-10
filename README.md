# tbengy 1.3
**tbengy** Python Tool for UVM Testbench Generation. The tool uses newly available capability of **Vivado tool by Xilinx (WebPack Version)** to compile and run UVM Testbench

# Demo
[![asciicast](https://asciinema.org/a/tgGhndUghxvtgQwwM3qKGgNjt.svg)](https://asciinema.org/a/tgGhndUghxvtgQwwM3qKGgNjt)

# Requirements
* Python 3.x
* Xilinx Vivado 2020.x
* GNU Make

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
usage: tbengy.py [-h] [-v] -m <module_name> [-d <dir_path>]

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         Show tbengy version and exit
  -m <module_name>, --modulename <module_name>
                        Module name for which TB to be generated. Ex. -m my_design
  -d <dir_path>, --dirpath <dir_path>
                        Directory under which TB should be generated. Ex. -d ./myProjects/TB. Default is present working dir.
```
- Enter you module name with '-m <module_name>', the tool will generate a complete UVM testbench
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

#### For batch mode
```
make run_all
```
#### For generating wave and debugging in Vivado Simulator
```
make run_all_gui
```

Contact me on prasadp4009@gmail.com for any questions.

Hope the tool helps. Thanks!

# Tool Developement Plan
- [x] Generation of UVM Testbench with RTL Example and ready to compile and run
- [x] Add simple RAM RTL and simple sanity test
- [x] Create a seperate template file for configuring generated code
- [x] Code CLI for tbengy
- [x] Add support for simple SV TB
- [ ] Add generation of synthesis script for Digilent/Xilinx FPGA boards for validation
- [ ] Add support to select Digilent Xilinx FPGA boards to auto-synthesize, elaboration and implementation with programming bitstream on board
- [ ] Add support for Modelsim compilation instruction in Makefile
- [ ] Add support for Vivado wdb wave dump to Modelsim WLF dump conversion for debugging waves generated by Vivado in Modelsim (May or may not happen)
