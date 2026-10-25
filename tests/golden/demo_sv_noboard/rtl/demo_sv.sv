`ifndef DEMO_SV__SV
`define DEMO_SV__SV

  module demo_sv
  (
    input  logic clk,
    input  logic rst,
    input  logic [7:0] wdata,
    output logic [7:0] rdata
  );

  always_ff @(posedge clk or negedge rst) begin
    if(!rst) begin
      rdata <= 'd0;
    end
    else begin
      rdata <= wdata;
    end
  end

  endmodule : demo_sv

`endif

//End of demo_sv
