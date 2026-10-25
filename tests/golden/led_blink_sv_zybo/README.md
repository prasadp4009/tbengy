## led_blink Architecture, Design and Verification Details

### Commands to run test
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
### To run Synthesis
```bash
cd scripts
make synth
```
### Directory Structure
```
led_blink
.
├── docs
├── README.md
├── rtl
│   └── led_blink.sv
├── scripts
│   ├── logw.tcl
│   ├── synth.tcl
│   └── Makefile
├── sim
│   └── tb
│       └── led_blink_tb.sv
└── synth
    └── Zybo-Master.xdc
```
**Note** : .gitignore is added to project directory for easy git integration.
