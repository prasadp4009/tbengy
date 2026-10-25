`ifndef DEMO_UVM__SV
`define DEMO_UVM__SV

  module demo_uvm
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

  endmodule : demo_uvm

`endif

//End of demo_uvm
