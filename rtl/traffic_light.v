module traffic_light (
    input wire clk,
    input wire rst_n,
    input wire sensor_req,     // Handshake/Trigger input
    output reg [1:0] light,    // 00: Green, 01: Yellow, 10: Red
    output reg done_tick       // Status flag
);

    // State Encoding
    parameter S_GREEN  = 2'b00;
    parameter S_YELLOW = 2'b01;
    parameter S_RED    = 2'b10;

    reg [1:0] state_reg, state_next;
    reg [3:0] timer;

    // State Register
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            state_reg <= S_GREEN;
            timer     <= 4'b0;
        end else begin
            state_reg <= state_next;
            if (state_reg != state_next)
                timer <= 4'b0;
            else
                timer <= timer + 1'b1;
        end
    end

    // Next State Logic
    always @(*) begin
        state_next = state_reg;
        done_tick = 1'b0;

        case (state_reg)
            S_GREEN: begin
                if (sensor_req && timer > 4'd10)
                    state_next = S_YELLOW;
            end
            S_YELLOW: begin
                if (timer > 4'd3)
                    state_next = S_RED;
            end
            S_RED: begin
                if (timer > 4'd10) begin
                    state_next = S_GREEN;
                    done_tick = 1'b1;
                end
            end
            default: state_next = S_GREEN;
        endcase
    end

    // Output Logic
    always @(*) begin
        light = state_reg;
    end

endmodule