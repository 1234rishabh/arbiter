`timescale 1us/1us

module fixed_priority_arbiter (
    input  logic        clk,
    input  logic [3:0]  req,
    output logic [3:0]  grant
);
always_ff @(posedge clk) begin
    if (req[3])       grant <= 4'b1000;
    else if (req[2])  grant <= 4'b0100;
    else if (req[1])  grant <= 4'b0010;
    else if (req[0])  grant <= 4'b0001;
    else              grant <= 4'b0000;
end

endmodule
