`ifndef DEMO_UVM_INTF__SV
`define DEMO_UVM_INTF__SV

  interface demo_uvm_intf(input clk);

    // Signals
    logic we;
    logic [3:0] addr;
    logic [7:0] wdata;
    logic [7:0] rdata;

  endinterface

`endif

//End of demo_uvm_intf
