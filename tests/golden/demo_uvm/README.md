## demo_uvm Architecture, Design and Verification Details

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
demo_uvm
.
├── docs
├── README.md
├── rtl
│   └── demo_uvm.sv
├── scripts
│   ├── logw.tcl
│   └── Makefile
├── sim
│   ├── env
│   │   ├── agent
│   │   │   ├── demo_uvm_agent_cfg.sv
│   │   │   ├── demo_uvm_agent_pkg.sv
│   │   │   ├── demo_uvm_agent.sv
│   │   │   ├── demo_uvm_driver.sv
│   │   │   ├── demo_uvm_intf.sv
│   │   │   ├── demo_uvm_monitor.sv
│   │   │   ├── demo_uvm_sequencer.sv
│   │   │   ├── regs
│   │   │   │   └── demo_uvm_regs_pkg.sv
│   │   │   └── sequence_lib
│   │   │       ├── demo_uvm_base_seq.sv
│   │   │       ├── demo_uvm_sanity_seq.sv
│   │   │       ├── demo_uvm_seq_item.sv
│   │   │       └── demo_uvm_seq_pkg.sv
│   │   ├── demo_uvm_cov.sv
│   │   ├── demo_uvm_env_pkg.sv
│   │   ├── demo_uvm_env.sv
│   │   └── demo_uvm_sb.sv
│   ├── tb
│   │   └── demo_uvm_tb.sv
│   └── tests
│       ├── demo_uvm_base_test.sv
│       ├── demo_uvm_sanity_test.sv
│       └── demo_uvm_test_pkg.sv
└── synth
```
**Note** : .gitignore is added to project directory for easy git integration.
