`ifndef LED_BLINK__SV
`define LED_BLINK__SV

  module led_blink
  (
    input  logic clk,
    input  logic rst,
    output logic ledOut
  );

  `ifndef SIM
    localparam bit [31:0] FREQCOUNT = 'd125000000;
  `else
    localparam bit [31:0] FREQCOUNT = 'd100;
  `endif

  logic [31:0] count;

  always_ff @(posedge clk or posedge rst) begin
    if (rst) begin
      count <= 'd0;
      ledOut <= 'd0;
    end
    else begin
      if (count <= (FREQCOUNT-1)/2) begin
        count <= count + 'd1;
      end
      else begin
        count <= 'd0;
        ledOut <= ~ledOut;
      end
    end
  end

  endmodule : led_blink

`endif

//End of led_blink
