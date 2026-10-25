## demo_sv Architecture, Design and Verification Details

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
demo_sv
.
├── docs
├── README.md
├── rtl
│   └── demo_sv.sv
├── scripts
│   ├── logw.tcl
│   └── Makefile
├── sim
│   └── tb
│       └── demo_sv_tb.sv
└── synth
```
**Note** : .gitignore is added to project directory for easy git integration.
